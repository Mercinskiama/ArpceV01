from django.conf.urls import include, url
from . import views

urlpatterns = [
	# DASHBOARD AND HOME URL
    url(r'^$', views.get_dashboard, name='module_configuration_index'),
	url(r'^dashboard', views.get_dashboard, name='module_configuration_dashboard'),

	#JSON
	url(r'all_sous_module_of_module', views.get_json_sous_modules, name='module_configuration_get_json_sous_modules'),
	 
	# UTILISATEUR URLS
	url(r'^utilisateurs/list', views.get_lister_utilisateurs, name='module_configuration_list_utilisateurs'),
	url(r'^utilisateurs/add', views.get_creer_utilisateur, name='module_configuration_add_utilisateur'),
	url(r'^utilisateurs/post_add', views.post_creer_utilisateur, name='module_configuration_post_add_utilisateur'),
	url(r'^utilisateurs/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_utilisateur, name='module_configuration_update_utilisateur'),
	url(r'^utilisateurs/item/post_update/$', views.post_modifier_utilisateur, name='module_configuration_post_update_utilisateur'),
	url(r'^utilisateurs/item/(?P<ref>[0-9]+)/$', views.get_details_utilisateur, name='module_configuration_details_utilisateur'),

	# ROLES URLS
	url(r'^roles/list', views.get_lister_roles, name='module_configuration_list_roles'),
	url(r'^roles/add', views.get_creer_role, name='module_configuration_add_role'),
	url(r'^roles/post_add', views.post_creer_role, name='module_configuration_post_add_role'),
	url(r'^roles/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_role, name='module_configuration_update_role'),

	
	url(r'^roles/item/post_update/$', views.post_modifier_role, name='module_configuration_post_update_role'),
	url(r'^roles/item/(?P<ref>[0-9]+)/$', views.get_details_role, name='module_configuration_details_role'),
	url(r'^roles/item/(?P<ref>[0-9]+)/rights/add/$', views.get_ajouter_droits, name='module_configuration_add_rights'),
	url(r'^roles/item/rights/post_add/$', views.post_ajouter_droits, name='module_configuration_post_add_rights'),
	url(r'^roles/item/(?P<ref>[0-9]+)/rights/remove/$', views.get_retirer_droits, name='module_configuration_remove_rights'),
	url(r'^roles/item/rights/post_remove/$', views.post_retirer_droits, name='module_configuration_post_remove_rights'),

	
	# DROIT URLS
	#url(r'^droit/add', views.get_creer_droits, name='module_configuration_add_droits'),
	#url(r'^droit/list', views.get_lister_droits, name='module_configuration_list_droits'),
	#url(r'^droit/item/(?P<ref>[0-9]+)/$', views.get_details_droits, name='module_configuration_details_droit'),

	# ROLES UTILISATEUR
	url(r'^utilisateurs/item/(?P<ref>[0-9]+)/roles/attribute/$', views.get_attribuer_role, name='module_configuration_attribuer_role'),
	url(r'^utilisateurs/item/roles/post_attribute/$', views.post_attribuer_role, name='module_configuration_post_attribuer_role'),
	url(r'^utilisateurs/item/(?P<ref_utilisateur>[0-9]+)/roles/item/(?P<ref_role>[0-9]+)/retire/$', views.get_retirer_role, name='module_configuration_retirer_role'),

	# PLACE URLS
	url(r'^places/filles', views.get_json_list_places_filles, name='module_configuration_list_places_filles'),
	
	#EMPLOYEE URLS JSON

	url(r'^json/employee', views.get_json_employee, name='module_configuration_list_json_employee'),

	# CONFIGURATION URLS	
	url(r'^configuration', views.get_configuration, name='module_configuration_configuration'),
	url(r'^configuration/post_update/$', views.post_modifier_configuration, name='module_configuration_post_modifier_configuration'),	
	
	

	#MODULE URLS (GENERATION)
	url(r'^modules/list', views.get_lister_modules, name='module_configuration_list_modules'),
	url(r'^modules/add', views.get_creer_module, name='module_configuration_add_module'),
	url(r'^modules/post_add', views.post_creer_module, name='module_configuration_post_add_module'),
	url(r'^modules/item/(?P<ref>[0-9]+)/$', views.get_details_module, name='module_configuration_details_module'),
	url(r'^modules/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_module, name='module_configuration_update_module'),
	url(r'^modules/item/post_update/$', views.post_modifier_module, name='module_configuration_post_update_module'),
	url(r'^modules/item/(?P<ref>[0-9]+)/addModel/$', views.get_creer_modele, name='module_configuration_add_modele'),
	url(r'^modules/item/(?P<ref>[0-9]+)/post_addModel/$', views.post_creer_modele, name='module_configuration_post_add_modele'),
	url(r'^modules/item/(?P<ref>[0-9]+)/exportModel/$', views.get_exporter_modele, name='module_configuration_exporter_modele'),

	#SQUELETTE module_configuration_add_dao_template
	url(r'^framework/generate', views.get_creer_framework, name='module_configuration_generate_framework'),
	url(r'^framework/post_generate', views.post_creer_framework, name='module_configuration_post_generate_framework'),

	#TEST UNIT
	url(r'^test/generate', views.get_creer_test, name='module_configuration_generate_test'),
	url(r'^test/post_generate', views.post_creer_test, name='module_configuration_post_generate_test'),

	#TEST SELENIUM
	url(r'^selenium/generate', views.get_creer_selenium, name='module_configuration_generate_selenium'),
	url(r'^selenium/post_generate', views.post_creer_selenium, name='module_configuration_post_generate_selenium'),

	#DAO ET TEMPLATES
	url(r'^modules/dao_template/add', views.get_creer_dao_template, name='module_configuration_add_dao_template'),
	url(r'^modules/dao_template/post_add', views.post_creer_dao_template, name='module_configuration_post_add_dao_template'),

	#SOUS MODULES (GENERATION)
	url(r'^sous_modules/list/(?P<ref>[0-9]+)/$', views.get_lister_sous_modules_of_module, name='module_configuration_list_sous_modules'),
	url(r'^sous_modules/add/(?P<ref>[0-9]+)/$', views.get_creer_sous_module_of_module, name='module_configuration_add_sous_module'),
	url(r'^sous_modules/post_add/(?P<ref>[0-9]+)/$', views.post_creer_sous_module_of_module, name='module_configuration_post_add_sous_module'),
	url(r'^sous_modules/item/(?P<ref>[0-9]+)/(?P<ref2>[0-9]+)/$', views.get_details_sous_module_of_module, name='module_configuration_details_sous_module'),
	url(r'^sous_modules/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_sous_module_of_module, name='module_configuration_update_sous_module'),
	url(r'^sous_modules/item/module/post_update', views.post_modifier_sous_module_of_module, name='module_configuration_post_update_sous_module'),
    url(r'^ajax/sous_modules/get/model/related/$', views.ajax_get_related_models, name="ajax_get_related_models"),
    url(r'^ajax/sous_modules/get/urls/names/$', views.ajax_get_urls_names, name="ajax_get_urls_names"),
	
	#WORKFLOW
	url(r'^workflow/list', views.get_lister_workflow, name='module_configuration_list_workflow'),
	url(r'^workflow/add', views.get_creer_workflow, name='module_configuration_add_workflow'),
	url(r'^workflow/post_add', views.post_creer_workflow, name='module_configuration_post_add_workflow'),
	url(r'^workflow/item/(?P<ref>[0-9]+)/$', views.get_details_workflow, name='module_configuration_detail_workflow'),

	#ETAPE
	#url(r'^etape/list', views.get_lister_etape, name='module_configuration_list_etape'),
	url(r'^etape/add/(?P<ref>[0-9]+)', views.get_creer_etape, name='module_configuration_add_etape'),
	url(r'^etape/post_add', views.post_creer_etape, name='module_configuration_post_add_etape'),

	# TRANSITION
	url(r'^transition/add/(?P<ref>[0-9]+)', views.get_creer_transition, name='module_configuration_add_transition'),
	url(r'^transition/post_add', views.post_creer_transition, name='module_configuration_post_add_transition'),


	# REGLES URLS
	url(r'^regle/list', views.get_lister_regle, name='module_configuration_list_regle'),
	url(r'^regle/add', views.get_creer_regle, name='module_configuration_add_regle'),
	url(r'^regle/item/(?P<ref>[0-9]+)/$', views.get_details_regle, name='module_configuration_details_regle'),
	url(r'^regle/post_add', views.post_creer_regle, name='module_configuration_post_add_regle'),
	
]
urlpatterns.append(url(r'^permission/list', views.get_lister_permission, name = 'module_Configuration_list_permission'))
urlpatterns.append(url(r'^permission/add', views.get_creer_permission, name = 'module_Configuration_add_permission'))
urlpatterns.append(url(r'^permission/post_add', views.post_creer_permission, name = 'module_Configuration_post_add_permission'))
urlpatterns.append(url(r'^permission/item/(?P<ref>[0-9]+)/$', views.get_details_permission, name = 'module_Configuration_detail_permission'))
urlpatterns.append(url(r'^permission/item/post_update/$', views.post_modifier_permission, name = 'module_Configuration_post_update_permission'))
urlpatterns.append(url(r'^permission/item/(?P<ref>[0-9]+)/update$', views.get_modifier_permission, name = 'module_Configuration_update_permission'))
urlpatterns.append(url(r'^actionutilisateur/list', views.get_lister_actionutilisateur, name = 'module_Configuration_list_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/add', views.get_creer_actionutilisateur, name = 'module_Configuration_add_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/post_add', views.post_creer_actionutilisateur, name = 'module_Configuration_post_add_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/item/(?P<ref>[0-9]+)/$', views.get_details_actionutilisateur, name = 'module_Configuration_detail_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/item/post_update/$', views.post_modifier_actionutilisateur, name = 'module_Configuration_post_update_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/item/(?P<ref>[0-9]+)/update$', views.get_modifier_actionutilisateur, name = 'module_Configuration_update_actionutilisateur'))
urlpatterns.append(url(r'^sousmodule/list', views.get_lister_sousmodule, name = 'module_Configuration_list_sousmodule'))
urlpatterns.append(url(r'^sousmodule/add', views.get_creer_sousmodule, name = 'module_Configuration_add_sousmodule'))
urlpatterns.append(url(r'^sousmodule/post_add', views.post_creer_sousmodule, name = 'module_Configuration_post_add_sousmodule'))
urlpatterns.append(url(r'^sousmodule/item/(?P<ref>[0-9]+)/$', views.get_details_sousmodule, name = 'module_Configuration_detail_sousmodule'))
urlpatterns.append(url(r'^sousmodule/item/post_update/$', views.post_modifier_sousmodule, name = 'module_Configuration_post_update_sousmodule'))
urlpatterns.append(url(r'^sousmodule/item/(?P<ref>[0-9]+)/update$', views.get_modifier_sousmodule, name = 'module_Configuration_update_sousmodule'))
urlpatterns.append(url(r'^groupemenu/list', views.get_lister_groupemenu, name = 'module_Configuration_list_groupemenu'))
urlpatterns.append(url(r'^groupemenu/add', views.get_creer_groupemenu, name = 'module_Configuration_add_groupemenu'))
urlpatterns.append(url(r'^groupemenu/post_add', views.post_creer_groupemenu, name = 'module_Configuration_post_add_groupemenu'))
urlpatterns.append(url(r'^groupemenu/item/(?P<ref>[0-9]+)/$', views.get_details_groupemenu, name = 'module_Configuration_detail_groupemenu'))
urlpatterns.append(url(r'^groupemenu/item/post_update/$', views.post_modifier_groupemenu, name = 'module_Configuration_post_update_groupemenu'))
urlpatterns.append(url(r'^groupemenu/item/(?P<ref>[0-9]+)/update$', views.get_modifier_groupemenu, name = 'module_Configuration_update_groupemenu'))


urlpatterns.append(url(r'^sousmodule/wizard', views.get_creer_wizard_menu, name = 'module_Configuration_add_wizard_menu'))
urlpatterns.append(url(r'^sousmodule/post_wizard', views.post_creer_wizard_menu, name = 'module_Configuration_post_add_wizard_menu'))

#SOCIETE URLS
#=====================================
#SOCIETE CRUD URLS
urlpatterns.append(url(r'^societe/list', views.get_lister_societe, name = 'module_configuration_list_societe'))
urlpatterns.append(url(r'^societe/add', views.get_creer_societe, name = 'module_configuration_add_societe'))
urlpatterns.append(url(r'^societe/post_add', views.post_creer_societe, name = 'module_configuration_post_add_societe'))
urlpatterns.append(url(r'^societe/select/(?P<ref>[0-9]+)/$', views.get_select_societe, name = 'module_configuration_select_societe'))
urlpatterns.append(url(r'^societe/item/(?P<ref>[0-9]+)/$', views.get_details_societe, name = 'module_configuration_detail_societe'))
urlpatterns.append(url(r'^societe/item/(?P<ref>[0-9]+)/update$', views.get_modifier_societe, name = 'module_configuration_update_societe'))
urlpatterns.append(url(r'^societe/item/post_update/$', views.post_modifier_societe, name = 'module_configuration_post_update_societe'))
urlpatterns.append(url(r'^societe/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_societe, name = 'module_configuration_duplicate_societe'))
urlpatterns.append(url(r'^societe/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_societe, name = 'module_configuration_print_societe'))
#SOCIETE UPLOAD URLS
urlpatterns.append(url(r'^societe/upload/add', views.get_upload_societe, name = 'module_configuration_get_upload_societe'))
urlpatterns.append(url(r'^societe/upload/post_add', views.post_upload_societe, name = 'module_configuration_post_upload_societe'))

#SOCIETE API URLS
urlpatterns.append(url(r'^api/societe/list', views.get_list_societe, name = 'module_configuration_api_list_societe'))
urlpatterns.append(url(r'^api/societe/item', views.get_item_societe, name = 'module_configuration_api_item_societe'))
urlpatterns.append(url(r'^api/societe/create', views.post_create_societe, name = 'module_configuration_api_create_societe'))

#CONTACT URLS
#=====================================
#CONTACT CRUD URLS
urlpatterns.append(url(r'^contact/list', views.get_lister_contact, name = 'module_configuration_list_contact'))
urlpatterns.append(url(r'^contact/add', views.get_creer_contact, name = 'module_configuration_add_contact'))
urlpatterns.append(url(r'^contact/post_add', views.post_creer_contact, name = 'module_configuration_post_add_contact'))
urlpatterns.append(url(r'^contact/select/(?P<ref>[0-9]+)/$', views.get_select_contact, name = 'module_configuration_select_contact'))
urlpatterns.append(url(r'^contact/item/(?P<ref>[0-9]+)/$', views.get_details_contact, name = 'module_configuration_detail_contact'))
urlpatterns.append(url(r'^contact/item/(?P<ref>[0-9]+)/update$', views.get_modifier_contact, name = 'module_configuration_update_contact'))
urlpatterns.append(url(r'^contact/item/post_update/$', views.post_modifier_contact, name = 'module_configuration_post_update_contact'))
urlpatterns.append(url(r'^contact/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_contact, name = 'module_configuration_duplicate_contact'))
urlpatterns.append(url(r'^contact/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_contact, name = 'module_configuration_print_contact'))
#CONTACT UPLOAD URLS
urlpatterns.append(url(r'^contact/upload/add', views.get_upload_contact, name = 'module_configuration_get_upload_contact'))
urlpatterns.append(url(r'^contact/upload/post_add', views.post_upload_contact, name = 'module_configuration_post_upload_contact'))

#CONTACT API URLS
urlpatterns.append(url(r'^api/contact/list', views.get_list_contact, name = 'module_configuration_api_list_contact'))
urlpatterns.append(url(r'^api/contact/item', views.get_item_contact, name = 'module_configuration_api_item_contact'))
urlpatterns.append(url(r'^api/contact/create', views.post_create_contact, name = 'module_configuration_api_create_contact'))

#ADRESSE URLS
#=====================================
#ADRESSE CRUD URLS
urlpatterns.append(url(r'^adresse/list', views.get_lister_adresse, name = 'module_configuration_list_adresse'))
urlpatterns.append(url(r'^adresse/add', views.get_creer_adresse, name = 'module_configuration_add_adresse'))
urlpatterns.append(url(r'^adresse/post_add', views.post_creer_adresse, name = 'module_configuration_post_add_adresse'))
urlpatterns.append(url(r'^adresse/select/(?P<ref>[0-9]+)/$', views.get_select_adresse, name = 'module_configuration_select_adresse'))
urlpatterns.append(url(r'^adresse/item/(?P<ref>[0-9]+)/$', views.get_details_adresse, name = 'module_configuration_detail_adresse'))
urlpatterns.append(url(r'^adresse/item/(?P<ref>[0-9]+)/update$', views.get_modifier_adresse, name = 'module_configuration_update_adresse'))
urlpatterns.append(url(r'^adresse/item/post_update/$', views.post_modifier_adresse, name = 'module_configuration_post_update_adresse'))
urlpatterns.append(url(r'^adresse/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_adresse, name = 'module_configuration_duplicate_adresse'))
urlpatterns.append(url(r'^adresse/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_adresse, name = 'module_configuration_print_adresse'))
#ADRESSE UPLOAD URLS
urlpatterns.append(url(r'^adresse/upload/add', views.get_upload_adresse, name = 'module_configuration_get_upload_adresse'))
urlpatterns.append(url(r'^adresse/upload/post_add', views.post_upload_adresse, name = 'module_configuration_post_upload_adresse'))

#ADRESSE API URLS
urlpatterns.append(url(r'^api/adresse/list', views.get_list_adresse, name = 'module_configuration_api_list_adresse'))
urlpatterns.append(url(r'^api/adresse/item', views.get_item_adresse, name = 'module_configuration_api_item_adresse'))
urlpatterns.append(url(r'^api/adresse/create', views.post_create_adresse, name = 'module_configuration_api_create_adresse'))

#PAYS URLS
#=====================================
#PAYS CRUD URLS
urlpatterns.append(url(r'^pays/list', views.get_lister_pays, name = 'module_configuration_list_pays'))
urlpatterns.append(url(r'^pays/add', views.get_creer_pays, name = 'module_configuration_add_pays'))
urlpatterns.append(url(r'^pays/post_add', views.post_creer_pays, name = 'module_configuration_post_add_pays'))
urlpatterns.append(url(r'^pays/select/(?P<ref>[0-9]+)/$', views.get_select_pays, name = 'module_configuration_select_pays'))
urlpatterns.append(url(r'^pays/item/(?P<ref>[0-9]+)/$', views.get_details_pays, name = 'module_configuration_detail_pays'))
urlpatterns.append(url(r'^pays/item/(?P<ref>[0-9]+)/update$', views.get_modifier_pays, name = 'module_configuration_update_pays'))
urlpatterns.append(url(r'^pays/item/post_update/$', views.post_modifier_pays, name = 'module_configuration_post_update_pays'))
urlpatterns.append(url(r'^pays/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_pays, name = 'module_configuration_duplicate_pays'))
urlpatterns.append(url(r'^pays/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_pays, name = 'module_configuration_print_pays'))
#PAYS UPLOAD URLS
urlpatterns.append(url(r'^pays/upload/add', views.get_upload_pays, name = 'module_configuration_get_upload_pays'))
urlpatterns.append(url(r'^pays/upload/post_add', views.post_upload_pays, name = 'module_configuration_post_upload_pays'))

#PAYS API URLS
urlpatterns.append(url(r'^api/pays/list', views.get_list_pays, name = 'module_configuration_api_list_pays'))
urlpatterns.append(url(r'^api/pays/item', views.get_item_pays, name = 'module_configuration_api_item_pays'))
urlpatterns.append(url(r'^api/pays/create', views.post_create_pays, name = 'module_configuration_api_create_pays'))

#PROVINCE URLS
#=====================================
#PROVINCE CRUD URLS
urlpatterns.append(url(r'^province/list', views.get_lister_province, name = 'module_configuration_list_province'))
urlpatterns.append(url(r'^province/add', views.get_creer_province, name = 'module_configuration_add_province'))
urlpatterns.append(url(r'^province/post_add', views.post_creer_province, name = 'module_configuration_post_add_province'))
urlpatterns.append(url(r'^province/select/(?P<ref>[0-9]+)/$', views.get_select_province, name = 'module_configuration_select_province'))
urlpatterns.append(url(r'^province/item/(?P<ref>[0-9]+)/$', views.get_details_province, name = 'module_configuration_detail_province'))
urlpatterns.append(url(r'^province/item/(?P<ref>[0-9]+)/update$', views.get_modifier_province, name = 'module_configuration_update_province'))
urlpatterns.append(url(r'^province/item/post_update/$', views.post_modifier_province, name = 'module_configuration_post_update_province'))
urlpatterns.append(url(r'^province/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_province, name = 'module_configuration_duplicate_province'))
urlpatterns.append(url(r'^province/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_province, name = 'module_configuration_print_province'))
#PROVINCE UPLOAD URLS
urlpatterns.append(url(r'^province/upload/add', views.get_upload_province, name = 'module_configuration_get_upload_province'))
urlpatterns.append(url(r'^province/upload/post_add', views.post_upload_province, name = 'module_configuration_post_upload_province'))

#PROVINCE API URLS
urlpatterns.append(url(r'^api/province/list', views.get_list_province, name = 'module_configuration_api_list_province'))
urlpatterns.append(url(r'^api/province/item', views.get_item_province, name = 'module_configuration_api_item_province'))
urlpatterns.append(url(r'^api/province/create', views.post_create_province, name = 'module_configuration_api_create_province'))

#VILLE URLS
#=====================================
#VILLE CRUD URLS
urlpatterns.append(url(r'^ville/list', views.get_lister_ville, name = 'module_configuration_list_ville'))
urlpatterns.append(url(r'^ville/add', views.get_creer_ville, name = 'module_configuration_add_ville'))
urlpatterns.append(url(r'^ville/post_add', views.post_creer_ville, name = 'module_configuration_post_add_ville'))
urlpatterns.append(url(r'^ville/select/(?P<ref>[0-9]+)/$', views.get_select_ville, name = 'module_configuration_select_ville'))
urlpatterns.append(url(r'^ville/item/(?P<ref>[0-9]+)/$', views.get_details_ville, name = 'module_configuration_detail_ville'))
urlpatterns.append(url(r'^ville/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ville, name = 'module_configuration_update_ville'))
urlpatterns.append(url(r'^ville/item/post_update/$', views.post_modifier_ville, name = 'module_configuration_post_update_ville'))
urlpatterns.append(url(r'^ville/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_ville, name = 'module_configuration_duplicate_ville'))
urlpatterns.append(url(r'^ville/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_ville, name = 'module_configuration_print_ville'))
#VILLE UPLOAD URLS
urlpatterns.append(url(r'^ville/upload/add', views.get_upload_ville, name = 'module_configuration_get_upload_ville'))
urlpatterns.append(url(r'^ville/upload/post_add', views.post_upload_ville, name = 'module_configuration_post_upload_ville'))

#VILLE API URLS
urlpatterns.append(url(r'^api/ville/list', views.get_list_ville, name = 'module_configuration_api_list_ville'))
urlpatterns.append(url(r'^api/ville/item', views.get_item_ville, name = 'module_configuration_api_item_ville'))
urlpatterns.append(url(r'^api/ville/create', views.post_create_ville, name = 'module_configuration_api_create_ville'))

#DISTRICT URLS
#=====================================
#DISTRICT CRUD URLS
urlpatterns.append(url(r'^district/list', views.get_lister_district, name = 'module_configuration_list_district'))
urlpatterns.append(url(r'^district/add', views.get_creer_district, name = 'module_configuration_add_district'))
urlpatterns.append(url(r'^district/post_add', views.post_creer_district, name = 'module_configuration_post_add_district'))
urlpatterns.append(url(r'^district/select/(?P<ref>[0-9]+)/$', views.get_select_district, name = 'module_configuration_select_district'))
urlpatterns.append(url(r'^district/item/(?P<ref>[0-9]+)/$', views.get_details_district, name = 'module_configuration_detail_district'))
urlpatterns.append(url(r'^district/item/(?P<ref>[0-9]+)/update$', views.get_modifier_district, name = 'module_configuration_update_district'))
urlpatterns.append(url(r'^district/item/post_update/$', views.post_modifier_district, name = 'module_configuration_post_update_district'))
urlpatterns.append(url(r'^district/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_district, name = 'module_configuration_duplicate_district'))
urlpatterns.append(url(r'^district/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_district, name = 'module_configuration_print_district'))
#DISTRICT UPLOAD URLS
urlpatterns.append(url(r'^district/upload/add', views.get_upload_district, name = 'module_configuration_get_upload_district'))
urlpatterns.append(url(r'^district/upload/post_add', views.post_upload_district, name = 'module_configuration_post_upload_district'))

#DISTRICT API URLS
urlpatterns.append(url(r'^api/district/list', views.get_list_district, name = 'module_configuration_api_list_district'))
urlpatterns.append(url(r'^api/district/item', views.get_item_district, name = 'module_configuration_api_item_district'))
urlpatterns.append(url(r'^api/district/create', views.post_create_district, name = 'module_configuration_api_create_district'))

#COMMUNE URLS
#=====================================
#COMMUNE CRUD URLS
urlpatterns.append(url(r'^commune/list', views.get_lister_commune, name = 'module_configuration_list_commune'))
urlpatterns.append(url(r'^commune/add', views.get_creer_commune, name = 'module_configuration_add_commune'))
urlpatterns.append(url(r'^commune/post_add', views.post_creer_commune, name = 'module_configuration_post_add_commune'))
urlpatterns.append(url(r'^commune/select/(?P<ref>[0-9]+)/$', views.get_select_commune, name = 'module_configuration_select_commune'))
urlpatterns.append(url(r'^commune/item/(?P<ref>[0-9]+)/$', views.get_details_commune, name = 'module_configuration_detail_commune'))
urlpatterns.append(url(r'^commune/item/(?P<ref>[0-9]+)/update$', views.get_modifier_commune, name = 'module_configuration_update_commune'))
urlpatterns.append(url(r'^commune/item/post_update/$', views.post_modifier_commune, name = 'module_configuration_post_update_commune'))
urlpatterns.append(url(r'^commune/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_commune, name = 'module_configuration_duplicate_commune'))
urlpatterns.append(url(r'^commune/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_commune, name = 'module_configuration_print_commune'))
#COMMUNE UPLOAD URLS
urlpatterns.append(url(r'^commune/upload/add', views.get_upload_commune, name = 'module_configuration_get_upload_commune'))
urlpatterns.append(url(r'^commune/upload/post_add', views.post_upload_commune, name = 'module_configuration_post_upload_commune'))

#COMMUNE API URLS
urlpatterns.append(url(r'^api/commune/list', views.get_list_commune, name = 'module_configuration_api_list_commune'))
urlpatterns.append(url(r'^api/commune/item', views.get_item_commune, name = 'module_configuration_api_item_commune'))
urlpatterns.append(url(r'^api/commune/create', views.post_create_commune, name = 'module_configuration_api_create_commune'))

#TYPE_PERIODE URLS
#=====================================
#TYPE_PERIODE CRUD URLS
urlpatterns.append(url(r'^type_periode/list', views.get_lister_type_periode, name = 'module_configuration_list_type_periode'))
urlpatterns.append(url(r'^type_periode/add', views.get_creer_type_periode, name = 'module_configuration_add_type_periode'))
urlpatterns.append(url(r'^type_periode/post_add', views.post_creer_type_periode, name = 'module_configuration_post_add_type_periode'))
urlpatterns.append(url(r'^type_periode/select/(?P<ref>[0-9]+)/$', views.get_select_type_periode, name = 'module_configuration_select_type_periode'))
urlpatterns.append(url(r'^type_periode/item/(?P<ref>[0-9]+)/$', views.get_details_type_periode, name = 'module_configuration_detail_type_periode'))
urlpatterns.append(url(r'^type_periode/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_periode, name = 'module_configuration_update_type_periode'))
urlpatterns.append(url(r'^type_periode/item/post_update/$', views.post_modifier_type_periode, name = 'module_configuration_post_update_type_periode'))
urlpatterns.append(url(r'^type_periode/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_type_periode, name = 'module_configuration_duplicate_type_periode'))
urlpatterns.append(url(r'^type_periode/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_type_periode, name = 'module_configuration_print_type_periode'))
#TYPE_PERIODE UPLOAD URLS
urlpatterns.append(url(r'^type_periode/upload/add', views.get_upload_type_periode, name = 'module_configuration_get_upload_type_periode'))
urlpatterns.append(url(r'^type_periode/upload/post_add', views.post_upload_type_periode, name = 'module_configuration_post_upload_type_periode'))

#TYPE_PERIODE API URLS
urlpatterns.append(url(r'^api/type_periode/list', views.get_list_type_periode, name = 'module_configuration_api_list_type_periode'))
urlpatterns.append(url(r'^api/type_periode/item', views.get_item_type_periode, name = 'module_configuration_api_item_type_periode'))
urlpatterns.append(url(r'^api/type_periode/create', views.post_create_type_periode, name = 'module_configuration_api_create_type_periode'))
