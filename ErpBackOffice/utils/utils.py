from django.utils import timezone
import random
import string
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
import urllib	
from ModuleSupport.dao.dao_historique_action import dao_historique_action
from django.urls import resolve
from ModuleSupport.dao.dao_log import dao_log	
from sys import platform
import os

class utils(object):
		
	@staticmethod
	def remove_duplicate_in_list(the_list):
		new_list = []
		for i in the_list:
			if i not in new_list:
				new_list.append(i)
		return new_list

	@staticmethod
	def get_list_request(request):
		try:
			if request.method == 'POST': view = str(request.POST.get('view','list'))
			else: view = str(request.GET.get('view','list'))
		except Exception as e: view = 'list'
   
		try:
			if request.method == 'POST': query = str(request.POST.get('q',''))
			else: query = str(request.GET.get('q',''))
		except Exception as e: query = ''

		try:
			if request.method == 'POST': page = int(request.POST.get("page",1))
			else: page = int(request.GET.get("page",1))
		except Exception as e: page = 1 
   
		try:
			if request.method == 'POST': count = int(request.POST.get("count",10))
			else: count = int(request.GET.get("count",50))
		except Exception as e: count = 50
  
		return view, query, page, count


	@staticmethod
	def write_log_in_database(data):
		user = data['auteur']
		model = data['modele']
		erreur_log = data['erreur']
		log = dao_log.toCreate(erreur_log,model,user)
		dao_log.toSave(log)
		return True
	
	@staticmethod
	def history_in_database(data):
		historique = dao_historique_action.toCreate(data['auteur'],data['valeur_avant'],data['valeur_apres'],data['modele'])
		dao_historique_action.toSave(historique)
		return True

	@staticmethod
	def format_path(path):
		path = path.replace('\\', os.path.sep) 
		return path

