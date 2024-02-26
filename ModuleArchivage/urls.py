from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.get_index, name='module_archivage_index'),
    url(r'^tableau', views.get_index, name='module_archivage_tableau_de_bord'),
]

#DOCUMENT URLS
#=====================================
#DOCUMENT CRUD URLS
urlpatterns.append(url(r'^document/list', views.get_lister_document, name = 'module_archivage_list_document'))
urlpatterns.append(url(r'^document/add', views.get_creer_document, name = 'module_archivage_add_document'))
urlpatterns.append(url(r'^document/post_add', views.post_creer_document, name = 'module_archivage_post_add_document'))
urlpatterns.append(url(r'^document/item/(?P<ref>[0-9]+)/$', views.get_details_document, name = 'module_archivage_detail_document'))
urlpatterns.append(url(r'^document/item/post_update/$', views.post_modifier_document, name = 'module_archivage_post_update_document'))
urlpatterns.append(url(r'^document/item/(?P<ref>[0-9]+)/update$', views.get_modifier_document, name = 'module_archivage_update_document'))
urlpatterns.append(url(r'^document/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_document, name = 'module_archivage_duplicate_document'))
urlpatterns.append(url(r'^document/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_document, name = 'module_archivage_print_document'))
#DOCUMENT UPLOAD URLS
urlpatterns.append(url(r'^document/upload/add', views.get_upload_document, name = 'module_archivage_get_upload_document'))
urlpatterns.append(url(r'^document/upload/post_add', views.post_upload_document, name = 'module_archivage_post_upload_document'))

#DOCUMENT REPORTING URLS
urlpatterns.append(url(r'^document/generate', views.get_generer_document, name = 'module_archivage_get_generer_document'))
urlpatterns.append(url(r'^document/post_generate', views.post_generer_document, name = 'module_archivage_post_generer_document'))
urlpatterns.append(url(r'^document/print_generate', views.post_imprimer_rapport_document, name = 'module_archivage_post_imprimer_rapport_document'))

#DOSSIER URLS
#=====================================
#DOSSIER CRUD URLS
urlpatterns.append(url(r'^dossier/list', views.get_lister_dossier, name = 'module_archivage_list_dossier'))
urlpatterns.append(url(r'^dossier/add', views.get_creer_dossier, name = 'module_archivage_add_dossier'))
urlpatterns.append(url(r'^dossier/post_add', views.post_creer_dossier, name = 'module_archivage_post_add_dossier'))
urlpatterns.append(url(r'^dossier/item/(?P<ref>[0-9]+)/$', views.get_details_dossier, name = 'module_archivage_detail_dossier'))
urlpatterns.append(url(r'^dossier/item/post_update/$', views.post_modifier_dossier, name = 'module_archivage_post_update_dossier'))
urlpatterns.append(url(r'^dossier/item/(?P<ref>[0-9]+)/update$', views.get_modifier_dossier, name = 'module_archivage_update_dossier'))
urlpatterns.append(url(r'^dossier/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_dossier, name = 'module_archivage_duplicate_dossier'))
urlpatterns.append(url(r'^dossier/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_dossier, name = 'module_archivage_print_dossier'))
#DOSSIER UPLOAD URLS
urlpatterns.append(url(r'^dossier/upload/add', views.get_upload_dossier, name = 'module_archivage_get_upload_dossier'))
urlpatterns.append(url(r'^dossier/upload/post_add', views.post_upload_dossier, name = 'module_archivage_post_upload_dossier'))

#CATEGORIE_TAG URLS
#=====================================
#CATEGORIE_TAG CRUD URLS
urlpatterns.append(url(r'^categorie_tag/list', views.get_lister_categorie_tag, name = 'module_archivage_list_categorie_tag'))
urlpatterns.append(url(r'^categorie_tag/add', views.get_creer_categorie_tag, name = 'module_archivage_add_categorie_tag'))
urlpatterns.append(url(r'^categorie_tag/post_add', views.post_creer_categorie_tag, name = 'module_archivage_post_add_categorie_tag'))
urlpatterns.append(url(r'^categorie_tag/item/(?P<ref>[0-9]+)/$', views.get_details_categorie_tag, name = 'module_archivage_detail_categorie_tag'))
urlpatterns.append(url(r'^categorie_tag/item/post_update/$', views.post_modifier_categorie_tag, name = 'module_archivage_post_update_categorie_tag'))
urlpatterns.append(url(r'^categorie_tag/item/(?P<ref>[0-9]+)/update$', views.get_modifier_categorie_tag, name = 'module_archivage_update_categorie_tag'))
urlpatterns.append(url(r'^categorie_tag/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_categorie_tag, name = 'module_archivage_duplicate_categorie_tag'))
urlpatterns.append(url(r'^categorie_tag/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_categorie_tag, name = 'module_archivage_print_categorie_tag'))
#CATEGORIE_TAG UPLOAD URLS
urlpatterns.append(url(r'^categorie_tag/upload/add', views.get_upload_categorie_tag, name = 'module_archivage_get_upload_categorie_tag'))
urlpatterns.append(url(r'^categorie_tag/upload/post_add', views.post_upload_categorie_tag, name = 'module_archivage_post_upload_categorie_tag'))

#TAG URLS
#=====================================
#TAG CRUD URLS
urlpatterns.append(url(r'^tag/list', views.get_lister_tag, name = 'module_archivage_list_tag'))
urlpatterns.append(url(r'^tag/add', views.get_creer_tag, name = 'module_archivage_add_tag'))
urlpatterns.append(url(r'^tag/post_add', views.post_creer_tag, name = 'module_archivage_post_add_tag'))
urlpatterns.append(url(r'^tag/item/(?P<ref>[0-9]+)/$', views.get_details_tag, name = 'module_archivage_detail_tag'))
urlpatterns.append(url(r'^tag/item/post_update/$', views.post_modifier_tag, name = 'module_archivage_post_update_tag'))
urlpatterns.append(url(r'^tag/item/(?P<ref>[0-9]+)/update$', views.get_modifier_tag, name = 'module_archivage_update_tag'))
urlpatterns.append(url(r'^tag/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_tag, name = 'module_archivage_duplicate_tag'))
urlpatterns.append(url(r'^tag/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_tag, name = 'module_archivage_print_tag'))
#TAG UPLOAD URLS
urlpatterns.append(url(r'^tag/upload/add', views.get_upload_tag, name = 'module_archivage_get_upload_tag'))
urlpatterns.append(url(r'^tag/upload/post_add', views.post_upload_tag, name = 'module_archivage_post_upload_tag'))

#DOCUMENT_PARTAGE URLS
#=====================================
#DOCUMENT_PARTAGE CRUD URLS
urlpatterns.append(url(r'^document_partage/list', views.get_lister_document_partage, name = 'module_archivage_list_document_partage'))
urlpatterns.append(url(r'^document_partage/add', views.get_creer_document_partage, name = 'module_archivage_add_document_partage'))
urlpatterns.append(url(r'^document_partage/post_add', views.post_creer_document_partage, name = 'module_archivage_post_add_document_partage'))
urlpatterns.append(url(r'^document_partage/item/(?P<ref>[0-9]+)/$', views.get_details_document_partage, name = 'module_archivage_detail_document_partage'))
urlpatterns.append(url(r'^document_partage/item/post_update/$', views.post_modifier_document_partage, name = 'module_archivage_post_update_document_partage'))
urlpatterns.append(url(r'^document_partage/item/(?P<ref>[0-9]+)/update$', views.get_modifier_document_partage, name = 'module_archivage_update_document_partage'))
urlpatterns.append(url(r'^document_partage/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_document_partage, name = 'module_archivage_duplicate_document_partage'))
urlpatterns.append(url(r'^document_partage/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_document_partage, name = 'module_archivage_print_document_partage'))
#DOCUMENT_PARTAGE UPLOAD URLS
urlpatterns.append(url(r'^document_partage/upload/add', views.get_upload_document_partage, name = 'module_archivage_get_upload_document_partage'))
urlpatterns.append(url(r'^document_partage/upload/post_add', views.post_upload_document_partage, name = 'module_archivage_post_upload_document_partage'))
