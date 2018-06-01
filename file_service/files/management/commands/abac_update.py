import json

import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.urls import RegexURLResolver, RegexURLPattern
from rest_framework.utils import encoders
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class Command(BaseCommand):
    help = """Importing MethodologyTemplate from JSON format"""

    def add_arguments(self, parser):
        # parser.add_argument('file_path', type=str, help="paths to JSON file")
        # parser.add_argument(
        #     '-r', '--recursive',
        #     action='store_true', dest='recursive', default=False, help="Import all files from path"
        # )
        pass

    def handle(self, *args, **options):
        root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
        all_urlpatterns = root_urlconf.urls.urlpatterns  # project's urlpatterns

        abac_resources = {}

        def get_all_view_names(urlpatterns):

            for pattern in urlpatterns:

                if isinstance(pattern, RegexURLResolver):
                    get_all_view_names(pattern.url_patterns)
                elif isinstance(pattern, RegexURLPattern):
                    if hasattr(pattern.callback, "cls") and hasattr(pattern.callback.cls, "_is_abac"):
                        clb = pattern.callback

                        if clb.cls._abac_resource not in abac_resources.keys():
                            abac_resources[clb.cls._abac_resource] = {
                                "info": clb.cls.__doc__,
                                "actions": set(),
                                "attributes": set(),
                            }

                        if issubclass(clb.cls, ModelViewSet):
                            abac_resources[clb.cls._abac_resource]['actions'] |= set(
                                clb.__wrapped__.actions.values()
                            )
                            qs = clb.cls.get_queryset(clb.cls)

                            abac_resources[clb.cls._abac_resource]['attributes'] |= self.get_flat_model_fields(qs.model)

                            continue

                        if issubclass(clb.cls, APIView):
                            keys = set(clb.cls.__dict__.keys())
                            need = set(clb.cls.http_method_names)
                            abac_resources[clb.cls._abac_resource]['actions'] |= keys & need

                            continue

            return abac_resources

        get_all_view_names(all_urlpatterns)

        print(json.dumps(self.cleanup_sets(abac_resources), indent=4))
        self.provision_abac_service(abac_resources)

    def cleanup_sets(self, resources):
        return {k: {
            "info": v['info'],
            "actions": list(v['actions']),
            "attributes": list(v['attributes'])
        } for k, v in resources.items()}

    def provision_abac_service(self, resources):
        # @todo: use setting or Director for getting url
        response = requests.post(
            "http://authorization.trood:8000/api/v1.0/abac-provision/",
            headers={"Authorization": "Service fileservice"},
            json={
                "domain": settings.DOMAIN,
                "resources":  self.cleanup_sets(resources)
            },
        )

        print("Provisioned:")
        print(json.dumps(response.json(), indent=4))

    def prefix_model_fields(self, name, prefix):
        if prefix:
            return "%s.%s" % (prefix, name)
        return name

    def get_flat_model_fields(self, model):
        return {name for name in self.iter_model_fields(model)}

    def iter_model_fields(self, model, prefix=None):
        fields = model._meta.fields
        for field in fields:
            name = self.prefix_model_fields(field.attname, prefix)
            yield name
            if field.rel:
                rel = field.rel.to
                for f in self.iter_model_fields(rel, name):
                    yield f
