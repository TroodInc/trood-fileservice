import os
import hashlib
import magic
import uuid

from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from file_service import settings


def create_unique_filename(instance, filename):
    name, ext = os.path.splitext(filename)
    return '{}{}'.format(instance.id, ext)


def validate_file_extention(value):
    ext = value.name.split('.')[-1]
    file_extensions = FileExtensions.objects.get_or_create(id=1)[0]
    if not ext.lower() in file_extensions:
        raise ValidationError(_('Unsupported file type'))


class File(models.Model):

    TYPE_OTHER = 'OTHER'
    TYPE_AUDIO = 'AUDIO'
    TYPE_IMAGE = 'IMAGE'

    FILE_TYPES = (
        (TYPE_OTHER, _('Other')),
        (TYPE_AUDIO, _('Audio')),
        (TYPE_IMAGE, _('Image')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.UUIDField(_('Owner'), null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True)

    file = models.FileField(_('File'), upload_to=create_unique_filename, validators=(validate_file_extention, ))

    filename = models.CharField(max_length=128, blank=True, null=True)
    origin_filename = models.CharField(_('Original filename'), max_length=128, blank=True, null=True)

    type = models.CharField(_('Type'), max_length=24, choices=FILE_TYPES, default=TYPE_OTHER)
    mimetype = models.CharField(_('Mimetype'), max_length=128, blank=True, null=True)
    size = models.IntegerField(_('File size'))
    ready = models.BooleanField(_('Ready'), default=False)

    deleted = models.BooleanField(_('Deleted'), default=False)

    metadata = JSONField(_('Meta data'), null=True, blank=True)

    def __str__(self):
        return self.filename if self.filename else 'No name'

    def save(self, *args, **kwargs):
        self.origin_filename = self.file.name

        self.file.save(self.file.name, self.file, save=False)

        if not self.filename:
            self.filename = self.origin_filename

        self.mimetype = magic.from_file(self.file.path, mime=True)

        if self.mimetype:
            maintype, subtype = self.mimetype.split('/')

            if maintype == 'audio':
                self.type = File.TYPE_AUDIO
            elif maintype == 'image':
                self.type = File.TYPE_IMAGE
            else:
                self.type = File.TYPE_OTHER

        else:
            self.type = File.TYPE_OTHER

        self.size = self.file.size

        super(File, self).save(*args, **kwargs)


class FileExtensions(models.Model):
    allowed_extensions = models.TextField(blank=True, null=True,
                                            default='jpg, jpeg, png, wav, aac, '
                                                    'mp3, ogg, m4a, amr')

    def get_allowed_extensions(self):
        return self.allowed_extensions.splitlines()