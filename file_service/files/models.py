import os
import magic
import uuid

from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


def create_unique_filename(instance, filename):
    name, ext = os.path.splitext(filename)
    return '{}{}'.format(instance.id, ext)


def validate_file_extention(value):
    ext = value.name.split('.')[-1]
    allowed_extensions = FileExtension.objects.all().values_list('extension',
                                                                 flat=True)
    if not ext.lower() in allowed_extensions and "*" not in allowed_extensions:
        raise ValidationError(_('Unsupported file type'))


class FileType(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    mime = models.TextField()


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.IntegerField(_('Owner'), null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True)

    file = models.FileField(_('File'), upload_to=create_unique_filename, validators=(validate_file_extention, ))

    filename = models.CharField(max_length=128, blank=True, null=True)
    origin_filename = models.CharField(_('Original filename'), max_length=128, blank=True, null=True)

    type = models.ForeignKey(FileType, null=True, blank=True, on_delete=models.SET_NULL)
    mimetype = models.CharField(_('Mimetype'), max_length=128, blank=True, null=True)
    size = models.IntegerField(_('File size'))
    ready = models.BooleanField(_('Ready'), default=False)

    deleted = models.BooleanField(_('Deleted'), default=False)

    metadata = JSONField(_('Meta data'), null=True, blank=True)

    def __str__(self):
        return self.filename if self.filename else 'No name'

    def save(self, *args, **kwargs):
        self.file.save(self.file.name, self.file, save=False)

        self.mimetype = magic.from_file(self.file.path, mime=True)

        if self.mimetype:
            self.type = FileType.objects.filter(mime__contains=self.mimetype).first()

        self.size = self.file.size

        super(File, self).save(*args, **kwargs)


class FileExtension(models.Model):
    extension = models.CharField(max_length=255)
