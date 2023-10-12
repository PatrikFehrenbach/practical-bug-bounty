from django.shortcuts import render
from django.db.models import Q, Count
from .models import Resource, Tag
from django.core.paginator import Paginator

def resources(request):
    # Constants
    ITEMS_PER_PAGE = 10  # Change this to your desired items per page

    # Fetch all resources initially
    resource_list = Resource.objects.all()

    # Filter by resource_type if provided
    resource_type = request.GET.get('resource_type')
    if resource_type:
        resource_list = resource_list.filter(resource_type=resource_type)

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

    # Pagination for resources
    paginator = Paginator(resource_list, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    resource_type_counts = {res_type[0]: Resource.objects.filter(resource_type=res_type[0]).count() for res_type in Resource.RESOURCE_TYPES}

    icons = {
        'blog_post': 'bi bi-journal-text',
        'github_repo': 'bi bi-github',
        'article': 'bi bi-file-earmark-text',
        'video': 'bi bi-camera-video',
    }

    # Fetch tags ordered by their usage frequency and with minimum occurrences
    tags_with_count = Tag.objects.annotate(resource_count=Count('resources')).filter(resource_count__gte=3).values_list('name', 'resource_count').order_by('-resource_count')

    context = {
        'resource_type_counts': resource_type_counts,
        'resources': page_obj,  # Update this to pass the paginated resources
        'tags_with_count': tags_with_count,  # Pass tags with their count
        'resource_type': resource_type,  # Pass the selected resource type
        'tag_name': tag_name,  # Pass the selected tag for retaining the filter during pagination
        'RESOURCE_TYPES': Resource.RESOURCE_TYPES,
        'icons': icons
    }

    return render(request, 'resources.html', context)

