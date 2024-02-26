from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_commune(object):
	name = ''
	ville_id = None
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Commune.objects.all().order_by('-creation_date')
				return Model_Commune.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Commune.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Commune.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE COMMUNE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Commune.objects.all().order_by('-creation_date')

			return Model_Commune.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE COMMUNE')
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
					'ville' : item.ville.__str__() if item.ville else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE COMMUNE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', ville_id = None, description = '', societe_id = None):
		try:
			commune = dao_commune()
			commune.name = name
			commune.ville_id = ville_id
			commune.description = description
			commune.societe_id = societe_id
			return commune
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA COMMUNE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_commune, request_post = []):
		try:
			commune  = Model_Commune()
			commune.name = objet_dao_commune.name
			if objet_dao_commune.ville_id != None : commune.ville_id = objet_dao_commune.ville_id
			if objet_dao_commune.description != None : commune.description = objet_dao_commune.description
			if objet_dao_commune.societe_id != None : commune.societe_id = objet_dao_commune.societe_id
			if auteur != None : commune.auteur_id = auteur.id

			commune.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Commune [Model_Commune]'
				utils.history_in_database(data)

			return True, commune, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA COMMUNE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_commune, auteur = None, request_post = []):
		try:
			commune = Model_Commune.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_commune = model_to_dict(commune)

			commune.name = objet_dao_commune.name
			commune.ville_id = objet_dao_commune.ville_id
			commune.description = objet_dao_commune.description
			commune.societe_id = objet_dao_commune.societe_id
			if auteur != None : commune.update_by_id = auteur.id
			commune.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_commune, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Commune [Model_Commune]'
				utils.history_in_database(data)

			return True, commune, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA COMMUNE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Commune.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Commune.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			commune = Model_Commune.objects.get(pk = id)
			commune.delete()
			return True
		except Exception as e:
			return False