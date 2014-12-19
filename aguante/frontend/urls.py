from django.conf.urls import patterns, url
from .views import IndexView, LoginView, DashboardView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/(?P<fecha>\d+)/$', DashboardView.as_view(), name='dashboard'),
)
