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
from rest_framework.decorators import api_view
import base64, uuid
from locale import atof, setlocale, LC_NUMERIC
import numpy as np
from dateutil.relativedelta import relativedelta
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
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
from ErpBackOffice.utils.pagination import pagination
from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.wkf_task import wkf_task
from ErpBackOffice.utils.endpoint import endpoint
from ErpBackOffice.utils.print import weasy_print
from ErpBackOffice.dao.dao_query_builder import dao_query_builder


#LOGGING
import logging, inspect, unidecode
from ModuleArchivage.models import *
monLog = logging.getLogger("logger")
module= "ModuleArchivage"
var_module_id = 7
vars_module = {"name" : "MODULE_ARCHIVAGE", "value" : 97 }


def get_index(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(var_module_id, request)
		if response != None:
			return response

		context = {
			"title" : "Tableau de Bord",
			"utilisateur" : utilisateur,
			"organisation": dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			"module" : vars_module
		}

		template = loader.get_template("ErpProject/ModuleArchivage/index.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

# DOCUMENT CONTROLLERS
from ModuleArchivage.dao.dao_document import dao_document

def get_lister_document(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
		except Exception as e:
			view = 'list'
			query = ''

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_document.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des documents',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_document(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Document',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Document(),
			'dossiers' : Model_Dossier.objects.all(),
			'contenttypes' : ContentType.objects.all(),
			'personnes' : Model_Personne.objects.all(),
			'tags' : Model_Tag.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_document(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_archivage_add_document'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		type = makeInt(request.POST['type'])

		taille = makeInt(request.POST['taille'])

		type_mime = makeInt(request.POST['type_mime'])

		mime = str(request.POST['mime'])
		if mime in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Mime\' est obligatoire, Veuillez le renseigner SVP!')

		dossier_id = makeIntId(request.POST['dossier_id'])

		res_model_id = makeIntId(request.POST['res_model_id'])

		res_field = str(request.POST['res_field'])

		res_id = makeInt(request.POST['res_id'])

		est_public = True if 'est_public' in request.POST else False

		est_archive = True if 'est_archive' in request.POST else False

		est_bloque = True if 'est_bloque' in request.POST else False

		auteur_blocage_id = makeIntId(request.POST['auteur_blocage_id'])

		access_token = str(request.POST['access_token'])

		url = str(request.POST['url'])

		description = str(request.POST['description'])

		indexation = str(request.POST['indexation'])

		fichier = request.FILES['fichier'] if 'fichier' in request.FILES else None

		miniature = request.FILES['miniature'] if 'miniature' in request.FILES else None

		tags = request.POST.getlist('tags', None)

		favoris = request.POST.getlist('favoris', None)

		auteur = identite.utilisateur(request)

		document = dao_document.toCreate(designation = designation, type = type, taille = taille, type_mime = type_mime, mime = mime, dossier_id = dossier_id, res_model_id = res_model_id, res_field = res_field, res_id = res_id, est_public = est_public, est_archive = est_archive, est_bloque = est_bloque, auteur_blocage_id = auteur_blocage_id, access_token = access_token, url = url, description = description, indexation = indexation, fichier = fichier, miniature = miniature, tags = tags, favoris = favoris)
		saved, document, message = dao_document.toSave(auteur, document)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_document.toListById(document.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(document.id),'obj': str(document)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_document', args=(document.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_document(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		document = auth.toGetWithRules(dao_document.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if document == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Document : {}'.format(document),
			'model' : document,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_archivage_list_document'))

def get_modifier_document(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_document.toGet(ref)
		context = {
			'title' : 'Modifier Document',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossiers' : Model_Dossier.objects.all(),
			'contenttypes' : ContentType.objects.all(),
			'personnes' : Model_Personne.objects.all(),
			'tags' : Model_Tag.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_document(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_archivage_update_document'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		type = makeInt(request.POST['type'])

		taille = makeInt(request.POST['taille'])

		type_mime = makeInt(request.POST['type_mime'])

		mime = str(request.POST['mime'])
		if mime in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Mime\' est obligatoire, Veuillez le renseigner SVP!')

		dossier_id = makeIntId(request.POST['dossier_id'])

		res_model_id = makeIntId(request.POST['res_model_id'])

		res_field = str(request.POST['res_field'])

		res_id = makeInt(request.POST['res_id'])

		est_public = True if 'est_public' in request.POST else False

		est_archive = True if 'est_archive' in request.POST else False

		est_bloque = True if 'est_bloque' in request.POST else False

		auteur_blocage_id = makeIntId(request.POST['auteur_blocage_id'])

		access_token = str(request.POST['access_token'])

		url = str(request.POST['url'])

		description = str(request.POST['description'])

		indexation = str(request.POST['indexation'])

		fichier = request.FILES['fichier'] if 'fichier' in request.FILES else None

		miniature = request.FILES['miniature'] if 'miniature' in request.FILES else None

		tags = request.POST.getlist('tags', None)

		favoris = request.POST.getlist('favoris', None)
		auteur = identite.utilisateur(request)

		document = dao_document.toCreate(designation = designation, type = type, taille = taille, type_mime = type_mime, mime = mime, dossier_id = dossier_id, res_model_id = res_model_id, res_field = res_field, res_id = res_id, est_public = est_public, est_archive = est_archive, est_bloque = est_bloque, auteur_blocage_id = auteur_blocage_id, access_token = access_token, url = url, description = description, indexation = indexation, fichier = fichier, miniature = miniature, tags = tags, favoris = favoris)
		saved, document, message = dao_document.toUpdate(id, document)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_document.toListById(document.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_document', args=(document.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_document(request,ref):
	try:
		same_perm_with = 'module_archivage_add_document'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_document.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossiers' : Model_Dossier.objects.all(),
			'contenttypes' : ContentType.objects.all(),
			'personnes' : Model_Personne.objects.all(),
			'tags' : Model_Tag.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_document(request,ref):
	try:
		same_perm_with = 'module_archivage_list_document'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		document = auth.toGetWithRules(dao_document.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if document == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Document : {}'.format(document),
			'model' : document,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleArchivage/reporting/print_document.html', 'print_document.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_document(request):
	try:
		same_perm_with = 'module_archivage_add_document'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des documents',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_document(request):
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

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			type = makeInt(df['type'][i])
			taille = makeInt(df['taille'][i])
			type_mime = makeInt(df['type_mime'][i])
			mime = str(df['mime'][i])
			if mime in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Mime\' est obligatoire, Veuillez le renseigner SVP!')
			dossier_id = makeIntId(str(df['dossier_id'][i]))
			res_model_id = makeIntId(str(df['res_model_id'][i]))
			res_field = str(df['res_field'][i])
			res_id = makeInt(df['res_id'][i])
			est_public = True if str(df['est_public'][i]) == 'True' else False
			est_archive = True if str(df['est_archive'][i]) == 'True' else False
			est_bloque = True if str(df['est_bloque'][i]) == 'True' else False
			auteur_blocage_id = makeIntId(str(df['auteur_blocage_id'][i]))
			access_token = str(df['access_token'][i])
			url = str(df['url'][i])
			description = str(df['description'][i])
			indexation = str(df['indexation'][i])

			document = dao_document.toCreate(designation = designation, type = type, taille = taille, type_mime = type_mime, mime = mime, dossier_id = dossier_id, res_model_id = res_model_id, res_field = res_field, res_id = res_id, est_public = est_public, est_archive = est_archive, est_bloque = est_bloque, auteur_blocage_id = auteur_blocage_id, access_token = access_token, url = url, description = description, indexation = indexation)
			saved, document, message = dao_document.toSave(auteur, document)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_list_document'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# DOCUMENT REPORTING CONTROLLERS
def get_generer_document(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Rapport document',
			'devises' : dao_devise.toListDevisesActives(),
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document/generate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def post_traiter_document(request, utilisateur = None, modules = [], sous_modules = [], enum_module = vars_module):
	#On recupère et format les inputs reçus
	date_debut = request.POST['date_debut']
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST['date_fin']
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#On récupère les données suivant le filtre défini
	model = Model_Document.objects.filter(creation_date__range = [date_debut, date_fin]).order_by('-creation_date')

	context = {
		'title' : 'Rapport Document',
		'model' : model,
		'date_debut' : request.POST['date_debut'],
		'date_fin' : request.POST['date_fin'],
		'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : enum_module,
		'organisation' : dao_organisation.toGetMainOrganisation(),
	}
	return context

def post_generer_document(request):
	try:
		same_perm_with = 'module_archivage_get_generer_document'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = post_traiter_document(request, utilisateur, modules, sous_modules)
		template = loader.get_template('ErpProject/ModuleArchivage/document/generated.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def post_imprimer_rapport_document(request):
	try:
		context = post_traiter_document(request)
		return weasy_print('ErpProject/ModuleArchivage/reporting/rapport_document.html', 'rapport_document.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_archivage_get_generer_document'))

# DOSSIER CONTROLLERS
from ModuleArchivage.dao.dao_dossier import dao_dossier

def get_lister_dossier(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
		except Exception as e:
			view = 'list'
			query = ''

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_dossier.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des dossiers',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleArchivage/dossier/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_dossier(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Dossier',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Dossier(),
			'dossiers' : Model_Dossier.objects.all(),
			'groupepermissions' : Model_GroupePermission.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/dossier/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_dossier(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_archivage_add_dossier'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		sequence = str(request.POST['sequence'])

		parent_id = makeIntId(request.POST['parent_id'])

		description = str(request.POST['description'])

		owner_read = True if 'owner_read' in request.POST else False

		est_racine = True if 'est_racine' in request.POST else False

		est_archivage = True if 'est_archivage' in request.POST else False

		write_groups = request.POST.getlist('write_groups', None)

		read_groups = request.POST.getlist('read_groups', None)

		auteur = identite.utilisateur(request)

		dossier = dao_dossier.toCreate(designation = designation, sequence = sequence, parent_id = parent_id, description = description, owner_read = owner_read, est_racine = est_racine, est_archivage = est_archivage, write_groups = write_groups, read_groups = read_groups)
		saved, dossier, message = dao_dossier.toSave(auteur, dossier)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_dossier.toListById(dossier.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Ajout Champ (OneToMany - Creation)
		categorie_tag_dossier_ids = request.POST.getlist('categorie_tag_dossier_ids', [])
		for i in range(0, len(categorie_tag_dossier_ids)):
			try:
				objet = Model_Categorie_tag.objects.get(pk = categorie_tag_dossier_ids[i])
				objet.dossier = dossier
				objet.save()
			except Exception as e: pass

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(dossier.id),'obj': str(dossier)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_dossier', args=(dossier.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_dossier(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		dossier = auth.toGetWithRules(dao_dossier.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if dossier == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Dossier : {}'.format(dossier),
			'model' : dossier,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/dossier/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_archivage_list_dossier'))

def get_modifier_dossier(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_dossier.toGet(ref)
		context = {
			'title' : 'Modifier Dossier',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossiers' : Model_Dossier.objects.all(),
			'groupepermissions' : Model_GroupePermission.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/dossier/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_dossier(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_archivage_update_dossier'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		sequence = str(request.POST['sequence'])

		parent_id = makeIntId(request.POST['parent_id'])

		description = str(request.POST['description'])

		owner_read = True if 'owner_read' in request.POST else False

		est_racine = True if 'est_racine' in request.POST else False

		est_archivage = True if 'est_archivage' in request.POST else False

		write_groups = request.POST.getlist('write_groups', None)

		read_groups = request.POST.getlist('read_groups', None)
		auteur = identite.utilisateur(request)

		dossier = dao_dossier.toCreate(designation = designation, sequence = sequence, parent_id = parent_id, description = description, owner_read = owner_read, est_racine = est_racine, est_archivage = est_archivage, write_groups = write_groups, read_groups = read_groups)
		saved, dossier, message = dao_dossier.toUpdate(id, dossier)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_dossier.toListById(dossier.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		#MAJ Champ (OneToMany - Modification)
		categorie_tag_dossier_ids = request.POST.getlist('categorie_tag_dossier_ids', [])
		dossier.categorie_tags.all().update(dossier = None)
		for i in range(0, len(categorie_tag_dossier_ids)):
			try:
				objet = Model_Categorie_tag.objects.get(pk = categorie_tag_dossier_ids[i])
				objet.dossier = dossier
				objet.save()
			except Exception as e: pass

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_dossier', args=(dossier.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_dossier(request,ref):
	try:
		same_perm_with = 'module_archivage_add_dossier'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_dossier.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossiers' : Model_Dossier.objects.all(),
			'groupepermissions' : Model_GroupePermission.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/dossier/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_dossier(request,ref):
	try:
		same_perm_with = 'module_archivage_list_dossier'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		dossier = auth.toGetWithRules(dao_dossier.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if dossier == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Dossier : {}'.format(dossier),
			'model' : dossier,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleArchivage/reporting/print_dossier.html', 'print_dossier.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_dossier(request):
	try:
		same_perm_with = 'module_archivage_add_dossier'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response
  
		model_content_type = dao_query_builder.toGetContentTypeByName('model_dossier')
		champs = dao_query_builder.toListFieldOfModel(model_content_type.id)

		context = {
			'title' : 'Import de la liste des dossiers',
			'utilisateur' : utilisateur,
			'champs' : champs,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/dossier/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_dossier(request):
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

		df = pd.read_excel(io=file_name, sheet_name=sheet, engine='openpyxl')
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

			sequence = str(df['sequence'][i])
			parent_id = makeIntId(str(df['parent_id'][i]))
			description = str(df['description'][i])
			owner_read = True if str(df['owner_read'][i]) == 'True' else False
			est_racine = True if str(df['est_racine'][i]) == 'True' else False
			est_archivage = True if str(df['est_archivage'][i]) == 'True' else False

			dossier = dao_dossier.toCreate(designation = designation, sequence = sequence, parent_id = parent_id, description = description, owner_read = owner_read, est_racine = est_racine, est_archivage = est_archivage)
			saved, dossier, message = dao_dossier.toSave(auteur, dossier)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_list_dossier'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# CATEGORIE_TAG CONTROLLERS
from ModuleArchivage.dao.dao_categorie_tag import dao_categorie_tag

def get_lister_categorie_tag(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
		except Exception as e:
			view = 'list'
			query = ''

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_categorie_tag.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des catégories d\'étiquette',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleArchivage/categorie_tag/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_categorie_tag(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Catégorie d\'étiquette',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Categorie_tag(),
			'dossiers' : Model_Dossier.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/categorie_tag/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_categorie_tag(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_archivage_add_categorie_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		code = str(request.POST['code'])

		description = str(request.POST['description'])

		dossier_id = makeIntId(request.POST['dossier_id'])

		auteur = identite.utilisateur(request)

		categorie_tag = dao_categorie_tag.toCreate(designation = designation, code = code, description = description, dossier_id = dossier_id)
		saved, categorie_tag, message = dao_categorie_tag.toSave(auteur, categorie_tag)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_categorie_tag.toListById(categorie_tag.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Ajout Champ (OneToMany - Creation)
		tag_categorie_ids = request.POST.getlist('tag_categorie_ids', [])
		for i in range(0, len(tag_categorie_ids)):
			try:
				objet = Model_Tag.objects.get(pk = tag_categorie_ids[i])
				objet.categorie = categorie_tag
				objet.save()
			except Exception as e: pass

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(categorie_tag.id),'obj': str(categorie_tag)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_categorie_tag', args=(categorie_tag.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_categorie_tag(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		categorie_tag = auth.toGetWithRules(dao_categorie_tag.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if categorie_tag == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Catégorie d\'étiquette : {}'.format(categorie_tag),
			'model' : categorie_tag,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/categorie_tag/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_archivage_list_categorie_tag'))

def get_modifier_categorie_tag(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_categorie_tag.toGet(ref)
		context = {
			'title' : 'Modifier Catégorie d\'étiquette',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossiers' : Model_Dossier.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/categorie_tag/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_categorie_tag(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_archivage_update_categorie_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		code = str(request.POST['code'])

		description = str(request.POST['description'])

		dossier_id = makeIntId(request.POST['dossier_id'])
		auteur = identite.utilisateur(request)

		categorie_tag = dao_categorie_tag.toCreate(designation = designation, code = code, description = description, dossier_id = dossier_id)
		saved, categorie_tag, message = dao_categorie_tag.toUpdate(id, categorie_tag)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_categorie_tag.toListById(categorie_tag.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		#MAJ Champ (OneToMany - Modification)
		tag_categorie_ids = request.POST.getlist('tag_categorie_ids', [])
		categorie_tag.tags_categorie.all().update(categorie = None)
		for i in range(0, len(tag_categorie_ids)):
			try:
				objet = Model_Tag.objects.get(pk = tag_categorie_ids[i])
				objet.categorie = categorie_tag
				objet.save()
			except Exception as e: pass

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_categorie_tag', args=(categorie_tag.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_categorie_tag(request,ref):
	try:
		same_perm_with = 'module_archivage_add_categorie_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_categorie_tag.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossiers' : Model_Dossier.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/categorie_tag/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_categorie_tag(request,ref):
	try:
		same_perm_with = 'module_archivage_list_categorie_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		categorie_tag = auth.toGetWithRules(dao_categorie_tag.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if categorie_tag == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Catégorie d\'étiquette : {}'.format(categorie_tag),
			'model' : categorie_tag,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleArchivage/reporting/print_categorie_tag.html', 'print_categorie_tag.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_categorie_tag(request):
	try:
		same_perm_with = 'module_archivage_add_categorie_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des catégories d\'étiquette',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/categorie_tag/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_categorie_tag(request):
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

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			code = str(df['code'][i])
			description = str(df['description'][i])
			dossier_id = makeIntId(str(df['dossier_id'][i]))

			categorie_tag = dao_categorie_tag.toCreate(designation = designation, code = code, description = description, dossier_id = dossier_id)
			saved, categorie_tag, message = dao_categorie_tag.toSave(auteur, categorie_tag)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_list_categorie_tag'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# TAG CONTROLLERS
from ModuleArchivage.dao.dao_tag import dao_tag

def get_lister_tag(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
		except Exception as e:
			view = 'list'
			query = ''

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_tag.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des etiquettes',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleArchivage/tag/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_tag(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Etiquette',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Tag(),
			'categorie_tags' : Model_Categorie_tag.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/tag/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_tag(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_archivage_add_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		code = str(request.POST['code'])

		categorie_id = makeIntId(request.POST['categorie_id'])

		couleur = str(request.POST['couleur'])

		description = str(request.POST['description'])

		auteur = identite.utilisateur(request)

		tag = dao_tag.toCreate(designation = designation, code = code, categorie_id = categorie_id, couleur = couleur, description = description)
		saved, tag, message = dao_tag.toSave(auteur, tag)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_tag.toListById(tag.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(tag.id),'obj': str(tag)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_tag', args=(tag.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_tag(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		tag = auth.toGetWithRules(dao_tag.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if tag == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Etiquette : {}'.format(tag),
			'model' : tag,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/tag/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_archivage_list_tag'))

def get_modifier_tag(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_tag.toGet(ref)
		context = {
			'title' : 'Modifier Etiquette',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'categorie_tags' : Model_Categorie_tag.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/tag/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_tag(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_archivage_update_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		code = str(request.POST['code'])

		categorie_id = makeIntId(request.POST['categorie_id'])

		couleur = str(request.POST['couleur'])

		description = str(request.POST['description'])
		auteur = identite.utilisateur(request)

		tag = dao_tag.toCreate(designation = designation, code = code, categorie_id = categorie_id, couleur = couleur, description = description)
		saved, tag, message = dao_tag.toUpdate(id, tag)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_tag.toListById(tag.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_tag', args=(tag.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_tag(request,ref):
	try:
		same_perm_with = 'module_archivage_add_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_tag.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'categorie_tags' : Model_Categorie_tag.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/tag/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_tag(request,ref):
	try:
		same_perm_with = 'module_archivage_list_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		tag = auth.toGetWithRules(dao_tag.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if tag == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Etiquette : {}'.format(tag),
			'model' : tag,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleArchivage/reporting/print_tag.html', 'print_tag.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_tag(request):
	try:
		same_perm_with = 'module_archivage_add_tag'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des etiquettes',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/tag/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_tag(request):
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

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			code = str(df['code'][i])
			categorie_id = makeIntId(str(df['categorie_id'][i]))
			couleur = str(df['couleur'][i])
			description = str(df['description'][i])

			tag = dao_tag.toCreate(designation = designation, code = code, categorie_id = categorie_id, couleur = couleur, description = description)
			saved, tag, message = dao_tag.toSave(auteur, tag)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_list_tag'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# DOCUMENT_PARTAGE CONTROLLERS
from ModuleArchivage.dao.dao_document_partage import dao_document_partage

def get_lister_document_partage(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
		except Exception as e:
			view = 'list'
			query = ''

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_document_partage.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des liens partagés',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document_partage/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_document_partage(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Lien partagé',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Document_partage(),
			'documents' : Model_Document.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document_partage/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_document_partage(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_archivage_add_document_partage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		type = makeInt(request.POST['type'])

		url = str(request.POST['url'])

		date_echeance = str(request.POST['date_echeance'])
		date_echeance = timezone.datetime(int(date_echeance[6:10]), int(date_echeance[3:5]), int(date_echeance[0:2]), int(date_echeance[11:13]), int(date_echeance[14:16]))

		description = str(request.POST['description'])

		documents = request.POST.getlist('documents', None)

		auteur = identite.utilisateur(request)

		document_partage = dao_document_partage.toCreate(designation = designation, type = type, url = url, date_echeance = date_echeance, description = description, documents = documents)
		saved, document_partage, message = dao_document_partage.toSave(auteur, document_partage)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_document_partage.toListById(document_partage.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(document_partage.id),'obj': str(document_partage)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_document_partage', args=(document_partage.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_document_partage(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		document_partage = auth.toGetWithRules(dao_document_partage.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if document_partage == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Lien partagé : {}'.format(document_partage),
			'model' : document_partage,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document_partage/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_archivage_list_document_partage'))

def get_modifier_document_partage(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_document_partage.toGet(ref)
		context = {
			'title' : 'Modifier Lien partagé',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'documents' : Model_Document.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document_partage/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_document_partage(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_archivage_update_document_partage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		type = makeInt(request.POST['type'])

		url = str(request.POST['url'])

		date_echeance = str(request.POST['date_echeance'])
		date_echeance = timezone.datetime(int(date_echeance[6:10]), int(date_echeance[3:5]), int(date_echeance[0:2]), int(date_echeance[11:13]), int(date_echeance[14:16]))

		description = str(request.POST['description'])

		documents = request.POST.getlist('documents', None)
		auteur = identite.utilisateur(request)

		document_partage = dao_document_partage.toCreate(designation = designation, type = type, url = url, date_echeance = date_echeance, description = description, documents = documents)
		saved, document_partage, message = dao_document_partage.toUpdate(id, document_partage)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_document_partage.toListById(document_partage.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_detail_document_partage', args=(document_partage.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_document_partage(request,ref):
	try:
		same_perm_with = 'module_archivage_add_document_partage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_document_partage.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'documents' : Model_Document.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document_partage/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_document_partage(request,ref):
	try:
		same_perm_with = 'module_archivage_list_document_partage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		document_partage = auth.toGetWithRules(dao_document_partage.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if document_partage == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Lien partagé : {}'.format(document_partage),
			'model' : document_partage,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleArchivage/reporting/print_document_partage.html', 'print_document_partage.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_document_partage(request):
	try:
		same_perm_with = 'module_archivage_add_document_partage'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des liens partagés',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleArchivage/document_partage/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_document_partage(request):
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

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			type = makeInt(df['type'][i])
			url = str(df['url'][i])
			date_echeance = str(df['date_echeance'][i])
			date_echeance = timezone.datetime(int(date_echeance[6:10]), int(date_echeance[3:5]), int(date_echeance[0:2]), int(date_echeance[11:13]), int(date_echeance[14:16]))
			description = str(df['description'][i])

			document_partage = dao_document_partage.toCreate(designation = designation, type = type, url = url, date_echeance = date_echeance, description = description)
			saved, document_partage, message = dao_document_partage.toSave(auteur, document_partage)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_archivage_list_document_partage'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)