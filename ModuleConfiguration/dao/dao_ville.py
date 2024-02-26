from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_ville(object):
	name = ''
	province_id = None
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Ville.objects.all().order_by('-creation_date')
				return Model_Ville.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Ville.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Ville.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE VILLE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Ville.objects.all().order_by('-creation_date')

			return Model_Ville.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE VILLE')
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
					'province' : item.province.__str__() if item.province else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE VILLE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', province_id = None, description = '', societe_id = None):
		try:
			ville = dao_ville()
			ville.name = name
			ville.province_id = province_id
			ville.description = description
			ville.societe_id = societe_id
			return ville
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA VILLE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_ville, request_post = []):
		try:
			ville  = Model_Ville()
			ville.name = objet_dao_ville.name
			if objet_dao_ville.province_id != None : ville.province_id = objet_dao_ville.province_id
			if objet_dao_ville.description != None : ville.description = objet_dao_ville.description
			if objet_dao_ville.societe_id != None : ville.societe_id = objet_dao_ville.societe_id
			if auteur != None : ville.auteur_id = auteur.id

			ville.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Ville [Model_Ville]'
				utils.history_in_database(data)

			return True, ville, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA VILLE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_ville, auteur = None, request_post = []):
		try:
			ville = Model_Ville.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_ville = model_to_dict(ville)

			ville.name = objet_dao_ville.name
			ville.province_id = objet_dao_ville.province_id
			ville.description = objet_dao_ville.description
			ville.societe_id = objet_dao_ville.societe_id
			if auteur != None : ville.update_by_id = auteur.id
			ville.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_ville, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Ville [Model_Ville]'
				utils.history_in_database(data)

			return True, ville, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA VILLE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Ville.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Ville.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			ville = Model_Ville.objects.get(pk = id)
			ville.delete()
			return True
		except Exception as e:
			return False