from django.shortcuts import render, redirect
from .models import Category, Video
from .forms import VideoSuggestionForm, CategorySuggestionForm
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
import re
import logging

def index(request):
    video_suggestion_form = VideoSuggestionForm()
    category_suggestion_form = CategorySuggestionForm()
    feedback_message = None

    if request.method == 'POST':
        if 'video_suggestion' in request.POST:
            video_suggestion_form = VideoSuggestionForm(request.POST)
            if video_suggestion_form.is_valid():

                try:
                    video_suggestion_form.save()
                    logging.info(f"Video suggestion form data: {video_suggestion_form.cleaned_data}")
                    feedback_message = "Thank you for your video suggestion!"
                except:
                    feedback_message = "An error occurred while saving your video suggestion."
                    logging.exception("An error occurred while saving a video suggestion.")
                    logging.info(f"Video suggestion form data: {video_suggestion_form.cleaned_data}")
            if not video_suggestion_form.is_valid():
                print(video_suggestion_form.errors)        

        elif 'category_suggestion' in request.POST:
            category_suggestion_form = CategorySuggestionForm(request.POST)
            if category_suggestion_form.is_valid():
                try:
                    category_suggestion_form.save()
                    print(category_suggestion_form.cleaned_data)
                    logging.info(f"Category suggestion form data: {category_suggestion_form.cleaned_data}")
                    feedback_message = "Thank you for your category suggestion!"
                except:
                    print(category_suggestion_form.cleaned_data)
                    feedback_message = "An error occurred while saving your category suggestion."
                    logging.exception("An error occurred while saving a category suggestion.")
                    logging.info(f"Category suggestion form data: {category_suggestion_form.cleaned_data}")
            if not category_suggestion_form.is_valid():
                print(category_suggestion_form.errors)

    categories = Category.objects.all()
    return render(request, 'index.html', {
        'categories': categories,
        'video_suggestion_form': video_suggestion_form,
        'category_suggestion_form': category_suggestion_form,
        'feedback_message': feedback_message
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
