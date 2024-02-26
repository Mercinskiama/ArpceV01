from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_province(object):
	name = ''
	country_id = None
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Province.objects.all().order_by('-creation_date')
				return Model_Province.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Province.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Province.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE PROVINCE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Province.objects.all().order_by('-creation_date')

			return Model_Province.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE PROVINCE')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'name' : str(item.name),
					'country' : item.country.__str__() if item.country else '-',
					'description' : str(item.description),
					'societe' : item.societe.__str__() if item.societe else '-',
					'statut' : item.statut.__str__() if item.statut else '-',
					'etat' : str(item.etat),
					'creation_date' : item.creation_date,
					'update_date' : item.update_date,
					'update_by' : item.update_by.__str__() if item.update_by else '-',
					'auteur' : item.auteur.__str__() if item.auteur else '-',
				}
				listes.append(element)
			return listes
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE PROVINCE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', country_id = None, description = '', societe_id = None):
		try:
			province = dao_province()
			province.name = name
			province.country_id = country_id
			province.description = description
			province.societe_id = societe_id
			return province
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PROVINCE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_province, request_post = []):
		try:
			province  = Model_Province()
			province.name = objet_dao_province.name
			if objet_dao_province.country_id != None : province.country_id = objet_dao_province.country_id
			if objet_dao_province.description != None : province.description = objet_dao_province.description
			if objet_dao_province.societe_id != None : province.societe_id = objet_dao_province.societe_id
			if auteur != None : province.auteur_id = auteur.id

			province.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Province [Model_Province]'
				utils.history_in_database(data)

			return True, province, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PROVINCE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_province, auteur = None, request_post = []):
		try:
			province = Model_Province.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_province = model_to_dict(province)

			province.name = objet_dao_province.name
			province.country_id = objet_dao_province.country_id
			province.description = objet_dao_province.description
			province.societe_id = objet_dao_province.societe_id
			if auteur != None : province.update_by_id = auteur.id
			province.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_province, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Province [Model_Province]'
				utils.history_in_database(data)

			return True, province, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PROVINCE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Province.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Province.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			province = Model_Province.objects.get(pk = id)
			province.delete()
			return True
		except Exception as e:
			return False