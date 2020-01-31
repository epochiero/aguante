from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from futbol.views import FechaViewSet, PartidoViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'fecha', FechaViewSet)
router.register(r'partido', PartidoViewSet)

urlpatterns = [
    # Apps
    path('', include('frontend.urls')),

    # API
    path('api/', include(router.urls)),

    # Third-party
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(
        path('^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )

    # Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
