from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.get_index, name='module_support_index'),
    url(r'^tableau', views.get_index, name='module_support_tableau_de_bord'),
]
    
#HISTORIQUE_ACTION URLS
#=====================================
#HISTORIQUE_ACTION CRUD URLS
urlpatterns.append(url(r'^historique_action/list', views.get_lister_historique_action, name = 'module_support_list_historique_action'))
urlpatterns.append(url(r'^historique_action/add', views.get_creer_historique_action, name = 'module_support_add_historique_action'))
urlpatterns.append(url(r'^historique_action/post_add', views.post_creer_historique_action, name = 'module_support_post_add_historique_action'))
urlpatterns.append(url(r'^historique_action/select/(?P<ref>[0-9]+)/$', views.get_select_historique_action, name = 'module_support_select_historique_action'))
urlpatterns.append(url(r'^historique_action/item/(?P<ref>[0-9]+)/$', views.get_details_historique_action, name = 'module_support_detail_historique_action'))
urlpatterns.append(url(r'^historique_action/item/(?P<ref>[0-9]+)/update$', views.get_modifier_historique_action, name = 'module_support_update_historique_action'))
urlpatterns.append(url(r'^historique_action/item/post_update/$', views.post_modifier_historique_action, name = 'module_support_post_update_historique_action'))
urlpatterns.append(url(r'^historique_action/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_historique_action, name = 'module_support_duplicate_historique_action'))
urlpatterns.append(url(r'^historique_action/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_historique_action, name = 'module_support_print_historique_action'))
#HISTORIQUE_ACTION UPLOAD URLS
urlpatterns.append(url(r'^historique_action/upload/add', views.get_upload_historique_action, name = 'module_support_get_upload_historique_action'))
urlpatterns.append(url(r'^historique_action/upload/post_add', views.post_upload_historique_action, name = 'module_support_post_upload_historique_action'))

#HISTORIQUE_ACTION API URLS
urlpatterns.append(url(r'^api/historique_action/list', views.get_list_historique_action, name = 'module_support_api_list_historique_action'))
urlpatterns.append(url(r'^api/historique_action/item', views.get_item_historique_action, name = 'module_support_api_item_historique_action'))
urlpatterns.append(url(r'^api/historique_action/create', views.post_create_historique_action, name = 'module_support_api_create_historique_action'))

#LOG URLS
#=====================================
#LOG CRUD URLS
urlpatterns.append(url(r'^log/list', views.get_lister_log, name = 'module_support_list_log'))
urlpatterns.append(url(r'^log/add', views.get_creer_log, name = 'module_support_add_log'))
urlpatterns.append(url(r'^log/post_add', views.post_creer_log, name = 'module_support_post_add_log'))
urlpatterns.append(url(r'^log/select/(?P<ref>[0-9]+)/$', views.get_select_log, name = 'module_support_select_log'))
urlpatterns.append(url(r'^log/item/(?P<ref>[0-9]+)/$', views.get_details_log, name = 'module_support_detail_log'))
urlpatterns.append(url(r'^log/item/(?P<ref>[0-9]+)/update$', views.get_modifier_log, name = 'module_support_update_log'))
urlpatterns.append(url(r'^log/item/post_update/$', views.post_modifier_log, name = 'module_support_post_update_log'))
urlpatterns.append(url(r'^log/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_log, name = 'module_support_duplicate_log'))
urlpatterns.append(url(r'^log/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_log, name = 'module_support_print_log'))
#LOG UPLOAD URLS
urlpatterns.append(url(r'^log/upload/add', views.get_upload_log, name = 'module_support_get_upload_log'))
urlpatterns.append(url(r'^log/upload/post_add', views.post_upload_log, name = 'module_support_post_upload_log'))
