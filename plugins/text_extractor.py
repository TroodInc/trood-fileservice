import io
import re
import zipfile

from django.conf import settings
from django.db.models import signals

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from file_service.files.models import File
from file_service.trood_plugins.core import TroodBasePlugin


class TextExtractorPlugin(TroodBasePlugin):
    id = 'extract_text'
    name = 'Text Extrator Plugin'
    version = 'v0.0.1'

    default_config = {
        'async': False,
        'types': ['TXT']
    }

    @classmethod
    def register(cls):
        signals.post_save.connect(cls.extract, File)

    @classmethod
    def extract(cls, sender, instance, **kwargs):
        config = cls.get_config()
        if instance.type_id in config['types']:
            extractor = cls.get_extractor(instance.type_id)
            raw_text = extractor(instance.file.filepath)
            text = re.sub(r'\s+', ' ', re.sub(r'<[^<]+>', ' ', raw_text))
            FileTextContent.objects.create(source=instance, content=text)

    @classmethod
    def get_extractor(cls, type_id):
        return getattr(Extractor, instance.type_id)


class Extrator:

    @classmethod
    def txt(cls, filepath):
        with open(filepath, 'r') as input_file:
            text = ' '.join(input_file.readlines())

        return text

    @classmethod
    def xml(cls, filepath):
        with zipfile.ZipFile(filepath) as doc:
            text = doc.read('word/document.xml').decode()

        return text

    @classmethod
    def pdf(cls, filepath):
        resource_manager = PDFResourceManager()
        with io.StringIO() as fake_file_handle:
            with TextConverter(resource_manager, fake_file_handle) as converter:
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                with open(filepath, 'rb') as pdf:
                    pages = PDFPage.get_pages(pdf, caching=True, check_extractable=True)
                    [page_interpreter.process_page(p) for p in pages]
                
            text = fake_file_handle.getvalue()

        return text
