import json
import os
from uuid import uuid4

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers

from file_service.files import models as files_models

from file_service import settings


def move_uploaded_file(file, name=str(uuid4())):
    _, ext = os.path.splitext(file.name)
    file_path = default_storage.save(name + ext, ContentFile(file.read()))

    return file_path


class MessageMetaDataSerializer(serializers.Serializer):
    message = serializers.CharField(required=False)

    class Meta:
        fields = ('message', )

    def save(self, *args, **kwargs):
        self.instance.ready = False
        self.instance.metadata = {
            'message': self.validated_data['message']
        }

        self.instance.save()
        return self.instance


class AudioMetaDataSerializer(serializers.Serializer):
    mp3 = serializers.FileField()
    length = serializers.IntegerField()

    def save(self, *args, **kwargs):
        self.instance.ready = True

        file_path = move_uploaded_file(self.validated_data['mp3'])

        self.instance.metadata = {
            'length': self.validated_data['length'],
            'mp3': file_path
        }
        self.instance.save()

        return self.instance

    def to_representation(self, instance):
        result = super(AudioMetaDataSerializer, self).to_representation(instance)
        result['mp3'] = settings.FILES_BASE_URL + instance['mp3']

        return result


class ImageMetaDataSerializer(serializers.Serializer):
    small = serializers.FileField()
    medium = serializers.FileField()
    large = serializers.FileField()
    xlarge = serializers.FileField()

    def save(self, *args, **kwargs):
        self.instance.ready = True

        self.instance.metadata = {
            'small': move_uploaded_file(self.validated_data['small'], '{}_small'.format(self.instance.id)),
            'medium': move_uploaded_file(self.validated_data['medium'], '{}_medium'.format(self.instance.id)),
            'large': move_uploaded_file(self.validated_data['large'], '{}_large'.format(self.instance.id)),
            'xlarge': move_uploaded_file(self.validated_data['xlarge'], '{}_xlarge'.format(self.instance.id)),
        }
        self.instance.save()

        return self.instance

    def to_representation(self, instance):
        result = {k: settings.FILES_BASE_URL + v for k, v in instance.items()}

        return result


class FileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    metadata_serializers = {
        files_models.File.TYPE_AUDIO: AudioMetaDataSerializer,
        files_models.File.TYPE_IMAGE: ImageMetaDataSerializer
    }

    class Meta:
        model = files_models.File
        fields = (
            'id', 'owner', 'created', 'file',
            'file_url', 'filename', 'origin_filename',
            'type', 'mimetype', 'size',
            'ready', 'metadata'
        )
        read_only_fields = ('created', 'id', 'type', 'mimetype', 'size', 'file_url', 'origin_filename', )

    def get_file_url(self, obj):
        return settings.FILES_BASE_URL + obj.file.name

    def to_representation(self, instance):
        result = super(FileSerializer, self).to_representation(instance)

        if instance.ready:
            serializer = self.metadata_serializers.get(instance.type, None)

            if serializer:
                serializer = serializer(instance=instance.metadata)
                result['metadata'] = serializer.data

        result.pop('file')

        return result


class FileExtensionsSerializer(serializers.ModelSerializer):
    allowed_extensions = serializers.JSONField()

    class Meta:
        model = files_models.FileExtensions
        fields = ('allowed_extensions',)