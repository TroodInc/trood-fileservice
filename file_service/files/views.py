from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from file_service.files import models, serializers
from rest_framework.response import Response
from file_service.files.models import FileTemplate, File
from django.template import Context
from django.template import Template as DjangoTemplate


class FilesViewSet(viewsets.ModelViewSet):
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    filter_fields = ('deleted', )
    permission_classes = (IsAuthenticated, )

    @detail_route(methods=['PATCH'])
    def metadata(self, request, pk):
        try:
            file = models.File.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.data.get('ready', False) in ['true', 'True', True]:
            serializer = serializers.MessageMetaDataSerializer(instance=file, data=request.data)
        else:
            serializer = serializers.FileSerializer.metadata_serializers.get(file.type.id)(instance=file, data=request.data)

        serializer.is_valid(raise_exception=True)
        file = serializer.save()

        result = serializers.FileSerializer(file).data
        return Response(data=result, status=status.HTTP_200_OK)

    @list_route(methods=['POST'])
    def from_template(self, request):
        template = request.data.pop("template", None)
        template = get_object_or_404(FileTemplate.objects.all(), alias=template)

        file_format = request.data.pop("format", None)
        generator = settings.FILE_GENERATORS.get(file_format, None)
        data = request.data.pop("data", None)

        if not generator:
            return Response(
                data={"error": "File with format {} cannot be created".format(file_format)},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            file_data = generator.create(template.body_template, data)

            file_name = DjangoTemplate(
                template.filename_template
            ).render(Context(data)) + generator.get_config('extension')

            file = File(
                owner=self.request.user.id,
                file=ContentFile(file_data, name=file_name),
                origin_filename=file_name,
                filename=file_name
            )
            file.save()

            return Response(serializers.FileSerializer(file).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.id)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class FileExtensionViewSet(viewsets.ModelViewSet):
    queryset = models.FileExtension.objects.all()
    serializer_class = serializers.FileExtensionSerializer
    permission_classes = (IsAuthenticated,)


class FileTypeViewSet(viewsets.ModelViewSet):
    queryset = models.FileType.objects.all()
    serializer_class = serializers.FileTypeSerializer
    permission_classes = (IsAuthenticated, )


class FileTemplateViewSet(viewsets.ModelViewSet):
    queryset = models.FileTemplate.objects.all()
    serializer_class = serializers.FileTemplateSerializer
    permission_classes = (IsAuthenticated, )
