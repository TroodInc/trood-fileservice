# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-15 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_auto_20180528_1151'),
    ]

    operations = [
        migrations.RemoveField(model_name='file', name='owner'),
        migrations.AddField(
            model_name='file',
            name='owner',
            field=models.IntegerField(null=True, verbose_name='Owner'),
        ),
    ]
