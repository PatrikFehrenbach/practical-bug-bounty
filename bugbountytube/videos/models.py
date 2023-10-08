from django.db import models
from markdownx.models import MarkdownxField

class Module(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class SubModule(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='submodules')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.module.name} - {self.name}"

class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    submodule = models.ForeignKey(SubModule, on_delete=models.CASCADE, related_name='topics')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.submodule.name} - {self.name}"

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated tags
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='videos', blank=True, null=True)

    def __str__(self):
        return self.title

class CourseNote(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return f"Note for {self.topic.name}"

class AdditionalLink(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='additional_links')
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.url


class CategorySuggestion(models.Model):
    name = models.CharField(max_length=255)
    description = MarkdownxField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class VideoSuggestion(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    tags = models.CharField(max_length=255, blank=True)  
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title