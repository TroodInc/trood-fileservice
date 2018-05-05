from django.contrib import admin

from file_service.files import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'file', 'filename', 'deleted')
