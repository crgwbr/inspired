# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 22:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bible', '0005_auto_20160214_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='footnote',
            name='edition',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='footnotes', to='bible.Edition'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='footnote',
            name='fnid',
            field=models.SlugField(),
        ),
        migrations.AlterUniqueTogether(
            name='footnote',
            unique_together=set([('edition', 'fnid')]),
        ),
    ]
