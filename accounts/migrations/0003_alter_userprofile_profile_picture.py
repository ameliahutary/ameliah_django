# Generated by Django 5.0.4 on 2024-05-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpg', upload_to='profile_pictures/'),
        ),
    ]
