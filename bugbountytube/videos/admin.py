from django.contrib import admin
from .models import Category, Video

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'parent']
    list_filter = ['parent']
    search_fields = ['name', 'description']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'tags', 'category']
    list_filter = ['category']
    search_fields = ['title', 'tags']
