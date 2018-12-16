from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from file_service.files import models, serializers
from rest_framework.response import Response


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