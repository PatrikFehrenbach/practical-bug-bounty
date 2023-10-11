from django.shortcuts import render
from .models import Resource, Tag

def resources(request):
    # Start with all resources
    resource_list = Resource.objects.all()

    # Filter by resource_type if provided
    resource_type = request.GET.get('resource_type')
    if resource_type:
        resource_list = resource_list.filter(resource_type=resource_type)

    # Filter by tag if provided
    tag = request.GET.get('tag')
    if tag:
        resource_list = resource_list.filter(tags__name=tag)

    # Search by title or description if search term is provided
    search_term = request.GET.get('search')
    if search_term:
        resource_list = resource_list.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        )

    context = {
        'resources': resource_list,
        'tags': Tag.objects.all()  # Pass all tags to populate the filter buttons
    }

    return render(request, 'resources.html', context)
