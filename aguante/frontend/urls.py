from .views import IndexView, LoginView, DashboardView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', DashboardView.as_view(), name='dashboard'),
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^dashboard/(?P<fecha>\d+)/$',
                           DashboardView.as_view(), name='dashboard'),
                       )
