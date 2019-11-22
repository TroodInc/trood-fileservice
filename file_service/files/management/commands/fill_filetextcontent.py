import logging
from django.core.management.base import BaseCommand
from file_service.files.models import File, FileTextContent
from plugins.text_extractor import TextExtractorPlugin
import textract
import re
import os.path


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # TODO make this command async/or able to run in background via textextractor plagin
        files = File.objects.all()
        config = TextExtractorPlugin.default_config
        for file in files:
            if file.mimetype in config['extractable_mimetypes']:
                filepath = file.file.path
                if os.path.exists(filepath):
                    b_text = textract.process(filepath)
                    raw_text = b_text.decode("utf-8")
                    title = file.origin_filename.split('.')[0]
                    text = re.sub(r'\s+', ' ', re.sub(r'<[^<]+>', ' ', raw_text))
                    FileTextContent.objects.get_or_create(
                        source=file, content=text, title=title
                        )
        logger.debug("Extraction complited")


