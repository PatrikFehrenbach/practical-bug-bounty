from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        unique_together = ('name', 'parent',)  # Ensure name is unique under a specific parent
        verbose_name_plural = "categories"
        ordering = ['order']

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated tags
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title
