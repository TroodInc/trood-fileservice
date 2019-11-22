import io
import re

import textract
from django.db.models import signals

from file_service.files.models import File, FileTextContent
from trood.contrib.django.apps.plugins.core import TroodBasePlugin


class TextExtractorPlugin(TroodBasePlugin):
    id = 'extract_text'
    name = 'Text Extrator Plugin'
    version = 'v0.0.1'

    default_config = {
        'async': False,
        'extractable_mimetypes': [
            "application/pdf", "text/plain", "text/rtf", "application/rtf",
            "application/x-rtf", "text/csv", "application/msword",
            "text/richtext",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
            "application/vnd.ms-word.document.macroEnabled.12",
            "application/vnd.ms-word.template.macroEnabled.12", "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.template", 
            "application/vnd.ms-excel.sheet.macroEnabled.12",
            "application/vnd.ms-excel.template.macroEnabled.12",
            "application/vnd.ms-excel.addin.macroEnabled.12",
            "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/vnd.openxmlformats-officedocument.presentationml.template",
            "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
            "application/vnd.ms-powerpoint.addin.macroEnabled.12", 
            "application/vnd.ms-powerpoint.presentation.macroEnabled.12",
            "application/vnd.ms-powerpoint.template.macroEnabled.12",
            "application/vnd.ms-powerpoint.slideshow.macroEnabled.12", 
            "application/vnd.oasis.opendocument.spreadsheet", 
            "application/vnd.oasis.opendocument.text",
            "application/vnd.oasis.opendocument.presentation"
            ]
    }

    @classmethod
    def register(cls):
        signals.post_save.connect(cls.extract, File)

    @classmethod
    def extract(cls, sender, **kwargs):
        file = kwargs.get('instance')
        config = cls.get_config()
        if file.mimetype in config['extractable_mimetypes']:
            filepath = file.file.path
            b_text = textract.process(filepath)
            title = file.origin_filename.split('.')[0]
            raw_text = b_text.decode("utf-8")
            text = re.sub(r'\s+', ' ', re.sub(r'<[^<]+>', ' ', raw_text))
            FileTextContent.objects.create(source=file, content=text, title=title)

