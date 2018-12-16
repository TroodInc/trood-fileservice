from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from file_service.trood_plugins import views

router = DefaultRouter()

router.register(r'plugins', views.TroodPluginsViewSet)

urlpatterns = [
    url(r'^api/v1.0/', include(router.urls, namespace='plugins-api')),
]
