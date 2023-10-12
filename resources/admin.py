from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import Resource, Tag
import requests
import os 
ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')

# Admin for the Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin for the Resource model
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'added_date', 'author')
    list_filter = ('resource_type', 'added_date', 'tags')
    search_fields = ('title', 'description', 'author')
    ordering = ('-added_date',)
    date_hierarchy = 'added_date'
    filter_horizontal = ('tags',)
    # change_list_template = "admin/resources_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-github/', self.import_github, name='import-github'),
        ]
        return custom_urls + urls

    def import_github(self, request):
        print("Entered import_github method")

        if request.method == "POST":
            repo_urls = request.POST.get('repo_urls').splitlines()
            print(f"Received the following repo URLs: {repo_urls}")

            for repo_url in repo_urls:
                print(f"Processing {repo_url}")
                details = fetch_github_repo_details(repo_url.strip())
                if details and details.get('title'):  
                    print(f"Details fetched for {repo_url}: {details}")
                    existing_resource = Resource.objects.filter(title=details['title']).first()
                    if not existing_resource:
                        resource = Resource(
                            resource_type='github_repo',
                            title=details['title'],
                            description=details.get('description') or '',  # Updated this line
                            url=details.get('url', ''),  # Default to empty string if missing
                            author=details.get('author', ''),  # Default to empty string if missing
                        )
                        resource.save()
                        print(f"Saved new resource for {repo_url}")

                        # Process tags
                        for topic in details['tags']:
                            tag, created = Tag.objects.get_or_create(name=topic)
                            resource.tags.add(tag)
                        resource.save()
                        print(f"Tags added for {repo_url}")
                    else:
                        print(f"Resource with title '{details['title']}' already exists. Skipping...")
            return redirect("..")
        return render(request, "admin/import_github.html")

def fetch_github_repo_details(repo_url):
    print(f"Fetching details for {repo_url}")
    # Extract owner and repo name from URL
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
        response = requests.get(api_url, headers=headers)  # Add headers here
        data = response.json()
    except Exception as e:
        print(f"An error occurred while fetching repo details: {e}")
        return None

    # Fetch topics (tags) associated with the repo
    topics_response = requests.get(api_url + "/topics", headers=headers)
    topics = topics_response.json().get('names', [])

    print(f"Details fetched for {repo_url}: {data}")
    return {
        'title': data.get('name'),
        'description': data.get('description'),
        'url': data.get('html_url'),
        'author': data.get('owner', {}).get('login'),
        'tags': topics,
    }
