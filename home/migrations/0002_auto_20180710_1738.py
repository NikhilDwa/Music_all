# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-10 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='song_file',
            field=models.FileField(blank=True, upload_to=b''),
        ),
    ]
