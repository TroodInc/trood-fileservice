from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from trood.contrib.django.apps.plugins.views import TroodPluginsViewSet
from .files import views as files_views


admin.autodiscover()

router = DefaultRouter()

router.register(r'files', files_views.FilesViewSet)
router.register(r'extensions', files_views.FileExtensionViewSet)
router.register(r'types', files_views.FileTypeViewSet)
router.register(r'templates', files_views.FileTemplateViewSet)
router.register(r'plugins', TroodPluginsViewSet)

urlpatterns = [
    url(r'^api/v1.0/', include((router.urls, 'file_service'), namespace='api')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^admin/', include(admin.site.urls)),
        url('swagger/', TemplateView.as_view(template_name='swagger_ui.html'), name='swagger-ui'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
      + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
