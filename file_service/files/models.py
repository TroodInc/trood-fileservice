import os
import magic
import uuid
import mimetypes

from slugify import slugify
from datetime import datetime
from jsonfield import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


def create_unique_filename(instance, filename):
    name, ext = os.path.splitext(filename)
    return '{}-{}{}'.format(slugify(name), datetime.now().strftime('%d%m%y%H%M%S'), ext)


def validate_file_extention(value):
    ext = value.name.split('.')[-1]
    allowed_extensions = FileExtension.objects.all().values_list('extension', flat=True)
    if len(allowed_extensions) and not ext.lower() in allowed_extensions and "*" not in allowed_extensions:
        raise ValidationError(_('Unsupported file type'))


class FileType(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    mime = models.TextField()


class File(models.Model):
    ACCESS_CHOICES = (
        ('PRIVATE', _('Private')),
        ('PROTECTED', _('Protected')),
        ('PUBLIC', _('Public'))
    )

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
    tags = models.ManyToManyField('Tag')
    access = models.CharField(choices=ACCESS_CHOICES, max_length=10, default='PROTECTED')

    def __str__(self):
        return self.filename if self.filename else 'No name'

    def save(self, *args, **kwargs):
        if not self.size:
            self.file.save(self.file.name, self.file, save=False)

        self.mimetype, enc = mimetypes.guess_type(self.file.path)

        if not self.mimetype:
            self.mimetype = magic.from_file(self.file.path, mime=True)

        if self.mimetype:
            self.type = FileType.objects.filter(mime__contains=self.mimetype).first()

        self.size = self.file.size

        super(File, self).save(*args, **kwargs)


class FileExtension(models.Model):
    extension = models.CharField(max_length=255)


class FileTemplate(models.Model):
    alias = models.CharField(unique=True, max_length=128, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    filename_template = models.CharField(max_length=128, blank=True, null=True)
    body_template = models.TextField()
    example_data = JSONField(null=True)


class Tag(models.Model):
    tag = models.CharField(unique=True, max_length=128)


class FileTextContent(models.Model):
    source = models.ForeignKey(File, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
