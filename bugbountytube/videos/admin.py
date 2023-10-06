from django.contrib import admin
from .models import Category, Video, VideoSuggestion, CategorySuggestion
from adminsortable2.admin import SortableAdminMixin

@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'description', 'parent']
    list_filter = ['parent']
    search_fields = ['name', 'description']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'tags', 'category']
    list_filter = ['category']
    search_fields = ['title', 'tags']


@admin.register(VideoSuggestion)
class VideoSuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'approved']
    list_filter = ['category', 'approved']

@admin.register(CategorySuggestion)
class CategorySuggestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'approved']
    list_filter = ['parent', 'approved']
