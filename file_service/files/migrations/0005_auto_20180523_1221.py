# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-23 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import file_service.files.models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_auto_20171102_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_extensions', models.TextField(blank=True, default='jpg, jpeg, png, wav, aac, mp3, ogg, m4a, amr', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=file_service.files.models.create_unique_filename, validators=[file_service.files.models.validate_file_extention], verbose_name='File'),
        ),
    ]
