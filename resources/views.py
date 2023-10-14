from django.shortcuts import render
from django.db.models import Q, Count
from .models import Resource, Tag
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings
import os
import subprocess
from django.core.management import call_command
from django.http import HttpResponse
import io


def backup_database(request):
    # Use an in-memory file to store the output of the dumpdata command
    output = io.StringIO()
    call_command('dumpdata', format='json', stdout=output)
    output.seek(0)

    # Create a response to send the backup data as an attachment
    response = HttpResponse(output, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=db_backup.json'
    return response


def resources(request):
    # Constants
    ITEMS_PER_PAGE = 10  # Change this to your desired items per page

    # Fetch all resources initially
    resource_list = Resource.objects.all()

    # Filter by resource_type if provided
    resource_type = request.GET.get('resource_type')

    # Check if the resource_type has changed since the last request
    last_resource_type = request.session.get('last_resource_type')
    page_number = request.GET.get('page')
    if last_resource_type != resource_type:
        page_number = 1  # Reset page number to 1

    # Update the session with the current resource_type
    request.session['last_resource_type'] = resource_type

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
