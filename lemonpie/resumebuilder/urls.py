from django.conf.urls import url

from . import views

app_name = 'resumebuilder'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<cv_id>[0-9]+)/$', views.cv_view, name='cv_view'),
    url(r'^(?P<cv_id>[0-9]+)/modify/$', views.modify_cv, name='modify_cv'),
    url(r'^add/$', views.add_new_cv, name='add_new_cv'),
    url(r'^(?P<cv_id>[0-9]+)/delete/$', views.delete_cv, name='delete_cv'),
]
