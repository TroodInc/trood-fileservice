from rest_framework import serializers

from file_service.trood_plugins.models import TroodPluginModel


class TroodPluginSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = TroodPluginModel
        fields = ('id', 'name', 'version', 'config')
