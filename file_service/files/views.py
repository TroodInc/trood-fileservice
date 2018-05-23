from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FormParser, MultiPartParser

from file_service.files import models, serializers
from rest_framework.response import Response

import requests
from rest_framework.views import APIView


class FilesViewSet(viewsets.ModelViewSet):
    parser_classes = (FormParser, MultiPartParser, )

    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    filter_fields = ('deleted', )

    @detail_route(methods=['PATCH'])
    def metadata(self, request, pk):
        try:
            file = models.File.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.data.get('ready', False) in ['true', 'True', True]:
            serializer = serializers.MessageMetaDataSerializer(instance=file, data=request.data)
        else:
            serializer = serializers.FileSerializer.metadata_serializers.get(file.type)(instance=file, data=request.data)

        serializer.is_valid(raise_exception=True)
        file = serializer.save()

        result = serializers.FileSerializer(file).data
        return Response(data=result, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class FilesExtensionManagerViewSet(viewsets.ModelViewSet):
    queryset = models.FileExtensions.objects.all()
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    @list_route(methods=['GET'])
    def allowed_extensions(self, request):
        file_extensions= models.FileExtensions.objects.get_or_create(id=1)[0]
        result = serializers.FileExtensionsSerializer(file_extensions).data
        return Response(data=result, status=status.HTTP_200_OK)

    @list_route(methods=['POST'])
    def set_extensions(self, request, id=None):
        serializer = serializers.FileExtensionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            allowed_extensions = serializer.validated_data.get(
                'allowed_extensions'
            )
            file_extensions = models.FileExtensions.objects.get_or_create(id=1)[0]
            file_extensions.allowed_extensions = allowed_extensions
            file_extensions.save()
        except Exception as e:
            raise ParseError(detail='Bad request: {}'.format(str(e)))
        result = serializers.FileExtensionsSerializer(file_extensions).data
        return Response(data=result, status=status.HTTP_200_OK)
