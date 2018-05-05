from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from .files import views as files_views

admin.autodiscover()

router = DefaultRouter()

router.register(r'files', files_views.FilesViewSet)

urlpatterns = [
    url(r'^api/v1.0/', include(router.urls, namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # @todo: @orn0t need to serve media by nginx

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
