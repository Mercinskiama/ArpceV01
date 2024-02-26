# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import traceback
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
from ErpBackOffice.utils.utils import utils
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
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
monLog = logging.getLogger("logger")
module= "ModuleStock"
var_module_id = 9
vars_module = {"name" : "MODULE_STOCK", "value" : 3 }


def get_index(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(var_module_id, request)
		if response != None:
			return response

		#NOTIFCATION
		module_name = vars_module["name"]
		temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
		temp_notif_count = temp_notif_list.count()
		message_no_open = dao_temp_notification.toCountTempNotificationUnread(identite.utilisateur(request).id, module_name)

		context = {
			"title" : "Accueil",
			"utilisateur" : utilisateur,
			"organisation": dao_organisation.toGetMainOrganisation(),
			"temp_notif_count": temp_notif_count,
			"temp_notif_list": temp_notif_list,
			"msg_no_open": message_no_open,
			"sous_modules":sous_modules,
			"modules" : modules,
			"module" : vars_module
		}

		template = loader.get_template("ErpProject/ModuleStock/index.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('backoffice_index'))


def get_dashboard(request):
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

		template = loader.get_template("ErpProject/ModuleStock/dashboard.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('backoffice_index'))

# ARTICLE CONTROLLERS
from ModuleStock.dao.dao_article import dao_article

def get_lister_article(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_article.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_article.toListJson(model.object_list),
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
			'title' : "Liste des articles",
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
		template = loader.get_template('ErpProject/ModuleStock/article/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_article(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Article",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Article(),
			'devises' : Model_Devise.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'type_articles' : Model_Type_article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'categories' : Model_Categorie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/article/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_article'))

@transaction.atomic
def post_creer_article(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		name = str(request.POST['name'])

		code = str(request.POST['code'])

		amount = makeFloat(request.POST['amount'])

		devise_id = makeIntId(request.POST['devise_id'])

		type_article_id = makeIntId(request.POST['type_article_id'])

		picture_icon = request.FILES['picture_icon'] if 'picture_icon' in request.FILES else None

		societe_id = makeIntId(request.POST['societe_id'])

		quota_quantity = makeInt(request.POST['quota_quantity'])

		category_id = makeIntId(request.POST['category_id'])

		measure_unit_id = makeIntId(request.POST['measure_unit_id'])

		description = str(request.POST['description'])

		auteur = identite.utilisateur(request)

		article = dao_article.toCreate(name = name, code = code, amount = amount, devise_id = devise_id, type_article_id = type_article_id, picture_icon = picture_icon, societe_id = societe_id, quota_quantity = quota_quantity, category_id = category_id, measure_unit_id = measure_unit_id, description = description)
		saved, article, message = dao_article.toSave(auteur, article, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_article.toListById(article.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, article)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : article.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_article(request,ref):
	try:
		same_perm_with = 'module_stock_list_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		article = dao_article.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(article.id),'obj': str(article)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_article', args=(article.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_article(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		article = auth.toGetWithRules(dao_article.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if article == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, article) 

		context = {
			'title' : "Détails - Article : {}".format(article),
			'model' : article,
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
		template = loader.get_template('ErpProject/ModuleStock/article/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_article'))

def get_modifier_article(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_article.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Article",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'devises' : Model_Devise.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'type_articles' : Model_Type_article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'categories' : Model_Categorie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/article/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_article(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		name = str(request.POST['name'])

		code = str(request.POST['code'])

		amount = makeFloat(request.POST['amount'])

		devise_id = makeIntId(request.POST['devise_id'])

		type_article_id = makeIntId(request.POST['type_article_id'])

		picture_icon = request.FILES['picture_icon'] if 'picture_icon' in request.FILES else None

		societe_id = makeIntId(request.POST['societe_id'])

		quota_quantity = makeInt(request.POST['quota_quantity'])

		category_id = makeIntId(request.POST['category_id'])

		measure_unit_id = makeIntId(request.POST['measure_unit_id'])

		description = str(request.POST['description'])
		auteur = identite.utilisateur(request)

		article = dao_article.toCreate(name = name, code = code, amount = amount, devise_id = devise_id, type_article_id = type_article_id, picture_icon = picture_icon, societe_id = societe_id, quota_quantity = quota_quantity, category_id = category_id, measure_unit_id = measure_unit_id, description = description)
		saved, article, message = dao_article.toUpdate(id, article, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_article.toListById(article.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : article.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_article(request,ref):
	try:
		same_perm_with = 'module_stock_add_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_article.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'devises' : Model_Devise.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'type_articles' : Model_Type_article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'categories' : Model_Categorie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/article/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_article(request,ref):
	try:
		same_perm_with = 'module_stock_list_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		article = auth.toGetWithRules(dao_article.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if article == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Article : {}".format(article),
			'model' : article,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_article.html', 'print_article.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_article(request):
	try:
		same_perm_with = 'module_stock_add_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_article')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des articles",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/article/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_article(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_name = makeString(request.POST['name'])
		#print(f'header_name_id: {header_name_id}')

		header_code = makeString(request.POST['code'])
		#print(f'header_code_id: {header_code_id}')

		header_amount = makeString(request.POST['amount'])
		#print(f'header_amount_id: {header_amount_id}')

		header_devise_id = makeString(request.POST['devise_id'])
		#print(f'header_devise_id: {header_devise_id}')

		header_type_article_id = makeString(request.POST['type_article_id'])
		#print(f'header_type_article_id: {header_type_article_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_quota_quantity = makeString(request.POST['quota_quantity'])
		#print(f'header_quota_quantity_id: {header_quota_quantity_id}')

		header_category_id = makeString(request.POST['category_id'])
		#print(f'header_category_id: {header_category_id}')

		header_measure_unit_id = makeString(request.POST['measure_unit_id'])
		#print(f'header_measure_unit_id: {header_measure_unit_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		for i in df.index:

			name = ''
			if header_name != '': name = makeString(df[header_name][i])

			code = ''
			if header_code != '': code = makeString(df[header_code][i])

			amount = 0
			if header_amount != '': amount = makeFloat(df[header_amount][i])

			devise_id = None
			if header_devise_id != '': devise_id = makeIntId(str(df[header_devise_id][i]))

			type_article_id = None
			if header_type_article_id != '': type_article_id = makeIntId(str(df[header_type_article_id][i]))

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			quota_quantity = 0
			if header_quota_quantity != '': quota_quantity = makeInt(df[header_quota_quantity][i])

			category_id = None
			if header_category_id != '': category_id = makeIntId(str(df[header_category_id][i]))

			measure_unit_id = None
			if header_measure_unit_id != '': measure_unit_id = makeIntId(str(df[header_measure_unit_id][i]))

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			article = dao_article.toCreate(name = name, code = code, amount = amount, devise_id = devise_id, type_article_id = type_article_id, societe_id = societe_id, quota_quantity = quota_quantity, category_id = category_id, measure_unit_id = measure_unit_id, description = description)
			saved, article, message = dao_article.toSave(auteur, article)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_article'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# ARTICLE BI CONTROLLERS
def get_bi_article(request):
	try:
		same_perm_with = 'module_stock_get_generer_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		try:
			view = str(request.GET.get('view','table'))
		except Exception as e:
			view = 'table'

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_article.toList(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model, 100)

		model_content_type = dao_query_builder.toGetContentTypeByName('model_article')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)
		champs_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)
		champs_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)
		champs_date = dao_query_builder.toListFieldsDate(model_content_type.id)

		context = {
			'title' : "Analyse des articles",
			'model' : model,
			'model_id' : model_content_type.id,
			'modele' : Model_Article(),
			'champs' : champs,
			'champs_nombre' : champs_nombre,
			'champs_date' : champs_date,
			'champs_dimension' : champs_texte,
			'view' : view,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleStock/article/bi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

# ARTICLE API CONTROLLERS
def get_list_article(request):
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
		model = dao_article.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'name' : str(item.name),
				'code' : str(item.code),
				'amount' : makeFloat(item.amount),
				'devise_id' : makeIntId(item.devise_id),
				'type_article_id' : makeIntId(item.type_article_id),
				'picture_icon' : item.picture_icon.url if item.picture_icon != None else None,
				'societe_id' : makeIntId(item.societe_id),
				'quota_quantity' : makeInt(item.quota_quantity),
				'category_id' : makeIntId(item.category_id),
				'measure_unit_id' : makeIntId(item.measure_unit_id),
				'description' : str(item.description),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_article(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_article.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'name' : str(model.name),
				'code' : str(model.code),
				'amount' : makeFloat(model.amount),
				'devise_id' : makeIntId(model.devise_id),
				'type_article_id' : makeIntId(model.type_article_id),
				'picture_icon' : model.picture_icon.url if model.picture_icon != None else None,
				'societe_id' : makeIntId(model.societe_id),
				'quota_quantity' : makeInt(model.quota_quantity),
				'category_id' : makeIntId(model.category_id),
				'measure_unit_id' : makeIntId(model.measure_unit_id),
				'description' : str(model.description),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_article(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		name = ''
		if 'name' in request.POST : name = str(request.POST['name'])

		code = ''
		if 'code' in request.POST : code = str(request.POST['code'])

		amount = 0.0
		if 'amount' in request.POST : amount = makeFloat(request.POST['amount'])

		devise_id = None
		if 'devise' in request.POST : devise_id = makeIntId(request.POST['devise_id'])

		type_article_id = None
		if 'type_article' in request.POST : type_article_id = makeIntId(request.POST['type_article_id'])

		picture_icon = request.FILES['picture_icon'] if 'picture_icon' in request.FILES else None

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		quota_quantity = 0
		if 'quota_quantity' in request.POST : quota_quantity = makeInt(request.POST['quota_quantity'])

		category_id = None
		if 'category' in request.POST : category_id = makeIntId(request.POST['category_id'])

		measure_unit_id = None
		if 'measure_unit' in request.POST : measure_unit_id = makeIntId(request.POST['measure_unit_id'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		article = dao_article.toCreate(name = name, code = code, amount = amount, devise_id = devise_id, type_article_id = type_article_id, picture_icon = picture_icon, societe_id = societe_id, quota_quantity = quota_quantity, category_id = category_id, measure_unit_id = measure_unit_id, description = description)
		saved, article, message = dao_article.toSave(auteur, article)

		if saved == False: raise Exception(message)

		objet = {
			'id' : article.id,
			'name' : str(article.name),
			'code' : str(article.code),
			'amount' : makeFloat(article.amount),
			'devise_id' : makeIntId(article.devise_id),
			'type_article_id' : makeIntId(article.type_article_id),
			'picture_icon' : article.picture_icon.url if article.picture_icon != None else None,
			'societe_id' : makeIntId(article.societe_id),
			'quota_quantity' : makeInt(article.quota_quantity),
			'category_id' : makeIntId(article.category_id),
			'measure_unit_id' : makeIntId(article.measure_unit_id),
			'description' : str(article.description),
			'statut_id' : makeIntId(article.statut_id),
			'etat' : str(article.etat),
			'creation_date' : article.creation_date,
			'update_date' : article.update_date,
			'update_by_id' : makeIntId(article.update_by_id),
			'auteur_id' : makeIntId(article.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# STOCKAGE CONTROLLERS
from ModuleStock.dao.dao_stockage import dao_stockage

def get_lister_stockage(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_stockage.toListStock(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_stockage.toListJson(model.object_list),
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
			'title' : "Liste des stockages",
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
		template = loader.get_template('ErpProject/ModuleStock/stockage/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))



def get_list_stock_from_empl(request, ref):
	try:
		same_perm_with = 'module_stock_list_stockage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		print(f'REF::::::::{ref}')
		emplacement = dao_emplacement.toGet(ref)
		print("  File: ModuleStock/views.py | Line: 2100 | get_list_stock_from_empl ~ emplacement",emplacement)
		#On recupere le stockage par rapport à un emplacement
		stockages = Model_Stockage.objects.filter(emplacement_id = emplacement.id).order_by('creation_date')
		print(f'stockages ::: {stockages}') 
		# historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, stockage)

		context = {
			'title' : f"Détails - Stockage : {emplacement}", #.format(stockage)s
			'model' : emplacement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'roles': groupe_permissions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'stockages': stockages
		}
		template = loader.get_template('ErpProject/ModuleStock/stockage/detail_item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_stock_list_stockage'))		



def get_creer_stockage(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Stockage",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Stockage(),
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/stockage/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_stockage'))

@transaction.atomic
def post_creer_stockage(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_stockage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		quantite = makeFloat(request.POST['quantite'])

		unite_id = makeIntId(request.POST['unite_id'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		stockage = dao_stockage.toCreate(emplacement_id = emplacement_id, article_id = article_id, quantite = quantite, unite_id = unite_id, societe_id = societe_id)
		saved, stockage, message = dao_stockage.toSave(auteur, stockage, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_stockage.toListById(stockage.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, stockage)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : stockage.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_stockage(request,ref):
	try:
		same_perm_with = 'module_stock_list_stockage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		stockage = dao_stockage.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(stockage.id),'obj': str(stockage)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_stockage', args=(stockage.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_stockage(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		stockage = auth.toGetWithRules(dao_stockage.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if stockage == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, stockage) 

		context = {
			'title' : "Détails - Stockage : {}".format(stockage),
			'model' : stockage,
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
		template = loader.get_template('ErpProject/ModuleStock/stockage/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_stockage'))

def get_modifier_stockage(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_stockage.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Stockage",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/stockage/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_stockage(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_stockage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		quantite = makeFloat(request.POST['quantite'])

		unite_id = makeIntId(request.POST['unite_id'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		stockage = dao_stockage.toCreate(emplacement_id = emplacement_id, article_id = article_id, quantite = quantite, unite_id = unite_id, societe_id = societe_id)
		saved, stockage, message = dao_stockage.toUpdate(id, stockage, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_stockage.toListById(stockage.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : stockage.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_stockage(request,ref):
	try:
		same_perm_with = 'module_stock_add_stockage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_stockage.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/stockage/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_stockage(request,ref):
	try:
		same_perm_with = 'module_stock_list_stockage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		stockage = auth.toGetWithRules(dao_stockage.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if stockage == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Stockage : {}".format(stockage),
			'model' : stockage,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_stockage.html', 'print_stockage.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_stockage(request):
	try:
		same_perm_with = 'module_stock_add_stockage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_stockage')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des stockages",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/stockage/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_stockage(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_emplacement_id = makeString(request.POST['emplacement_id'])
		if header_emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_emplacement_id: {header_emplacement_id}')

		header_article_id = makeString(request.POST['article_id'])
		if header_article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_article_id: {header_article_id}')

		header_quantite = makeString(request.POST['quantite'])
		#print(f'header_quantite_id: {header_quantite_id}')

		header_unite_id = makeString(request.POST['unite_id'])
		#print(f'header_unite_id: {header_unite_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			emplacement_id = None
			if header_emplacement_id != '': emplacement_id = makeIntId(str(df[header_emplacement_id][i]))
			if emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

			article_id = None
			if header_article_id != '': article_id = makeIntId(str(df[header_article_id][i]))
			if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

			quantite = 0
			if header_quantite != '': quantite = makeFloat(df[header_quantite][i])

			unite_id = None
			if header_unite_id != '': unite_id = makeIntId(str(df[header_unite_id][i]))

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			stockage = dao_stockage.toCreate(emplacement_id = emplacement_id, article_id = article_id, quantite = quantite, unite_id = unite_id, societe_id = societe_id)
			saved, stockage, message = dao_stockage.toSave(auteur, stockage)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_stockage'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# STOCKAGE API CONTROLLERS
def get_list_stockage(request):
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
		model = dao_stockage.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'emplacement_id' : makeIntId(item.emplacement_id),
				'article_id' : makeIntId(item.article_id),
				'quantite' : makeFloat(item.quantite),
				'unite_id' : makeIntId(item.unite_id),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_stockage(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_stockage.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'emplacement_id' : makeIntId(model.emplacement_id),
				'article_id' : makeIntId(model.article_id),
				'quantite' : makeFloat(model.quantite),
				'unite_id' : makeIntId(model.unite_id),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_stockage(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		emplacement_id = None
		if 'emplacement' in request.POST : emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = None
		if 'article' in request.POST : article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		quantite = 0.0
		if 'quantite' in request.POST : quantite = makeFloat(request.POST['quantite'])

		unite_id = None
		if 'unite' in request.POST : unite_id = makeIntId(request.POST['unite_id'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		stockage = dao_stockage.toCreate(emplacement_id = emplacement_id, article_id = article_id, quantite = quantite, unite_id = unite_id, societe_id = societe_id)
		saved, stockage, message = dao_stockage.toSave(auteur, stockage)

		if saved == False: raise Exception(message)

		objet = {
			'id' : stockage.id,
			'emplacement_id' : makeIntId(stockage.emplacement_id),
			'article_id' : makeIntId(stockage.article_id),
			'quantite' : makeFloat(stockage.quantite),
			'unite_id' : makeIntId(stockage.unite_id),
			'statut_id' : makeIntId(stockage.statut_id),
			'etat' : str(stockage.etat),
			'societe_id' : makeIntId(stockage.societe_id),
			'creation_date' : stockage.creation_date,
			'update_date' : stockage.update_date,
			'update_by_id' : makeIntId(stockage.update_by_id),
			'auteur_id' : makeIntId(stockage.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# TYPE_ARTICLE CONTROLLERS
from ModuleStock.dao.dao_type_article import dao_type_article

def get_lister_type_article(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_type_article.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_type_article.toListJson(model.object_list),
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
			'title' : "Liste des types d'articles",
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
		template = loader.get_template('ErpProject/ModuleStock/type_article/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_type_article(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Type d'Article",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Type_article(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_article/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_type_article'))

@transaction.atomic
def post_creer_type_article(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_type_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')

		est_service = True if 'est_service' in request.POST else False

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		type_article = dao_type_article.toCreate(designation = designation, est_service = est_service, societe_id = societe_id)
		saved, type_article, message = dao_type_article.toSave(auteur, type_article, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_type_article.toListById(type_article.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, type_article)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : type_article.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_type_article(request,ref):
	try:
		same_perm_with = 'module_stock_list_type_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		type_article = dao_type_article.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(type_article.id),'obj': str(type_article)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_type_article', args=(type_article.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_type_article(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		type_article = auth.toGetWithRules(dao_type_article.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if type_article == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, type_article) 

		context = {
			'title' : "Détails - Type d'Article : {}".format(type_article),
			'model' : type_article,
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
		template = loader.get_template('ErpProject/ModuleStock/type_article/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_type_article'))

def get_modifier_type_article(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_type_article.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Type d'Article",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_article/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_type_article(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_type_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')

		est_service = True if 'est_service' in request.POST else False

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		type_article = dao_type_article.toCreate(designation = designation, est_service = est_service, societe_id = societe_id)
		saved, type_article, message = dao_type_article.toUpdate(id, type_article, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_type_article.toListById(type_article.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : type_article.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_type_article(request,ref):
	try:
		same_perm_with = 'module_stock_add_type_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_type_article.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_article/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_type_article(request,ref):
	try:
		same_perm_with = 'module_stock_list_type_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		type_article = auth.toGetWithRules(dao_type_article.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if type_article == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Type d'Article : {}".format(type_article),
			'model' : type_article,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_type_article.html', 'print_type_article.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_type_article(request):
	try:
		same_perm_with = 'module_stock_add_type_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_type_article')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des types d'articles",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_article/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_type_article(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_designation = makeString(request.POST['designation'])
		if header_designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_designation_id: {header_designation_id}')

		header_est_service = makeString(request.POST['est_service'])
		#print(f'header_est_service_id: {header_est_service_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			designation = ''
			if header_designation != '': designation = makeString(df[header_designation][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')

			est_service = False
			if header_est_service != '': est_service = True if makeString(df[header_est_service][i]) == 'True' else False

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			type_article = dao_type_article.toCreate(designation = designation, est_service = est_service, societe_id = societe_id)
			saved, type_article, message = dao_type_article.toSave(auteur, type_article)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_type_article'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# TYPE_ARTICLE API CONTROLLERS
def get_list_type_article(request):
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
		model = dao_type_article.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'designation' : str(item.designation),
				'est_service' : item.est_service,
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_type_article(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_type_article.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'designation' : str(model.designation),
				'est_service' : model.est_service,
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_type_article(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		designation = ''
		if 'designation' in request.POST : designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')

		est_service = True if 'est_service' in request.POST else False

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		type_article = dao_type_article.toCreate(designation = designation, est_service = est_service, societe_id = societe_id)
		saved, type_article, message = dao_type_article.toSave(auteur, type_article)

		if saved == False: raise Exception(message)

		objet = {
			'id' : type_article.id,
			'designation' : str(type_article.designation),
			'est_service' : type_article.est_service,
			'statut_id' : makeIntId(type_article.statut_id),
			'etat' : str(type_article.etat),
			'societe_id' : makeIntId(type_article.societe_id),
			'creation_date' : type_article.creation_date,
			'update_date' : type_article.update_date,
			'update_by_id' : makeIntId(type_article.update_by_id),
			'auteur_id' : makeIntId(type_article.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# TYPE_EMPLACEMENT CONTROLLERS
from ModuleStock.dao.dao_type_emplacement import dao_type_emplacement

def get_lister_type_emplacement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_type_emplacement.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_type_emplacement.toListJson(model.object_list),
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
			'title' : "Liste des types d'emplacement",
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
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_type_emplacement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Type d'emplacement",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Type_emplacement(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_type_emplacement'))

@transaction.atomic
def post_creer_type_emplacement(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_type_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		code = str(request.POST['code'])

		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		type_emplacement = dao_type_emplacement.toCreate(code = code, designation = designation, societe_id = societe_id)
		saved, type_emplacement, message = dao_type_emplacement.toSave(auteur, type_emplacement, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_type_emplacement.toListById(type_emplacement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, type_emplacement)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : type_emplacement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_type_emplacement(request,ref):
	try:
		same_perm_with = 'module_stock_list_type_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		type_emplacement = dao_type_emplacement.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(type_emplacement.id),'obj': str(type_emplacement)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_type_emplacement', args=(type_emplacement.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_type_emplacement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		type_emplacement = auth.toGetWithRules(dao_type_emplacement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if type_emplacement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, type_emplacement) 

		context = {
			'title' : "Détails - Type d'emplacement : {}".format(type_emplacement),
			'model' : type_emplacement,
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
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_type_emplacement'))

def get_modifier_type_emplacement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_type_emplacement.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Type d'emplacement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_type_emplacement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_type_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		code = str(request.POST['code'])

		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		type_emplacement = dao_type_emplacement.toCreate(code = code, designation = designation, societe_id = societe_id)
		saved, type_emplacement, message = dao_type_emplacement.toUpdate(id, type_emplacement, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_type_emplacement.toListById(type_emplacement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : type_emplacement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_type_emplacement(request,ref):
	try:
		same_perm_with = 'module_stock_add_type_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_type_emplacement.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_type_emplacement(request,ref):
	try:
		same_perm_with = 'module_stock_list_type_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		type_emplacement = auth.toGetWithRules(dao_type_emplacement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if type_emplacement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Type d'emplacement : {}".format(type_emplacement),
			'model' : type_emplacement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_type_emplacement.html', 'print_type_emplacement.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_type_emplacement(request):
	try:
		same_perm_with = 'module_stock_add_type_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_type_emplacement')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des types d'emplacement",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_type_emplacement(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_code = makeString(request.POST['code'])
		#print(f'header_code_id: {header_code_id}')

		header_designation = makeString(request.POST['designation'])
		if header_designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_designation_id: {header_designation_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			code = ''
			if header_code != '': code = makeString(df[header_code][i])

			designation = ''
			if header_designation != '': designation = makeString(df[header_designation][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			type_emplacement = dao_type_emplacement.toCreate(code = code, designation = designation, societe_id = societe_id)
			saved, type_emplacement, message = dao_type_emplacement.toSave(auteur, type_emplacement)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_type_emplacement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# TYPE_EMPLACEMENT API CONTROLLERS
def get_list_type_emplacement(request):
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
		model = dao_type_emplacement.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'code' : str(item.code),
				'designation' : str(item.designation),
				'societe_id' : makeIntId(item.societe_id),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_type_emplacement(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_type_emplacement.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'code' : str(model.code),
				'designation' : str(model.designation),
				'societe_id' : makeIntId(model.societe_id),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_type_emplacement(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		code = ''
		if 'code' in request.POST : code = str(request.POST['code'])

		designation = ''
		if 'designation' in request.POST : designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		type_emplacement = dao_type_emplacement.toCreate(code = code, designation = designation, societe_id = societe_id)
		saved, type_emplacement, message = dao_type_emplacement.toSave(auteur, type_emplacement)

		if saved == False: raise Exception(message)

		objet = {
			'id' : type_emplacement.id,
			'code' : str(type_emplacement.code),
			'designation' : str(type_emplacement.designation),
			'societe_id' : makeIntId(type_emplacement.societe_id),
			'statut_id' : makeIntId(type_emplacement.statut_id),
			'etat' : str(type_emplacement.etat),
			'creation_date' : type_emplacement.creation_date,
			'update_date' : type_emplacement.update_date,
			'update_by_id' : makeIntId(type_emplacement.update_by_id),
			'auteur_id' : makeIntId(type_emplacement.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# TYPE_MVT_STOCK CONTROLLERS
from ModuleStock.dao.dao_type_mvt_stock import dao_type_mvt_stock

def get_lister_type_mvt_stock(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_type_mvt_stock.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_type_mvt_stock.toListJson(model.object_list),
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
			'title' : "Liste des types de mouvement stock",
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
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_type_mvt_stock(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Type de mouvement stock",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Type_mvt_stock(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_type_mvt_stock'))

@transaction.atomic
def post_creer_type_mvt_stock(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_type_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		type_mvt_stock = dao_type_mvt_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, type_mvt_stock, message = dao_type_mvt_stock.toSave(auteur, type_mvt_stock, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_type_mvt_stock.toListById(type_mvt_stock.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, type_mvt_stock)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : type_mvt_stock.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_type_mvt_stock(request,ref):
	try:
		same_perm_with = 'module_stock_list_type_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		type_mvt_stock = dao_type_mvt_stock.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(type_mvt_stock.id),'obj': str(type_mvt_stock)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_type_mvt_stock', args=(type_mvt_stock.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_type_mvt_stock(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		type_mvt_stock = auth.toGetWithRules(dao_type_mvt_stock.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if type_mvt_stock == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, type_mvt_stock) 

		context = {
			'title' : "Détails - Type de mouvement stock : {}".format(type_mvt_stock),
			'model' : type_mvt_stock,
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
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_type_mvt_stock'))

def get_modifier_type_mvt_stock(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_type_mvt_stock.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Type de mouvement stock",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_type_mvt_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_type_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		type_mvt_stock = dao_type_mvt_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, type_mvt_stock, message = dao_type_mvt_stock.toUpdate(id, type_mvt_stock, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_type_mvt_stock.toListById(type_mvt_stock.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : type_mvt_stock.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_type_mvt_stock(request,ref):
	try:
		same_perm_with = 'module_stock_add_type_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_type_mvt_stock.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_type_mvt_stock(request,ref):
	try:
		same_perm_with = 'module_stock_list_type_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		type_mvt_stock = auth.toGetWithRules(dao_type_mvt_stock.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if type_mvt_stock == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Type de mouvement stock : {}".format(type_mvt_stock),
			'model' : type_mvt_stock,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_type_mvt_stock.html', 'print_type_mvt_stock.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_type_mvt_stock(request):
	try:
		same_perm_with = 'module_stock_add_type_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_type_mvt_stock')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des types de mouvement stock",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_type_mvt_stock(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_designation = makeString(request.POST['designation'])
		#print(f'header_designation_id: {header_designation_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			designation = ''
			if header_designation != '': designation = makeString(df[header_designation][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			type_mvt_stock = dao_type_mvt_stock.toCreate(designation = designation, societe_id = societe_id)
			saved, type_mvt_stock, message = dao_type_mvt_stock.toSave(auteur, type_mvt_stock)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_type_mvt_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# TYPE_MVT_STOCK API CONTROLLERS
def get_list_type_mvt_stock(request):
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
		model = dao_type_mvt_stock.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'designation' : str(item.designation),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_type_mvt_stock(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_type_mvt_stock.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'designation' : str(model.designation),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_type_mvt_stock(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		designation = ''
		if 'designation' in request.POST : designation = str(request.POST['designation'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		type_mvt_stock = dao_type_mvt_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, type_mvt_stock, message = dao_type_mvt_stock.toSave(auteur, type_mvt_stock)

		if saved == False: raise Exception(message)

		objet = {
			'id' : type_mvt_stock.id,
			'designation' : str(type_mvt_stock.designation),
			'statut_id' : makeIntId(type_mvt_stock.statut_id),
			'etat' : str(type_mvt_stock.etat),
			'societe_id' : makeIntId(type_mvt_stock.societe_id),
			'creation_date' : type_mvt_stock.creation_date,
			'update_date' : type_mvt_stock.update_date,
			'update_by_id' : makeIntId(type_mvt_stock.update_by_id),
			'auteur_id' : makeIntId(type_mvt_stock.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# UNITE_MESURE CONTROLLERS
from ModuleStock.dao.dao_unite_mesure import dao_unite_mesure

def get_lister_unite_mesure(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_unite_mesure.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_unite_mesure.toListJson(model.object_list),
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
			'title' : "Liste des unités de mesure",
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
		template = loader.get_template('ErpProject/ModuleStock/unite_mesure/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_unite_mesure(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Unité de mesure",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Unite_mesure(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/unite_mesure/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_unite_mesure'))

@transaction.atomic
def post_creer_unite_mesure(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_unite_mesure'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		name = str(request.POST['name'])

		short_name = str(request.POST['short_name'])

		description = str(request.POST['description'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		unite_mesure = dao_unite_mesure.toCreate(name = name, short_name = short_name, description = description, societe_id = societe_id)
		saved, unite_mesure, message = dao_unite_mesure.toSave(auteur, unite_mesure, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_unite_mesure.toListById(unite_mesure.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, unite_mesure)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : unite_mesure.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_unite_mesure(request,ref):
	try:
		same_perm_with = 'module_stock_list_unite_mesure'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		unite_mesure = dao_unite_mesure.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(unite_mesure.id),'obj': str(unite_mesure)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_unite_mesure', args=(unite_mesure.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_unite_mesure(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		unite_mesure = auth.toGetWithRules(dao_unite_mesure.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if unite_mesure == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, unite_mesure) 

		context = {
			'title' : "Détails - Unité de mesure : {}".format(unite_mesure),
			'model' : unite_mesure,
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
		template = loader.get_template('ErpProject/ModuleStock/unite_mesure/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_unite_mesure'))

def get_modifier_unite_mesure(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_unite_mesure.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Unité de mesure",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/unite_mesure/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_unite_mesure(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_unite_mesure'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		name = str(request.POST['name'])

		short_name = str(request.POST['short_name'])

		description = str(request.POST['description'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		unite_mesure = dao_unite_mesure.toCreate(name = name, short_name = short_name, description = description, societe_id = societe_id)
		saved, unite_mesure, message = dao_unite_mesure.toUpdate(id, unite_mesure, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_unite_mesure.toListById(unite_mesure.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : unite_mesure.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_unite_mesure(request,ref):
	try:
		same_perm_with = 'module_stock_add_unite_mesure'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_unite_mesure.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/unite_mesure/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_unite_mesure(request,ref):
	try:
		same_perm_with = 'module_stock_list_unite_mesure'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		unite_mesure = auth.toGetWithRules(dao_unite_mesure.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if unite_mesure == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Unité de mesure : {}".format(unite_mesure),
			'model' : unite_mesure,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_unite_mesure.html', 'print_unite_mesure.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_unite_mesure(request):
	try:
		same_perm_with = 'module_stock_add_unite_mesure'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_unite_mesure')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des unités de mesure",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/unite_mesure/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_unite_mesure(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_name = makeString(request.POST['name'])
		#print(f'header_name_id: {header_name_id}')

		header_short_name = makeString(request.POST['short_name'])
		#print(f'header_short_name_id: {header_short_name_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			name = ''
			if header_name != '': name = makeString(df[header_name][i])

			short_name = ''
			if header_short_name != '': short_name = makeString(df[header_short_name][i])

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			unite_mesure = dao_unite_mesure.toCreate(name = name, short_name = short_name, description = description, societe_id = societe_id)
			saved, unite_mesure, message = dao_unite_mesure.toSave(auteur, unite_mesure)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_unite_mesure'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# UNITE_MESURE API CONTROLLERS
def get_list_unite_mesure(request):
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
		model = dao_unite_mesure.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'name' : str(item.name),
				'short_name' : str(item.short_name),
				'description' : str(item.description),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_unite_mesure(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_unite_mesure.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'name' : str(model.name),
				'short_name' : str(model.short_name),
				'description' : str(model.description),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_unite_mesure(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		name = ''
		if 'name' in request.POST : name = str(request.POST['name'])

		short_name = ''
		if 'short_name' in request.POST : short_name = str(request.POST['short_name'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		unite_mesure = dao_unite_mesure.toCreate(name = name, short_name = short_name, description = description, societe_id = societe_id)
		saved, unite_mesure, message = dao_unite_mesure.toSave(auteur, unite_mesure)

		if saved == False: raise Exception(message)

		objet = {
			'id' : unite_mesure.id,
			'name' : str(unite_mesure.name),
			'short_name' : str(unite_mesure.short_name),
			'description' : str(unite_mesure.description),
			'statut_id' : makeIntId(unite_mesure.statut_id),
			'etat' : str(unite_mesure.etat),
			'societe_id' : makeIntId(unite_mesure.societe_id),
			'creation_date' : unite_mesure.creation_date,
			'update_date' : unite_mesure.update_date,
			'update_by_id' : makeIntId(unite_mesure.update_by_id),
			'auteur_id' : makeIntId(unite_mesure.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# STATUT_OPERATION_STOCK CONTROLLERS
from ModuleStock.dao.dao_statut_operation_stock import dao_statut_operation_stock

def get_lister_statut_operation_stock(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_statut_operation_stock.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_statut_operation_stock.toListJson(model.object_list),
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
			'title' : "Liste des statuts d'opération stock",
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
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_statut_operation_stock(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Statut d'opération stock",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Statut_operation_stock(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_statut_operation_stock'))

@transaction.atomic
def post_creer_statut_operation_stock(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_statut_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		statut_operation_stock = dao_statut_operation_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, statut_operation_stock, message = dao_statut_operation_stock.toSave(auteur, statut_operation_stock, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_statut_operation_stock.toListById(statut_operation_stock.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, statut_operation_stock)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : statut_operation_stock.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_statut_operation_stock(request,ref):
	try:
		same_perm_with = 'module_stock_list_statut_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		statut_operation_stock = dao_statut_operation_stock.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(statut_operation_stock.id),'obj': str(statut_operation_stock)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_statut_operation_stock', args=(statut_operation_stock.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_statut_operation_stock(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		statut_operation_stock = auth.toGetWithRules(dao_statut_operation_stock.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if statut_operation_stock == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, statut_operation_stock) 

		context = {
			'title' : "Détails - Statut d'opération stock : {}".format(statut_operation_stock),
			'model' : statut_operation_stock,
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
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_statut_operation_stock'))

def get_modifier_statut_operation_stock(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_statut_operation_stock.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Statut d'opération stock",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_statut_operation_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_statut_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		statut_operation_stock = dao_statut_operation_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, statut_operation_stock, message = dao_statut_operation_stock.toUpdate(id, statut_operation_stock, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_statut_operation_stock.toListById(statut_operation_stock.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : statut_operation_stock.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_statut_operation_stock(request,ref):
	try:
		same_perm_with = 'module_stock_add_statut_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_statut_operation_stock.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_statut_operation_stock(request,ref):
	try:
		same_perm_with = 'module_stock_list_statut_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		statut_operation_stock = auth.toGetWithRules(dao_statut_operation_stock.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if statut_operation_stock == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Statut d'opération stock : {}".format(statut_operation_stock),
			'model' : statut_operation_stock,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_statut_operation_stock.html', 'print_statut_operation_stock.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_statut_operation_stock(request):
	try:
		same_perm_with = 'module_stock_add_statut_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_statut_operation_stock')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des statuts d'opération stock",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_statut_operation_stock(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_designation = makeString(request.POST['designation'])
		#print(f'header_designation_id: {header_designation_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			designation = ''
			if header_designation != '': designation = makeString(df[header_designation][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			statut_operation_stock = dao_statut_operation_stock.toCreate(designation = designation, societe_id = societe_id)
			saved, statut_operation_stock, message = dao_statut_operation_stock.toSave(auteur, statut_operation_stock)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_statut_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# STATUT_OPERATION_STOCK API CONTROLLERS
def get_list_statut_operation_stock(request):
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
		model = dao_statut_operation_stock.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'designation' : str(item.designation),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_statut_operation_stock(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_statut_operation_stock.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'designation' : str(model.designation),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_statut_operation_stock(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		designation = ''
		if 'designation' in request.POST : designation = str(request.POST['designation'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		statut_operation_stock = dao_statut_operation_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, statut_operation_stock, message = dao_statut_operation_stock.toSave(auteur, statut_operation_stock)

		if saved == False: raise Exception(message)

		objet = {
			'id' : statut_operation_stock.id,
			'designation' : str(statut_operation_stock.designation),
			'statut_id' : makeIntId(statut_operation_stock.statut_id),
			'etat' : str(statut_operation_stock.etat),
			'societe_id' : makeIntId(statut_operation_stock.societe_id),
			'creation_date' : statut_operation_stock.creation_date,
			'update_date' : statut_operation_stock.update_date,
			'update_by_id' : makeIntId(statut_operation_stock.update_by_id),
			'auteur_id' : makeIntId(statut_operation_stock.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# STATUT_AJUSTEMENT CONTROLLERS
from ModuleStock.dao.dao_statut_ajustement import dao_statut_ajustement

def get_lister_statut_ajustement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_statut_ajustement.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_statut_ajustement.toListJson(model.object_list),
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
			'title' : "Liste des statuts inventaire",
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
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_statut_ajustement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Statut inventaire",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Statut_ajustement(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_statut_ajustement'))

@transaction.atomic
def post_creer_statut_ajustement(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_statut_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		statut_ajustement = dao_statut_ajustement.toCreate(designation = designation, societe_id = societe_id)
		saved, statut_ajustement, message = dao_statut_ajustement.toSave(auteur, statut_ajustement, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_statut_ajustement.toListById(statut_ajustement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, statut_ajustement)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : statut_ajustement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_statut_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_list_statut_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		statut_ajustement = dao_statut_ajustement.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(statut_ajustement.id),'obj': str(statut_ajustement)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_statut_ajustement', args=(statut_ajustement.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_statut_ajustement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		statut_ajustement = auth.toGetWithRules(dao_statut_ajustement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if statut_ajustement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, statut_ajustement) 

		context = {
			'title' : "Détails - Statut inventaire : {}".format(statut_ajustement),
			'model' : statut_ajustement,
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
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_statut_ajustement'))

def get_modifier_statut_ajustement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_statut_ajustement.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Statut inventaire",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_statut_ajustement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_statut_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		statut_ajustement = dao_statut_ajustement.toCreate(designation = designation, societe_id = societe_id)
		saved, statut_ajustement, message = dao_statut_ajustement.toUpdate(id, statut_ajustement, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_statut_ajustement.toListById(statut_ajustement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : statut_ajustement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_statut_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_add_statut_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_statut_ajustement.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_statut_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_list_statut_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		statut_ajustement = auth.toGetWithRules(dao_statut_ajustement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if statut_ajustement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Statut inventaire : {}".format(statut_ajustement),
			'model' : statut_ajustement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_statut_ajustement.html', 'print_statut_ajustement.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_statut_ajustement(request):
	try:
		same_perm_with = 'module_stock_add_statut_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_statut_ajustement')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des statuts inventaire",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_statut_ajustement(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_designation = makeString(request.POST['designation'])
		#print(f'header_designation_id: {header_designation_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			designation = ''
			if header_designation != '': designation = makeString(df[header_designation][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			statut_ajustement = dao_statut_ajustement.toCreate(designation = designation, societe_id = societe_id)
			saved, statut_ajustement, message = dao_statut_ajustement.toSave(auteur, statut_ajustement)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_statut_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# STATUT_AJUSTEMENT API CONTROLLERS
def get_list_statut_ajustement(request):
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
		model = dao_statut_ajustement.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'designation' : str(item.designation),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_statut_ajustement(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_statut_ajustement.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'designation' : str(model.designation),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_statut_ajustement(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		designation = ''
		if 'designation' in request.POST : designation = str(request.POST['designation'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		statut_ajustement = dao_statut_ajustement.toCreate(designation = designation, societe_id = societe_id)
		saved, statut_ajustement, message = dao_statut_ajustement.toSave(auteur, statut_ajustement)

		if saved == False: raise Exception(message)

		objet = {
			'id' : statut_ajustement.id,
			'designation' : str(statut_ajustement.designation),
			'statut_id' : makeIntId(statut_ajustement.statut_id),
			'etat' : str(statut_ajustement.etat),
			'societe_id' : makeIntId(statut_ajustement.societe_id),
			'creation_date' : statut_ajustement.creation_date,
			'update_date' : statut_ajustement.update_date,
			'update_by_id' : makeIntId(statut_ajustement.update_by_id),
			'auteur_id' : makeIntId(statut_ajustement.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# REBUT CONTROLLERS
from ModuleStock.dao.dao_rebut import dao_rebut

def get_lister_rebut(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_rebut.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_rebut.toListJson(model.object_list),
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
			'title' : "Liste des rebuts",
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
		template = loader.get_template('ErpProject/ModuleStock/rebut/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_rebut(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		emplacement_origine = Model_Emplacement.objects.filter(defaut = True)
		emplacement_rebut = Model_Emplacement.objects.filter(id = 3, defaut = False)

		context = {
			'title' : "Formulaire d'enregistrement - Rebut",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Rebut(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id'),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:20],
			'emplacements_origine' : emplacement_origine,
			'emplacement_rebut':emplacement_rebut,
		}
		template = loader.get_template('ErpProject/ModuleStock/rebut/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_rebut'))

@transaction.atomic
def post_creer_rebut(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_rebut'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		numero = dao_rebut.toGenerateNumeroRebut()

		date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		is_formated, date = checkDateTimeFormat(date)
		if is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \'Date\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')

		article_id = makeIntId(request.POST['article_id'])

		serie_article = ""

		quantite = makeFloat(request.POST['quantite'])

		societe_id = makeIntId(request.POST['societe_id'])

		status_id = 3

		article = dao_article.toGet(article_id)
		unite_id = article.measure_unit.id

		emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		emplacement_rebut_id = makeIntId(request.POST['emplacement_rebut_id'])

		document = str(request.POST['document'])

		auteur = identite.utilisateur(request)

		rebut = dao_rebut.toCreate(numero = numero, date = date, article_id = article_id, serie_article = serie_article, quantite = quantite, societe_id = societe_id, status_id = status_id, unite_id = unite_id, emplacement_origine_id = emplacement_origine_id, emplacement_rebut_id = emplacement_rebut_id, document = document)
		saved, rebut, message = dao_rebut.toSave(auteur, rebut, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_rebut.toListById(rebut.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		emplacement = dao_emplacement.toGet(emplacement_origine_id)
		#Stockage de l'article
		stockage = Model_Stockage.objects.filter(article_id = article.id, emplacement_id = emplacement.id).first()
		print("   File: ModuleStock/views.py | Line: 4208 | post_creer_rebut ~ stockage",stockage)
		if stockage:
			if stockage.quantite < quantite :
				transaction.savepoint_rollback(sid)
				return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', msg = "La quantité saisie de l'article "+ article.name + " est supérieure au stock")

			qi = stockage.quantite
			stockage.quantite -= quantite
			stockage.save()

		else:
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', msg = "L'article "+ article.name + " est vide dans le stock")

		#On recherche le stockage de l'emplacement Rébis
		stockage_dest = Model_Stockage.objects.filter(article_id = article_id, emplacement_id = emplacement_rebut_id).first()
		print(" File: ModuleStock/views.py | Line: 13723 | post_creer_rebus ~ stockage_dest:::",stockage_dest)

		qi_dest = 0
		if stockage_dest:
			qi_dest = stockage_dest.quantite
			stockage_dest.quantite += quantite
			stockage_dest.save()
			print(f'stockage_destination cas 1  {stockage_dest}')
		else:
			qi_dest = 0
			stockage = Model_Stockage()
			stockage.emplacement_id = emplacement_rebut_id
			stockage.article_id = article_id
			stockage.quantite = quantite
			stockage.unite_id = unite_id
			stockage.societe_id = societe_id
			stockage.save()
			print(f'stockage_destination cas 2  {stockage}')


		#On enregistre le mouvement de stock
		mvt = Model_Mvt_stock()
		mvt.type_id = 3
		mvt.article_id = article.id
		mvt.emplacement_id = emplacement.id
		mvt.quantite_initiale = qi_dest
		mvt.unite_initiale_id = article.measure_unit.id
		mvt.quantite = quantite
		mvt.unite_id = article.measure_unit.id
		mvt.rebut_id = rebut.id
		mvt.auteur_id = auteur.id
		mvt.document = rebut.numero
		mvt.societe_id = societe_id
		mvt.save()
		print(f'::::Mouvement {mvt}')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, rebut)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : rebut.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_rebut(request,ref):
	try:
		same_perm_with = 'module_stock_list_rebut'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		rebut = dao_rebut.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(rebut.id),'obj': str(rebut)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_rebut', args=(rebut.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_rebut(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		rebut = auth.toGetWithRules(dao_rebut.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if rebut == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, rebut) 

		context = {
			'title' : "Détails - Rebut : {}".format(rebut),
			'model' : rebut,
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
		template = loader.get_template('ErpProject/ModuleStock/rebut/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_rebut'))

def get_modifier_rebut(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_rebut.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Rebut",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/rebut/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_rebut(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_rebut'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		numero = str(request.POST['numero'])

		date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		is_formated, date = checkDateTimeFormat(date)
		if is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \'Date\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')

		article_id = makeIntId(request.POST['article_id'])

		serie_article = str(request.POST['serie_article'])

		quantite = makeFloat(request.POST['quantite'])

		societe_id = makeIntId(request.POST['societe_id'])

		status_id = makeIntId(request.POST['status_id'])

		unite_id = makeIntId(request.POST['unite_id'])

		emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		emplacement_rebut_id = makeIntId(request.POST['emplacement_rebut_id'])

		document = str(request.POST['document'])
		auteur = identite.utilisateur(request)

		rebut = dao_rebut.toCreate(numero = numero, date = date, article_id = article_id, serie_article = serie_article, quantite = quantite, societe_id = societe_id, status_id = status_id, unite_id = unite_id, emplacement_origine_id = emplacement_origine_id, emplacement_rebut_id = emplacement_rebut_id, document = document)
		saved, rebut, message = dao_rebut.toUpdate(id, rebut, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_rebut.toListById(rebut.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : rebut.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_rebut(request,ref):
	try:
		same_perm_with = 'module_stock_add_rebut'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_rebut.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/rebut/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_rebut(request,ref):
	try:
		same_perm_with = 'module_stock_list_rebut'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		rebut = auth.toGetWithRules(dao_rebut.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if rebut == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Rebut : {}".format(rebut),
			'model' : rebut,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_rebut.html', 'print_rebut.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_rebut(request):
	try:
		same_perm_with = 'module_stock_add_rebut'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_rebut')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des rebuts",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/rebut/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_rebut(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_numero = makeString(request.POST['numero'])
		#print(f'header_numero_id: {header_numero_id}')

		header_date = makeString(request.POST['date'])
		if header_date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_date_id: {header_date_id}')

		header_article_id = makeString(request.POST['article_id'])
		#print(f'header_article_id: {header_article_id}')

		header_serie_article = makeString(request.POST['serie_article'])
		#print(f'header_serie_article_id: {header_serie_article_id}')

		header_quantite = makeString(request.POST['quantite'])
		#print(f'header_quantite_id: {header_quantite_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_status_id = makeString(request.POST['status_id'])
		#print(f'header_status_id: {header_status_id}')

		header_unite_id = makeString(request.POST['unite_id'])
		#print(f'header_unite_id: {header_unite_id}')

		header_emplacement_origine_id = makeString(request.POST['emplacement_origine_id'])
		#print(f'header_emplacement_origine_id: {header_emplacement_origine_id}')

		header_emplacement_rebut_id = makeString(request.POST['emplacement_rebut_id'])
		#print(f'header_emplacement_rebut_id: {header_emplacement_rebut_id}')

		header_document = makeString(request.POST['document'])
		#print(f'header_document_id: {header_document_id}')

		for i in df.index:

			numero = ''
			if header_numero != '': numero = makeString(df[header_numero][i])

			date = None
			if header_date != '': date = df[header_date][i]
			if date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')

			article_id = None
			if header_article_id != '': article_id = makeIntId(str(df[header_article_id][i]))

			serie_article = ''
			if header_serie_article != '': serie_article = makeString(df[header_serie_article][i])

			quantite = 0
			if header_quantite != '': quantite = makeFloat(df[header_quantite][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			status_id = None
			if header_status_id != '': status_id = makeIntId(str(df[header_status_id][i]))

			unite_id = None
			if header_unite_id != '': unite_id = makeIntId(str(df[header_unite_id][i]))

			emplacement_origine_id = None
			if header_emplacement_origine_id != '': emplacement_origine_id = makeIntId(str(df[header_emplacement_origine_id][i]))

			emplacement_rebut_id = None
			if header_emplacement_rebut_id != '': emplacement_rebut_id = makeIntId(str(df[header_emplacement_rebut_id][i]))

			document = ''
			if header_document != '': document = makeString(df[header_document][i])

			rebut = dao_rebut.toCreate(numero = numero, date = date, article_id = article_id, serie_article = serie_article, quantite = quantite, societe_id = societe_id, status_id = status_id, unite_id = unite_id, emplacement_origine_id = emplacement_origine_id, emplacement_rebut_id = emplacement_rebut_id, document = document)
			saved, rebut, message = dao_rebut.toSave(auteur, rebut)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_rebut'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# REBUT BI CONTROLLERS
def get_bi_rebut(request):
	try:
		same_perm_with = 'module_stock_get_generer_rebut'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		try:
			view = str(request.GET.get('view','table'))
		except Exception as e:
			view = 'table'

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_rebut.toList(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model, 100)

		model_content_type = dao_query_builder.toGetContentTypeByName('model_rebut')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)
		champs_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)
		champs_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)
		champs_date = dao_query_builder.toListFieldsDate(model_content_type.id)

		context = {
			'title' : "Analyse des rebuts",
			'model' : model,
			'model_id' : model_content_type.id,
			'modele' : Model_Rebut(),
			'champs' : champs,
			'champs_nombre' : champs_nombre,
			'champs_date' : champs_date,
			'champs_dimension' : champs_texte,
			'view' : view,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleStock/rebut/bi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

# REBUT API CONTROLLERS
def get_list_rebut(request):
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
		model = dao_rebut.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'numero' : str(item.numero),
				'date' : item.date,
				'article_id' : makeIntId(item.article_id),
				'serie_article' : str(item.serie_article),
				'quantite' : makeFloat(item.quantite),
				'societe_id' : makeIntId(item.societe_id),
				'status_id' : makeIntId(item.status_id),
				'unite_id' : makeIntId(item.unite_id),
				'emplacement_origine_id' : makeIntId(item.emplacement_origine_id),
				'emplacement_rebut_id' : makeIntId(item.emplacement_rebut_id),
				'document' : str(item.document),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_rebut(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_rebut.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'numero' : str(model.numero),
				'date' : model.date,
				'article_id' : makeIntId(model.article_id),
				'serie_article' : str(model.serie_article),
				'quantite' : makeFloat(model.quantite),
				'societe_id' : makeIntId(model.societe_id),
				'status_id' : makeIntId(model.status_id),
				'unite_id' : makeIntId(model.unite_id),
				'emplacement_origine_id' : makeIntId(model.emplacement_origine_id),
				'emplacement_rebut_id' : makeIntId(model.emplacement_rebut_id),
				'document' : str(model.document),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_rebut(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		numero = ''
		if 'numero' in request.POST : numero = str(request.POST['numero'])

		date = ''
		if 'date' in request.POST : date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		date = timezone.datetime(int(date[6:10]), int(date[3:5]), int(date[0:2]), int(date[11:13]), int(date[14:16]))

		article_id = None
		if 'article' in request.POST : article_id = makeIntId(request.POST['article_id'])

		serie_article = ''
		if 'serie_article' in request.POST : serie_article = str(request.POST['serie_article'])

		quantite = 0.0
		if 'quantite' in request.POST : quantite = makeFloat(request.POST['quantite'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		status_id = None
		if 'status' in request.POST : status_id = makeIntId(request.POST['status_id'])

		unite_id = None
		if 'unite' in request.POST : unite_id = makeIntId(request.POST['unite_id'])

		emplacement_origine_id = None
		if 'emplacement_origine' in request.POST : emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		emplacement_rebut_id = None
		if 'emplacement_rebut' in request.POST : emplacement_rebut_id = makeIntId(request.POST['emplacement_rebut_id'])

		document = ''
		if 'document' in request.POST : document = str(request.POST['document'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		rebut = dao_rebut.toCreate(numero = numero, date = date, article_id = article_id, serie_article = serie_article, quantite = quantite, societe_id = societe_id, status_id = status_id, unite_id = unite_id, emplacement_origine_id = emplacement_origine_id, emplacement_rebut_id = emplacement_rebut_id, document = document)
		saved, rebut, message = dao_rebut.toSave(auteur, rebut)

		if saved == False: raise Exception(message)

		objet = {
			'id' : rebut.id,
			'numero' : str(rebut.numero),
			'date' : rebut.date,
			'article_id' : makeIntId(rebut.article_id),
			'serie_article' : str(rebut.serie_article),
			'quantite' : makeFloat(rebut.quantite),
			'societe_id' : makeIntId(rebut.societe_id),
			'status_id' : makeIntId(rebut.status_id),
			'unite_id' : makeIntId(rebut.unite_id),
			'emplacement_origine_id' : makeIntId(rebut.emplacement_origine_id),
			'emplacement_rebut_id' : makeIntId(rebut.emplacement_rebut_id),
			'document' : str(rebut.document),
			'statut_id' : makeIntId(rebut.statut_id),
			'etat' : str(rebut.etat),
			'creation_date' : rebut.creation_date,
			'update_date' : rebut.update_date,
			'update_by_id' : makeIntId(rebut.update_by_id),
			'auteur_id' : makeIntId(rebut.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# OPERATION_STOCK CONTROLLERS
from ModuleStock.dao.dao_operation_stock import dao_operation_stock

def get_lister_operation_stock(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_operation_stock.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_operation_stock.toListJson(model.object_list),
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
			'title' : "Liste des opérations stock",
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
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_operation_stock(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Opération stock",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Operation_stock(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_operation_stock'))

@transaction.atomic
def post_creer_operation_stock(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		operation_stock = dao_operation_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, operation_stock, message = dao_operation_stock.toSave(auteur, operation_stock, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_operation_stock.toListById(operation_stock.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, operation_stock)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : operation_stock.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_operation_stock(request,ref):
	try:
		same_perm_with = 'module_stock_list_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		operation_stock = dao_operation_stock.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(operation_stock.id),'obj': str(operation_stock)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_operation_stock', args=(operation_stock.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_operation_stock(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		operation_stock = auth.toGetWithRules(dao_operation_stock.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if operation_stock == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, operation_stock) 

		context = {
			'title' : "Détails - Opération stock : {}".format(operation_stock),
			'model' : operation_stock,
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
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_operation_stock'))

def get_modifier_operation_stock(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_operation_stock.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Opération stock",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_operation_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		operation_stock = dao_operation_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, operation_stock, message = dao_operation_stock.toUpdate(id, operation_stock, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_operation_stock.toListById(operation_stock.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : operation_stock.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_operation_stock(request,ref):
	try:
		same_perm_with = 'module_stock_add_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_operation_stock.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_operation_stock(request,ref):
	try:
		same_perm_with = 'module_stock_list_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		operation_stock = auth.toGetWithRules(dao_operation_stock.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if operation_stock == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Opération stock : {}".format(operation_stock),
			'model' : operation_stock,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_operation_stock.html', 'print_operation_stock.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_operation_stock(request):
	try:
		same_perm_with = 'module_stock_add_operation_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_operation_stock')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des opérations stock",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_operation_stock(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_designation = makeString(request.POST['designation'])
		#print(f'header_designation_id: {header_designation_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			designation = ''
			if header_designation != '': designation = makeString(df[header_designation][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			operation_stock = dao_operation_stock.toCreate(designation = designation, societe_id = societe_id)
			saved, operation_stock, message = dao_operation_stock.toSave(auteur, operation_stock)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# OPERATION_STOCK API CONTROLLERS
def get_list_operation_stock(request):
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
		model = dao_operation_stock.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'designation' : str(item.designation),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_operation_stock(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_operation_stock.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'designation' : str(model.designation),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_operation_stock(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		designation = ''
		if 'designation' in request.POST : designation = str(request.POST['designation'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		operation_stock = dao_operation_stock.toCreate(designation = designation, societe_id = societe_id)
		saved, operation_stock, message = dao_operation_stock.toSave(auteur, operation_stock)

		if saved == False: raise Exception(message)

		objet = {
			'id' : operation_stock.id,
			'designation' : str(operation_stock.designation),
			'statut_id' : makeIntId(operation_stock.statut_id),
			'etat' : str(operation_stock.etat),
			'societe_id' : makeIntId(operation_stock.societe_id),
			'creation_date' : operation_stock.creation_date,
			'update_date' : operation_stock.update_date,
			'update_by_id' : makeIntId(operation_stock.update_by_id),
			'auteur_id' : makeIntId(operation_stock.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# MVT_STOCK CONTROLLERS
from ModuleStock.dao.dao_mvt_stock import dao_mvt_stock

def get_lister_mvt_stock(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_mvt_stock.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_mvt_stock.toListJson(model.object_list),
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
			'title' : "Liste des mouvements stocks",
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
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_mvt_stock(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Mouvement stock",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Mvt_stock(),
			'type_mvt_stocks' : Model_Type_mvt_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_receptions' : Model_Bon_reception.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_transferts' : Model_Bon_transfert.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_sorties' : Model_Bon_sortie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_retours' : Model_Bon_retour.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'ajustements' : Model_Ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'rebuts' : Model_Rebut.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_mvt_stock'))

@transaction.atomic
def post_creer_mvt_stock(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		is_formated, date = checkDateTimeFormat(date)
		if is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \'Date\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')

		type_id = makeIntId(request.POST['type_id'])
		if type_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Type mouvement\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		reception_id = makeIntId(request.POST['reception_id'])

		transfert_id = makeIntId(request.POST['transfert_id'])

		sortie_id = makeIntId(request.POST['sortie_id'])

		retour_id = makeIntId(request.POST['retour_id'])

		ajustement_id = makeIntId(request.POST['ajustement_id'])

		rebut_id = makeIntId(request.POST['rebut_id'])

		quantite_initiale = makeFloat(request.POST['quantite_initiale'])

		unite_initiale_id = makeIntId(request.POST['unite_initiale_id'])

		quantite = makeFloat(request.POST['quantite'])

		societe_id = makeIntId(request.POST['societe_id'])

		unite_id = makeIntId(request.POST['unite_id'])

		est_rebut = True if 'est_rebut' in request.POST else False

		series = request.POST.getlist('series', None)

		auteur = identite.utilisateur(request)

		mvt_stock = dao_mvt_stock.toCreate(date = date, type_id = type_id, article_id = article_id, emplacement_id = emplacement_id, reception_id = reception_id, transfert_id = transfert_id, sortie_id = sortie_id, retour_id = retour_id, ajustement_id = ajustement_id, rebut_id = rebut_id, quantite_initiale = quantite_initiale, unite_initiale_id = unite_initiale_id, quantite = quantite, societe_id = societe_id, unite_id = unite_id, est_rebut = est_rebut, series = series)
		saved, mvt_stock, message = dao_mvt_stock.toSave(auteur, mvt_stock, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_mvt_stock.toListById(mvt_stock.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, mvt_stock)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : mvt_stock.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_mvt_stock(request,ref):
	try:
		same_perm_with = 'module_stock_list_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		mvt_stock = dao_mvt_stock.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(mvt_stock.id),'obj': str(mvt_stock)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_mvt_stock', args=(mvt_stock.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_mvt_stock(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		mvt_stock = auth.toGetWithRules(dao_mvt_stock.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if mvt_stock == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, mvt_stock) 

		context = {
			'title' : "Détails - Mouvement stock : {}".format(mvt_stock),
			'model' : mvt_stock,
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
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_mvt_stock'))

def get_modifier_mvt_stock(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_mvt_stock.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Mouvement stock",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'type_mvt_stocks' : Model_Type_mvt_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_receptions' : Model_Bon_reception.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_transferts' : Model_Bon_transfert.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_sorties' : Model_Bon_sortie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_retours' : Model_Bon_retour.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'ajustements' : Model_Ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'rebuts' : Model_Rebut.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_mvt_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		is_formated, date = checkDateTimeFormat(date)
		if is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \'Date\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')

		type_id = makeIntId(request.POST['type_id'])
		if type_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Type mouvement\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		reception_id = makeIntId(request.POST['reception_id'])

		transfert_id = makeIntId(request.POST['transfert_id'])

		sortie_id = makeIntId(request.POST['sortie_id'])

		retour_id = makeIntId(request.POST['retour_id'])

		ajustement_id = makeIntId(request.POST['ajustement_id'])

		rebut_id = makeIntId(request.POST['rebut_id'])

		quantite_initiale = makeFloat(request.POST['quantite_initiale'])

		unite_initiale_id = makeIntId(request.POST['unite_initiale_id'])

		quantite = makeFloat(request.POST['quantite'])

		societe_id = makeIntId(request.POST['societe_id'])

		unite_id = makeIntId(request.POST['unite_id'])

		est_rebut = True if 'est_rebut' in request.POST else False

		series = request.POST.getlist('series', None)
		auteur = identite.utilisateur(request)

		mvt_stock = dao_mvt_stock.toCreate(date = date, type_id = type_id, article_id = article_id, emplacement_id = emplacement_id, reception_id = reception_id, transfert_id = transfert_id, sortie_id = sortie_id, retour_id = retour_id, ajustement_id = ajustement_id, rebut_id = rebut_id, quantite_initiale = quantite_initiale, unite_initiale_id = unite_initiale_id, quantite = quantite, societe_id = societe_id, unite_id = unite_id, est_rebut = est_rebut, series = series)
		saved, mvt_stock, message = dao_mvt_stock.toUpdate(id, mvt_stock, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_mvt_stock.toListById(mvt_stock.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : mvt_stock.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_mvt_stock(request,ref):
	try:
		same_perm_with = 'module_stock_add_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_mvt_stock.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'type_mvt_stocks' : Model_Type_mvt_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_receptions' : Model_Bon_reception.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_transferts' : Model_Bon_transfert.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_sorties' : Model_Bon_sortie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_retours' : Model_Bon_retour.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'ajustements' : Model_Ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'rebuts' : Model_Rebut.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_mvt_stock(request,ref):
	try:
		same_perm_with = 'module_stock_list_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		mvt_stock = auth.toGetWithRules(dao_mvt_stock.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if mvt_stock == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Mouvement stock : {}".format(mvt_stock),
			'model' : mvt_stock,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_mvt_stock.html', 'print_mvt_stock.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_mvt_stock(request):
	try:
		same_perm_with = 'module_stock_add_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_mvt_stock')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des mouvements stocks",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_mvt_stock(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_date = makeString(request.POST['date'])
		if header_date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_date_id: {header_date_id}')

		header_type_id = makeString(request.POST['type_id'])
		if header_type_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Type mouvement\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_type_id: {header_type_id}')

		header_article_id = makeString(request.POST['article_id'])
		if header_article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_article_id: {header_article_id}')

		header_emplacement_id = makeString(request.POST['emplacement_id'])
		if header_emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_emplacement_id: {header_emplacement_id}')

		header_reception_id = makeString(request.POST['reception_id'])
		#print(f'header_reception_id: {header_reception_id}')

		header_transfert_id = makeString(request.POST['transfert_id'])
		#print(f'header_transfert_id: {header_transfert_id}')

		header_sortie_id = makeString(request.POST['sortie_id'])
		#print(f'header_sortie_id: {header_sortie_id}')

		header_retour_id = makeString(request.POST['retour_id'])
		#print(f'header_retour_id: {header_retour_id}')

		header_ajustement_id = makeString(request.POST['ajustement_id'])
		#print(f'header_ajustement_id: {header_ajustement_id}')

		header_rebut_id = makeString(request.POST['rebut_id'])
		#print(f'header_rebut_id: {header_rebut_id}')

		header_quantite_initiale = makeString(request.POST['quantite_initiale'])
		#print(f'header_quantite_initiale_id: {header_quantite_initiale_id}')

		header_unite_initiale_id = makeString(request.POST['unite_initiale_id'])
		#print(f'header_unite_initiale_id: {header_unite_initiale_id}')

		header_quantite = makeString(request.POST['quantite'])
		#print(f'header_quantite_id: {header_quantite_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_unite_id = makeString(request.POST['unite_id'])
		#print(f'header_unite_id: {header_unite_id}')

		header_est_rebut = makeString(request.POST['est_rebut'])
		#print(f'header_est_rebut_id: {header_est_rebut_id}')

		for i in df.index:

			date = None
			if header_date != '': date = df[header_date][i]
			if date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')

			type_id = None
			if header_type_id != '': type_id = makeIntId(str(df[header_type_id][i]))
			if type_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Type mouvement\' est obligatoire, Veuillez le renseigner SVP!')

			article_id = None
			if header_article_id != '': article_id = makeIntId(str(df[header_article_id][i]))
			if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

			emplacement_id = None
			if header_emplacement_id != '': emplacement_id = makeIntId(str(df[header_emplacement_id][i]))
			if emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

			reception_id = None
			if header_reception_id != '': reception_id = makeIntId(str(df[header_reception_id][i]))

			transfert_id = None
			if header_transfert_id != '': transfert_id = makeIntId(str(df[header_transfert_id][i]))

			sortie_id = None
			if header_sortie_id != '': sortie_id = makeIntId(str(df[header_sortie_id][i]))

			retour_id = None
			if header_retour_id != '': retour_id = makeIntId(str(df[header_retour_id][i]))

			ajustement_id = None
			if header_ajustement_id != '': ajustement_id = makeIntId(str(df[header_ajustement_id][i]))

			rebut_id = None
			if header_rebut_id != '': rebut_id = makeIntId(str(df[header_rebut_id][i]))

			quantite_initiale = 0
			if header_quantite_initiale != '': quantite_initiale = makeFloat(df[header_quantite_initiale][i])

			unite_initiale_id = None
			if header_unite_initiale_id != '': unite_initiale_id = makeIntId(str(df[header_unite_initiale_id][i]))

			quantite = 0
			if header_quantite != '': quantite = makeFloat(df[header_quantite][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			unite_id = None
			if header_unite_id != '': unite_id = makeIntId(str(df[header_unite_id][i]))

			est_rebut = False
			if header_est_rebut != '': est_rebut = True if makeString(df[header_est_rebut][i]) == 'True' else False

			mvt_stock = dao_mvt_stock.toCreate(date = date, type_id = type_id, article_id = article_id, emplacement_id = emplacement_id, reception_id = reception_id, transfert_id = transfert_id, sortie_id = sortie_id, retour_id = retour_id, ajustement_id = ajustement_id, rebut_id = rebut_id, quantite_initiale = quantite_initiale, unite_initiale_id = unite_initiale_id, quantite = quantite, societe_id = societe_id, unite_id = unite_id, est_rebut = est_rebut)
			saved, mvt_stock, message = dao_mvt_stock.toSave(auteur, mvt_stock)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_mvt_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# MVT_STOCK BI CONTROLLERS
def get_bi_mvt_stock(request):
	try:
		same_perm_with = 'module_stock_get_generer_mvt_stock'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		try:
			view = str(request.GET.get('view','table'))
		except Exception as e:
			view = 'table'

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_mvt_stock.toList(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model, 100)

		model_content_type = dao_query_builder.toGetContentTypeByName('model_mvt_stock')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)
		champs_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)
		champs_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)
		champs_date = dao_query_builder.toListFieldsDate(model_content_type.id)

		context = {
			'title' : "Analyse des mouvements stocks",
			'model' : model,
			'model_id' : model_content_type.id,
			'modele' : Model_Mvt_stock(),
			'champs' : champs,
			'champs_nombre' : champs_nombre,
			'champs_date' : champs_date,
			'champs_dimension' : champs_texte,
			'view' : view,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/bi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

# MVT_STOCK API CONTROLLERS
def get_list_mvt_stock(request):
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
		model = dao_mvt_stock.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'date' : item.date,
				'type_id' : makeIntId(item.type_id),
				'article_id' : makeIntId(item.article_id),
				'emplacement_id' : makeIntId(item.emplacement_id),
				'reception_id' : makeIntId(item.reception_id),
				'transfert_id' : makeIntId(item.transfert_id),
				'sortie_id' : makeIntId(item.sortie_id),
				'retour_id' : makeIntId(item.retour_id),
				'ajustement_id' : makeIntId(item.ajustement_id),
				'rebut_id' : makeIntId(item.rebut_id),
				'quantite_initiale' : makeFloat(item.quantite_initiale),
				'unite_initiale_id' : makeIntId(item.unite_initiale_id),
				'quantite' : makeFloat(item.quantite),
				'societe_id' : makeIntId(item.societe_id),
				'unite_id' : makeIntId(item.unite_id),
				'est_rebut' : item.est_rebut,
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_mvt_stock(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_mvt_stock.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'date' : model.date,
				'type_id' : makeIntId(model.type_id),
				'article_id' : makeIntId(model.article_id),
				'emplacement_id' : makeIntId(model.emplacement_id),
				'reception_id' : makeIntId(model.reception_id),
				'transfert_id' : makeIntId(model.transfert_id),
				'sortie_id' : makeIntId(model.sortie_id),
				'retour_id' : makeIntId(model.retour_id),
				'ajustement_id' : makeIntId(model.ajustement_id),
				'rebut_id' : makeIntId(model.rebut_id),
				'quantite_initiale' : makeFloat(model.quantite_initiale),
				'unite_initiale_id' : makeIntId(model.unite_initiale_id),
				'quantite' : makeFloat(model.quantite),
				'societe_id' : makeIntId(model.societe_id),
				'unite_id' : makeIntId(model.unite_id),
				'est_rebut' : model.est_rebut,
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_mvt_stock(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		date = ''
		if 'date' in request.POST : date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		date = timezone.datetime(int(date[6:10]), int(date[3:5]), int(date[0:2]), int(date[11:13]), int(date[14:16]))

		type_id = None
		if 'type' in request.POST : type_id = makeIntId(request.POST['type_id'])
		if type_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Type mouvement\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = None
		if 'article' in request.POST : article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		emplacement_id = None
		if 'emplacement' in request.POST : emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		reception_id = None
		if 'reception' in request.POST : reception_id = makeIntId(request.POST['reception_id'])

		transfert_id = None
		if 'transfert' in request.POST : transfert_id = makeIntId(request.POST['transfert_id'])

		sortie_id = None
		if 'sortie' in request.POST : sortie_id = makeIntId(request.POST['sortie_id'])

		retour_id = None
		if 'retour' in request.POST : retour_id = makeIntId(request.POST['retour_id'])

		ajustement_id = None
		if 'ajustement' in request.POST : ajustement_id = makeIntId(request.POST['ajustement_id'])

		rebut_id = None
		if 'rebut' in request.POST : rebut_id = makeIntId(request.POST['rebut_id'])

		quantite_initiale = 0.0
		if 'quantite_initiale' in request.POST : quantite_initiale = makeFloat(request.POST['quantite_initiale'])

		unite_initiale_id = None
		if 'unite_initiale' in request.POST : unite_initiale_id = makeIntId(request.POST['unite_initiale_id'])

		quantite = 0.0
		if 'quantite' in request.POST : quantite = makeFloat(request.POST['quantite'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		unite_id = None
		if 'unite' in request.POST : unite_id = makeIntId(request.POST['unite_id'])

		est_rebut = True if 'est_rebut' in request.POST else False

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		series = []

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		mvt_stock = dao_mvt_stock.toCreate(date = date, type_id = type_id, article_id = article_id, emplacement_id = emplacement_id, reception_id = reception_id, transfert_id = transfert_id, sortie_id = sortie_id, retour_id = retour_id, ajustement_id = ajustement_id, rebut_id = rebut_id, quantite_initiale = quantite_initiale, unite_initiale_id = unite_initiale_id, quantite = quantite, societe_id = societe_id, unite_id = unite_id, est_rebut = est_rebut, series = series)
		saved, mvt_stock, message = dao_mvt_stock.toSave(auteur, mvt_stock)

		if saved == False: raise Exception(message)

		objet = {
			'id' : mvt_stock.id,
			'date' : mvt_stock.date,
			'type_id' : makeIntId(mvt_stock.type_id),
			'article_id' : makeIntId(mvt_stock.article_id),
			'emplacement_id' : makeIntId(mvt_stock.emplacement_id),
			'reception_id' : makeIntId(mvt_stock.reception_id),
			'transfert_id' : makeIntId(mvt_stock.transfert_id),
			'sortie_id' : makeIntId(mvt_stock.sortie_id),
			'retour_id' : makeIntId(mvt_stock.retour_id),
			'ajustement_id' : makeIntId(mvt_stock.ajustement_id),
			'rebut_id' : makeIntId(mvt_stock.rebut_id),
			'quantite_initiale' : makeFloat(mvt_stock.quantite_initiale),
			'unite_initiale_id' : makeIntId(mvt_stock.unite_initiale_id),
			'quantite' : makeFloat(mvt_stock.quantite),
			'societe_id' : makeIntId(mvt_stock.societe_id),
			'unite_id' : makeIntId(mvt_stock.unite_id),
			'est_rebut' : mvt_stock.est_rebut,
			'statut_id' : makeIntId(mvt_stock.statut_id),
			'etat' : str(mvt_stock.etat),
			'creation_date' : mvt_stock.creation_date,
			'update_date' : mvt_stock.update_date,
			'update_by_id' : makeIntId(mvt_stock.update_by_id),
			'auteur_id' : makeIntId(mvt_stock.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# LIGNE_RECEPTION CONTROLLERS
from ModuleStock.dao.dao_ligne_reception import dao_ligne_reception

def get_lister_ligne_reception(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_ligne_reception.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_ligne_reception.toListJson(model.object_list),
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
			'title' : "Liste des lines bons de receptions",
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
		template = loader.get_template('ErpProject/ModuleStock/ligne_reception/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_ligne_reception(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Line Bon de Reception",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Ligne_reception(),
			'bon_receptions' : Model_Bon_reception.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'devises' : Model_Devise.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_reception/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ligne_reception'))

@transaction.atomic
def post_creer_ligne_reception(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_ligne_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		bon_reception_id = makeIntId(request.POST['bon_reception_id'])
		if bon_reception_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Opération stock\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		societe_id = makeIntId(request.POST['societe_id'])

		quantite_demandee = makeFloat(request.POST['quantite_demandee'])

		quantite_fait = makeFloat(request.POST['quantite_fait'])

		quantite_reste = makeFloat(request.POST['quantite_reste'])

		prix_unitaire = makeFloat(request.POST['prix_unitaire'])

		unite_id = makeIntId(request.POST['unite_id'])

		devise_id = makeIntId(request.POST['devise_id'])

		description = str(request.POST['description'])

		fait = True if 'fait' in request.POST else False

		series = request.POST.getlist('series', None)

		auteur = identite.utilisateur(request)

		ligne_reception = dao_ligne_reception.toCreate(bon_reception_id = bon_reception_id, article_id = article_id, societe_id = societe_id, quantite_demandee = quantite_demandee, quantite_fait = quantite_fait, quantite_reste = quantite_reste, prix_unitaire = prix_unitaire, unite_id = unite_id, devise_id = devise_id, description = description, fait = fait, series = series)
		saved, ligne_reception, message = dao_ligne_reception.toSave(auteur, ligne_reception, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ligne_reception.toListById(ligne_reception.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, ligne_reception)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : ligne_reception.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_ligne_reception(request,ref):
	try:
		same_perm_with = 'module_stock_list_ligne_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ligne_reception = dao_ligne_reception.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(ligne_reception.id),'obj': str(ligne_reception)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_ligne_reception', args=(ligne_reception.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_ligne_reception(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ligne_reception = auth.toGetWithRules(dao_ligne_reception.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ligne_reception == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, ligne_reception) 

		context = {
			'title' : "Détails - Line Bon de Reception : {}".format(ligne_reception),
			'model' : ligne_reception,
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
		template = loader.get_template('ErpProject/ModuleStock/ligne_reception/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ligne_reception'))

def get_modifier_ligne_reception(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_ligne_reception.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Line Bon de Reception",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'bon_receptions' : Model_Bon_reception.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'devises' : Model_Devise.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_reception/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_ligne_reception(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_ligne_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		bon_reception_id = makeIntId(request.POST['bon_reception_id'])
		if bon_reception_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Opération stock\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		societe_id = makeIntId(request.POST['societe_id'])

		quantite_demandee = makeFloat(request.POST['quantite_demandee'])

		quantite_fait = makeFloat(request.POST['quantite_fait'])

		quantite_reste = makeFloat(request.POST['quantite_reste'])

		prix_unitaire = makeFloat(request.POST['prix_unitaire'])

		unite_id = makeIntId(request.POST['unite_id'])

		devise_id = makeIntId(request.POST['devise_id'])

		description = str(request.POST['description'])

		fait = True if 'fait' in request.POST else False

		series = request.POST.getlist('series', None)
		auteur = identite.utilisateur(request)

		ligne_reception = dao_ligne_reception.toCreate(bon_reception_id = bon_reception_id, article_id = article_id, societe_id = societe_id, quantite_demandee = quantite_demandee, quantite_fait = quantite_fait, quantite_reste = quantite_reste, prix_unitaire = prix_unitaire, unite_id = unite_id, devise_id = devise_id, description = description, fait = fait, series = series)
		saved, ligne_reception, message = dao_ligne_reception.toUpdate(id, ligne_reception, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ligne_reception.toListById(ligne_reception.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : ligne_reception.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_ligne_reception(request,ref):
	try:
		same_perm_with = 'module_stock_add_ligne_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_ligne_reception.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'bon_receptions' : Model_Bon_reception.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'devises' : Model_Devise.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_reception/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_ligne_reception(request,ref):
	try:
		same_perm_with = 'module_stock_list_ligne_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ligne_reception = auth.toGetWithRules(dao_ligne_reception.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ligne_reception == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Line Bon de Reception : {}".format(ligne_reception),
			'model' : ligne_reception,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_ligne_reception.html', 'print_ligne_reception.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_ligne_reception(request):
	try:
		same_perm_with = 'module_stock_add_ligne_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_ligne_reception')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des lines bons de receptions",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_reception/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_ligne_reception(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_bon_reception_id = makeString(request.POST['bon_reception_id'])
		if header_bon_reception_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Opération stock\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_bon_reception_id: {header_bon_reception_id}')

		header_article_id = makeString(request.POST['article_id'])
		if header_article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_article_id: {header_article_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_quantite_demandee = makeString(request.POST['quantite_demandee'])
		#print(f'header_quantite_demandee_id: {header_quantite_demandee_id}')

		header_quantite_fait = makeString(request.POST['quantite_fait'])
		#print(f'header_quantite_fait_id: {header_quantite_fait_id}')

		header_quantite_reste = makeString(request.POST['quantite_reste'])
		#print(f'header_quantite_reste_id: {header_quantite_reste_id}')

		header_prix_unitaire = makeString(request.POST['prix_unitaire'])
		#print(f'header_prix_unitaire_id: {header_prix_unitaire_id}')

		header_unite_id = makeString(request.POST['unite_id'])
		#print(f'header_unite_id: {header_unite_id}')

		header_devise_id = makeString(request.POST['devise_id'])
		#print(f'header_devise_id: {header_devise_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_fait = makeString(request.POST['fait'])
		#print(f'header_fait_id: {header_fait_id}')

		for i in df.index:

			bon_reception_id = None
			if header_bon_reception_id != '': bon_reception_id = makeIntId(str(df[header_bon_reception_id][i]))
			if bon_reception_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Opération stock\' est obligatoire, Veuillez le renseigner SVP!')

			article_id = None
			if header_article_id != '': article_id = makeIntId(str(df[header_article_id][i]))
			if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			quantite_demandee = 0
			if header_quantite_demandee != '': quantite_demandee = makeFloat(df[header_quantite_demandee][i])

			quantite_fait = 0
			if header_quantite_fait != '': quantite_fait = makeFloat(df[header_quantite_fait][i])

			quantite_reste = 0
			if header_quantite_reste != '': quantite_reste = makeFloat(df[header_quantite_reste][i])

			prix_unitaire = 0
			if header_prix_unitaire != '': prix_unitaire = makeFloat(df[header_prix_unitaire][i])

			unite_id = None
			if header_unite_id != '': unite_id = makeIntId(str(df[header_unite_id][i]))

			devise_id = None
			if header_devise_id != '': devise_id = makeIntId(str(df[header_devise_id][i]))

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			fait = False
			if header_fait != '': fait = True if makeString(df[header_fait][i]) == 'True' else False

			ligne_reception = dao_ligne_reception.toCreate(bon_reception_id = bon_reception_id, article_id = article_id, societe_id = societe_id, quantite_demandee = quantite_demandee, quantite_fait = quantite_fait, quantite_reste = quantite_reste, prix_unitaire = prix_unitaire, unite_id = unite_id, devise_id = devise_id, description = description, fait = fait)
			saved, ligne_reception, message = dao_ligne_reception.toSave(auteur, ligne_reception)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_ligne_reception'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# LIGNE_RECEPTION API CONTROLLERS
def get_list_ligne_reception(request):
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
		model = dao_ligne_reception.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'bon_reception_id' : makeIntId(item.bon_reception_id),
				'article_id' : makeIntId(item.article_id),
				'societe_id' : makeIntId(item.societe_id),
				'quantite_demandee' : makeFloat(item.quantite_demandee),
				'quantite_fait' : makeFloat(item.quantite_fait),
				'quantite_reste' : makeFloat(item.quantite_reste),
				'prix_unitaire' : makeFloat(item.prix_unitaire),
				'unite_id' : makeIntId(item.unite_id),
				'devise_id' : makeIntId(item.devise_id),
				'description' : str(item.description),
				'fait' : item.fait,
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_ligne_reception(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_ligne_reception.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'bon_reception_id' : makeIntId(model.bon_reception_id),
				'article_id' : makeIntId(model.article_id),
				'societe_id' : makeIntId(model.societe_id),
				'quantite_demandee' : makeFloat(model.quantite_demandee),
				'quantite_fait' : makeFloat(model.quantite_fait),
				'quantite_reste' : makeFloat(model.quantite_reste),
				'prix_unitaire' : makeFloat(model.prix_unitaire),
				'unite_id' : makeIntId(model.unite_id),
				'devise_id' : makeIntId(model.devise_id),
				'description' : str(model.description),
				'fait' : model.fait,
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_ligne_reception(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		bon_reception_id = None
		if 'bon_reception' in request.POST : bon_reception_id = makeIntId(request.POST['bon_reception_id'])
		if bon_reception_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Opération stock\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = None
		if 'article' in request.POST : article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		quantite_demandee = 0.0
		if 'quantite_demandee' in request.POST : quantite_demandee = makeFloat(request.POST['quantite_demandee'])

		quantite_fait = 0.0
		if 'quantite_fait' in request.POST : quantite_fait = makeFloat(request.POST['quantite_fait'])

		quantite_reste = 0.0
		if 'quantite_reste' in request.POST : quantite_reste = makeFloat(request.POST['quantite_reste'])

		prix_unitaire = 0.0
		if 'prix_unitaire' in request.POST : prix_unitaire = makeFloat(request.POST['prix_unitaire'])

		unite_id = None
		if 'unite' in request.POST : unite_id = makeIntId(request.POST['unite_id'])

		devise_id = None
		if 'devise' in request.POST : devise_id = makeIntId(request.POST['devise_id'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		fait = True if 'fait' in request.POST else False

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		series = []

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		ligne_reception = dao_ligne_reception.toCreate(bon_reception_id = bon_reception_id, article_id = article_id, societe_id = societe_id, quantite_demandee = quantite_demandee, quantite_fait = quantite_fait, quantite_reste = quantite_reste, prix_unitaire = prix_unitaire, unite_id = unite_id, devise_id = devise_id, description = description, fait = fait, series = series)
		saved, ligne_reception, message = dao_ligne_reception.toSave(auteur, ligne_reception)

		if saved == False: raise Exception(message)

		objet = {
			'id' : ligne_reception.id,
			'bon_reception_id' : makeIntId(ligne_reception.bon_reception_id),
			'article_id' : makeIntId(ligne_reception.article_id),
			'societe_id' : makeIntId(ligne_reception.societe_id),
			'quantite_demandee' : makeFloat(ligne_reception.quantite_demandee),
			'quantite_fait' : makeFloat(ligne_reception.quantite_fait),
			'quantite_reste' : makeFloat(ligne_reception.quantite_reste),
			'prix_unitaire' : makeFloat(ligne_reception.prix_unitaire),
			'unite_id' : makeIntId(ligne_reception.unite_id),
			'devise_id' : makeIntId(ligne_reception.devise_id),
			'description' : str(ligne_reception.description),
			'fait' : ligne_reception.fait,
			'statut_id' : makeIntId(ligne_reception.statut_id),
			'etat' : str(ligne_reception.etat),
			'creation_date' : ligne_reception.creation_date,
			'update_date' : ligne_reception.update_date,
			'update_by_id' : makeIntId(ligne_reception.update_by_id),
			'auteur_id' : makeIntId(ligne_reception.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# LIGNE_BON_TRANSFERT CONTROLLERS
from ModuleStock.dao.dao_ligne_bon_transfert import dao_ligne_bon_transfert

def get_lister_ligne_bon_transfert(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_ligne_bon_transfert.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_ligne_bon_transfert.toListJson(model.object_list),
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
			'title' : "Liste des lines bons de transferts",
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
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_transfert/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_ligne_bon_transfert(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Line bon de Transfert",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Ligne_bon_transfert(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_transferts' : Model_Bon_transfert.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'stockages' : Model_Stockage.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_transfert/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ligne_bon_transfert'))

@transaction.atomic
def post_creer_ligne_bon_transfert(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_ligne_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		quantite = makeFloat(request.POST['quantite'])

		quantite_fait = makeFloat(request.POST['quantite_fait'])

		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])

		societe_id = makeIntId(request.POST['societe_id'])

		fait = True if 'fait' in request.POST else False

		bon_transfert_id = makeIntId(request.POST['bon_transfert_id'])

		stockage_id = makeIntId(request.POST['stockage_id'])

		series = request.POST.getlist('series', None)

		auteur = identite.utilisateur(request)

		ligne_bon_transfert = dao_ligne_bon_transfert.toCreate(quantite = quantite, quantite_fait = quantite_fait, article_id = article_id, description = description, societe_id = societe_id, fait = fait, bon_transfert_id = bon_transfert_id, stockage_id = stockage_id, series = series)
		saved, ligne_bon_transfert, message = dao_ligne_bon_transfert.toSave(auteur, ligne_bon_transfert, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ligne_bon_transfert.toListById(ligne_bon_transfert.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, ligne_bon_transfert)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : ligne_bon_transfert.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_ligne_bon_transfert(request,ref):
	try:
		same_perm_with = 'module_stock_list_ligne_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ligne_bon_transfert = dao_ligne_bon_transfert.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(ligne_bon_transfert.id),'obj': str(ligne_bon_transfert)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_ligne_bon_transfert', args=(ligne_bon_transfert.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_ligne_bon_transfert(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ligne_bon_transfert = auth.toGetWithRules(dao_ligne_bon_transfert.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ligne_bon_transfert == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, ligne_bon_transfert) 

		context = {
			'title' : "Détails - Line bon de Transfert : {}".format(ligne_bon_transfert),
			'model' : ligne_bon_transfert,
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
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_transfert/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ligne_bon_transfert'))

def get_modifier_ligne_bon_transfert(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_ligne_bon_transfert.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Line bon de Transfert",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_transferts' : Model_Bon_transfert.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'stockages' : Model_Stockage.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_transfert/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_ligne_bon_transfert(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_ligne_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		quantite = makeFloat(request.POST['quantite'])

		quantite_fait = makeFloat(request.POST['quantite_fait'])

		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])

		societe_id = makeIntId(request.POST['societe_id'])

		fait = True if 'fait' in request.POST else False

		bon_transfert_id = makeIntId(request.POST['bon_transfert_id'])

		stockage_id = makeIntId(request.POST['stockage_id'])

		series = request.POST.getlist('series', None)
		auteur = identite.utilisateur(request)

		ligne_bon_transfert = dao_ligne_bon_transfert.toCreate(quantite = quantite, quantite_fait = quantite_fait, article_id = article_id, description = description, societe_id = societe_id, fait = fait, bon_transfert_id = bon_transfert_id, stockage_id = stockage_id, series = series)
		saved, ligne_bon_transfert, message = dao_ligne_bon_transfert.toUpdate(id, ligne_bon_transfert, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ligne_bon_transfert.toListById(ligne_bon_transfert.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : ligne_bon_transfert.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_ligne_bon_transfert(request,ref):
	try:
		same_perm_with = 'module_stock_add_ligne_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_ligne_bon_transfert.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_transferts' : Model_Bon_transfert.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'stockages' : Model_Stockage.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_transfert/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_ligne_bon_transfert(request,ref):
	try:
		same_perm_with = 'module_stock_list_ligne_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ligne_bon_transfert = auth.toGetWithRules(dao_ligne_bon_transfert.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ligne_bon_transfert == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Line bon de Transfert : {}".format(ligne_bon_transfert),
			'model' : ligne_bon_transfert,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_ligne_bon_transfert.html', 'print_ligne_bon_transfert.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_ligne_bon_transfert(request):
	try:
		same_perm_with = 'module_stock_add_ligne_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_ligne_bon_transfert')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des lines bons de transferts",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_transfert/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_ligne_bon_transfert(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_quantite = makeString(request.POST['quantite'])
		#print(f'header_quantite_id: {header_quantite_id}')

		header_quantite_fait = makeString(request.POST['quantite_fait'])
		#print(f'header_quantite_fait_id: {header_quantite_fait_id}')

		header_article_id = makeString(request.POST['article_id'])
		if header_article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_article_id: {header_article_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_fait = makeString(request.POST['fait'])
		#print(f'header_fait_id: {header_fait_id}')

		header_bon_transfert_id = makeString(request.POST['bon_transfert_id'])
		#print(f'header_bon_transfert_id: {header_bon_transfert_id}')

		header_stockage_id = makeString(request.POST['stockage_id'])
		#print(f'header_stockage_id: {header_stockage_id}')

		for i in df.index:

			quantite = 0
			if header_quantite != '': quantite = makeFloat(df[header_quantite][i])

			quantite_fait = 0
			if header_quantite_fait != '': quantite_fait = makeFloat(df[header_quantite_fait][i])

			article_id = None
			if header_article_id != '': article_id = makeIntId(str(df[header_article_id][i]))
			if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			fait = False
			if header_fait != '': fait = True if makeString(df[header_fait][i]) == 'True' else False

			bon_transfert_id = None
			if header_bon_transfert_id != '': bon_transfert_id = makeIntId(str(df[header_bon_transfert_id][i]))

			stockage_id = None
			if header_stockage_id != '': stockage_id = makeIntId(str(df[header_stockage_id][i]))

			ligne_bon_transfert = dao_ligne_bon_transfert.toCreate(quantite = quantite, quantite_fait = quantite_fait, article_id = article_id, description = description, societe_id = societe_id, fait = fait, bon_transfert_id = bon_transfert_id, stockage_id = stockage_id)
			saved, ligne_bon_transfert, message = dao_ligne_bon_transfert.toSave(auteur, ligne_bon_transfert)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_ligne_bon_transfert'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# LIGNE_BON_TRANSFERT API CONTROLLERS
def get_list_ligne_bon_transfert(request):
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
		model = dao_ligne_bon_transfert.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'quantite' : makeFloat(item.quantite),
				'quantite_fait' : makeFloat(item.quantite_fait),
				'article_id' : makeIntId(item.article_id),
				'description' : str(item.description),
				'societe_id' : makeIntId(item.societe_id),
				'fait' : item.fait,
				'bon_transfert_id' : makeIntId(item.bon_transfert_id),
				'stockage_id' : makeIntId(item.stockage_id),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_ligne_bon_transfert(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_ligne_bon_transfert.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'quantite' : makeFloat(model.quantite),
				'quantite_fait' : makeFloat(model.quantite_fait),
				'article_id' : makeIntId(model.article_id),
				'description' : str(model.description),
				'societe_id' : makeIntId(model.societe_id),
				'fait' : model.fait,
				'bon_transfert_id' : makeIntId(model.bon_transfert_id),
				'stockage_id' : makeIntId(model.stockage_id),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_ligne_bon_transfert(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		quantite = 0.0
		if 'quantite' in request.POST : quantite = makeFloat(request.POST['quantite'])

		quantite_fait = 0.0
		if 'quantite_fait' in request.POST : quantite_fait = makeFloat(request.POST['quantite_fait'])

		article_id = None
		if 'article' in request.POST : article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		fait = True if 'fait' in request.POST else False

		bon_transfert_id = None
		if 'bon_transfert' in request.POST : bon_transfert_id = makeIntId(request.POST['bon_transfert_id'])

		stockage_id = None
		if 'stockage' in request.POST : stockage_id = makeIntId(request.POST['stockage_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		series = []

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		ligne_bon_transfert = dao_ligne_bon_transfert.toCreate(quantite = quantite, quantite_fait = quantite_fait, article_id = article_id, description = description, societe_id = societe_id, fait = fait, bon_transfert_id = bon_transfert_id, stockage_id = stockage_id, series = series)
		saved, ligne_bon_transfert, message = dao_ligne_bon_transfert.toSave(auteur, ligne_bon_transfert)

		if saved == False: raise Exception(message)

		objet = {
			'id' : ligne_bon_transfert.id,
			'quantite' : makeFloat(ligne_bon_transfert.quantite),
			'quantite_fait' : makeFloat(ligne_bon_transfert.quantite_fait),
			'article_id' : makeIntId(ligne_bon_transfert.article_id),
			'description' : str(ligne_bon_transfert.description),
			'societe_id' : makeIntId(ligne_bon_transfert.societe_id),
			'fait' : ligne_bon_transfert.fait,
			'bon_transfert_id' : makeIntId(ligne_bon_transfert.bon_transfert_id),
			'stockage_id' : makeIntId(ligne_bon_transfert.stockage_id),
			'statut_id' : makeIntId(ligne_bon_transfert.statut_id),
			'etat' : str(ligne_bon_transfert.etat),
			'creation_date' : ligne_bon_transfert.creation_date,
			'update_date' : ligne_bon_transfert.update_date,
			'update_by_id' : makeIntId(ligne_bon_transfert.update_by_id),
			'auteur_id' : makeIntId(ligne_bon_transfert.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# LIGNE_BON_SORTIE CONTROLLERS
from ModuleStock.dao.dao_ligne_bon_sortie import dao_ligne_bon_sortie

def get_lister_ligne_bon_sortie(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_ligne_bon_sortie.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_ligne_bon_sortie.toListJson(model.object_list),
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
			'title' : "Liste des lines bons de sorties",
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
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_sortie/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_ligne_bon_sortie(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Line Bon de Sortie",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Ligne_bon_sortie(),
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_sorties' : Model_Bon_sortie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'stockages' : Model_Stockage.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_sortie/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ligne_bon_sortie'))

@transaction.atomic
def post_creer_ligne_bon_sortie(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_ligne_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		quantite_demandee = makeFloat(request.POST['quantite_demandee'])

		quantite_sortie = makeFloat(request.POST['quantite_sortie'])

		serie_id = makeIntId(request.POST['serie_id'])

		description = str(request.POST['description'])

		bon_sortie_id = makeIntId(request.POST['bon_sortie_id'])

		article_id = makeIntId(request.POST['article_id'])

		stockage_id = makeIntId(request.POST['stockage_id'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		ligne_bon_sortie = dao_ligne_bon_sortie.toCreate(quantite_demandee = quantite_demandee, quantite_sortie = quantite_sortie, serie_id = serie_id, description = description, bon_sortie_id = bon_sortie_id, article_id = article_id, stockage_id = stockage_id, societe_id = societe_id)
		saved, ligne_bon_sortie, message = dao_ligne_bon_sortie.toSave(auteur, ligne_bon_sortie, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ligne_bon_sortie.toListById(ligne_bon_sortie.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, ligne_bon_sortie)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : ligne_bon_sortie.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_ligne_bon_sortie(request,ref):
	try:
		same_perm_with = 'module_stock_list_ligne_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ligne_bon_sortie = dao_ligne_bon_sortie.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(ligne_bon_sortie.id),'obj': str(ligne_bon_sortie)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_ligne_bon_sortie', args=(ligne_bon_sortie.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_ligne_bon_sortie(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ligne_bon_sortie = auth.toGetWithRules(dao_ligne_bon_sortie.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ligne_bon_sortie == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, ligne_bon_sortie) 

		context = {
			'title' : "Détails - Line Bon de Sortie : {}".format(ligne_bon_sortie),
			'model' : ligne_bon_sortie,
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
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_sortie/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ligne_bon_sortie'))

def get_modifier_ligne_bon_sortie(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_ligne_bon_sortie.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Line Bon de Sortie",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_sorties' : Model_Bon_sortie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'stockages' : Model_Stockage.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_sortie/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_ligne_bon_sortie(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_ligne_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		quantite_demandee = makeFloat(request.POST['quantite_demandee'])

		quantite_sortie = makeFloat(request.POST['quantite_sortie'])

		serie_id = makeIntId(request.POST['serie_id'])

		description = str(request.POST['description'])

		bon_sortie_id = makeIntId(request.POST['bon_sortie_id'])

		article_id = makeIntId(request.POST['article_id'])

		stockage_id = makeIntId(request.POST['stockage_id'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		ligne_bon_sortie = dao_ligne_bon_sortie.toCreate(quantite_demandee = quantite_demandee, quantite_sortie = quantite_sortie, serie_id = serie_id, description = description, bon_sortie_id = bon_sortie_id, article_id = article_id, stockage_id = stockage_id, societe_id = societe_id)
		saved, ligne_bon_sortie, message = dao_ligne_bon_sortie.toUpdate(id, ligne_bon_sortie, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ligne_bon_sortie.toListById(ligne_bon_sortie.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : ligne_bon_sortie.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_ligne_bon_sortie(request,ref):
	try:
		same_perm_with = 'module_stock_add_ligne_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_ligne_bon_sortie.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'bon_sorties' : Model_Bon_sortie.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'stockages' : Model_Stockage.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_sortie/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_ligne_bon_sortie(request,ref):
	try:
		same_perm_with = 'module_stock_list_ligne_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ligne_bon_sortie = auth.toGetWithRules(dao_ligne_bon_sortie.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ligne_bon_sortie == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Line Bon de Sortie : {}".format(ligne_bon_sortie),
			'model' : ligne_bon_sortie,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_ligne_bon_sortie.html', 'print_ligne_bon_sortie.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_ligne_bon_sortie(request):
	try:
		same_perm_with = 'module_stock_add_ligne_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_ligne_bon_sortie')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des lines bons de sorties",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_bon_sortie/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_ligne_bon_sortie(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_quantite_demandee = makeString(request.POST['quantite_demandee'])
		#print(f'header_quantite_demandee_id: {header_quantite_demandee_id}')

		header_quantite_sortie = makeString(request.POST['quantite_sortie'])
		#print(f'header_quantite_sortie_id: {header_quantite_sortie_id}')

		header_serie_id = makeString(request.POST['serie_id'])
		#print(f'header_serie_id: {header_serie_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_bon_sortie_id = makeString(request.POST['bon_sortie_id'])
		#print(f'header_bon_sortie_id: {header_bon_sortie_id}')

		header_article_id = makeString(request.POST['article_id'])
		#print(f'header_article_id: {header_article_id}')

		header_stockage_id = makeString(request.POST['stockage_id'])
		#print(f'header_stockage_id: {header_stockage_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			quantite_demandee = 0
			if header_quantite_demandee != '': quantite_demandee = makeFloat(df[header_quantite_demandee][i])

			quantite_sortie = 0
			if header_quantite_sortie != '': quantite_sortie = makeFloat(df[header_quantite_sortie][i])

			serie_id = None
			if header_serie_id != '': serie_id = makeIntId(str(df[header_serie_id][i]))

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			bon_sortie_id = None
			if header_bon_sortie_id != '': bon_sortie_id = makeIntId(str(df[header_bon_sortie_id][i]))

			article_id = None
			if header_article_id != '': article_id = makeIntId(str(df[header_article_id][i]))

			stockage_id = None
			if header_stockage_id != '': stockage_id = makeIntId(str(df[header_stockage_id][i]))

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			ligne_bon_sortie = dao_ligne_bon_sortie.toCreate(quantite_demandee = quantite_demandee, quantite_sortie = quantite_sortie, serie_id = serie_id, description = description, bon_sortie_id = bon_sortie_id, article_id = article_id, stockage_id = stockage_id, societe_id = societe_id)
			saved, ligne_bon_sortie, message = dao_ligne_bon_sortie.toSave(auteur, ligne_bon_sortie)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_ligne_bon_sortie'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# LIGNE_BON_SORTIE API CONTROLLERS
def get_list_ligne_bon_sortie(request):
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
		model = dao_ligne_bon_sortie.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'quantite_demandee' : makeFloat(item.quantite_demandee),
				'quantite_sortie' : makeFloat(item.quantite_sortie),
				'serie_id' : makeIntId(item.serie_id),
				'description' : str(item.description),
				'bon_sortie_id' : makeIntId(item.bon_sortie_id),
				'article_id' : makeIntId(item.article_id),
				'stockage_id' : makeIntId(item.stockage_id),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_ligne_bon_sortie(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_ligne_bon_sortie.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'quantite_demandee' : makeFloat(model.quantite_demandee),
				'quantite_sortie' : makeFloat(model.quantite_sortie),
				'serie_id' : makeIntId(model.serie_id),
				'description' : str(model.description),
				'bon_sortie_id' : makeIntId(model.bon_sortie_id),
				'article_id' : makeIntId(model.article_id),
				'stockage_id' : makeIntId(model.stockage_id),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_ligne_bon_sortie(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		quantite_demandee = 0.0
		if 'quantite_demandee' in request.POST : quantite_demandee = makeFloat(request.POST['quantite_demandee'])

		quantite_sortie = 0.0
		if 'quantite_sortie' in request.POST : quantite_sortie = makeFloat(request.POST['quantite_sortie'])

		serie_id = None
		if 'serie' in request.POST : serie_id = makeIntId(request.POST['serie_id'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		bon_sortie_id = None
		if 'bon_sortie' in request.POST : bon_sortie_id = makeIntId(request.POST['bon_sortie_id'])

		article_id = None
		if 'article' in request.POST : article_id = makeIntId(request.POST['article_id'])

		stockage_id = None
		if 'stockage' in request.POST : stockage_id = makeIntId(request.POST['stockage_id'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		ligne_bon_sortie = dao_ligne_bon_sortie.toCreate(quantite_demandee = quantite_demandee, quantite_sortie = quantite_sortie, serie_id = serie_id, description = description, bon_sortie_id = bon_sortie_id, article_id = article_id, stockage_id = stockage_id, societe_id = societe_id)
		saved, ligne_bon_sortie, message = dao_ligne_bon_sortie.toSave(auteur, ligne_bon_sortie)

		if saved == False: raise Exception(message)

		objet = {
			'id' : ligne_bon_sortie.id,
			'quantite_demandee' : makeFloat(ligne_bon_sortie.quantite_demandee),
			'quantite_sortie' : makeFloat(ligne_bon_sortie.quantite_sortie),
			'serie_id' : makeIntId(ligne_bon_sortie.serie_id),
			'description' : str(ligne_bon_sortie.description),
			'bon_sortie_id' : makeIntId(ligne_bon_sortie.bon_sortie_id),
			'article_id' : makeIntId(ligne_bon_sortie.article_id),
			'stockage_id' : makeIntId(ligne_bon_sortie.stockage_id),
			'statut_id' : makeIntId(ligne_bon_sortie.statut_id),
			'etat' : str(ligne_bon_sortie.etat),
			'societe_id' : makeIntId(ligne_bon_sortie.societe_id),
			'creation_date' : ligne_bon_sortie.creation_date,
			'update_date' : ligne_bon_sortie.update_date,
			'update_by_id' : makeIntId(ligne_bon_sortie.update_by_id),
			'auteur_id' : makeIntId(ligne_bon_sortie.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# LIGNE_AJUSTEMENT CONTROLLERS
from ModuleStock.dao.dao_ligne_ajustement import dao_ligne_ajustement

def get_lister_ligne_ajustement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_ligne_ajustement.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_ligne_ajustement.toListJson(model.object_list),
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
			'title' : "Liste des lignes inventaires",
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
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_ligne_ajustement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Ligne Inventaire",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Ligne_ajustement(),
			'ajustements' : Model_Ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ligne_ajustement'))

@transaction.atomic
def post_creer_ligne_ajustement(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_ligne_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		ajustement_id = makeIntId(request.POST['ajustement_id'])
		if ajustement_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Inventaire\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = makeIntId(request.POST['article_id'])

		societe_id = makeIntId(request.POST['societe_id'])

		quantite_theorique = makeFloat(request.POST['quantite_theorique'])

		quantite_reelle = makeFloat(request.POST['quantite_reelle'])

		unite_id = makeIntId(request.POST['unite_id'])

		fait = True if 'fait' in request.POST else False

		series = request.POST.getlist('series', None)

		auteur = identite.utilisateur(request)

		ligne_ajustement = dao_ligne_ajustement.toCreate(ajustement_id = ajustement_id, article_id = article_id, societe_id = societe_id, quantite_theorique = quantite_theorique, quantite_reelle = quantite_reelle, unite_id = unite_id, fait = fait, series = series)
		saved, ligne_ajustement, message = dao_ligne_ajustement.toSave(auteur, ligne_ajustement, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ligne_ajustement.toListById(ligne_ajustement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, ligne_ajustement)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : ligne_ajustement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_ligne_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_list_ligne_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ligne_ajustement = dao_ligne_ajustement.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(ligne_ajustement.id),'obj': str(ligne_ajustement)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_ligne_ajustement', args=(ligne_ajustement.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_ligne_ajustement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ligne_ajustement = auth.toGetWithRules(dao_ligne_ajustement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ligne_ajustement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, ligne_ajustement) 

		context = {
			'title' : "Détails - Ligne Inventaire : {}".format(ligne_ajustement),
			'model' : ligne_ajustement,
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
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ligne_ajustement'))

def get_modifier_ligne_ajustement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_ligne_ajustement.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Ligne Inventaire",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'ajustements' : Model_Ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_ligne_ajustement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_ligne_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		ajustement_id = makeIntId(request.POST['ajustement_id'])
		if ajustement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Inventaire\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = makeIntId(request.POST['article_id'])

		societe_id = makeIntId(request.POST['societe_id'])

		quantite_theorique = makeFloat(request.POST['quantite_theorique'])

		quantite_reelle = makeFloat(request.POST['quantite_reelle'])

		unite_id = makeIntId(request.POST['unite_id'])

		fait = True if 'fait' in request.POST else False

		series = request.POST.getlist('series', None)
		auteur = identite.utilisateur(request)

		ligne_ajustement = dao_ligne_ajustement.toCreate(ajustement_id = ajustement_id, article_id = article_id, societe_id = societe_id, quantite_theorique = quantite_theorique, quantite_reelle = quantite_reelle, unite_id = unite_id, fait = fait, series = series)
		saved, ligne_ajustement, message = dao_ligne_ajustement.toUpdate(id, ligne_ajustement, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ligne_ajustement.toListById(ligne_ajustement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : ligne_ajustement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_ligne_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_add_ligne_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_ligne_ajustement.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'ajustements' : Model_Ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'unite_mesures' : Model_Unite_mesure.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'actifs' : Model_Actif.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_ligne_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_list_ligne_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ligne_ajustement = auth.toGetWithRules(dao_ligne_ajustement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ligne_ajustement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Ligne Inventaire : {}".format(ligne_ajustement),
			'model' : ligne_ajustement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_ligne_ajustement.html', 'print_ligne_ajustement.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_ligne_ajustement(request):
	try:
		same_perm_with = 'module_stock_add_ligne_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_ligne_ajustement')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des lignes inventaires",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_ligne_ajustement(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_ajustement_id = makeString(request.POST['ajustement_id'])
		if header_ajustement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Inventaire\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_ajustement_id: {header_ajustement_id}')

		header_article_id = makeString(request.POST['article_id'])
		#print(f'header_article_id: {header_article_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_quantite_theorique = makeString(request.POST['quantite_theorique'])
		#print(f'header_quantite_theorique_id: {header_quantite_theorique_id}')

		header_quantite_reelle = makeString(request.POST['quantite_reelle'])
		#print(f'header_quantite_reelle_id: {header_quantite_reelle_id}')

		header_unite_id = makeString(request.POST['unite_id'])
		#print(f'header_unite_id: {header_unite_id}')

		header_fait = makeString(request.POST['fait'])
		#print(f'header_fait_id: {header_fait_id}')

		for i in df.index:

			ajustement_id = None
			if header_ajustement_id != '': ajustement_id = makeIntId(str(df[header_ajustement_id][i]))
			if ajustement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Inventaire\' est obligatoire, Veuillez le renseigner SVP!')

			article_id = None
			if header_article_id != '': article_id = makeIntId(str(df[header_article_id][i]))

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			quantite_theorique = 0
			if header_quantite_theorique != '': quantite_theorique = makeFloat(df[header_quantite_theorique][i])

			quantite_reelle = 0
			if header_quantite_reelle != '': quantite_reelle = makeFloat(df[header_quantite_reelle][i])

			unite_id = None
			if header_unite_id != '': unite_id = makeIntId(str(df[header_unite_id][i]))

			fait = False
			if header_fait != '': fait = True if makeString(df[header_fait][i]) == 'True' else False

			ligne_ajustement = dao_ligne_ajustement.toCreate(ajustement_id = ajustement_id, article_id = article_id, societe_id = societe_id, quantite_theorique = quantite_theorique, quantite_reelle = quantite_reelle, unite_id = unite_id, fait = fait)
			saved, ligne_ajustement, message = dao_ligne_ajustement.toSave(auteur, ligne_ajustement)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_ligne_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# LIGNE_AJUSTEMENT API CONTROLLERS
def get_list_ligne_ajustement(request):
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
		model = dao_ligne_ajustement.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'ajustement_id' : makeIntId(item.ajustement_id),
				'article_id' : makeIntId(item.article_id),
				'societe_id' : makeIntId(item.societe_id),
				'quantite_theorique' : makeFloat(item.quantite_theorique),
				'quantite_reelle' : makeFloat(item.quantite_reelle),
				'unite_id' : makeIntId(item.unite_id),
				'fait' : item.fait,
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_ligne_ajustement(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_ligne_ajustement.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'ajustement_id' : makeIntId(model.ajustement_id),
				'article_id' : makeIntId(model.article_id),
				'societe_id' : makeIntId(model.societe_id),
				'quantite_theorique' : makeFloat(model.quantite_theorique),
				'quantite_reelle' : makeFloat(model.quantite_reelle),
				'unite_id' : makeIntId(model.unite_id),
				'fait' : model.fait,
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_ligne_ajustement(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		ajustement_id = None
		if 'ajustement' in request.POST : ajustement_id = makeIntId(request.POST['ajustement_id'])
		if ajustement_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Inventaire\' est obligatoire, Veuillez le renseigner SVP!')

		article_id = None
		if 'article' in request.POST : article_id = makeIntId(request.POST['article_id'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		quantite_theorique = 0.0
		if 'quantite_theorique' in request.POST : quantite_theorique = makeFloat(request.POST['quantite_theorique'])

		quantite_reelle = 0.0
		if 'quantite_reelle' in request.POST : quantite_reelle = makeFloat(request.POST['quantite_reelle'])

		unite_id = None
		if 'unite' in request.POST : unite_id = makeIntId(request.POST['unite_id'])

		fait = True if 'fait' in request.POST else False

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		series = []

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		ligne_ajustement = dao_ligne_ajustement.toCreate(ajustement_id = ajustement_id, article_id = article_id, societe_id = societe_id, quantite_theorique = quantite_theorique, quantite_reelle = quantite_reelle, unite_id = unite_id, fait = fait, series = series)
		saved, ligne_ajustement, message = dao_ligne_ajustement.toSave(auteur, ligne_ajustement)

		if saved == False: raise Exception(message)

		objet = {
			'id' : ligne_ajustement.id,
			'ajustement_id' : makeIntId(ligne_ajustement.ajustement_id),
			'article_id' : makeIntId(ligne_ajustement.article_id),
			'societe_id' : makeIntId(ligne_ajustement.societe_id),
			'quantite_theorique' : makeFloat(ligne_ajustement.quantite_theorique),
			'quantite_reelle' : makeFloat(ligne_ajustement.quantite_reelle),
			'unite_id' : makeIntId(ligne_ajustement.unite_id),
			'fait' : ligne_ajustement.fait,
			'statut_id' : makeIntId(ligne_ajustement.statut_id),
			'etat' : str(ligne_ajustement.etat),
			'creation_date' : ligne_ajustement.creation_date,
			'update_date' : ligne_ajustement.update_date,
			'update_by_id' : makeIntId(ligne_ajustement.update_by_id),
			'auteur_id' : makeIntId(ligne_ajustement.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# EMPLACEMENT CONTROLLERS
from ModuleStock.dao.dao_emplacement import dao_emplacement

def get_lister_emplacement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_emplacement.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_emplacement.toListJson(model.object_list),
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
			'title' : "Liste des emplacements",
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
		template = loader.get_template('ErpProject/ModuleStock/emplacement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_emplacement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Emplacement",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Emplacement(),
			'type_emplacements' : Model_Type_emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/emplacement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_emplacement'))

@transaction.atomic
def post_creer_emplacement(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		designation_court = str(request.POST['designation_court'])

		code = str(request.POST['code'])

		description = str(request.POST['description'])

		type_emplacement_id = makeIntId(request.POST['type_emplacement_id'])

		defaut = True if 'defaut' in request.POST else False

		societe_id = makeIntId(request.POST['societe_id'])

		visible = True if 'visible' in request.POST else False

		auteur = identite.utilisateur(request)

		emplacement = dao_emplacement.toCreate(designation = designation, designation_court = designation_court, code = code, description = description, type_emplacement_id = type_emplacement_id, defaut = defaut, societe_id = societe_id, visible = visible)
		saved, emplacement, message = dao_emplacement.toSave(auteur, emplacement, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_emplacement.toListById(emplacement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, emplacement)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : emplacement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_emplacement(request,ref):
	try:
		same_perm_with = 'module_stock_list_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		emplacement = dao_emplacement.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(emplacement.id),'obj': str(emplacement)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_emplacement', args=(emplacement.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_emplacement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		emplacement = auth.toGetWithRules(dao_emplacement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if emplacement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, emplacement) 

		context = {
			'title' : "Détails - Emplacement : {}".format(emplacement),
			'model' : emplacement,
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
		template = loader.get_template('ErpProject/ModuleStock/emplacement/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_emplacement'))

def get_modifier_emplacement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_emplacement.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Emplacement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'type_emplacements' : Model_Type_emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/emplacement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_emplacement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])

		designation_court = str(request.POST['designation_court'])

		code = str(request.POST['code'])

		description = str(request.POST['description'])

		type_emplacement_id = makeIntId(request.POST['type_emplacement_id'])

		defaut = True if 'defaut' in request.POST else False

		societe_id = makeIntId(request.POST['societe_id'])

		visible = True if 'visible' in request.POST else False
		auteur = identite.utilisateur(request)

		emplacement = dao_emplacement.toCreate(designation = designation, designation_court = designation_court, code = code, description = description, type_emplacement_id = type_emplacement_id, defaut = defaut, societe_id = societe_id, visible = visible)
		saved, emplacement, message = dao_emplacement.toUpdate(id, emplacement, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_emplacement.toListById(emplacement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : emplacement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_emplacement(request,ref):
	try:
		same_perm_with = 'module_stock_add_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_emplacement.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'type_emplacements' : Model_Type_emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/emplacement/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_emplacement(request,ref):
	try:
		same_perm_with = 'module_stock_list_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		emplacement = auth.toGetWithRules(dao_emplacement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if emplacement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Emplacement : {}".format(emplacement),
			'model' : emplacement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_emplacement.html', 'print_emplacement.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_emplacement(request):
	try:
		same_perm_with = 'module_stock_add_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_emplacement')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des emplacements",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/emplacement/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_emplacement(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_designation = makeString(request.POST['designation'])
		#print(f'header_designation_id: {header_designation_id}')

		header_designation_court = makeString(request.POST['designation_court'])
		#print(f'header_designation_court_id: {header_designation_court_id}')

		header_code = makeString(request.POST['code'])
		#print(f'header_code_id: {header_code_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_type_emplacement_id = makeString(request.POST['type_emplacement_id'])
		#print(f'header_type_emplacement_id: {header_type_emplacement_id}')

		header_defaut = makeString(request.POST['defaut'])
		#print(f'header_defaut_id: {header_defaut_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_visible = makeString(request.POST['visible'])
		#print(f'header_visible_id: {header_visible_id}')

		for i in df.index:

			designation = ''
			if header_designation != '': designation = makeString(df[header_designation][i])

			designation_court = ''
			if header_designation_court != '': designation_court = makeString(df[header_designation_court][i])

			code = ''
			if header_code != '': code = makeString(df[header_code][i])

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			type_emplacement_id = None
			if header_type_emplacement_id != '': type_emplacement_id = makeIntId(str(df[header_type_emplacement_id][i]))

			defaut = False
			if header_defaut != '': defaut = True if makeString(df[header_defaut][i]) == 'True' else False

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			visible = False
			if header_visible != '': visible = True if makeString(df[header_visible][i]) == 'True' else False

			emplacement = dao_emplacement.toCreate(designation = designation, designation_court = designation_court, code = code, description = description, type_emplacement_id = type_emplacement_id, defaut = defaut, societe_id = societe_id, visible = visible)
			saved, emplacement, message = dao_emplacement.toSave(auteur, emplacement)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_emplacement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# EMPLACEMENT BI CONTROLLERS
def get_bi_emplacement(request):
	try:
		same_perm_with = 'module_stock_get_generer_emplacement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		try:
			view = str(request.GET.get('view','table'))
		except Exception as e:
			view = 'table'

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_emplacement.toList(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model, 100)

		model_content_type = dao_query_builder.toGetContentTypeByName('model_emplacement')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)
		champs_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)
		champs_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)
		champs_date = dao_query_builder.toListFieldsDate(model_content_type.id)

		context = {
			'title' : "Analyse des emplacements",
			'model' : model,
			'model_id' : model_content_type.id,
			'modele' : Model_Emplacement(),
			'champs' : champs,
			'champs_nombre' : champs_nombre,
			'champs_date' : champs_date,
			'champs_dimension' : champs_texte,
			'view' : view,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleStock/emplacement/bi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

# EMPLACEMENT API CONTROLLERS
def get_list_emplacement(request):
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
		model = dao_emplacement.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'designation' : str(item.designation),
				'designation_court' : str(item.designation_court),
				'code' : str(item.code),
				'description' : str(item.description),
				'type_emplacement_id' : makeIntId(item.type_emplacement_id),
				'defaut' : item.defaut,
				'societe_id' : makeIntId(item.societe_id),
				'visible' : item.visible,
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_emplacement(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_emplacement.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'designation' : str(model.designation),
				'designation_court' : str(model.designation_court),
				'code' : str(model.code),
				'description' : str(model.description),
				'type_emplacement_id' : makeIntId(model.type_emplacement_id),
				'defaut' : model.defaut,
				'societe_id' : makeIntId(model.societe_id),
				'visible' : model.visible,
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_emplacement(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		designation = ''
		if 'designation' in request.POST : designation = str(request.POST['designation'])

		designation_court = ''
		if 'designation_court' in request.POST : designation_court = str(request.POST['designation_court'])

		code = ''
		if 'code' in request.POST : code = str(request.POST['code'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		type_emplacement_id = None
		if 'type_emplacement' in request.POST : type_emplacement_id = makeIntId(request.POST['type_emplacement_id'])

		defaut = True if 'defaut' in request.POST else False

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		visible = True if 'visible' in request.POST else False

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		emplacement = dao_emplacement.toCreate(designation = designation, designation_court = designation_court, code = code, description = description, type_emplacement_id = type_emplacement_id, defaut = defaut, societe_id = societe_id, visible = visible)
		saved, emplacement, message = dao_emplacement.toSave(auteur, emplacement)

		if saved == False: raise Exception(message)

		objet = {
			'id' : emplacement.id,
			'designation' : str(emplacement.designation),
			'designation_court' : str(emplacement.designation_court),
			'code' : str(emplacement.code),
			'description' : str(emplacement.description),
			'type_emplacement_id' : makeIntId(emplacement.type_emplacement_id),
			'defaut' : emplacement.defaut,
			'societe_id' : makeIntId(emplacement.societe_id),
			'visible' : emplacement.visible,
			'statut_id' : makeIntId(emplacement.statut_id),
			'etat' : str(emplacement.etat),
			'creation_date' : emplacement.creation_date,
			'update_date' : emplacement.update_date,
			'update_by_id' : makeIntId(emplacement.update_by_id),
			'auteur_id' : makeIntId(emplacement.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# CATEGORIE CONTROLLERS
from ModuleStock.dao.dao_categorie import dao_categorie

def get_lister_categorie(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_categorie.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_categorie.toListJson(model.object_list),
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
			'title' : "Liste des catégories",
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
		template = loader.get_template('ErpProject/ModuleStock/categorie/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_categorie(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Catégorie",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Categorie(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/categorie/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_categorie'))

@transaction.atomic
def post_creer_categorie(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_categorie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		name = str(request.POST['name'])

		short_name = str(request.POST['short_name'])

		code = str(request.POST['code'])

		description = str(request.POST['description'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		categorie = dao_categorie.toCreate(name = name, short_name = short_name, code = code, description = description, societe_id = societe_id)
		saved, categorie, message = dao_categorie.toSave(auteur, categorie, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_categorie.toListById(categorie.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, categorie)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : categorie.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_categorie(request,ref):
	try:
		same_perm_with = 'module_stock_list_categorie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		categorie = dao_categorie.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(categorie.id),'obj': str(categorie)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_categorie', args=(categorie.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_categorie(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		categorie = auth.toGetWithRules(dao_categorie.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if categorie == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, categorie) 

		context = {
			'title' : "Détails - Catégorie : {}".format(categorie),
			'model' : categorie,
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
		template = loader.get_template('ErpProject/ModuleStock/categorie/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_categorie'))

def get_modifier_categorie(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_categorie.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Catégorie",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/categorie/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_categorie(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_categorie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		name = str(request.POST['name'])

		short_name = str(request.POST['short_name'])

		code = str(request.POST['code'])

		description = str(request.POST['description'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		categorie = dao_categorie.toCreate(name = name, short_name = short_name, code = code, description = description, societe_id = societe_id)
		saved, categorie, message = dao_categorie.toUpdate(id, categorie, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_categorie.toListById(categorie.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : categorie.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_categorie(request,ref):
	try:
		same_perm_with = 'module_stock_add_categorie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_categorie.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/categorie/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_categorie(request,ref):
	try:
		same_perm_with = 'module_stock_list_categorie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		categorie = auth.toGetWithRules(dao_categorie.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if categorie == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Catégorie : {}".format(categorie),
			'model' : categorie,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_categorie.html', 'print_categorie.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_categorie(request):
	try:
		same_perm_with = 'module_stock_add_categorie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_categorie')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des catégories",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/categorie/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_categorie(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_name = makeString(request.POST['name'])
		#print(f'header_name_id: {header_name_id}')

		header_short_name = makeString(request.POST['short_name'])
		#print(f'header_short_name_id: {header_short_name_id}')

		header_code = makeString(request.POST['code'])
		#print(f'header_code_id: {header_code_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			name = ''
			if header_name != '': name = makeString(df[header_name][i])

			short_name = ''
			if header_short_name != '': short_name = makeString(df[header_short_name][i])

			code = ''
			if header_code != '': code = makeString(df[header_code][i])

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			categorie = dao_categorie.toCreate(name = name, short_name = short_name, code = code, description = description, societe_id = societe_id)
			saved, categorie, message = dao_categorie.toSave(auteur, categorie)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_categorie'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# CATEGORIE API CONTROLLERS
def get_list_categorie(request):
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
		model = dao_categorie.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'name' : str(item.name),
				'short_name' : str(item.short_name),
				'code' : str(item.code),
				'description' : str(item.description),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_categorie(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_categorie.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'name' : str(model.name),
				'short_name' : str(model.short_name),
				'code' : str(model.code),
				'description' : str(model.description),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_categorie(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		name = ''
		if 'name' in request.POST : name = str(request.POST['name'])

		short_name = ''
		if 'short_name' in request.POST : short_name = str(request.POST['short_name'])

		code = ''
		if 'code' in request.POST : code = str(request.POST['code'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		categorie = dao_categorie.toCreate(name = name, short_name = short_name, code = code, description = description, societe_id = societe_id)
		saved, categorie, message = dao_categorie.toSave(auteur, categorie)

		if saved == False: raise Exception(message)

		objet = {
			'id' : categorie.id,
			'name' : str(categorie.name),
			'short_name' : str(categorie.short_name),
			'code' : str(categorie.code),
			'description' : str(categorie.description),
			'statut_id' : makeIntId(categorie.statut_id),
			'etat' : str(categorie.etat),
			'societe_id' : makeIntId(categorie.societe_id),
			'creation_date' : categorie.creation_date,
			'update_date' : categorie.update_date,
			'update_by_id' : makeIntId(categorie.update_by_id),
			'auteur_id' : makeIntId(categorie.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# BON_TRANSFERT CONTROLLERS
from ModuleStock.dao.dao_bon_transfert import dao_bon_transfert

def get_lister_bon_transfert(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_bon_transfert.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_bon_transfert.toListJson(model.object_list),
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
			'title' : "Liste des bons de transferts",
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
		template = loader.get_template('ErpProject/ModuleStock/bon_transfert/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_bon_transfert(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response
		emplacements  = Model_Emplacement.objects.filter(defaut = True).order_by('id')
		context = {
			'title' : "Formulaire d'enregistrement - Bon de Transfert",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Bon_transfert(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : emplacements,
			# 'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(pk = 3,).order_by('-id')[:10],
			'operation_stocks' : Model_Operation_stock.objects.filter(pk = 2).order_by('-id'),
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id'),
			'articles' : Model_Article.objects.filter(societe__code = 'MD'),
			'reference': dao_bon_transfert.toGenerateNumeroBonTransfert()
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_transfert/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_bon_transfert'))

@transaction.atomic
def post_creer_bon_transfert(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		code = str(request.POST['code'])

		societe_id = makeIntId(request.POST['societe_id'])

		emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		status_id = 1

		operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		description = str(request.POST['description'])

		responsable_transfert_id = makeIntId(request.POST['responsable_transfert_id'])

		auteur = identite.utilisateur(request)

		bon_transfert = dao_bon_transfert.toCreate(code = code, societe_id = societe_id, emplacement_origine_id = emplacement_origine_id, emplacement_destination_id = emplacement_destination_id, status_id = status_id, operation_stock_id = operation_stock_id, description = description, responsable_transfert_id = responsable_transfert_id)
		saved, bon_transfert, message = dao_bon_transfert.toSave(auteur, bon_transfert, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_bon_transfert.toListById(bon_transfert.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		list_articles = request.POST.getlist('articles', None)
		list_quantites = request.POST.getlist("quantites", None)
		list_decriptions = request.POST.getlist("decriptions", None)
		print("File: ModuleStock/views.py | Line: 13557 | list_articles ~ list_quantites",list_quantites)

		for i in range(0, len(list_articles)):
			print(f'::::::ITERATION {i}')
			article_id = int(list_articles[i])
			quantite = makeFloat(list_quantites[i])
			description = str(list_decriptions[i])

			quantite_demandee = quantite

			
			#verification Conformité
			# if quantite_recue > quantite : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Quantité\' Transferée est superieur à la quantité demandée, Veuillez le verifié SVP!')


			#Recuperer le stockage dans laquelle l'article est sortie
			emplacement = Model_Emplacement.objects.get(pk = emplacement_origine_id)
			stockage = Model_Stockage.objects.filter(emplacement_id = emplacement.id).first()
			# print("File: ModuleStock/views.py | Line: 13587 | post_creer_bon_transfert ~ stockage",stockage)

			article = Model_Article.objects.get(pk = article_id)
			# print("File: ModuleStock/views.py | Line: 13588 | post_creer_bon_transfert ~ article",article)	

			#Enregistrement des informations de la ligne de bon de transfert
			ligne = Model_Ligne_bon_transfert()
			ligne.bon_transfert_id = bon_transfert.id
			ligne.quantite = quantite
			ligne.article_id = article.id
			ligne.description = description
			ligne.fait = False
			ligne.stockage_id = stockage.id
			ligne.save()
			# print(f'cas 4 :: Ligne de bon de transfert {ligne}')

			#On cherche l'Emplacement dont le type est interne & dont l'article est de type stockable
			if bon_transfert.emplacement_origine.type_emplacement.id == 2 and article.type_article.id == 1:
				#On recupere le stockage de l'emplacement d'origine
				stockage = Model_Stockage.objects.filter(article_id = article_id, emplacement_id = bon_transfert.emplacement_origine.id).first()
				print(" File: ModuleStock/views.py | Line: 13699 | post_creer_transfert_confirme_stock ~ stockage",stockage)
				print('Check Stackage')

			#Ici on recupere le stock actuelle et on fait la reduction de la quantité
			if stockage:
				if stockage.quantite < quantite_demandee :
					transaction.savepoint_rollback(sid)
					return auth.toReturnFailed(request, 'Erreur de destockage !', msg = "La quantité saisie de l'article " + article.name + " est supérieure au stock")

				qi = stockage.quantite
				stockage.quantite -= quantite_demandee
				stockage.save()
				print(':::Stockage', stockage)

			else:
				transaction.savepoint_rollback(sid)
				return auth.toReturnFailed(request, 'Erreur de destockage !', msg = "L'article " + article.name + " dont selectionné pour le transfert ne se trouve pas dans votre stock")

			#On recherche le stockage de l'emplacement destination
			if bon_transfert.emplacement_destination.type_emplacement.id == 2 and article.type_article.id == 1:
				#On recupere le stockage de l'emplacement de destination
				stockage_dest = Model_Stockage.objects.filter(article_id = article_id, emplacement_id = bon_transfert.emplacement_destination.id).first()
				print(" File: ModuleStock/views.py | Line: 13723 | post_creer_transfert_confirme_stock ~ stockage_dest:::",stockage_dest)

			qi_dest = 0
			if stockage_dest:
				qi_dest = stockage_dest.quantite
				stockage_dest.quantite += quantite_demandee
				stockage_dest.save()
				print(f'stockage_destination cas 1  {stockage_dest}')
			else:
				qi_dest = 0
				stockage = Model_Stockage()
				stockage.emplacement_id = bon_transfert.emplacement_destination.id
				stockage.article_id = article_id
				stockage.quantite = quantite_demandee
				stockage.unite_id = article.measure_unit.id
				stockage.societe_id = societe_id
				stockage.save()
				print(f'stockage_destination cas 2  {stockage}')

			mvt = Model_Mvt_stock()
			mvt.type_id = 3
			mvt.article_id = article_id
			mvt.emplacement_id = bon_transfert.emplacement_destination.id
			mvt.transfert_id = bon_transfert.id
			mvt.quantite_initiale = qi_dest
			mvt.unite_initiale_id = article.measure_unit.id
			mvt.quantite_final = quantite_demandee
			mvt.unite_id = article.measure_unit.id
			mvt.document = bon_transfert.code
			mvt.auteur_id = auteur.id
			mvt.societe_id = societe_id
			mvt.save()
			print('::::Mvt', mvt)

			bon_transfert.status_id = 3
			bon_transfert.save()

			ligne = Model_Ligne_bon_transfert.objects.filter(bon_transfert__id = bon_transfert.id).first()
			ligne.quantite_fait = quantite_demandee
			ligne.fait = True
			ligne.save()


		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, bon_transfert)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : bon_transfert.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_bon_transfert(request,ref):
	try:
		same_perm_with = 'module_stock_list_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		bon_transfert = dao_bon_transfert.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(bon_transfert.id),'obj': str(bon_transfert)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_bon_transfert', args=(bon_transfert.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_bon_transfert(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		bon_transfert = auth.toGetWithRules(dao_bon_transfert.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if bon_transfert == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, bon_transfert) 

		context = {
			'title' : "Détails - Bon de Transfert : {}".format(bon_transfert),
			'model' : bon_transfert,
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
		template = loader.get_template('ErpProject/ModuleStock/bon_transfert/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_bon_transfert'))

def get_modifier_bon_transfert(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_bon_transfert.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Bon de Transfert",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'operation_stocks' : Model_Operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_transfert/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_bon_transfert(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		code = str(request.POST['code'])

		societe_id = makeIntId(request.POST['societe_id'])

		emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		status_id = makeIntId(request.POST['status_id'])

		operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		description = str(request.POST['description'])

		responsable_transfert_id = makeIntId(request.POST['responsable_transfert_id'])
		auteur = identite.utilisateur(request)

		bon_transfert = dao_bon_transfert.toCreate(code = code, societe_id = societe_id, emplacement_origine_id = emplacement_origine_id, emplacement_destination_id = emplacement_destination_id, status_id = status_id, operation_stock_id = operation_stock_id, description = description, responsable_transfert_id = responsable_transfert_id)
		saved, bon_transfert, message = dao_bon_transfert.toUpdate(id, bon_transfert, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_bon_transfert.toListById(bon_transfert.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : bon_transfert.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_bon_transfert(request,ref):
	try:
		same_perm_with = 'module_stock_add_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_bon_transfert.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'operation_stocks' : Model_Operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_transfert/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_bon_transfert(request,ref):
	try:
		same_perm_with = 'module_stock_list_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		bon_transfert = auth.toGetWithRules(dao_bon_transfert.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if bon_transfert == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Bon de Transfert : {}".format(bon_transfert),
			'model' : bon_transfert,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_bon_transfert.html', 'print_bon_transfert.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_bon_transfert(request):
	try:
		same_perm_with = 'module_stock_add_bon_transfert'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_bon_transfert')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des bons de transferts",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_transfert/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_bon_transfert(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_code = makeString(request.POST['code'])
		#print(f'header_code_id: {header_code_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_emplacement_origine_id = makeString(request.POST['emplacement_origine_id'])
		#print(f'header_emplacement_origine_id: {header_emplacement_origine_id}')

		header_emplacement_destination_id = makeString(request.POST['emplacement_destination_id'])
		#print(f'header_emplacement_destination_id: {header_emplacement_destination_id}')

		header_status_id = makeString(request.POST['status_id'])
		#print(f'header_status_id: {header_status_id}')

		header_operation_stock_id = makeString(request.POST['operation_stock_id'])
		#print(f'header_operation_stock_id: {header_operation_stock_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_responsable_transfert_id = makeString(request.POST['responsable_transfert_id'])
		#print(f'header_responsable_transfert_id: {header_responsable_transfert_id}')

		for i in df.index:

			code = ''
			if header_code != '': code = makeString(df[header_code][i])

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			emplacement_origine_id = None
			if header_emplacement_origine_id != '': emplacement_origine_id = makeIntId(str(df[header_emplacement_origine_id][i]))

			emplacement_destination_id = None
			if header_emplacement_destination_id != '': emplacement_destination_id = makeIntId(str(df[header_emplacement_destination_id][i]))

			status_id = None
			if header_status_id != '': status_id = makeIntId(str(df[header_status_id][i]))

			operation_stock_id = None
			if header_operation_stock_id != '': operation_stock_id = makeIntId(str(df[header_operation_stock_id][i]))

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			responsable_transfert_id = None
			if header_responsable_transfert_id != '': responsable_transfert_id = makeIntId(str(df[header_responsable_transfert_id][i]))

			bon_transfert = dao_bon_transfert.toCreate(code = code, societe_id = societe_id, emplacement_origine_id = emplacement_origine_id, emplacement_destination_id = emplacement_destination_id, status_id = status_id, operation_stock_id = operation_stock_id, description = description, responsable_transfert_id = responsable_transfert_id)
			saved, bon_transfert, message = dao_bon_transfert.toSave(auteur, bon_transfert)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_bon_transfert'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# BON_TRANSFERT API CONTROLLERS
def get_list_bon_transfert(request):
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
		model = dao_bon_transfert.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'code' : str(item.code),
				'societe_id' : makeIntId(item.societe_id),
				'emplacement_origine_id' : makeIntId(item.emplacement_origine_id),
				'emplacement_destination_id' : makeIntId(item.emplacement_destination_id),
				'status_id' : makeIntId(item.status_id),
				'operation_stock_id' : makeIntId(item.operation_stock_id),
				'description' : str(item.description),
				'responsable_transfert_id' : makeIntId(item.responsable_transfert_id),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_bon_transfert(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_bon_transfert.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'code' : str(model.code),
				'societe_id' : makeIntId(model.societe_id),
				'emplacement_origine_id' : makeIntId(model.emplacement_origine_id),
				'emplacement_destination_id' : makeIntId(model.emplacement_destination_id),
				'status_id' : makeIntId(model.status_id),
				'operation_stock_id' : makeIntId(model.operation_stock_id),
				'description' : str(model.description),
				'responsable_transfert_id' : makeIntId(model.responsable_transfert_id),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_bon_transfert(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		code = ''
		if 'code' in request.POST : code = str(request.POST['code'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		emplacement_origine_id = None
		if 'emplacement_origine' in request.POST : emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		emplacement_destination_id = None
		if 'emplacement_destination' in request.POST : emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		status_id = None
		if 'status' in request.POST : status_id = makeIntId(request.POST['status_id'])

		operation_stock_id = None
		if 'operation_stock' in request.POST : operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		responsable_transfert_id = None
		if 'responsable_transfert' in request.POST : responsable_transfert_id = makeIntId(request.POST['responsable_transfert_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		bon_transfert = dao_bon_transfert.toCreate(code = code, societe_id = societe_id, emplacement_origine_id = emplacement_origine_id, emplacement_destination_id = emplacement_destination_id, status_id = status_id, operation_stock_id = operation_stock_id, description = description, responsable_transfert_id = responsable_transfert_id)
		saved, bon_transfert, message = dao_bon_transfert.toSave(auteur, bon_transfert)

		if saved == False: raise Exception(message)

		objet = {
			'id' : bon_transfert.id,
			'code' : str(bon_transfert.code),
			'societe_id' : makeIntId(bon_transfert.societe_id),
			'emplacement_origine_id' : makeIntId(bon_transfert.emplacement_origine_id),
			'emplacement_destination_id' : makeIntId(bon_transfert.emplacement_destination_id),
			'status_id' : makeIntId(bon_transfert.status_id),
			'operation_stock_id' : makeIntId(bon_transfert.operation_stock_id),
			'description' : str(bon_transfert.description),
			'responsable_transfert_id' : makeIntId(bon_transfert.responsable_transfert_id),
			'statut_id' : makeIntId(bon_transfert.statut_id),
			'etat' : str(bon_transfert.etat),
			'creation_date' : bon_transfert.creation_date,
			'update_date' : bon_transfert.update_date,
			'update_by_id' : makeIntId(bon_transfert.update_by_id),
			'auteur_id' : makeIntId(bon_transfert.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# BON_SORTIE CONTROLLERS
from ModuleStock.dao.dao_bon_sortie import dao_bon_sortie

def get_lister_bon_sortie(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_bon_sortie.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_bon_sortie.toListJson(model.object_list),
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
			'title' : "Liste des bons de sorties",
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
		template = loader.get_template('ErpProject/ModuleStock/bon_sortie/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_bon_sortie(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response
		emplacements_destination = Model_Emplacement.objects.filter(pk = 2).order_by('id')

		emplacements_origine  = Model_Emplacement.objects.filter(defaut = True).order_by('id')


		context = {
			'title' : "Formulaire d'enregistrement - Bon de Sortie",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Bon_sortie(),
			'emplacements_destination' :emplacements_destination,
			'emplacements_origine': emplacements_origine,
			'operation_stocks' : Model_Operation_stock.objects.filter(pk = 3, societe__code = 'MD').order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(type_article = 1, societe__code = 'MD'),
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_sortie/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_bon_sortie'))


@transaction.atomic
def post_creer_bon_sortie(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		code = dao_bon_sortie.toGenerateNumeroBonSortie()

		description = str(request.POST['description'])

		emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		status_id = 3

		employe_id = makeIntId(request.POST['employe_id'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		bon_sortie = dao_bon_sortie.toCreate(code = code, description = description, emplacement_destination_id = emplacement_destination_id, emplacement_origine_id = emplacement_origine_id, operation_stock_id = operation_stock_id, status_id = status_id, employe_id = employe_id, societe_id = societe_id)
		saved, bon_sortie, message = dao_bon_sortie.toSave(auteur, bon_sortie, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_bon_sortie.toListById(bon_sortie.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Enregistrement des lignes Bon Sortie**
		list_articles = request.POST.getlist('articles', None)
		list_quantites = request.POST.getlist("quantites", None)
		list_decriptions = request.POST.getlist("decriptions", None)
		print("File: ModuleStock/views.py | Line: 1155 | post_creer_bon_reception ~ list_quantites",list_quantites)
		index = 0
		data_series = []

		for i in range(0, len(list_articles)):
			print(f'::::::ITERATION {i}')
			index += 1
			code_ligne = i
			article_id = int(list_articles[i])
			quantite = makeFloat(list_quantites[i])
			description = str(list_decriptions[i])


			#Recuperer le stockage dans laquelle l'article est sortie
			emplacement = Model_Emplacement.objects.get(pk = emplacement_origine_id)
			stockage = Model_Stockage.objects.filter(emplacement_id = emplacement.id).first()
			# print("File: ModuleStock/views.py | Line: 13587 | post_creer_bon_transfert ~ stockage",stockage)

			article = Model_Article.objects.get(pk = article_id)
			# print("File: ModuleStock/views.py | Line: 13588 | post_creer_bon_transfert ~ article",article)	

			stockage = ""

			#On cherche l'Emplacement dont le type est interne & dont l'article est de type stockable
			if bon_sortie.emplacement_origine.type_emplacement.id == 2 and article.type_article.id == 1:
				#On recupere le stockage de l'emplacement d'origine
				stockage = Model_Stockage.objects.filter(article_id = article_id, emplacement_id = bon_sortie.emplacement_origine.id).first()
				print(':::::Check Stockage', stockage)
			# Ici on recupere le stock actuelle et on fait la reduction de la quantité
			if stockage:
				if stockage.quantite < quantite :
					transaction.savepoint_rollback(sid)
					messages.add_message(request, messages.ERROR, "La quantité saisie de l'article " + article.name + " est supérieure au stock")
					return HttpResponseRedirect(reverse("module_stock_add_bon_sortie"))
				
				qi = stockage.quantite
				stockage.quantite -= quantite
				stockage.save()
				"........"
				print('Stockage', stockage)

				#Enregistrement des informations de la ligne de bon de sortie
				ligne_bon = Model_Ligne_bon_sortie()
				ligne_bon.bon_sortie_id = bon_sortie.id
				ligne_bon.quantite_demandee = quantite
				ligne_bon.quantite_sortie = quantite
				ligne_bon.article_id = article_id
				ligne_bon.stockage_id = stockage.id
				ligne_bon.save()
			else:
				print('Second 2')
				transaction.savepoint_rollback(sid)
				# messages.add_message(request, messages.ERROR, "L'article " + article.name + " dont selectionné pour la sortie ne se trouve pas dans votre stock")
				return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = "L'article " + article.name + " dont selectionné pour la sortie ne se trouve pas dans votre stock "+ emplacement.designation)
				# return HttpResponseRedirect(reverse("module_stock_add_bon_sortie"))

			#On saisi le mouvement du sortie de stock 
			mvt = Model_Mvt_stock()
			mvt.type_id = 2
			mvt.article_id = article.id
			mvt.emplacement_id = bon_sortie.emplacement_origine.id
			mvt.sortie_id = bon_sortie.id
			mvt.quantite_initiale = qi
			mvt.unite_initiale_id = article.measure_unit.id
			mvt.quantite = quantite
			mvt.unite_id = article.measure_unit.id
			mvt.document = bon_sortie.code
			mvt.auteur_id = auteur.id
			mvt.save()
			print('mvt', mvt)

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, bon_sortie)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : bon_sortie.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())


def get_select_bon_sortie(request,ref):
	try:
		same_perm_with = 'module_stock_list_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		bon_sortie = dao_bon_sortie.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(bon_sortie.id),'obj': str(bon_sortie)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_bon_sortie', args=(bon_sortie.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_bon_sortie(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		bon_sortie = auth.toGetWithRules(dao_bon_sortie.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if bon_sortie == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, bon_sortie) 

		context = {
			'title' : "Détails - Bon de Sortie : {}".format(bon_sortie),
			'model' : bon_sortie,
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
		template = loader.get_template('ErpProject/ModuleStock/bon_sortie/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_bon_sortie'))

def get_modifier_bon_sortie(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_bon_sortie.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Bon de Sortie",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'operation_stocks' : Model_Operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_sortie/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_bon_sortie(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		code = str(request.POST['code'])

		description = str(request.POST['description'])

		emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		status_id = makeIntId(request.POST['status_id'])

		employe_id = makeIntId(request.POST['employe_id'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		bon_sortie = dao_bon_sortie.toCreate(code = code, description = description, emplacement_destination_id = emplacement_destination_id, emplacement_origine_id = emplacement_origine_id, operation_stock_id = operation_stock_id, status_id = status_id, employe_id = employe_id, societe_id = societe_id)
		saved, bon_sortie, message = dao_bon_sortie.toUpdate(id, bon_sortie, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_bon_sortie.toListById(bon_sortie.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : bon_sortie.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_bon_sortie(request,ref):
	try:
		same_perm_with = 'module_stock_add_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_bon_sortie.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'operation_stocks' : Model_Operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_sortie/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_bon_sortie(request,ref):
	try:
		same_perm_with = 'module_stock_list_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		bon_sortie = auth.toGetWithRules(dao_bon_sortie.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if bon_sortie == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Bon de Sortie : {}".format(bon_sortie),
			'model' : bon_sortie,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_bon_sortie.html', 'print_bon_sortie.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_bon_sortie(request):
	try:
		same_perm_with = 'module_stock_add_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_bon_sortie')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des bons de sorties",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_sortie/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_bon_sortie(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_code = makeString(request.POST['code'])
		#print(f'header_code_id: {header_code_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_emplacement_destination_id = makeString(request.POST['emplacement_destination_id'])
		#print(f'header_emplacement_destination_id: {header_emplacement_destination_id}')

		header_emplacement_origine_id = makeString(request.POST['emplacement_origine_id'])
		#print(f'header_emplacement_origine_id: {header_emplacement_origine_id}')

		header_operation_stock_id = makeString(request.POST['operation_stock_id'])
		#print(f'header_operation_stock_id: {header_operation_stock_id}')

		header_status_id = makeString(request.POST['status_id'])
		#print(f'header_status_id: {header_status_id}')

		header_employe_id = makeString(request.POST['employe_id'])
		#print(f'header_employe_id: {header_employe_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			code = ''
			if header_code != '': code = makeString(df[header_code][i])

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			emplacement_destination_id = None
			if header_emplacement_destination_id != '': emplacement_destination_id = makeIntId(str(df[header_emplacement_destination_id][i]))

			emplacement_origine_id = None
			if header_emplacement_origine_id != '': emplacement_origine_id = makeIntId(str(df[header_emplacement_origine_id][i]))

			operation_stock_id = None
			if header_operation_stock_id != '': operation_stock_id = makeIntId(str(df[header_operation_stock_id][i]))

			status_id = None
			if header_status_id != '': status_id = makeIntId(str(df[header_status_id][i]))

			employe_id = None
			if header_employe_id != '': employe_id = makeIntId(str(df[header_employe_id][i]))

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			bon_sortie = dao_bon_sortie.toCreate(code = code, description = description, emplacement_destination_id = emplacement_destination_id, emplacement_origine_id = emplacement_origine_id, operation_stock_id = operation_stock_id, status_id = status_id, employe_id = employe_id, societe_id = societe_id)
			saved, bon_sortie, message = dao_bon_sortie.toSave(auteur, bon_sortie)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_bon_sortie'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# BON_SORTIE BI CONTROLLERS
def get_bi_bon_sortie(request):
	try:
		same_perm_with = 'module_stock_get_generer_bon_sortie'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		try:
			view = str(request.GET.get('view','table'))
		except Exception as e:
			view = 'table'

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_bon_sortie.toList(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model, 100)

		model_content_type = dao_query_builder.toGetContentTypeByName('model_bon_sortie')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)
		champs_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)
		champs_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)
		champs_date = dao_query_builder.toListFieldsDate(model_content_type.id)

		context = {
			'title' : "Analyse des bons de sorties",
			'model' : model,
			'model_id' : model_content_type.id,
			'modele' : Model_Bon_sortie(),
			'champs' : champs,
			'champs_nombre' : champs_nombre,
			'champs_date' : champs_date,
			'champs_dimension' : champs_texte,
			'view' : view,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_sortie/bi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

# BON_SORTIE API CONTROLLERS
def get_list_bon_sortie(request):
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
		model = dao_bon_sortie.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'code' : str(item.code),
				'description' : str(item.description),
				'emplacement_destination_id' : makeIntId(item.emplacement_destination_id),
				'emplacement_origine_id' : makeIntId(item.emplacement_origine_id),
				'operation_stock_id' : makeIntId(item.operation_stock_id),
				'status_id' : makeIntId(item.status_id),
				'employe_id' : makeIntId(item.employe_id),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_bon_sortie(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_bon_sortie.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'code' : str(model.code),
				'description' : str(model.description),
				'emplacement_destination_id' : makeIntId(model.emplacement_destination_id),
				'emplacement_origine_id' : makeIntId(model.emplacement_origine_id),
				'operation_stock_id' : makeIntId(model.operation_stock_id),
				'status_id' : makeIntId(model.status_id),
				'employe_id' : makeIntId(model.employe_id),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_bon_sortie(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		code = ''
		if 'code' in request.POST : code = str(request.POST['code'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		emplacement_destination_id = None
		if 'emplacement_destination' in request.POST : emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		emplacement_origine_id = None
		if 'emplacement_origine' in request.POST : emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		operation_stock_id = None
		if 'operation_stock' in request.POST : operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		status_id = None
		if 'status' in request.POST : status_id = makeIntId(request.POST['status_id'])

		employe_id = None
		if 'employe' in request.POST : employe_id = makeIntId(request.POST['employe_id'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		bon_sortie = dao_bon_sortie.toCreate(code = code, description = description, emplacement_destination_id = emplacement_destination_id, emplacement_origine_id = emplacement_origine_id, operation_stock_id = operation_stock_id, status_id = status_id, employe_id = employe_id, societe_id = societe_id)
		saved, bon_sortie, message = dao_bon_sortie.toSave(auteur, bon_sortie)

		if saved == False: raise Exception(message)

		objet = {
			'id' : bon_sortie.id,
			'code' : str(bon_sortie.code),
			'description' : str(bon_sortie.description),
			'emplacement_destination_id' : makeIntId(bon_sortie.emplacement_destination_id),
			'emplacement_origine_id' : makeIntId(bon_sortie.emplacement_origine_id),
			'operation_stock_id' : makeIntId(bon_sortie.operation_stock_id),
			'status_id' : makeIntId(bon_sortie.status_id),
			'employe_id' : makeIntId(bon_sortie.employe_id),
			'statut_id' : makeIntId(bon_sortie.statut_id),
			'etat' : str(bon_sortie.etat),
			'societe_id' : makeIntId(bon_sortie.societe_id),
			'creation_date' : bon_sortie.creation_date,
			'update_date' : bon_sortie.update_date,
			'update_by_id' : makeIntId(bon_sortie.update_by_id),
			'auteur_id' : makeIntId(bon_sortie.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# BON_RECEPTION CONTROLLERS
from ModuleStock.dao.dao_bon_reception import dao_bon_reception

def get_lister_bon_reception(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_bon_reception.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_bon_reception.toListJson(model.object_list),
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
			'title' : "Liste des bons de receptions",
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
		template = loader.get_template('ErpProject/ModuleStock/bon_reception/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_bon_reception(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response
		emplacements_origine = Model_Emplacement.objects.filter(pk = 1).order_by('id')

		emplacements_destination  = Model_Emplacement.objects.filter(defaut = True).order_by('id')
		context = {
			'title' : "Formulaire d'enregistrement - Bon de Reception",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Bon_reception(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements_destination' : emplacements_destination,
			'emplacements_origine': emplacements_origine,
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'operation_stocks' : Model_Operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'articles' : Model_Article.objects.filter(societe__code = 'MD'),
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_reception/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_bon_reception'))

@transaction.atomic
def post_creer_bon_reception(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_bon_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		code = dao_bon_reception.toGenerateNumeroBonReception()

		description = str(request.POST['description'])
		if description in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Observation de Livraison\' est obligatoire, Veuillez le renseigner SVP!')

		date_prevue = str(request.POST['date_prevue'])
		if date_prevue in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		is_formated, date_prevue = checkDateTimeFormat(date_prevue)
		if is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \'Date\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')

		societe_id = makeIntId(request.POST['societe_id'])

		emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		status_id = 3

		bon_livraison = request.FILES['bon_livraison'] if 'bon_livraison' in request.FILES else None

		employe_id = makeIntId(request.POST['employe_id'])

		auteur = identite.utilisateur(request)

		bon_reception = dao_bon_reception.toCreate(code = code, description = description, date_prevue = date_prevue, societe_id = societe_id, emplacement_destination_id = emplacement_destination_id, emplacement_origine_id = emplacement_origine_id, operation_stock_id = operation_stock_id, status_id = status_id, bon_livraison = bon_livraison, employe_id = employe_id)
		saved, bon_reception, message = dao_bon_reception.toSave(auteur, bon_reception, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_bon_reception.toListById(bon_reception.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		list_articles = request.POST.getlist('articles', None)
		list_quantites = request.POST.getlist("quantites", None)
		list_decriptions = request.POST.getlist("decriptions", None)
		print("File: ModuleStock/views.py | Line: 1155 | post_creer_bon_reception ~ list_quantites",list_quantites)
		index = 0
		data_series = []


		for i in range(0, len(list_articles)):
			print(f'::::::ITERATION {i}')
			index += 1
			code_ligne = i
			article_id = int(list_articles[i])
			quantite = makeFloat(list_quantites[i])
			description = str(list_decriptions[i])

			#Recuperer le stockage dans laquelle l'article est sortie
			emplacement = Model_Emplacement.objects.get(pk = emplacement_destination_id)
			stockage = Model_Stockage.objects.filter(emplacement_id = emplacement.id).first()
			# print("File: ModuleStock/views.py | Line: 13587 | post_creer_bon_transfert ~ stockage",stockage)

			article = Model_Article.objects.get(pk = article_id)
			# print("File: ModuleStock/views.py | Line: 13588 | post_creer_bon_transfert ~ article",article)	

			#Enregistrement des informations de la ligne de bon de transfert
			ligne = Model_Ligne_reception()
			ligne.bon_reception_id = bon_reception.id
			ligne.quantite_demandee = quantite
			ligne.quantite_fait = quantite
			ligne.article_id = article.id
			ligne.unite_id = article.measure_unit.id
			ligne.description = description
			ligne.fait = False
			ligne.stockage_id = stockage.id if stockage else None
			ligne.save()

			no_serie = f'XXX-{article.code}-XXX'
			quantite_recue_bcp = quantite
			quantite_recue = quantite

			#On cherche l'Emplacement dont le type est interne & dont l'article est de type stockable
			if emplacement.type_emplacement.id == 2 and article.type_article.id == 1:
				#On recupere le stockage de l'emplacement d'origine
				stockage = Model_Stockage.objects.filter(article_id = article_id, emplacement_id = emplacement.id).first()
				print(" File: ModuleStock/views.py | Line: 1188 | post_creer_bon_reception ~ stockage",stockage)
				print('Check Stackage')

				#Ici on recupere le stock actuelle et on fait la reduction de la quantité
				if stockage:
					#Le cas ou le stock existe déjà, on fait la mise à jour
					qi_dest = stockage.quantite
					stockage.quantite += quantite
					stockage.save()
				else:
					#Le cas ou le stock n'existe pas, on cree un nouveau stock, puis on affecte les elements et la quantité
					qi_dest = 0
					stockage = Model_Stockage()
					stockage.emplacement_id = emplacement.id
					stockage.article_id = article.id
					stockage.quantite = quantite
					stockage.unite_id = article.measure_unit.id
					stockage.societe_id = societe_id
					stockage.save()

				serie = Model_Actif.objects.filter(article_id = article.id, numero_serie__iexact = no_serie).first()
				if serie:
					# print(f'step 5')
					serie.emplacement_id = emplacement.id
					serie.est_actif = True
					serie.save()
				else:
					# if reception.operation_parent == None:
					# print(f'step 6')
					serie = Model_Actif()
					serie.article_id = article.id
					serie.emplacement_id = emplacement.id
					serie.numero_serie = no_serie
					serie.societe_id = societe_id
					serie.save()
				data_series.append(serie)
				ligne.series.add(serie)

				#On enregistre ce mouvement de Stock
				mvt = Model_Mvt_stock()
				mvt.type_id = 1
				mvt.article_id = article.id
				mvt.emplacement_id = emplacement.id
				mvt.reception_id = bon_reception.id
				mvt.quantite_initiale = qi_dest
				mvt.unite_initiale_id = article.measure_unit.id
				mvt.quantite = quantite
				mvt.unite_id = article.measure_unit.id
				mvt.document = code_ligne
				mvt.auteur_id = auteur.id
				mvt.ajustement_id = None
				mvt.rebut_id = None
				mvt.societe_id = societe_id
				mvt.save()

				mvt.series.add(serie)

			##Dans ce cas, comme les articles ne sont pas stockable, on enregistre simplement les mouvement d'approvisionnement effectué
			else:
				#On enregistre ce mouvement de Stock
				mvt = Model_Mvt_stock()
				mvt.type_id = 1
				mvt.article_id = article.id
				mvt.emplacement_id = bon_reception.emplacement_destination.id
				mvt.reception_id = bon_reception.id
				mvt.quantite_initiale = quantite_recue_bcp
				mvt.unite_initiale_id = article.measure_unit.id
				mvt.quantite = quantite_recue
				mvt.unite_id = article.measure_unit.id
				mvt.document = code_ligne
				mvt.auteur_id = auteur.id
				mvt.ajustement_id = None
				mvt.rebut_id = None
				mvt.societe_id = societe_id
				mvt.save()				
					
		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, bon_reception)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : bon_reception.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_bon_reception(request,ref):
	try:
		same_perm_with = 'module_stock_list_bon_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		bon_reception = dao_bon_reception.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(bon_reception.id),'obj': str(bon_reception)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_bon_reception', args=(bon_reception.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_bon_reception(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		bon_reception = auth.toGetWithRules(dao_bon_reception.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if bon_reception == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, bon_reception) 

		context = {
			'title' : "Détails - Bon de Reception : {}".format(bon_reception),
			'model' : bon_reception,
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
		template = loader.get_template('ErpProject/ModuleStock/bon_reception/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_bon_reception'))

def get_modifier_bon_reception(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_bon_reception.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Bon de Reception",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'operation_stocks' : Model_Operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_reception/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_bon_reception(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_bon_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		code = str(request.POST['code'])

		description = str(request.POST['description'])

		date_prevue = str(request.POST['date_prevue'])
		if date_prevue in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		is_formated, date_prevue = checkDateTimeFormat(date_prevue)
		if is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \'Date\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')

		societe_id = makeIntId(request.POST['societe_id'])

		emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		status_id = makeIntId(request.POST['status_id'])

		bon_livraison = request.FILES['bon_livraison'] if 'bon_livraison' in request.FILES else None

		employe_id = makeIntId(request.POST['employe_id'])
		auteur = identite.utilisateur(request)

		bon_reception = dao_bon_reception.toCreate(code = code, description = description, date_prevue = date_prevue, societe_id = societe_id, emplacement_destination_id = emplacement_destination_id, emplacement_origine_id = emplacement_origine_id, operation_stock_id = operation_stock_id, status_id = status_id, bon_livraison = bon_livraison, employe_id = employe_id)
		saved, bon_reception, message = dao_bon_reception.toUpdate(id, bon_reception, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_bon_reception.toListById(bon_reception.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : bon_reception.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_bon_reception(request,ref):
	try:
		same_perm_with = 'module_stock_add_bon_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_bon_reception.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'operation_stocks' : Model_Operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_operation_stocks' : Model_Statut_operation_stock.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'personnes' : Model_Personne.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_reception/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_bon_reception(request,ref):
	try:
		same_perm_with = 'module_stock_list_bon_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		bon_reception = auth.toGetWithRules(dao_bon_reception.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if bon_reception == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Bon de Reception : {}".format(bon_reception),
			'model' : bon_reception,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_bon_reception.html', 'print_bon_reception.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_bon_reception(request):
	try:
		same_perm_with = 'module_stock_add_bon_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_bon_reception')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des bons de receptions",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_reception/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_bon_reception(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_code = makeString(request.POST['code'])
		#print(f'header_code_id: {header_code_id}')

		header_description = makeString(request.POST['description'])
		#print(f'header_description_id: {header_description_id}')

		header_date_prevue = makeString(request.POST['date_prevue'])
		if header_date_prevue in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_date_prevue_id: {header_date_prevue_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_emplacement_destination_id = makeString(request.POST['emplacement_destination_id'])
		#print(f'header_emplacement_destination_id: {header_emplacement_destination_id}')

		header_emplacement_origine_id = makeString(request.POST['emplacement_origine_id'])
		#print(f'header_emplacement_origine_id: {header_emplacement_origine_id}')

		header_operation_stock_id = makeString(request.POST['operation_stock_id'])
		#print(f'header_operation_stock_id: {header_operation_stock_id}')

		header_status_id = makeString(request.POST['status_id'])
		#print(f'header_status_id: {header_status_id}')

		header_employe_id = makeString(request.POST['employe_id'])
		#print(f'header_employe_id: {header_employe_id}')

		for i in df.index:

			code = ''
			if header_code != '': code = makeString(df[header_code][i])

			description = ''
			if header_description != '': description = makeString(df[header_description][i])

			date_prevue = None
			if header_date_prevue != '': date_prevue = df[header_date_prevue][i]
			if date_prevue in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			emplacement_destination_id = None
			if header_emplacement_destination_id != '': emplacement_destination_id = makeIntId(str(df[header_emplacement_destination_id][i]))

			emplacement_origine_id = None
			if header_emplacement_origine_id != '': emplacement_origine_id = makeIntId(str(df[header_emplacement_origine_id][i]))

			operation_stock_id = None
			if header_operation_stock_id != '': operation_stock_id = makeIntId(str(df[header_operation_stock_id][i]))

			status_id = None
			if header_status_id != '': status_id = makeIntId(str(df[header_status_id][i]))

			employe_id = None
			if header_employe_id != '': employe_id = makeIntId(str(df[header_employe_id][i]))

			bon_reception = dao_bon_reception.toCreate(code = code, description = description, date_prevue = date_prevue, societe_id = societe_id, emplacement_destination_id = emplacement_destination_id, emplacement_origine_id = emplacement_origine_id, operation_stock_id = operation_stock_id, status_id = status_id, employe_id = employe_id)
			saved, bon_reception, message = dao_bon_reception.toSave(auteur, bon_reception)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_bon_reception'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# BON_RECEPTION BI CONTROLLERS
def get_bi_bon_reception(request):
	try:
		same_perm_with = 'module_stock_get_generer_bon_reception'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		try:
			view = str(request.GET.get('view','table'))
		except Exception as e:
			view = 'table'

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_bon_reception.toList(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model, 100)

		model_content_type = dao_query_builder.toGetContentTypeByName('model_bon_reception')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)
		champs_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)
		champs_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)
		champs_date = dao_query_builder.toListFieldsDate(model_content_type.id)

		context = {
			'title' : "Analyse des bons de receptions",
			'model' : model,
			'model_id' : model_content_type.id,
			'modele' : Model_Bon_reception(),
			'champs' : champs,
			'champs_nombre' : champs_nombre,
			'champs_date' : champs_date,
			'champs_dimension' : champs_texte,
			'view' : view,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleStock/bon_reception/bi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

# BON_RECEPTION API CONTROLLERS
def get_list_bon_reception(request):
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
		model = dao_bon_reception.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'code' : str(item.code),
				'description' : str(item.description),
				'date_prevue' : item.date_prevue,
				'societe_id' : makeIntId(item.societe_id),
				'emplacement_destination_id' : makeIntId(item.emplacement_destination_id),
				'emplacement_origine_id' : makeIntId(item.emplacement_origine_id),
				'operation_stock_id' : makeIntId(item.operation_stock_id),
				'status_id' : makeIntId(item.status_id),
				'bon_livraison' : item.bon_livraison.url if item.bon_livraison != None else None,
				'employe_id' : makeIntId(item.employe_id),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_bon_reception(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_bon_reception.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'code' : str(model.code),
				'description' : str(model.description),
				'date_prevue' : model.date_prevue,
				'societe_id' : makeIntId(model.societe_id),
				'emplacement_destination_id' : makeIntId(model.emplacement_destination_id),
				'emplacement_origine_id' : makeIntId(model.emplacement_origine_id),
				'operation_stock_id' : makeIntId(model.operation_stock_id),
				'status_id' : makeIntId(model.status_id),
				'bon_livraison' : model.bon_livraison.url if model.bon_livraison != None else None,
				'employe_id' : makeIntId(model.employe_id),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_bon_reception(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		code = ''
		if 'code' in request.POST : code = str(request.POST['code'])

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		date_prevue = ''
		if 'date_prevue' in request.POST : date_prevue = str(request.POST['date_prevue'])
		if date_prevue in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		date_prevue = timezone.datetime(int(date_prevue[6:10]), int(date_prevue[3:5]), int(date_prevue[0:2]), int(date_prevue[11:13]), int(date_prevue[14:16]))

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		emplacement_destination_id = None
		if 'emplacement_destination' in request.POST : emplacement_destination_id = makeIntId(request.POST['emplacement_destination_id'])

		emplacement_origine_id = None
		if 'emplacement_origine' in request.POST : emplacement_origine_id = makeIntId(request.POST['emplacement_origine_id'])

		operation_stock_id = None
		if 'operation_stock' in request.POST : operation_stock_id = makeIntId(request.POST['operation_stock_id'])

		status_id = None
		if 'status' in request.POST : status_id = makeIntId(request.POST['status_id'])

		bon_livraison = request.FILES['bon_livraison'] if 'bon_livraison' in request.FILES else None

		employe_id = None
		if 'employe' in request.POST : employe_id = makeIntId(request.POST['employe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		bon_reception = dao_bon_reception.toCreate(code = code, description = description, date_prevue = date_prevue, societe_id = societe_id, emplacement_destination_id = emplacement_destination_id, emplacement_origine_id = emplacement_origine_id, operation_stock_id = operation_stock_id, status_id = status_id, bon_livraison = bon_livraison, employe_id = employe_id)
		saved, bon_reception, message = dao_bon_reception.toSave(auteur, bon_reception)

		if saved == False: raise Exception(message)

		objet = {
			'id' : bon_reception.id,
			'code' : str(bon_reception.code),
			'description' : str(bon_reception.description),
			'date_prevue' : bon_reception.date_prevue,
			'societe_id' : makeIntId(bon_reception.societe_id),
			'emplacement_destination_id' : makeIntId(bon_reception.emplacement_destination_id),
			'emplacement_origine_id' : makeIntId(bon_reception.emplacement_origine_id),
			'operation_stock_id' : makeIntId(bon_reception.operation_stock_id),
			'status_id' : makeIntId(bon_reception.status_id),
			'bon_livraison' : bon_reception.bon_livraison.url if bon_reception.bon_livraison != None else None,
			'employe_id' : makeIntId(bon_reception.employe_id),
			'statut_id' : makeIntId(bon_reception.statut_id),
			'etat' : str(bon_reception.etat),
			'creation_date' : bon_reception.creation_date,
			'update_date' : bon_reception.update_date,
			'update_by_id' : makeIntId(bon_reception.update_by_id),
			'auteur_id' : makeIntId(bon_reception.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# AJUSTEMENT CONTROLLERS
from ModuleStock.dao.dao_ajustement import dao_ajustement

def get_lister_ajustement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_ajustement.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_ajustement.toListJson(model.object_list),
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
			'title' : "Liste des inventaires",
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
		template = loader.get_template('ErpProject/ModuleStock/ajustement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_ajustement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		categories = Model_Categorie.objects.all()

		articles = Model_Article.objects.filter(type_article = 1)

		context = {
			'title' : "Formulaire d'enregistrement - Inventaire",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Ajustement(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(defaut = True).order_by('-id')[:10],
			'statut_ajustements' : Model_Statut_ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'categories':categories,
			'les_articles': articles,
			'articles ': articles,
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ajustement'))

@transaction.atomic
def post_creer_ajustement(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		reference = dao_ajustement.toGenerateNumeroInv()

		date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		is_formated, date = checkDateTimeFormat(date)
		if is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \'Date\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')

		societe = Model_Societe.objects.get(pk=1)
		societe_id = societe.id

		emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		status_id = 1

		inventaire_de = makeInt(request.POST['inventaire_de'])

		auteur = identite.utilisateur(request)
		articles = ""
		emplac = None
		data = []
		valeur_stock = 0
		print('Defini moi les articles', articles)
		emplac = Model_Emplacement.objects.get(pk=emplacement_id)
		document = f"Inventaire Stockage {emplac.designation} du {date}"

		ajustement = dao_ajustement.toCreate(reference = reference, date = date, societe_id = societe_id, emplacement_id = emplacement_id, status_id = status_id, inventaire_de = inventaire_de, document = document)
		saved, ajustement, message = dao_ajustement.toSave(auteur, ajustement, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ajustement.toListById(ajustement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		qte = 0
		val = 0
		if inventaire_de == 0:
			#On recupere le stockage dont l'empacement est fixé puis on parcours les articles qui sont à l'interieur
			stockage = Model_Stockage.objects.filter(emplacement_id = emplac.id).first()
			if stockage != None:
				les_articles = Model_Article.objects.filter(id = stockage.article.id)
				if les_articles.count() > 0:
					for i in les_articles:
						stockage = Model_Stockage.objects.filter(article_id = i.id, emplacement_id = emplacement_id).order_by('emplacement__designation')
						for it in stockage:
							qte = it.quantite

						#On Enregistre les lignes ajustements
						ligne = Model_Ligne_ajustement()
						ligne.ajustement_id = ajustement.id
						ligne.article_id = i.id
						ligne.quantite_theorique = qte
						ligne.unite_id = i.measure_unit.id
						ligne.save()
						print("  File: ModuleStock/views.py | Line: 4737 | post_creer_ajustement ~ ligne",ligne)
			# articles = Model_Article.objects.filter(type_article_id = 1).order_by('name')
			print('cas 1')
			categorie = None
			article = None
			categories = None
		elif inventaire_de == 1:
			print('cas 2')
			categorie_id = int(request.POST["categorie_id"])
			categorie = Model_Categorie.objects.get(pk=categorie_id)
			articles = Model_Article.objects.filter(category_id = categorie_id, type_article_id = 1).order_by('name')

			#~~Ancienne version de traitement de l'ajustement~~
			for i in articles:
				stockage = Model_Stockage.objects.filter(article_id = i.id, emplacement_id = emplacement_id).order_by('emplacement__designation')
				if not stockage:
					continue
				else:
					for it in stockage:
						qte = it.quantite

					#On Enregistre les lignes ajustements
					ligne = Model_Ligne_ajustement()
					ligne.ajustement_id = ajustement.id
					ligne.article_id = i.id
					ligne.quantite_theorique = qte
					ligne.unite_id = i.measure_unit.id
					ligne.save()
					print("  File: ModuleStock/views.py | Line: 4765 | post_creer_ajustement ~ ligne",ligne)

		elif inventaire_de == 2:
			print('cas 3')
			article_id = int(request.POST["article_id"])
			articles = Model_Article.objects.filter(type_article_id = 1, pk = article_id).order_by('name')
			article = Model_Article.objects.get(pk=article_id)
			categorie = None
			categories = None				

			#~~Ancienne version de traitement de l'ajustement~~
			for i in articles:
				stockage = Model_Stockage.objects.filter(article_id = i.id, emplacement_id = emplacement_id).order_by('emplacement__designation')
				if not stockage:
					continue
				else:
					for it in stockage:
						qte = it.quantite

					#On Enregistre les lignes ajustements
					ligne = Model_Ligne_ajustement()
					ligne.ajustement_id = ajustement.id
					ligne.article_id = i.id
					ligne.quantite_theorique = qte
					ligne.unite_id = i.measure_unit.id
					ligne.save()
					print("  File: ModuleStock/views.py | Line: 4791 | post_creer_ajustement ~ ligne",ligne)


		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, ajustement)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : ajustement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())



def get_select_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_list_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ajustement = dao_ajustement.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(ajustement.id),'obj': str(ajustement)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_ajustement', args=(ajustement.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_ajustement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		data = []

		#*******Filtre sur les règles **********#
		ajustement = auth.toGetWithRules(dao_ajustement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ajustement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		lignes = Model_Ligne_ajustement.objects.filter(ajustement_id = ajustement.id)
		for item in lignes:
			un = []
			un.append(item.article.measure_unit)
			unites = Model_Unite_mesure.objects.all().exclude(pk = item.article.measure_unit.id)
			for i in unites:
				un.append(i)

			itm={
				'ligne' : item,
				'id' : item.id,
				'article_id' : item.article.id,
				'designation' : item.article.name,
				'unites' : un,
				'quantite_theorique' : item.quantite_theorique,
				'quantite_reelle' : item.quantite_reelle,
			}

			data.append(itm)


		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, ajustement) 

		context = {
			'title' : "Détails - Inventaire : {}".format(ajustement),
			'model' : ajustement,
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
			'lignes' : data,
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_ajustement'))



@transaction.atomic
def post_cloturer_ajustement(request):
	sid = transaction.savepoint()
	inventaire_id = request.POST['inventaire_id']
	inventaire = Model_Ajustement.objects.get(pk=inventaire_id)
	try:
		same_perm_with = 'module_stock_add_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		
		list_ligne_id = request.POST.getlist('ligne_id', None)
		list_unite_id = request.POST.getlist('unite_id', None)
		list_qte_theorique = request.POST.getlist('qte_theorique', None)
		list_qte_reele = request.POST.getlist('qte_reele', None)

		
		print("File: ModuleStock/views.py | Line: 4901 | post_cloturer_ajustement ~ inventaire",inventaire)

		auteur = identite.utilisateur(request)
		diff = 0

		for i in range(0, len(list_ligne_id)):
			ligne_id = int(list_ligne_id[i])
			unite_id = int(list_unite_id[i])
			qte_th = list_qte_theorique[i]
			qte_th = qte_th.replace(',','.')
			qte_th = makeFloat(qte_th)
			qte_r = makeFloat(list_qte_reele[i])

			#On fait la mise à jour des lignes inventaires
			ligne = Model_Ligne_ajustement.objects.get(pk=ligne_id)
			ligne.quantite_reelle = qte_r
			ligne.quantite_theorique = qte_th
			ligne.unite_id = unite_id
			ligne.fait = True
			ligne.save()
			print("File: ModuleStock/views.py | Line: 4921 | post_cloturer_ajustement ~ ligne",ligne)

			#On fait la mise à jour de la quantite en stock
			emplacement_id = inventaire.emplacement.id
			stockage = Model_Stockage.objects.get(emplacement_id = emplacement_id, article_id = ligne.article.id)
			qi = stockage.quantite
			stockage.quantite = qte_r
			stockage.save()
			print(" File: ModuleStock/views.py | Line: 4929 | post_cloturer_ajustement ~ stockage",stockage)

			quantite_reelle = float(ligne.quantite_reelle)
			quantite_theorique = float(ligne.quantite_theorique)

			mvt = Model_Mvt_stock()
			diff = 0

			if quantite_reelle > quantite_theorique :
				diff = quantite_reelle - quantite_theorique
			elif quantite_reelle < quantite_theorique :
				diff = quantite_theorique - quantite_reelle

			mvt.type_id = 4
			mvt.article_id = ligne.article.id
			mvt.emplacement_id = emplacement_id
			mvt.quantite_initiale = qi
			mvt.unite_initiale_id = ligne.article.measure_unit.id
			mvt.quantite = diff
			mvt.unite_id = ligne.unite.id
			mvt.ajustement_id = inventaire.id
			mvt.auteur_id = auteur.id
			mvt.document = inventaire.reference
			mvt.est_ajustement = True
			mvt.save()
			print("File: ModuleStock/views.py | Line: 4954 | post_cloturer_ajustement ~ mvt",mvt)

		#Mise A jour Status	
		inventaire.status_id = 2
		inventaire.save()

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_stock_detail_ajustement', args=(inventaire.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return auth.toReturnFailed(reverse('module_stock_detail_ajustement', args=(inventaire.id,)))

def get_modifier_ajustement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_ajustement.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Inventaire",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_ajustements' : Model_Statut_ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_ajustement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		reference = str(request.POST['reference'])

		date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		is_formated, date = checkDateTimeFormat(date)
		if is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \'Date\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')

		societe_id = makeIntId(request.POST['societe_id'])

		emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		status_id = makeIntId(request.POST['status_id'])

		inventaire_de = makeInt(request.POST['inventaire_de'])

		document = str(request.POST['document'])
		auteur = identite.utilisateur(request)

		ajustement = dao_ajustement.toCreate(reference = reference, date = date, societe_id = societe_id, emplacement_id = emplacement_id, status_id = status_id, inventaire_de = inventaire_de, document = document)
		saved, ajustement, message = dao_ajustement.toUpdate(id, ajustement, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_ajustement.toListById(ajustement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : ajustement.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_add_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_ajustement.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'statut_ajustements' : Model_Statut_ajustement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_ajustement(request,ref):
	try:
		same_perm_with = 'module_stock_list_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		ajustement = auth.toGetWithRules(dao_ajustement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if ajustement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Inventaire : {}".format(ajustement),
			'model' : ajustement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_ajustement.html', 'print_ajustement.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_ajustement(request):
	try:
		same_perm_with = 'module_stock_add_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_ajustement')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des inventaires",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_ajustement(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_reference = makeString(request.POST['reference'])
		#print(f'header_reference_id: {header_reference_id}')

		header_date = makeString(request.POST['date'])
		if header_date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_date_id: {header_date_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		header_emplacement_id = makeString(request.POST['emplacement_id'])
		if header_emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_emplacement_id: {header_emplacement_id}')

		header_status_id = makeString(request.POST['status_id'])
		#print(f'header_status_id: {header_status_id}')

		header_inventaire_de = makeString(request.POST['inventaire_de'])
		#print(f'header_inventaire_de_id: {header_inventaire_de_id}')

		header_document = makeString(request.POST['document'])
		#print(f'header_document_id: {header_document_id}')

		for i in df.index:

			reference = ''
			if header_reference != '': reference = makeString(df[header_reference][i])

			date = None
			if header_date != '': date = df[header_date][i]
			if date in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			emplacement_id = None
			if header_emplacement_id != '': emplacement_id = makeIntId(str(df[header_emplacement_id][i]))
			if emplacement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

			status_id = None
			if header_status_id != '': status_id = makeIntId(str(df[header_status_id][i]))

			inventaire_de = 0
			if header_inventaire_de != '': inventaire_de = makeInt(df[header_inventaire_de][i])

			document = ''
			if header_document != '': document = makeString(df[header_document][i])

			ajustement = dao_ajustement.toCreate(reference = reference, date = date, societe_id = societe_id, emplacement_id = emplacement_id, status_id = status_id, inventaire_de = inventaire_de, document = document)
			saved, ajustement, message = dao_ajustement.toSave(auteur, ajustement)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# AJUSTEMENT BI CONTROLLERS
def get_bi_ajustement(request):
	try:
		same_perm_with = 'module_stock_get_generer_ajustement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		try:
			view = str(request.GET.get('view','table'))
		except Exception as e:
			view = 'table'

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_ajustement.toList(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model, 100)

		model_content_type = dao_query_builder.toGetContentTypeByName('model_ajustement')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)
		champs_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)
		champs_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)
		champs_date = dao_query_builder.toListFieldsDate(model_content_type.id)

		context = {
			'title' : "Analyse des inventaires",
			'model' : model,
			'model_id' : model_content_type.id,
			'modele' : Model_Ajustement(),
			'champs' : champs,
			'champs_nombre' : champs_nombre,
			'champs_date' : champs_date,
			'champs_dimension' : champs_texte,
			'view' : view,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/bi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

# AJUSTEMENT API CONTROLLERS
def get_list_ajustement(request):
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
		model = dao_ajustement.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'reference' : str(item.reference),
				'date' : item.date,
				'societe_id' : makeIntId(item.societe_id),
				'emplacement_id' : makeIntId(item.emplacement_id),
				'status_id' : makeIntId(item.status_id),
				'inventaire_de' : makeInt(item.inventaire_de),
				'document' : str(item.document),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_ajustement(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_ajustement.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'reference' : str(model.reference),
				'date' : model.date,
				'societe_id' : makeIntId(model.societe_id),
				'emplacement_id' : makeIntId(model.emplacement_id),
				'status_id' : makeIntId(model.status_id),
				'inventaire_de' : makeInt(model.inventaire_de),
				'document' : str(model.document),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_ajustement(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		reference = ''
		if 'reference' in request.POST : reference = str(request.POST['reference'])

		date = ''
		if 'date' in request.POST : date = str(request.POST['date'])
		if date in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		date = timezone.datetime(int(date[6:10]), int(date[3:5]), int(date[0:2]), int(date[11:13]), int(date[14:16]))

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		emplacement_id = None
		if 'emplacement' in request.POST : emplacement_id = makeIntId(request.POST['emplacement_id'])
		if emplacement_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')

		status_id = None
		if 'status' in request.POST : status_id = makeIntId(request.POST['status_id'])

		inventaire_de = 0
		if 'inventaire_de' in request.POST : inventaire_de = makeInt(request.POST['inventaire_de'])

		document = ''
		if 'document' in request.POST : document = str(request.POST['document'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		ajustement = dao_ajustement.toCreate(reference = reference, date = date, societe_id = societe_id, emplacement_id = emplacement_id, status_id = status_id, inventaire_de = inventaire_de, document = document)
		saved, ajustement, message = dao_ajustement.toSave(auteur, ajustement)

		if saved == False: raise Exception(message)

		objet = {
			'id' : ajustement.id,
			'reference' : str(ajustement.reference),
			'date' : ajustement.date,
			'societe_id' : makeIntId(ajustement.societe_id),
			'emplacement_id' : makeIntId(ajustement.emplacement_id),
			'status_id' : makeIntId(ajustement.status_id),
			'inventaire_de' : makeInt(ajustement.inventaire_de),
			'document' : str(ajustement.document),
			'statut_id' : makeIntId(ajustement.statut_id),
			'etat' : str(ajustement.etat),
			'creation_date' : ajustement.creation_date,
			'update_date' : ajustement.update_date,
			'update_by_id' : makeIntId(ajustement.update_by_id),
			'auteur_id' : makeIntId(ajustement.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

# ACTIF CONTROLLERS
from ModuleStock.dao.dao_actif import dao_actif

def get_lister_actif(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		view, query, page, count = utils.get_list_request(request)
		#print(f'view {view} query {query} page {page} count {count}')

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_actif.toList(query,utilisateur), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGetData(model, page, count)

		if request.method == 'POST':
			context = {
				'error' : False,
				'message' : 'Recupération effectuée avec succès',
				'model' : dao_actif.toListJson(model.object_list),
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
			'title' : "Liste des actifs",
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
		template = loader.get_template('ErpProject/ModuleStock/actif/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		if request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())
		else: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_index'))

def get_creer_actif(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : "Formulaire d'enregistrement - Actif",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Actif(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/actif/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_actif'))

@transaction.atomic
def post_creer_actif(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_stock_add_actif'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		numero_serie = str(request.POST['numero_serie'])

		est_actif = True if 'est_actif' in request.POST else False

		emplacement_id = makeIntId(request.POST['emplacement_id'])

		societe_id = makeIntId(request.POST['societe_id'])

		auteur = identite.utilisateur(request)

		actif = dao_actif.toCreate(article_id = article_id, numero_serie = numero_serie, est_actif = est_actif, emplacement_id = emplacement_id, societe_id = societe_id)
		saved, actif, message = dao_actif.toSave(auteur, actif, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_actif.toListById(actif.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Initialisation du workflow
		wkf_task.initializeWorkflow(auteur, actif)

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Enregistrement effectué avec succès',
			'isPopup': isPopup,
			'id' : actif.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_select_actif(request,ref):
	try:
		same_perm_with = 'module_stock_list_actif'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		actif = dao_actif.toGet(ref)

		if 'isPopup' in request.GET:
			popup_response_data = json.dumps({'value': str(actif.id),'obj': str(actif)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		return HttpResponseRedirect(reverse('module_stock_detail_actif', args=(actif.id,)))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_details_actif(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		actif = auth.toGetWithRules(dao_actif.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if actif == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		historique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, actif) 

		context = {
			'title' : "Détails - Actif : {}".format(actif),
			'model' : actif,
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
		template = loader.get_template('ErpProject/ModuleStock/actif/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_actif'))

def get_modifier_actif(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_actif.toGet(ref)
		context = {
			'title' : "Formulaire de mise à jour - Actif",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/actif/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_modifier_actif(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_stock_update_actif'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		numero_serie = str(request.POST['numero_serie'])

		est_actif = True if 'est_actif' in request.POST else False

		emplacement_id = makeIntId(request.POST['emplacement_id'])

		societe_id = makeIntId(request.POST['societe_id'])
		auteur = identite.utilisateur(request)

		actif = dao_actif.toCreate(article_id = article_id, numero_serie = numero_serie, est_actif = est_actif, emplacement_id = emplacement_id, societe_id = societe_id)
		saved, actif, message = dao_actif.toUpdate(id, actif, auteur, request.POST)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_actif.toListById(actif.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		isPopup = 0
		if 'isPopup' in request.POST: isPopup = 1

		transaction.savepoint_commit(sid)
		context = {
			'error' : False,
			'message' : 'Mise à jour effectuée avec succès',
			'isPopup': isPopup,
			'id' : actif.id,
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_dupliquer_actif(request,ref):
	try:
		same_perm_with = 'module_stock_add_actif'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_actif.toGet(ref)
		context = {
			'title' : "Formulaire d'enregistrement",
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'articles' : Model_Article.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : Model_Emplacement.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		}
		template = loader.get_template('ErpProject/ModuleStock/actif/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_imprimer_actif(request,ref):
	try:
		same_perm_with = 'module_stock_list_actif'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		actif = auth.toGetWithRules(dao_actif.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if actif == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : "Détails - Actif : {}".format(actif),
			'model' : actif,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleStock/reporting/print_actif.html', 'print_actif.pdf', context, request)
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

def get_upload_actif(request):
	try:
		same_perm_with = 'module_stock_add_actif'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		model_content_type = dao_query_builder.toGetContentTypeByName('model_actif')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : "Import de la liste des actifs",
			'utilisateur' : utilisateur,
			'champs': champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleStock/actif/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

@transaction.atomic
def post_upload_actif(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT + '/excel/'
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)


		header_article_id = makeString(request.POST['article_id'])
		if header_article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
		#print(f'header_article_id: {header_article_id}')

		header_numero_serie = makeString(request.POST['numero_serie'])
		#print(f'header_numero_serie_id: {header_numero_serie_id}')

		header_est_actif = makeString(request.POST['est_actif'])
		#print(f'header_est_actif_id: {header_est_actif_id}')

		header_emplacement_id = makeString(request.POST['emplacement_id'])
		#print(f'header_emplacement_id: {header_emplacement_id}')

		header_societe_id = makeString(request.POST['societe_id'])
		#print(f'header_societe_id: {header_societe_id}')

		for i in df.index:

			article_id = None
			if header_article_id != '': article_id = makeIntId(str(df[header_article_id][i]))
			if article_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

			numero_serie = ''
			if header_numero_serie != '': numero_serie = makeString(df[header_numero_serie][i])

			est_actif = False
			if header_est_actif != '': est_actif = True if makeString(df[header_est_actif][i]) == 'True' else False

			emplacement_id = None
			if header_emplacement_id != '': emplacement_id = makeIntId(str(df[header_emplacement_id][i]))

			societe_id = None
			if header_societe_id != '': societe_id = makeIntId(str(df[header_societe_id][i]))

			actif = dao_actif.toCreate(article_id = article_id, numero_serie = numero_serie, est_actif = est_actif, emplacement_id = emplacement_id, societe_id = societe_id)
			saved, actif, message = dao_actif.toSave(auteur, actif)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_stock_list_actif'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, traceback.format_exc())

# ACTIF BI CONTROLLERS
def get_bi_actif(request):
	try:
		same_perm_with = 'module_stock_get_generer_actif'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		try:
			view = str(request.GET.get('view','table'))
		except Exception as e:
			view = 'table'

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_actif.toList(), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model, 100)

		model_content_type = dao_query_builder.toGetContentTypeByName('model_actif')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)
		champs_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)
		champs_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)
		champs_date = dao_query_builder.toListFieldsDate(model_content_type.id)

		context = {
			'title' : "Analyse des actifs",
			'model' : model,
			'model_id' : model_content_type.id,
			'modele' : Model_Actif(),
			'champs' : champs,
			'champs_nombre' : champs_nombre,
			'champs_date' : champs_date,
			'champs_dimension' : champs_texte,
			'view' : view,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleStock/actif/bi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc())

# ACTIF API CONTROLLERS
def get_list_actif(request):
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
		model = dao_actif.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'article_id' : makeIntId(item.article_id),
				'numero_serie' : str(item.numero_serie),
				'est_actif' : item.est_actif,
				'emplacement_id' : makeIntId(item.emplacement_id),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'societe_id' : makeIntId(item.societe_id),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'update_by_id' : makeIntId(item.update_by_id),
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

def get_item_actif(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_actif.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'article_id' : makeIntId(model.article_id),
				'numero_serie' : str(model.numero_serie),
				'est_actif' : model.est_actif,
				'emplacement_id' : makeIntId(model.emplacement_id),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'societe_id' : makeIntId(model.societe_id),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'update_by_id' : makeIntId(model.update_by_id),
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

@api_view(['POST'])
@transaction.atomic
def post_create_actif(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		article_id = None
		if 'article' in request.POST : article_id = makeIntId(request.POST['article_id'])
		if article_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')

		numero_serie = ''
		if 'numero_serie' in request.POST : numero_serie = str(request.POST['numero_serie'])

		est_actif = True if 'est_actif' in request.POST else False

		emplacement_id = None
		if 'emplacement' in request.POST : emplacement_id = makeIntId(request.POST['emplacement_id'])

		societe_id = None
		if 'societe' in request.POST : societe_id = makeIntId(request.POST['societe_id'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		actif = dao_actif.toCreate(article_id = article_id, numero_serie = numero_serie, est_actif = est_actif, emplacement_id = emplacement_id, societe_id = societe_id)
		saved, actif, message = dao_actif.toSave(auteur, actif)

		if saved == False: raise Exception(message)

		objet = {
			'id' : actif.id,
			'article_id' : makeIntId(actif.article_id),
			'numero_serie' : str(actif.numero_serie),
			'est_actif' : actif.est_actif,
			'emplacement_id' : makeIntId(actif.emplacement_id),
			'statut_id' : makeIntId(actif.statut_id),
			'etat' : str(actif.etat),
			'societe_id' : makeIntId(actif.societe_id),
			'creation_date' : actif.creation_date,
			'update_date' : actif.update_date,
			'update_by_id' : makeIntId(actif.update_by_id),
			'auteur_id' : makeIntId(actif.auteur_id),
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
		return auth.toReturnApiFailed(request, e, traceback.format_exc())

#RAPPORT ARTICLE EN STOCK
def get_creer_rapport_article(request):
	try:
		same_perm_with = 'module_stock_add_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request,same_perm_with)
		if response != None: return response

		context = {
			'title' : "Article en Stock",
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Article(),
			'devises' : Model_Devise.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
			'emplacements' : dao_emplacement.toList(),
			'articles': Model_Article.objects.all(),
			'categories': Model_Categorie.objects.all(),
			'societes' : Model_Societe.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],
		
		}
		template = loader.get_template('ErpProject/ModuleStock/reporting/article.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_article'))


def get_detail_article_stock(request):
	try:
		same_perm_with = 'module_stock_add_article'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request,same_perm_with)
		if response != None: return response

		emplacement_origine_id = int(request.POST['emplacement_origine_id'])
		inventaire_de = int(request.POST["inventaire_de"])
		checkprint = int(request.POST['print'])

		emplac = None

		if inventaire_de == 0:
			articles = dao_article.toList()
			categorie = None
			article = None
			categories = None

		elif inventaire_de == 1:
			categorie_id = int(request.POST["categorie_id"])
			categorie = Model_Categorie.objects.get(pk=categorie_id)
			articles = Model_Article.objects.filter(categorie_id = categorie_id).order_by('name')
			article = None
			categories = None

		elif inventaire_de == 2:
			article_id = int(request.POST["article_id"])
			articles = Model_Article.objects.filter(pk=article_id).order_by('name')
			article = Model_Article.objects.get(pk=article_id)
			categorie = None
			categories = None

		data = []
		valeur_stock = 0
		if emplacement_origine_id == 0:
			for i in articles:
				stockage = Model_Stockage.objects.filter(article_id = i.id).order_by('emplacement__designation').exclude(quantite = 0)
				if not stockage:
					stockage = None
				else :
					for it in stockage:
						valeur_stock += it.quantite * i.amount
				item = {
					'article' : i,
					'stockage' : stockage,
				}
				data.append(item)
		else:
			emplac = Model_Emplacement.objects.get(pk=emplacement_origine_id)
			for i in articles:
				qte = 0
				val = 0
				stockage = Model_Stockage.objects.filter(article_id = i.id, emplacement_id = emplacement_origine_id).order_by('emplacement__designation').exclude(quantite = 0)
				if not stockage:
					stockage = None
				else:
					for it in stockage:
						valeur_stock += it.quantite * i.amount
						val += it.quantite * i.amount
						qte = it.quantite
				item = {
					'article' : i,
					'stockage' : stockage,
					'qte' : qte,
					'val_inventaire' : val,
				}
				data.append(item)

		context = {
			'sous_modules':sous_modules,
			'title' : "Rapport des Articles en Stock",
			'model' : data,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'emplacement' : emplacement_origine_id,
			'empl' : emplac,
			'valeur_stock' : valeur_stock,

			'emplacement_origine_id' : request.POST['emplacement_origine_id'],
			'inventaire_de' : request.POST["inventaire_de"],
			'categorie_id' : request.POST["categorie_id"],
			'article_id' : request.POST["article_id"],
		}
		if checkprint == 0:
			template = loader.get_template("ErpProject/ModuleStock/reporting/article_item.html")
			return HttpResponse(template.render(context, request))
		else :
			return weasy_print("ErpProject/ModuleStock/reporting/print_rapport_article.html", "Article_en_stock.pdf", context, request)
	except Exception as e:
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_stock_creer_rapport'))
		# return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('module_stock_list_article'))
