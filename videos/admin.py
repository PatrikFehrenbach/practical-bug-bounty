from django.contrib import admin
from .models import Module, SubModule, Topic, Video, CourseNote, AdditionalLink
from adminsortable2.admin import SortableAdminMixin
from markdownx.admin import MarkdownxModelAdmin
from django.db.models.signals import post_save
from django.dispatch import receiver
from resources.models import Resource, Tag

@receiver(post_save, sender=Video)
def migrate_video_to_resource(sender, instance, **kwargs):
    # Check if a corresponding resource already exists
    resource, created = Resource.objects.get_or_create(
        title=instance.title,
        defaults={
            'resource_type': 'video',
            'description': '',
            'url': instance.url,
            'author': '',  # Adjust as needed
        }
    )
    
    # If the video has tags, migrate them too
    video_tags = instance.tags.split(",")  # Assuming comma-separated tags in Video model
    for tag_name in video_tags:
        tag_name = tag_name.strip()
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        resource.tags.add(tag)


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
