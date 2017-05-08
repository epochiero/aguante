from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
#from futbol.views import FechaViewSet, PartidoViewSet
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'fecha', FechaViewSet)
# router.register(r'partido', PartidoViewSet)

urlpatterns = (
    # Apps
    url(r'', include('frontend.urls')),

    # API
    # url(r'^api/', include(router.urls)),

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
    urlpatterns += tuple(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
