import json

from file_service.trood_plugins.models import TroodPluginModel


class TroodBasePlugin:
    id = None
    default_config = {}

    @classmethod
    def get_config(cls):
        try:
            plugin_config = TroodPluginModel.objects.get(pk=cls.id)
            return json.loads(plugin_config.config)

        except Exception:
            return cls.default_config
