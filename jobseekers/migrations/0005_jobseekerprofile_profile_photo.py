# Generated by Django 5.2 on 2025-04-17 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekers', '0004_jobseekerprofile_about_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekerprofile',
            name='profile_photo',
            field=models.ImageField(blank=True, help_text='Upload a profile photo (JPEG, PNG)', null=True, upload_to='profile_photos/'),
        ),
    ]
