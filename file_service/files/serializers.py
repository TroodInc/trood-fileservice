import os
from uuid import uuid4

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers

from file_service.files import models as files_models

from django.conf import settings


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
        thumbs = self.validated_data
        file_id = self.instance.id
        self.instance.metadata = {
            'small': move_uploaded_file(thumbs['small'], f'{file_id}_small'),
            'medium': move_uploaded_file(thumbs['medium'], f'{file_id}_medium'),
            'large': move_uploaded_file(thumbs['large'], f'{file_id}_large'),
            'xlarge': move_uploaded_file(thumbs['xlarge'], f'{file_id}_xlarge'),
        }

        self.instance.save()
        return self.instance

    def to_representation(self, instance):
        result = {k: settings.FILES_BASE_URL + v for k, v in instance.items()}
        return result


class FileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    metadata_serializers = {
        # @todo: autoload custom serrializers
        "AUDIO": AudioMetaDataSerializer,
        "IMAGE": ImageMetaDataSerializer
    }

    class Meta:
        model = files_models.File
        fields = (
            'id', 'owner', 'created', 'file',
            'file_url', 'filename', 'origin_filename',
            'type', 'mimetype', 'size',
            'ready', 'metadata'
        )
        read_only_fields = ('created', 'id', 'type', 'mimetype', 'size', 'file_url', )

    def get_file_url(self, obj):
        return settings.FILES_BASE_URL + obj.file.name

    def to_internal_value(self, data):
        if 'file' in data or data.get('filename', '') == '':
            data.update({
                'filename': data['file'].name,
                'origin_filename': data['file'].name
            })

        return super(FileSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        result = super(FileSerializer, self).to_representation(instance)
        serializer = self.metadata_serializers.get(instance.type, None)
        if serializer and instance.ready:
            serializer = serializer(instance=instance.metadata)
            result['metadata'] = serializer.data

        result.pop('file')
        return result


class FileExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = files_models.FileExtension
        fields = ('id', 'extension')

    def save(self, **kwargs):
        extension = self.validated_data['extension'].lower()
        instance = super().save(**kwargs)
        instance.extension = extension
        instance.save()
        return instance


class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = files_models.FileType
        fields = ('id', 'mime')


class FileTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = files_models.FileTemplate
        fields = ('id', 'alias', 'name', 'filename_template', 'body_template')


class FromTemplateSerializer(serializers.Serializer):
    data = serializers.JSONField()
    format = serializers.ChoiceField(choices=settings.FILE_GENERATORS.keys())
    template = serializers.CharField()
    access = serializers.ChoiceField(choices=files_models.File.ACCESS_CHOICES)
    tags = serializers.PrimaryKeyRelatedField(queryset=files_models.Tag.objects.all(), many=True)
