from django.core.management.base import BaseCommand
from resources.models import Resource, Tag
from videos.models import Video

class Command(BaseCommand):
    help = 'Migrate videos to resources'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting migration...')

        def migrate_videos_to_resources():
            for video in Video.objects.all():
                # Check if the video title already exists in resources
                if not Resource.objects.filter(title=video.title).exists():
                    # Create a new Resource entry for the video
                    resource = Resource(
                        resource_type='video',
                        title=video.title,
                        description='',  # If the Video model has a description, use video.description
                        url=video.url,
                        author='',  # Add the author if the Video model has one
                    )
                    resource.save()

                    # Add tags from the video to the resource
                    # Assuming the `tags` field in the Video model is a CharField with comma-separated values
                    for tag_name in video.tags.split(','):
                        tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                        resource.tags.add(tag)

        # Call the function
        migrate_videos_to_resources()

        self.stdout.write(self.style.SUCCESS('Migration complete!'))
