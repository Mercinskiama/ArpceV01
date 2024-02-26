# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
import os, calendar
import json
import pandas as pd
from openpyxl import load_workbook, Workbook, styles
from copy import copy
from io import BytesIO
from rest_framework.decorators import api_view
import base64, uuid
from locale import atof, setlocale, LC_NUMERIC
import numpy as np
from dateutil.relativedelta import relativedelta
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.db import transaction
from ErpBackOffice.dao.dao_organisation import dao_organisation
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_historique import dao_wkf_historique
from ErpBackOffice.models import *
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_devise import dao_devise
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification
from ErpBackOffice.utils.pagination import pagination
from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.wkf_task import wkf_task
from ErpBackOffice.utils.endpoint import endpoint
from ErpBackOffice.utils.print import weasy_print
from ErpBackOffice.utils.utils import utils
from ModuleConfiguration.dao.dao_query import dao_query
from ErpBackOffice.dao.dao_query_builder import dao_query_builder


#LOGGING
import logging, inspect, unidecode
from ModuleSupport.models import *
monLog = logging.getLogger("logger")
module= "ModuleSupport"
var_module_id = 8
vars_module = {"name" : "MODULE_SUPPORT", "value" : 101 }


def get_index(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(var_module_id, request)
		if response != None:
			return response

		#NOTIFCATION
		module_name = vars_module["name"]
		temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
		temp_notif_count = temp_notif_list.count()

		context = {
			"title" : "Tableau de Bord",
			"utilisateur" : utilisateur,
			"organisation": dao_organisation.toGetMainOrganisation(),
			"temp_notif_count": temp_notif_count,
			"temp_notif_list": temp_notif_list,
			"sous_modules":sous_modules,
			"modules" : modules,
			"module" : vars_module
		}

		template = loader.get_template("ErpProject/ModuleSupport/index.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('backoffice_index'))

# HISTORIQUE_ACTION CONTROLLERS
from ModuleSupport.dao.dao_historique_action import dao_historique_action

def get_lister_historique_action(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_historique_action.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_historique_action.toListJson(model.object_list),
				'view' : view,
				'query' : query,
				'page' : page,
				'count' : count,
			}
			context = pagination.toAddVarsToContext(model, context)
			return JsonResponse(context, safe=False)

		isPopup = False
		if 'isPopup' in request.GET:
			isPopup = True
			view = 'list'

		context = {
			'title' : "Liste des historiques actions",
			'model' : model,
			'view' : view,
			'query' : query,
			'page' : page,
			'count' : count,
			'isPopup' : isPopup,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleSupport/historique_action/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e)
		else: return auth.toReturnFailed(request, e, reverse('module_support_tableau_de_bord'))

def get_creer_historique_action(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Historique Action",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Historique_action(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/historique_action/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_support_list_historique_action'))

@transaction.atomic
def post_creer_historique_action(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_support_add_historique_action'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		valeur_avant = str(request.POST['valeur_avant'])

		valeur_apres = str(request.POST['valeur_apres'])

		modele = str(request.POST['modele'])

		auteur = identite.utilisateur(request)

		historique_action = dao_historique_action.toCreate(valeur_avant = valeur_avant, valeur_apres = valeur_apres, modele = modele)
		saved, historique_action, message = dao_historique_action.toSave(auteur, historique_action)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_historique_action.toListById(historique_action.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, historique_action)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : historique_action.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e)

def get_select_historique_action(request,ref):
	try:
		same_perm_with = 'module_support_list_historique_action'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		historique_action = dao_historique_action.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(historique_action.id),'obj': str(historique_action)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_support_detail_historique_action', args=(historique_action.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_details_historique_action(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		historique_action = auth.toGetWithRules(dao_historique_action.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if historique_action == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, historique_action) 

		context = {
			'title' : "Détails - Historique Action : {}".format(historique_action),
			'model' : historique_action,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'historique': historique,
			'etapes_suivantes' : transitions_etapes_suivantes,
			'content_type_id': content_type_id,
			'documents': documents,
			'roles': groupe_permissions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/historique_action/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_support_list_historique_action'))

def get_modifier_historique_action(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_historique_action.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Historique Action",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/historique_action/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_historique_action(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_support_update_historique_action'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		valeur_avant = str(request.POST['valeur_avant'])

		valeur_apres = str(request.POST['valeur_apres'])

		modele = str(request.POST['modele'])
		auteur = identite.utilisateur(request)

		historique_action = dao_historique_action.toCreate(valeur_avant = valeur_avant, valeur_apres = valeur_apres, modele = modele)
		saved, historique_action, message = dao_historique_action.toUpdate(id, historique_action, auteur)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_historique_action.toListById(historique_action.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : historique_action.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e)

def get_dupliquer_historique_action(request,ref):
	try:
		same_perm_with = 'module_support_add_historique_action'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_historique_action.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/historique_action/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_historique_action(request,ref):
	try:
		same_perm_with = 'module_support_list_historique_action'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		historique_action = auth.toGetWithRules(dao_historique_action.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if historique_action == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Historique Action : {}".format(historique_action),
			'model' : historique_action,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleSupport/reporting/print_historique_action.html', 'print_historique_action.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_historique_action(request):
	try:
		same_perm_with = 'module_support_add_historique_action'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : "Import de la liste des historiques actions",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/historique_action/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_historique_action(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=file_name, sheet_name=sheet, engine='openpyxl')
		#df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			valeur_avant = str(df['valeur_avant'][i])
			valeur_apres = str(df['valeur_apres'][i])
			modele = str(df['modele'][i])

			historique_action = dao_historique_action.toCreate(valeur_avant = valeur_avant, valeur_apres = valeur_apres, modele = modele)
			saved, historique_action, message = dao_historique_action.toSave(auteur, historique_action)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_support_list_historique_action'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# HISTORIQUE_ACTION API CONTROLLERS
def get_list_historique_action(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		filtered = False
		if 'filtered' in request.GET : filtered = str(request.GET['filtered'])
		date_from = None
		if 'date_from' in request.GET : date_from = request.GET['date_from']
		date_to = None
		if 'date_to' in request.GET : date_to = request.GET['date_to']
		query = ''
		if 'query' in request.GET : query = str(request.GET['query'])

		listes = []
		model = dao_historique_action.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'valeur_avant' : str(item.valeur_avant),
				'valeur_apres' : str(item.valeur_apres),
				'modele' : str(item.modele),
				'auteur' : str(item.auteur),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e)

def get_item_historique_action(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_historique_action.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'valeur_avant' : str(model.valeur_avant),
				'valeur_apres' : str(model.valeur_apres),
				'modele' : str(model.modele),
				'auteur' : str(model.auteur),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e)

@api_view(['POST'])
@transaction.atomic
def post_create_historique_action(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		valeur_avant = ''
		if 'valeur_avant' in request.POST : valeur_avant = str(request.POST['valeur_avant'])

		valeur_apres = ''
		if 'valeur_apres' in request.POST : valeur_apres = str(request.POST['valeur_apres'])

		modele = ''
		if 'modele' in request.POST : modele = str(request.POST['modele'])

		auteur = ''
		if 'auteur' in request.POST : auteur = str(request.POST['auteur'])

		auteur = dao_utilisateur.toGetUtilisateur(None)

		historique_action = dao_historique_action.toCreate(valeur_avant = valeur_avant, valeur_apres = valeur_apres, modele = modele)
		saved, historique_action, message = dao_historique_action.toSave(auteur, historique_action)

		if saved == False: raise Exception(message)

		objet = {
			'id' : historique_action.id,
			'valeur_avant' : str(historique_action.valeur_avant),
			'valeur_apres' : str(historique_action.valeur_apres),
			'modele' : str(historique_action.modele),
			'auteur' : str(historique_action.auteur),
			'etat' : str(historique_action.etat),
			'creation_date' : historique_action.creation_date,
			'update_date' : historique_action.update_date,
		}
		transaction.savepoint_commit(sid)

		context = {
			'error' : False,
			'message' : 'Enregistrement éffectué avec succès',
			'item' : objet
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e)

# LOG CONTROLLERS
from ModuleSupport.dao.dao_log import dao_log

def get_lister_log(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_log.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_log.toListJson(model.object_list),
				'view' : view,
				'query' : query,
				'page' : page,
				'count' : count,
			}
			context = pagination.toAddVarsToContext(model, context)
			return JsonResponse(context, safe=False)

		isPopup = False
		if 'isPopup' in request.GET:
			isPopup = True
			view = 'list'

		context = {
			'title' : "Liste des logs",
			'model' : model,
			'view' : view,
			'query' : query,
			'page' : page,
			'count' : count,
			'isPopup' : isPopup,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleSupport/log/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e)
		else: return auth.toReturnFailed(request, e, reverse('module_support_index'))

def get_creer_log(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Log",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Log(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/log/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_support_list_log'))

@transaction.atomic
def post_creer_log(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_support_add_log'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		erreur = str(request.POST['erreur'])

		modele = str(request.POST['modele'])

		auteur = identite.utilisateur(request)

		log = dao_log.toCreate(erreur = erreur, modele = modele)
		saved, log, message = dao_log.toSave(auteur, log)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_log.toListById(log.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, log)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : log.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e)

def get_select_log(request,ref):
	try:
		same_perm_with = 'module_support_list_log'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		log = dao_log.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(log.id),'obj': str(log)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_support_detail_log', args=(log.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_details_log(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		log = auth.toGetWithRules(dao_log.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if log == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, log) 

		context = {
			'title' : "Détails - Log : {}".format(log),
			'model' : log,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'historique': historique,
			'etapes_suivantes' : transitions_etapes_suivantes,
			'content_type_id': content_type_id,
			'documents': documents,
			'roles': groupe_permissions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/log/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_support_list_log'))

def get_modifier_log(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_log.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Log",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/log/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_log(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_support_update_log'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		erreur = str(request.POST['erreur'])

		modele = str(request.POST['modele'])
		auteur = identite.utilisateur(request)

		log = dao_log.toCreate(erreur = erreur, modele = modele)
		saved, log, message = dao_log.toUpdate(id, log, auteur)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_log.toListById(log.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : log.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e)

def get_dupliquer_log(request,ref):
	try:
		same_perm_with = 'module_support_add_log'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_log.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/log/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_log(request,ref):
	try:
		same_perm_with = 'module_support_list_log'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		log = auth.toGetWithRules(dao_log.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if log == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Log : {}".format(log),
			'model' : log,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleSupport/reporting/print_log.html', 'print_log.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_log(request):
	try:
		same_perm_with = 'module_support_add_log'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : "Import de la liste des logs",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleSupport/log/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_log(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=file_name, sheet_name=sheet, engine='openpyxl')
		#df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			erreur = str(df['erreur'][i])
			modele = str(df['modele'][i])

			log = dao_log.toCreate(erreur = erreur, modele = modele)
			saved, log, message = dao_log.toSave(auteur, log)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_support_list_log'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)