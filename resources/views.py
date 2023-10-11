from django.shortcuts import render
from django.db.models import Q
from .models import Resource, Tag

def resources(request):
    # Fetch all resources initially
    resource_list = Resource.objects.all()

    # Filter by tag if provided
    tag_name = request.GET.get('tag')
    if tag_name:
        resource_list = resource_list.filter(tags__name=tag_name)

    # Search by title or description if search term is provided
    search_term = request.GET.get('search')
    if search_term:
        resource_list = resource_list.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        )

    icons = {
        'blog_post': 'bi bi-journal-text',
        'github_repo': 'bi bi-github',
        'article': 'bi bi-file-earmark-text',
        'video': 'bi bi-camera-video',
    }
    context = {
        'resources': resource_list,
        'tags': Tag.objects.all(),  # Pass all tags to populate the filter links
        'RESOURCE_TYPES': Resource.RESOURCE_TYPES,  # Pass the resource types to the template
        'icons': icons
    }

    return render(request, 'resources.html', context)
