# Generated by Django 5.1.4 on 2024-12-30 06:48

import cms_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_app', '0002_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=cms_app.models.upload_teams),
        ),
    ]
