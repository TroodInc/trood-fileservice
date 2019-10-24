from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from file_service.files import models, serializers
from rest_framework.response import Response
from django.template import Context
from django.template import Template as DjangoTemplate


def render_file(template, file_format, data, user):
    generator = settings.FILE_GENERATORS.get(file_format, None)
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

        file = models.File(
            owner=user.id,
            file=ContentFile(file_data, name=file_name),
            origin_filename=file_name,
            filename=file_name
        )
        file.save()

        return serializers.FileSerializer(file).data


class FilesViewSet(viewsets.ModelViewSet):
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    filter_fields = ('deleted', )

    @action(detail=False, methods=['POST'])
    def from_template(self, request):
        template = request.data.pop("template", None)
        template = get_object_or_404(models.FileTemplate.objects.all(), alias=template)

        file_format = request.data.pop("format", None)
        data = request.data.pop("data", None)

        result = render_file(template, file_format, data, request.user)

        return Response(
            data=result, status=status.HTTP_201_CREATED,
            headers={
                "Warning": "Endpoint /api/v1.0/files/from_template is deprecated and will be removed in NOV-23-2019"
            }
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.id)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class FileExtensionViewSet(viewsets.ModelViewSet):
    queryset = models.FileExtension.objects.all()
    serializer_class = serializers.FileExtensionSerializer


class FileTypeViewSet(viewsets.ModelViewSet):
    queryset = models.FileType.objects.all()
    serializer_class = serializers.FileTypeSerializer


class FileTemplateViewSet(viewsets.ModelViewSet):
    queryset = models.FileTemplate.objects.all()
    serializer_class = serializers.FileTemplateSerializer

    @action(detail=False, methods=['POST'])
    def preview(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(True):
            template = models.FileTemplate(**serializer.validated_data)
            result = render_file(template, request.data.get('format'), template.example_data, request.user)
            return Response(data={"status": "OK", "data": result}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def render(self, request, pk=None):
        template = get_object_or_404(self.queryset, pk=pk)

        if request.data.get("preview") == 'true':
            data = template.example_data
        else:
            data = request.data.pop("data", None)

        result = render_file(template, request.data.get('format'), data, request.user)
        return Response(data={"status": "OK", "data": result}, status=status.HTTP_201_CREATED)
