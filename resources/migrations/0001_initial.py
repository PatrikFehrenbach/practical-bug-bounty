# Generated by Django 4.2.6 on 2023-10-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('blog_post', 'Blog Post'), ('github_repo', 'GitHub Repository'), ('article', 'Article'), ('video', 'Video')], default='article', max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField(max_length=500)),
                ('added_date', models.DateField(auto_now_add=True)),
                ('author', models.CharField(blank=True, max_length=255)),
                ('tags', models.ManyToManyField(blank=True, related_name='resources', to='resources.tag')),
            ],
        ),
    ]