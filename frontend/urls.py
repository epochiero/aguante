from .views import IndexView, LoginView, DashboardView
from django.conf.urls import url

urlpatterns = (url(r'^$', DashboardView.as_view()),
               url(r'^login/$', LoginView.as_view(), name='login'),
               url(r'^dashboard/(?P<torneo>\d+)/(?P<fecha>\d+)/$',
                   DashboardView.as_view(), name='dashboard'),
               )
