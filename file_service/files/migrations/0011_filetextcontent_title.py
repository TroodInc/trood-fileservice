# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-11-22 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0010_auto_20191023_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='filetextcontent',
            name='title',
            field=models.TextField(null=True),
        ),
    ]
