# Generated by Django 4.2.6 on 2023-10-12 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
