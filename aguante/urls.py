from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

urlpatterns = [
    # Apps
    path('', include('frontend.urls')),

    # Third-party
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )

    # Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
