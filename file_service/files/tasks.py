import tempfile
import zipfile
from celery import shared_task
from django.core.files.base import ContentFile

from file_service.files.models import File


@shared_task
def make_zip(file_ids, result_id):
    print(f"zip task started for {result_id}")
    files = File.objects.filter(id__in=file_ids)

    print(files)

    with tempfile.TemporaryFile() as result_file:
        with zipfile.ZipFile(result_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for f in files:
                zipf.writestr(f"{f.id}-{f.origin_filename}", f.file.read())
                print(f"{f.id}-{f.origin_filename} added to zip")

        name = f'{result_file.name}.zip'
        result_file.seek(0)

        result = File.objects.get(id=result_id)
        print(f"updating {result.id}")

        result.name = name
        result.origin_filename = name
        result.file = ContentFile(content=result_file.read(), name=name)
        result.ready = True
        result.save()

    print("zip saved")
