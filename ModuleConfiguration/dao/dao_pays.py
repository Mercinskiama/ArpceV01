from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_pays(object):
	name = ''
	code = ''
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Pays.objects.all().order_by('-creation_date')
				return Model_Pays.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Pays.objects.filter(Q(name__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Pays.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE PAYS')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Pays.objects.all().order_by('-creation_date')

			return Model_Pays.objects.filter(Q(name__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE PAYS')
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
					'code' : str(item.code),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE PAYS  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', code = '', description = '', societe_id = None):
		try:
			pays = dao_pays()
			pays.name = name
			pays.code = code
			pays.description = description
			pays.societe_id = societe_id
			return pays
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PAYS')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_pays, request_post = []):
		try:
			pays  = Model_Pays()
			pays.name = objet_dao_pays.name
			pays.code = objet_dao_pays.code
			if objet_dao_pays.description != None : pays.description = objet_dao_pays.description
			if objet_dao_pays.societe_id != None : pays.societe_id = objet_dao_pays.societe_id
			if auteur != None : pays.auteur_id = auteur.id

			pays.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Pays [Model_Pays]'
				utils.history_in_database(data)

			return True, pays, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PAYS')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_pays, auteur = None, request_post = []):
		try:
			pays = Model_Pays.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_pays = model_to_dict(pays)

			pays.name = objet_dao_pays.name
			pays.code = objet_dao_pays.code
			pays.description = objet_dao_pays.description
			pays.societe_id = objet_dao_pays.societe_id
			if auteur != None : pays.update_by_id = auteur.id
			pays.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_pays, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Pays [Model_Pays]'
				utils.history_in_database(data)

			return True, pays, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PAYS')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Pays.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Pays.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			pays = Model_Pays.objects.get(pk = id)
			pays.delete()
			return True
		except Exception as e:
			return False