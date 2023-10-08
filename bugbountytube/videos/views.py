from django.shortcuts import render, redirect,get_object_or_404
from .models import Module, SubModule, Topic, Video

import re
import logging

def index(request):
    feedback_message = None


    modules = Module.objects.all()
    return render(request, 'index.html', {
        'modules': modules,
        'feedback_message': feedback_message
    })



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
