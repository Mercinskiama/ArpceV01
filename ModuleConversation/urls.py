from django.conf.urls import include, url
from . import views
urlpatterns = [
        url(r'^$', views.get_index, name='module_conversation_index'),
]
    
urlpatterns.append(url(r'^message/list', views.get_lister_message, name = 'module_conversation_list_message'))
urlpatterns.append(url(r'^message/sent', views.get_lister_msg_sent, name = 'module_conversation_list_msg_sent'))
urlpatterns.append(url(r'^message/add', views.get_creer_message, name = 'module_conversation_add_message'))
urlpatterns.append(url(r'^message/post_add', views.post_creer_message, name = 'module_conversation_post_add_message'))
urlpatterns.append(url(r'^message/item/(?P<ref>[0-9]+)/$', views.get_details_message, name = 'module_conversation_detail_message'))
urlpatterns.append(url(r'^message/sent/(?P<ref>[0-9]+)/$', views.get_details_msg_sent, name = 'module_conversation_detail_msg_sent'))
urlpatterns.append(url(r'^message/item/post_update/$', views.post_modifier_message, name = 'module_conversation_post_update_message'))
urlpatterns.append(url(r'^message/item/(?P<ref>[0-9]+)/update$', views.get_modifier_message, name = 'module_conversation_update_message'))

urlpatterns.append(url(r'^notification/list', views.get_lister_notification, name = 'module_conversation_list_notification'))
urlpatterns.append(url(r'^notification/add', views.get_creer_notification, name = 'module_conversation_add_notification'))
urlpatterns.append(url(r'^notification/post_add', views.post_creer_notification, name = 'module_conversation_post_add_notification'))
urlpatterns.append(url(r'^notification/item/(?P<ref>[0-9]+)/$', views.get_details_notification, name = 'module_conversation_detail_notification'))
urlpatterns.append(url(r'^notification/item/post_update/$', views.post_modifier_notification, name = 'module_conversation_post_update_notification'))
urlpatterns.append(url(r'^notification/item/(?P<ref>[0-9]+)/update$', views.get_modifier_notification, name = 'module_conversation_update_notification'))

urlpatterns.append(url(r'^notification/delete/item/(?P<ref>[0-9]+)', views.get_delete_notification, name = 'module_conversation_get_delete_notification'))