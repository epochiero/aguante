from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers

from pronosticos.views import EquipoViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'equipos', EquipoViewSet)

urlpatterns = patterns('',
    # Apps
    url(r'', include('frontend.urls')),

    # API
    url(r'^api/', include(router.urls)),

    # Third-party
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += (
        url(r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework')),
    )

    # Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
