# Generated by Django 5.0.3 on 2024-04-29 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
        ('stardlune_app', '0003_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stardlune_app.account'),
        ),
    ]