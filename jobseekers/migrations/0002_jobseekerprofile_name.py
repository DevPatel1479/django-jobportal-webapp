# Generated by Django 5.1.7 on 2025-04-14 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekerprofile',
            name='name',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]
