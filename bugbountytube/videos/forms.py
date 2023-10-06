from django import forms
from .models import Category, Video, CategorySuggestion, VideoSuggestion

class CategorySuggestionForm(forms.ModelForm):
    class Meta:
        model = CategorySuggestion
        fields = ['name', 'description', 'parent']


class VideoSuggestionForm(forms.ModelForm):
    class Meta:
        model = VideoSuggestion
        fields = ['title', 'url', 'tags', 'category']
