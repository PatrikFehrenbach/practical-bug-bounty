from django.db import models

class Tag(models.Model):
    """Model to represent tags for resources."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    """Model to represent a bug bounty resource."""

    RESOURCE_TYPES = (
        ('blog_post', 'Blog Post'),
        ('github_repo', 'GitHub Repository'),
        ('article', 'Article'),
        ('video', 'Video'),
        # ... add more types as needed
    )

    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='article')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=500)
    added_date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(Tag, related_name="resources", blank=True)

    def __str__(self):
        return self.title
