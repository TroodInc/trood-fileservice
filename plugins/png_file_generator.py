from file_service.trood_plugins.core import TroodBasePlugin
from weasyprint import HTML
from django.conf import settings
from django.template import Context
from django.template import Template as DjangoTemplate


class PNGFileGenerator(TroodBasePlugin):
    id = 'png_file_generator'
    name = 'Generating png files'
    version = 'v1.0.0'

    default_config = {
        'extension': '.png'
    }

    @classmethod
    def register(cls):
        settings.FILE_GENERATORS["PNG"] = cls

    @classmethod
    def create(cls, template_string, data):
        template = DjangoTemplate(template_string)
        document = HTML(string=template.render(Context(data))).render()
        return document.write_png()
