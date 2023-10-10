# Generated by Django 4.1.6 on 2023-10-10 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengePlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('difficulty_level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], max_length=100)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Both', 'Both')], max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
