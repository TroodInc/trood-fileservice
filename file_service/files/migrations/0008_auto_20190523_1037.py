# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-23 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_auto_20181128_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=128, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('filename_template', models.CharField(blank=True, max_length=128, null=True)),
                ('body_template', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='access',
            field=models.CharField(choices=[('PRIVATE', 'Private'), ('PROTECTED', 'Protected'), ('PUBLIC', 'Public')], default='PROTECTED', max_length=10),
        ),
        migrations.AddField(
            model_name='file',
            name='tags',
            field=models.ManyToManyField(to='files.Tag'),
        ),
    ]
