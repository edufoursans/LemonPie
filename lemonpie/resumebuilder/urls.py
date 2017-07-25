from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cv_id>[0-9]+)/$', views.cv_view, name='cv_view'),
]
