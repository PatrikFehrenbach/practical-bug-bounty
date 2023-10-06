from django.shortcuts import render
from .models import Category, Video
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
import re


def index(request):
    api_key = ''
    categories = Category.objects.all()
    description = Video.objects.all()
    # Iterate through each category and its videos to fetch details from YouTube
    """
        for category in categories:
        for video in category.videos.all():
            video_id = extract_video_id_from_url(video.url)
            details = get_video_details(video_id, api_key)
             
            if details:
                print(details)
                video.title = details['title']
                video.author = details['channel_title']
                print(video.author)
   #             video.description = details['description']
   #             video.channel_title = details['channel_title'] 
    
    """


    return render(request, 'index.html', {
        'categories': categories,
    #    'author': video.author,
        'description': description,
   #     'video_description': video.description,
   #     'video_channel_title': video.channel_title
    })


def category_videos(request, category_id):
    description = Video.objects.filter(category=category_id)
    category = Category.objects.get(pk=category_id)
    videos = Video.objects.filter(category=category)
    return render(request, 'videos.html', {'category': category, 'videos': videos, 'description': description})

def extract_video_id_from_url(url):
    # Extract video ID from a YouTube URL using regex
    video_id_match = re.search(r'(?<=v=)[^&#]+', url)
    video_id_match = video_id_match or re.search(r'(?<=be/)[^&#]+', url)
    video_id = (video_id_match.group(0) if video_id_match else None)
    return video_id

def get_video_details(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        # Extract details from the response
        items = response.get('items', [])
        if not items:
            return None

        snippet = items[0]['snippet']
        title = snippet['title']
        description = snippet['description']
        channel_title = snippet['channelTitle']

        return {
            'title': title,
            'description': description,
            'channel_title': channel_title,
        }

    except HttpError as e:
        print(f"An error occurred: {e}")
        return None
