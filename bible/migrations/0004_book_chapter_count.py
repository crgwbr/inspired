# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bible', '0003_auto_20160214_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='chapter_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
