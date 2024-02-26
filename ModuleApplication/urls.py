from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^list', views.get_lister_applications, name='module_application_list_applications'),
    url(r'^item/(?P<ref>[0-9]+)/$', views.get_details_application, name='module_application_details_application'),
    url(r'^item/(?P<ref>[0-9]+)/installer/$', views.get_installer_application, name='module_application_installer_application'),
    url(r'^item/(?P<ref>[0-9]+)/desinstaller/$', views.get_desinstaller_application, name='module_application_desinstaller_application'),
]