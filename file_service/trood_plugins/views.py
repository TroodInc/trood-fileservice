from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from file_service.trood_plugins.models import TroodPluginModel
from file_service.trood_plugins.serialiers import TroodPluginSerizalizer


class TroodPluginsViewSet(viewsets.ModelViewSet):
    queryset = TroodPluginModel.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = TroodPluginSerizalizer