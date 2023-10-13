from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import Resource, Tag
from .forms import ImportMediumForm
import requests
import os
from threading import Thread
import csv
from io import TextIOWrapper
from .forms import HackerOneReportUploadForm
from difflib import get_close_matches
import json
from django.contrib import messages

ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')

# Admin for the Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class HackerOneImportMixin:
    
    def generate_description(self, data):
        description = {
            "vulnerability_information": data.get('vulnerability_information', ''),
            "reported_on": data.get('created_at', '').split('T')[0],  # Extract the date part
            "state": f"{data.get('state', 'N/A')} ({data.get('substate', 'N/A')})",
            "severity_rating": data.get('severity_rating', 'N/A'),
            "bounty_amount": f"${data.get('bounty_amount', 0)}",
            "researcher": data.get('reporter', {}).get('username', 'N/A'),  # Researcher's username from reporter field
            "website": data.get('team', {}).get('profile', {}).get('website', 'N/A')
        }
        
        return json.dumps(description)
     
    def import_hackerone(self, request):
        if request.method == 'POST':
            form = HackerOneReportUploadForm(request.POST, request.FILES)
            if form.is_valid():
                # Iterate through each uploaded file
                for uploaded_file in request.FILES.getlist('json_files'):
                    try:  # Start of try block
                        json_file = uploaded_file.read().decode('utf-8')
                        data = json.loads(json_file)

                        title = data.get('title')
                        url = data.get('url')
                        author = data.get('reporter', {}).get('username')
                        vulnerability_type = data.get('weakness', {}).get('name')
                        description = self.generate_description(data)  # Generate the description
                        
                        # Create or update the Resource
                        resource, created = Resource.objects.get_or_create(
                            title=title,
                            defaults={
                                'resource_type': 'hackerone_report',
                                'url': url,
                                'author': author,
                                'description': description,
                            }
                        )

                        # If the resource already exists, we might want to update some fields
                        if not created:
                            resource.url = url
                            resource.author = author
                            resource.description = description
                            resource.save()

                        # Fetch the best matching tag for the vulnerability type
                        all_tags = [tag.name for tag in Tag.objects.all()]
                        matches = get_close_matches(vulnerability_type, all_tags, n=1)
                        if matches:
                            matched_tag = Tag.objects.get(name=matches[0])
                            resource.tags.add(matched_tag)
                    except Exception as e:  # Handling exceptions
                        # Log the error for debugging purposes. You can also add more logging details if needed.
                        print(f"Error processing report from file {uploaded_file.name}: {e}")

                return redirect('admin:resources_resource_changelist')
        else:
            form = HackerOneReportUploadForm()

        return render(request, 'admin/csv_upload_form_hackerone.html', {'form': form})


    def get_hackerone_urls(self):
        return [
            path('import-hackerone/', self.admin_site.admin_view(self.import_hackerone), name='import-hackerone'),
        ]

# GitHub import mixin
class GitHubImportMixin:
    def import_github(self, request):
        if request.method == "POST":
            repo_urls = request.POST.get('repo_urls').splitlines()

            # Start the background task in a separate thread
            thread = Thread(target=self.import_github_thread, args=(repo_urls,))
            thread.start()

            return redirect("..")
        return render(request, "admin/import_github.html")

    def import_github_thread(self, repo_urls):
        for repo_url in repo_urls:
            details = fetch_github_repo_details(repo_url.strip())
            if details and details.get('title'):
                existing_resource = Resource.objects.filter(title=details['title']).first()
                if not existing_resource:
                    resource = Resource(
                        resource_type='github_repo',
                        title=details['title'],
                        description=details.get('description') or '',
                        url=details.get('url', ''),
                        author=details.get('author', ''),
                    )
                    resource.save()

                    # Process tags
                    for topic in details['tags']:
                        tag, created = Tag.objects.get_or_create(name=topic)
                        resource.tags.add(tag)
                    resource.save()

    def get_github_urls(self):
        return [
            path('import-github/', self.admin_site.admin_view(self.import_github), name='import-github'),
        ]

# Medium import mixin
class MediumImportMixin:
    def format_medium_title(self, title):
        parts = title.split('-')[:-1]  # split by '-' and discard the last part
        formatted_title = ' '.join([part.capitalize() for part in parts])
        return formatted_title

    def import_medium(self, request):
        if request.method == "POST":
            article_urls = request.POST.get('article_urls').splitlines()
            tag_ids = request.POST.getlist('tags')  # Get all selected tag IDs
            tags = Tag.objects.filter(id__in=tag_ids)  # Fetch all selected tags

            for url in article_urls:
                parts = url.split('/')
                author = parts[-2][1:]  # Remove '@' from the username
                raw_title = parts[-1]
                title = self.format_medium_title(raw_title)  # Note the 'self.' here
                resource = Resource(
                    resource_type='article',
                    title=title,
                    url=url,
                    author=author
                )
                try:
                    resource.save()
                    resource.tags.set(tags)  # Set multiple tags
                except Exception as e:
                    print(e)
                    continue

            return redirect("..")

        form = ImportMediumForm()
        return render(request, "admin/import_medium.html", {'form': form})



    def get_medium_urls(self):
        return [
            path('import-medium/', self.admin_site.admin_view(self.import_medium), name='import-medium'),
        ]

# ResourceAdmin inheriting from the mixins
@admin.register(Resource)
class ResourceAdmin(GitHubImportMixin, MediumImportMixin,HackerOneImportMixin, admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'added_date', 'author')
    list_filter = ('resource_type', 'added_date', 'tags')
    search_fields = ('title', 'description', 'author')
    ordering = ('-added_date',)
    date_hierarchy = 'added_date'
    filter_horizontal = ('tags',)

    def get_urls(self):
        urls = super().get_urls()
        return self.get_github_urls() + self.get_medium_urls() + self.get_hackerone_urls() + urls

# Fetch GitHub repo details function
def fetch_github_repo_details(repo_url):
    parts = repo_url.split('/')
    owner = parts[-2]
    repo_name = parts[-1]

    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch repo details using GitHub API
    try:
        api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
        response = requests.get(api_url, headers=headers)
        data = response.json()
    except Exception as e:
        return None

    # Fetch topics (tags) associated with the repo
    topics_response = requests.get(api_url + "/topics", headers=headers)
    topics = topics_response.json().get('names', [])

    return {
        'title': data.get('name'),
        'description': data.get('description'),
        'url': data.get('html_url'),
        'author': data.get('owner', {}).get('login'),
        'tags': topics,
    }
