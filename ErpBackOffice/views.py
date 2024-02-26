# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import contenttypes
from django.contrib.contenttypes import fields

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.utils.http import urlencode
from django.core import serializers
from random import randint
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
import datetime
import json
import os
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.print import render_to_pdf, my_exec, the_import_exec
from ErpBackOffice.dao.dao_print import *
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ErpBackOffice.dao.dao_permission import dao_permission
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_place import dao_place
from ModuleConfiguration.dao.dao_actionutilisateur import dao_actionutilisateur
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification
from ErpBackOffice.utils.auth import auth
import importlib
import inspect
from django.db import transaction
from ErpBackOffice.utils.wkf_task import wkf_task

from ErpBackOffice.dao.dao_session import dao_session


from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_organisation import dao_organisation
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_stakeholder import dao_wkf_stakeholder
from ErpBackOffice.utils.print import weasy_print
# Create your views here.

# ERROR PAGE CONTROLLER
def error_404(request, *args, **kwargs):     		
	messages.add_message(request, messages.ERROR, "404 - PAGE NON TROUVEE")
	#print("404 - PAGE NON TROUVEE")
	return HttpResponseRedirect(reverse('backoffice_index'))
    
def error_500(request, *args, **kwargs):
	messages.add_message(request, messages.ERROR, "500 - ERREUR SURVENUE")
	#print("500 - ERREUR SURVENUE")
	return HttpResponseRedirect(reverse('backoffice_index'))
    
def error_403(request, *args, **kwargs):
	messages.add_message(request, messages.ERROR, "403 - PAGE NON AUTORISEE")
	#print("403 - ERREUR SURVENUE")
	return HttpResponseRedirect(reverse('backoffice_index'))
    
def error_400(request, *args, **kwargs):
	messages.add_message(request, messages.ERROR, "400 - ERREUR SURVENUE")
	#print("400 - ERREUR SURVENUE")
	return HttpResponseRedirect(reverse('backoffice_index'))

# Dashboard Controller
def get_index(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)
	if response != None:
		return response

	context = {
		'title' : 'Accueil',
		"utilisateur" : utilisateur,
		"modules" : modules,
		'organisation': dao_organisation.toGetMainOrganisation()
	}
	template = loader.get_template("ErpProject/ErpBackOffice/dashboard.html")
	return HttpResponse(template.render(context, request))

# PROFILE UTILISATEUR PAGE
def get_profile(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)
	if response != None:
		return response

	model = dao_personne.toGetEmploye(identite.utilisateur(request).id)
	#print(model)

	context ={
		'title' : 'Profile utilisateur',
		'utilisateur' : utilisateur,
		'sous_modules': sous_modules,
		'utilisateur': utilisateur,
		'modules' : modules,
		'model' : model,
		'organisation': dao_organisation.toGetMainOrganisation()

	}
	template = loader.get_template("ErpProject/ErpBackOffice/utilisateur/profile.html")
	return HttpResponse(template.render(context, request))

def get_password(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)

	if response != None:
		return response

	context = {
		'title' : 'Modifier votre mot de passe',
		'sous_modules': sous_modules,
		'utilisateur': utilisateur,
		"modules" : modules,
		'organisation': dao_organisation.toGetMainOrganisation()
	}
	template = loader.get_template("ErpProject/ErpBackOffice/utilisateur/password.html")
	return HttpResponse(template.render(context, request))

def post_password(request):
	try:
		pswd = request.POST["pswd"]
		n_pswd = request.POST["n_pswd"]

		utilisateur = dao_personne.toGetEmploye(identite.utilisateur(request).id)
		user = utilisateur.user

		if pswd != n_pswd:
			messages.error(request,'Les deux champs doivent être identiques')
			return HttpResponseRedirect(reverse("backoffice_change_password"))

		user.set_password(n_pswd)
		user.save()
		messages.success(request,"Mot de Passe changé avec succès")
		return HttpResponseRedirect(reverse("backoffice_connexion"))

	except Exception as e:
		#print("Erreur lors du changement de mot de passe")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("backoffice_deconnexion"))


def get_connexion(request):
	try:
		accueil = request.GET["redirect_login"]
		#print("loula")

		if accueil != "OK":
			return HttpResponseRedirect(reverse("backoffice_acceuil"))

		organisation = dao_organisation.toGetMainOrganisation()
		context = {
			'title' : 'Identifiez-vous au système !',
			'organisation': organisation,
		}
		template = loader.get_template("ErpProject/ErpBackOffice/utilisateur/login.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("Erreur !")
		#print(e)
		return HttpResponseRedirect(reverse("backoffice_acceuil"))
		#print("Erreur !")
		#print(e)

def get_accueil(request):
	organisation = dao_organisation.toGetMainOrganisation()
	context = {
		'title' : f"Bienvenue à {organisation.nom}",
		'organisation': organisation
	}
	template = loader.get_template("ErpProject/ErpBackOffice/utilisateur/home.html")
	return HttpResponse(template.render(context, request))


def post_connexion(request):
	try:
		password = request.POST["password"]
		username = request.POST["email"].lower().strip()
		print("ICI")

		utilisateur = authenticate(request, password = password, username = username)
		if(utilisateur is not None):
			login(request, utilisateur)
			# dao_session.processingUniqueSession(request)

			return HttpResponseRedirect(reverse("backoffice_index"))
		else:
			print("haha")
			messages.add_message(request, messages.ERROR, "Nous ne reconnaissons pas ces identifiants !")
			params = "?{}".format(urlencode({'redirect_login':'OK'}))
			return HttpResponseRedirect(reverse("backoffice_connexion") + params)
	except Exception as e:
		print("ERREUR")
		print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentive de connexion")
		params = "?{}".format(urlencode({'redirect_login':'OK'}))
		return HttpResponseRedirect(reverse("backoffice_connexion") + params)

def get_deconnexion(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse("backoffice_connexion"))

	logout(request)
	return HttpResponseRedirect(reverse("backoffice_connexion"))

def get_not_autorize(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)

	if response != None:
		return response

	context = {
		'title' : "Faute d'autorisation",
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules,
	}
	template = loader.get_template("ErpProject/ErpBackOffice/erreur/autorisation.html")
	return HttpResponse(template.render(context, request))

def get_not_role(request):

	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)

	if response != None:
		return response

	context = {
		'title' : "Aucun role attribué",
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules,
	}
	template = loader.get_template("ErpProject/ErpBackOffice/erreur/role.html")
	return HttpResponse(template.render(context, request))


def get_json_list_places_filles(request):
	try:
		data = []
		parent_id = int(request.GET["ref"])
		places = dao_place.toListPlacesFilles(parent_id)
		for place in places:
			item = {
				"id" : place.id,
				"designation" : place.designation,
				"code_telephone" : place.code_telephone,
				"code_pays" : place.code_pays,
				"place_type" : place.place_type
			}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)


def get_model(texte):
	"""
	Cette méthode permet de retourner une class à partir d'un string

	1. 'importlib' lui permet de récuperer dynamiquement un module. Pour notre Exemple
	Il va récupérer le module 'models' contenu dans le package ErpBackOffice par sa méthode
	'import_module()'

	2. 'getattr' quant à lui, retourner la classe contenu dans le module précedemment récupérer
	via un string ici Texte

	3. 'inspect.isclass()' vérifier si l'objet récupérer au point 2 est bel et bien une classe.


	"""
	model = 'ErpBackOffice.models'
	module = importlib.import_module(model, ".")
	obj = getattr(module, texte)
	if inspect.isclass(obj):
		return obj

def backoffice_list_model(request):
	try:
		data = []
		mod = get_model(request.GET['model_choix']).objects.all()
		for model in mod:
			item = {
				'id' : model.id,
				'designation': model.__str__()
			}
			data.append(item)
		return JsonResponse(data, safe = False)
	except :
		return JsonResponse([], safe = False)

def backoffice_delete_doc(request, ref, modele, the_url):
	try:
		id = int(ref)

		#Supprime le fichier static dans son emplacement
		docu = None
		#print('je recupere ref %s' % (id))
		#print('je recupere url %s' % (the_url))
		#print('je recupere les doc à sup %s' % (docu))

		mygetcwd = os.getcwd()
		img = mygetcwd+"/static"+docu.url_document
		img = img.replace('\\', '/')
		os.remove(img)

		num = int(docu.source_document_id)

		objet = get_model(modele).objects.get(id=num)
		doc = False
		#print("confirmation de la sup doc %s" % (doc))
		if doc == True:
			return HttpResponseRedirect(reverse(the_url, args=(objet.id,)))
		return HttpResponseRedirect(reverse(the_url, args=(objet.id,)))
	except Exception as e:
		#print("proble au niveau du sup %s"%(e))
		pass



@transaction.atomic
def post_workflow(request):
	''' Traitement du postworkflow '''
	sid = transaction.savepoint()
	url_add = request.POST["url_add"]
	#print(url_add)
	url_detail = request.POST["url_detail"]
	#print(url_detail)
	try:
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		#print(etape_id)
		objet_id = request.POST["doc_id"]
		#print(objet_id)
		content_id = request.POST["content_id"]
		#print(content_id)



		utilisateur = dao_personne.toGetEmployeFromUser(utilisateur_id)
		#print("puritotita")

		historique = wkf_task.postworkflow(objet_id, content_id,utilisateur,etape_id, url_detail, request)
		#print("mama")

		if historique != None :
			transaction.savepoint_commit(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))


	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse(url_add))


@transaction.atomic
def post_cancel_workflow(request):
	''' Traitement pour passage à Annuler d'un workflow '''
	sid = transaction.savepoint()
	try:
		url_add = request.POST["url_add"]
		url_detail = request.POST["url_detail"]
		objet_id = request.POST["doc_id"]
		content_id = request.POST["content_id"]
		type_document = request.POST["type_doc"]
		notes = request.POST["notes"]
		action_id = int(request.POST["action_id"])

		if type_document == "":
			type_document = None

		utilisateur = identite.utilisateur(request)
		type_document = None
		
		etape_id = None if action_id == 0 else action_id
		historique = wkf_task.cancelWorkflow(utilisateur,objet_id,content_id, notes, type_document, etape_id)

		if historique != None :
			transaction.savepoint_commit(sid)
			#print("OKAY")
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))

	except Exception as e:
		print("ERREUR")
		print(e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse(url_add))


@transaction.atomic
def post_stakeholder_delegation_workflow(request):
	''' Traitement pour Délégation '''
	sid = transaction.savepoint()
	try:
		delegue_transition_id = request.POST["delegue_transition_id"]
		url_detail = request.POST["url_detail"]
		objet_id = request.POST["doc_id"]
		content_id = request.POST["content_id"]
		module_source = request.POST["module_source"] #String du style ErpModule.MODULE_ACHAT
		module_source = module_source.split(".")[1] #On obtient que "MODULE_ACHAT"
		comments = request.POST["comments"]		
		est_delegation = True
		employes = []
		carbon_copies = []
		if 'employe_id' in request.POST: employes.append(request.POST["employe_id"])

		auteur = identite.utilisateur(request)			
		stakeholder  = wkf_task.postStakeHolder(delegue_transition_id, objet_id, content_id,employes, carbon_copies, est_delegation, comments, url_detail, module_source, auteur)

		if stakeholder != None :
			transaction.savepoint_commit(sid)
			#print("OKAY")
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))

	except Exception as e:
		print("ERREUR on post_stakeholder_workflow")
		print(e)
		messages.error(request,'Une erreur est survenue pendant le traitement')
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))


@transaction.atomic
def post_stakeholder_configuration_workflow(request):
	''' Traitement pour Configurer '''
	sid = transaction.savepoint()
	try:
		url_detail = request.POST["url_detail"]
		objet_id = request.POST["doc_id"]
		content_id = request.POST["content_id"]
		module_source = request.POST["module_source"] #String du style ErpModule.MODULE_ACHAT
		module_source = module_source.split(".")[1] #On obtient que "MODULE_ACHAT"
		comments = request.POST["comments"]	
		est_delegation = False 
		employes = request.POST.getlist('employe_id', None)
		carbon_copies = request.POST.getlist('cc_id', None)
		current_transition_id = request.POST["current_transition_id"]

		#We can have multiple next transition or just one
		transition = dao_wkf_transition.toGetTransition(current_transition_id)	

		
		auteur = identite.utilisateur(request)	
		
		for next_transition in transition.transitions_suivantes:
			stakeholder  = wkf_task.postStakeHolder(next_transition.id, objet_id, content_id,employes, carbon_copies, est_delegation, comments, url_detail, module_source, auteur)


		if stakeholder != None :
			transaction.savepoint_commit(sid)
			#print("OKAY")
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))

	except Exception as e:
		print("ERREUR on post_stakeholder_configuration_workflow")
		print(e)
		messages.error(request,'Une erreur est survenue pendant le traitement')
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))


def post_weasyprint_objet(request):
	try:
		modele = request.POST["modele"]			
		ref = request.POST["ref"]	
		title = request.POST["title"]
		objet_modele = get_model(modele).objects.get(id=int(ref))
		context = {
			'title' : title,
			'model':objet_modele,
			'date_now': timezone.now(),
			'fields' : objet_modele._meta.get_fields(),
		}
		return weasy_print("ErpProject/ErpbackOffice/reporting/objet_print.html", f"{title}.pdf", context)
	except Exception as e:
		print(e)
		#Back to previous link http
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def post_supprimmer_objet(request, ref, modele, the_url):
	try:
		is_connect = identite.est_connecte(request)
		if is_connect == False: return HttpResponseRedirect(reverse("backoffice_connexion"))
  
		utilisateur = identite.utilisateur(request)
  
		print('Model from form %s'%(modele))
		action = dao_actionutilisateur.toGetActionByName(the_url)
		list_permission = action.permission
		sous_module = list_permission.sous_module  
		permissions = dao_permission.toListPermissionsOfSousModule(sous_module.id)
		delete_permission = permissions.filter(designation__startswith='SUPPRIMER_').first()
    
		is_checked = auth.toCheckUserPerm(utilisateur, delete_permission)
		if is_checked == False: raise Exception("L'utilisateur n'est pas habiter de supprimer cet objet")
  
		model_principal = sous_module.model_principal
		content_types = ContentType.objects.filter(model = modele.lower())
		if content_types.count() > 1: content_type = content_types.filter(pk = model_principal.id).first()
		elif content_types.count() == 1: content_type = content_types.first()
		else: raise Exception("Le Model defini n'existe pas !")
			
		model_class = content_type.model_class()
		objet = model_class.objects.get(id=int(ref))
		#print(objet)

		objet.delete()
		#print('Suppression reussie')
		messages.add_message(request, messages.SUCCESS, "L'objet a été supprimé avec succès !")
		return HttpResponseRedirect(reverse(the_url))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse(the_url), "Une erreur est survenue lors de la suppression!")


def post_generate_pdf(request):
	previous = request.POST.get('previous', '/')
	try:
		#template = loader.get_template("ErpProject/ErpBackOffice/shared/print.html")
		id = request.POST["id"]
		dao = request.POST["dao"]
		#model = None
		#print("************************************************")
		id = request.POST["id"]
		dao = request.POST["dao"]
		model = my_exec(dao,id)
		context = {
			'model':model,
			'organisation':dao_organisation.toGetMainOrganisation(),
		}
		#html = template.render(context)
		pdf = render_to_pdf('ErpProject/ErpBackOffice/printable/print.html', context, request)
		return HttpResponse(pdf, content_type='application/pdf')
		#return HttpResponse(html)

	except Exception as e:
		#print("ERREUR")
		#print(e)
		return HttpResponseRedirect(previous)


def post_print_html_to_pdf(request):

	fonction = request.POST["fonction"]
	return the_import_exec(fonction,request)


def get_json_next_transition(request):
	try:
		data = []
		transition_id = int(request.GET["ref"])
		content_type_id = (request.GET["content_type_id"])
		objet_id = int(request.GET["objet_id"])

		transition = dao_wkf_transition.toGetTransition(transition_id)
		for unetransition in transition.transitions_suivantes:
			print("unetransition", unetransition.id , content_type_id, objet_id)
			stakeholder = dao_wkf_stakeholder.toListTransitionOfObject(unetransition.id,content_type_id, objet_id).first()
			if stakeholder:
				list_employes = []
				for employe in stakeholder.employes.all():
					list_employes.append(employe.nom_complet)
					item = {
						"id" : unetransition.id,
						"etape_source" : unetransition.etape_source.designation,
						"etape_destination" : unetransition.etape_destination.designation,
						"groupe_permission": ','.join(list_employes)
					}
			else:
				item = {
					"id" : unetransition.id,
					"etape_source" : unetransition.etape_source.designation,
					"etape_destination" : unetransition.etape_destination.designation,
					"groupe_permission": unetransition.groupe_permission.designation
				}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		print(e)
		return JsonResponse([], safe=False)

def get_update_notification(request, ref):
	dao_temp_notification.toUpdateTempNotificationRead(ref)
	redirect = request.META.get('HTTP_REFERER')
	return HttpResponseRedirect(redirect)

from ModuleConfiguration.dao.dao_query import dao_query
from ErpBackOffice.dao.dao_query_builder import dao_query_builder
def get_data_request(request):
	try:
		context = {}
		auteur = identite.utilisateur(request)
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		#if 'id' in request.GET : id = int(request.GET['id'])
		
		model_row = []
		
		
		print("Data: {}".format(request.GET))

		if 'model_id' in request.GET : model_id = request.GET['model_id'] 
		else: model_id = None

		champs = dao_query_builder.toListFieldOfModel(model_id)

		if 'view' in request.GET : view = request.GET['view']
		else: view = "table"

		if 'filter_logic' in request.GET : filter_logic = request.GET.getlist('filter_logic', None)
		else: filter_logic = []

		if 'filter_item' in request.GET : filter_item = request.GET.getlist('filter_item', None)
		else: filter_item = []

		if 'filter_operateur' in request.GET : filter_operateur = request.GET.getlist('filter_operateur', None) 
		else: filter_operateur = []

		if 'filter_valeur' in request.GET : filter_valeur = request.GET.getlist('filter_valeur', None)
		else: filter_valeur = []

		if 'regrouper_item' in request.GET : regrouper_item = request.GET['regrouper_item']
		else: regrouper_item = []

		if 'regroupe_elements' in request.GET : regroupe_elements = request.GET['regroupe_elements']
		else: regroupe_elements = None

		if 'plage_item' in request.GET : plage_item = request.GET['plage_item'] 
		else: plage_item = []

		if 'plage_valeur' in request.GET : plage_valeur = request.GET['plage_valeur'] 
		else: plage_valeur = []

		if 'favoris_name' in request.GET : favoris_name = request.GET['favoris_name'] 
		else: favoris_name = None

		if 'favoris_numero' in request.GET : favoris_numero = request.GET['favoris_numero'] 
		else: favoris_numero = None

		if 'favoris_visibilite' in request.GET : favoris_visibilite = request.GET['favoris_visibilite'] 
		else: favoris_visibilite = 1

		if 'champs_afficher' in request.GET : champs_afficher = request.GET.getlist('champs_afficher', None)
		else: 
			champs_afficher = []
			for name, db_name, verbose_name, type, choices in champs:
				nom_champs = name
				if type == "ForeignKey": nom_champs = nom_champs + "_id"
				champs_afficher.append(nom_champs)

		if 'measure_function' in request.GET : measure_function = request.GET['measure_function'] 
		else: measure_function = ""

		if 'measure_function_title' in request.GET : measure_function_title = request.GET['measure_function_title'] 
		else: measure_function_title = ""

		if 'measure_attribute' in request.GET : measure_attribute = request.GET['measure_attribute']
		else: measure_attribute = ""

		if 'measure_attribute_title' in request.GET : measure_attribute_title = request.GET['measure_attribute_title']
		else: measure_attribute_title = ""

		if 'dimension' in request.GET : dimension = request.GET['dimension']
		else: dimension = ""

		if 'dimension_title' in request.GET : dimension_title = request.GET['dimension_title']
		else: dimension_title = ""  

		if 'more_chart' in request.GET : chart_type = request.GET['more_chart']
		else: chart_type = 0 

		if 'chart_view' in request.GET : chart_view = request.GET['chart_view']
		else: chart_view = "bar-chart"

		if 'champs_card' in request.GET : champs_card = request.GET['champs_card']
		else: champs_card = ""

		if 'champs_card_title' in request.GET : champs_card_title = request.GET['champs_card_title']
		else: champs_card_title = "" 

		if 'fonction_card' in request.GET : fonction_card = request.GET['fonction_card']
		else: fonction_card = ""

		if 'fonction_card_title' in request.GET : fonction_card_title = request.GET['fonction_card_title']
		else: fonction_card_title = "" 

		if 'order_by' in request.GET : order_by = request.GET['order_by']
		else: order_by = "id" 

		if 'order_sens' in request.GET : order_sens = request.GET['order_sens']
		else: order_sens = "asc"

		if 'limit' in request.GET : limit = request.GET['limit']
		else: limit = "10" 

		legend_dataset = f'{measure_function_title} {measure_attribute_title}'
		title_card = f'{fonction_card_title} {champs_card_title}'

		if view == "table":
			print("Is Table")
			model_row, slq_query = dao_query_builder.toPerformQueryForTable(auteur, model_id, champs_afficher, filter_logic, filter_item, filter_operateur, filter_valeur, regrouper_item, regroupe_elements, plage_item, plage_valeur, order_by, order_sens, limit)			
		elif view == "chart":
			print("Is Chart")
			model_row, slq_query = dao_query_builder.toPerformQueryForChart(auteur, model_id, champs_afficher, measure_function, measure_attribute, dimension , filter_logic, filter_item, filter_operateur, filter_valeur, chart_type, plage_item, plage_valeur, order_by, order_sens, limit)	
		elif view == "card":   
			print("Is Card")
			model_row, slq_query = dao_query_builder.toPerformQueryForCard(auteur, model_id, fonction_card, champs_card , filter_logic, filter_item, filter_operateur, filter_valeur, regrouper_item, plage_item, plage_valeur, order_by, order_sens, limit)

		elif view == "pivot":
			print("Is Pivot")
			model_row, slq_query = dao_query_builder.toPerformQueryForPivot(auteur, model_id, champs_afficher, filter_logic, filter_item, filter_operateur, filter_valeur, chart_type, plage_item, plage_valeur, order_by, order_sens, limit)	

		field_datas = []
		for name, db_name, verbose_name, type, choices in champs:
			nom_champs = name
			if type in ('ForeignKey', 'OneToOneField'): nom_champs = nom_champs + "_id"
			if nom_champs in champs_afficher:       
				field_data = {
					'name' : name,
					'verbose_name' : verbose_name,
					'type' : type,
					'choices' : choices
				}
				field_datas.append(field_data)

		est_regroupe = True
		if regrouper_item == []: est_regroupe = False

		regr_count = -1
		if regroupe_elements != None: 
			regr_el = regroupe_elements.split(";;")
			regr_count = regr_el[0]

		if chart_type == "1" or view == "pivot":
			list_obj = []
			for item_array in model_row:
				i=0
				obj = {}
				print(item_array)
				for item in item_array:
					print(item)
					obj[field_datas[i]["verbose_name"]] = item
					i = i+1
				list_obj.append(obj)
			model_row = list_obj
		
		est_favoris = False
		if favoris_name != None and favoris_numero != None:
			est_favoris = True
			# On charge les champs à afficher dans une variable
			chs_affich = ""
			for ch in champs_afficher:
				chs_affich += f"{ch},"
			chs_affich = chs_affich[:-1] #On enleve la dernière virgule

			#On enregistre le favoris
			#print(f"SQL: {slq_query}")
			query = dao_query.toCreate(numero = favoris_numero, designation = favoris_name, role_id = None, slq_query = slq_query, description = '', champs_afficher = chs_affich, visibilite = favoris_visibilite, type_view = view, est_regroupe = est_regroupe, regr_count = regr_count, chart_type = chart_type, chart_view = chart_view, legend_dataset = legend_dataset, title_card = title_card, model_id = model_id)
			saved, query, message = dao_query.toSave(auteur, query)
			if saved == False: raise Exception(message)
			
		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'view': view,
			'model' : model_row,
			'est_regroupe': est_regroupe,
			'est_favoris': est_favoris,
			'regr_count': regr_count,
			'chart_view': chart_view,
			'chart_type': chart_type,
			'legend_dataset' : legend_dataset,
			'title_card' : title_card,
			'field_datas' : field_datas
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e)

def get_data_list_choices(request):
	try:
		context = {}
		auteur = identite.utilisateur(request)
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		#if 'id' in request.GET : id = int(request.GET['id'])
		
		model_row = []
		
		
		print("Data: {}".format(request.GET))

		if 'model_id' in request.GET : model_id = request.GET['model_id'] 
		else: model_id = None

		if 'field' in request.GET : field = request.GET['field']
		else: field = ""

		list_choices = []
		model_content_ref = ContentType.objects.get(pk = model_id)          
		model_class = model_content_ref.model_class()
		if hasattr(model_class, f"list_{field}"):
			list_choices = eval(f"model_class().list_{field}")

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'list_choices': list_choices
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e)

def get_data_related_field(request):
	try:
		context = {}
		auteur = identite.utilisateur(request)
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		#if 'id' in request.GET : id = int(request.GET['id'])
		
		model_row = []
		
		
		print("Data: {}".format(request.GET))

		if 'model_id' in request.GET : model_id = request.GET['model_id'] 
		else: model_id = None

		if 'field' in request.GET : field = request.GET['field']
		else: field = ""

		#Pour gérer les conditions dans le workflow où l'on utilise que les champs de model et non les db_column
		if 'type' in request.GET : type = request.GET['type']
		else: type = ""

		champs = dao_query_builder.toListFieldRelated(model_id, type)
		field_rel = ""
		table_rel = ""
		fields_rel = []
		for name, db_column, type, table, field_name, fields in champs:
			if type in ('ForeignKey', 'OneToOneField') and name == field: 
				field_rel = field_name
				table_rel = table
				fields_rel = fields

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'table': table_rel,
			'field' : field_rel,
			'fields' : fields_rel
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e)