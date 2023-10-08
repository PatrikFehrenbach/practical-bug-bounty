from django.contrib import admin
from .models import Module, SubModule, Topic, Video, CourseNote, AdditionalLink
from adminsortable2.admin import SortableAdminMixin
from markdownx.admin import MarkdownxModelAdmin

@admin.register(Module)
class ModuleAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

@admin.register(SubModule)
class SubModuleAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'description', 'module']
    list_filter = ['module']
    search_fields = ['name', 'description']

@admin.register(Topic)
class TopicAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'description', 'submodule']
    list_filter = ['submodule']
    search_fields = ['name', 'description']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'tags', 'topic']
    list_filter = ['topic']
    search_fields = ['title', 'tags']

@admin.register(CourseNote)
class CourseNoteAdmin(MarkdownxModelAdmin):
    list_display = ['topic', 'content']
    list_filter = ['topic']

@admin.register(AdditionalLink)
class AdditionalLinkAdmin(admin.ModelAdmin):
    list_display = ['topic', 'url', 'description']
    list_filter = ['topic']
    search_fields = ['description', 'url']
