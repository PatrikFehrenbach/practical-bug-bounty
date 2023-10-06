from django.contrib import admin
from .models import Category, Video
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
