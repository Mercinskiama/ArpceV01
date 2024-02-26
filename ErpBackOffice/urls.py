from django.conf.urls import include, url
#from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.get_index, name='backoffice_index'),
    url(r'^erreur/autorisation', views.get_not_autorize, name='backoffice_erreur_autorisation'),
    url(r'^utilisateur/connexion/$', views.get_connexion, name='backoffice_connexion'),
    url(r'^utilisateur/post_connexion/$', views.post_connexion, name='backoffice_post_connexion'),
    url(r'^utilisateur/deconnexion/$', views.get_deconnexion, name='backoffice_deconnexion'),
    url(r'^erreur/role', views.get_not_role, name='backoffice_erreur_role'),
    url(r'^utilisateur/accueil', views.get_accueil, name='backoffice_acceuil'),
    url(r'^utilisateur/change_password/$', views.get_password, name='backoffice_change_password'),
    url(r'^utilisateur/post_change_password/$', views.post_password, name='backoffice_post_change_password'),
    url(r'^utilisateur/profile/$', views.get_profile, name='backoffice_profile'),

    # PLACE URLS
	url(r'^places/filles', views.get_json_list_places_filles, name='backoffice_list_places_filles'),

    url(r'get_transition_next', views.get_json_next_transition, name='backoffice_list_next_transition'),

    #url formulaire imbriqué
    url(r'^model/get', views.backoffice_list_model, name="backoffice_list_model"),
]

urlpatterns.append(url(r'^workflow_post', views.post_workflow, name = 'backoffice_workflow_post'))
urlpatterns.append(url(r'^cancel_workflow', views.post_cancel_workflow, name = 'backoffice_cancel_workflow_post'))
urlpatterns.append(url(r'^stakeholder_delegation_workflow', views.post_stakeholder_delegation_workflow, name = 'backoffice_stakeholder_delegation_workflow_post'))
urlpatterns.append(url(r'^stakeholder_configuration_workflow', views.post_stakeholder_configuration_workflow, name = 'backoffice_stakeholder_configuration_workflow_post'))
urlpatterns.append(url(r'document/delete/(?P<ref>[0-9]+)/(?P<modele>\w+)/(?P<the_url>\w+)/$', views.backoffice_delete_doc, name='backoffice_delete_document'))

urlpatterns.append(url(r'^objet/supprimer/(?P<ref>[0-9]+)/(?P<modele>\w+)/(?P<the_url>\w+)/$',views.post_supprimmer_objet, name='backoffice_supprimer_objet'))

urlpatterns.append(url(r'^objet/print/$',views.post_generate_pdf, name='back_office_print_objet'))
urlpatterns.append(url(r'^objet/html_to_pdf/$',views.post_print_html_to_pdf, name='back_office_html_to_pdf_objet'))

#WEASYPRINT ALL OBJECTS
urlpatterns.append(url(r'^objet/weasyprint/$',views.post_weasyprint_objet, name='back_office_weasyprint_objet'))

urlpatterns.append(url(r'^notification/vue/(?P<ref>[0-9]+)/', views.get_update_notification, name = 'back_office_notification'))

urlpatterns.append(url(r'^request/bi/data', views.get_data_request, name = 'back_office_data_request'))
urlpatterns.append(url(r'^request/list_choices', views.get_data_list_choices, name = 'back_office_data_list_choices'))
urlpatterns.append(url(r'^request/related_field', views.get_data_related_field, name = 'back_office_data_related_field'))
