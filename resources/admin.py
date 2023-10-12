from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import Resource, Tag
import requests
import os
from threading import Thread

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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-github/', self.import_github, name='import-github'),
        ]
        return custom_urls + urls

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
