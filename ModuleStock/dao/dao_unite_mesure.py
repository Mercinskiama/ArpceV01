from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_unite_mesure(object):
	name = ''
	short_name = ''
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Unite_mesure.objects.all().order_by('-creation_date')
				return Model_Unite_mesure.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Unite_mesure.objects.filter(Q(name__icontains = query) | Q(short_name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Unite_mesure.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(short_name__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE UNITE_MESURE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Unite_mesure.objects.all().order_by('-creation_date')

			return Model_Unite_mesure.objects.filter(Q(name__icontains = query) | Q(short_name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE UNITE_MESURE')
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
					'short_name' : str(item.short_name),
					'description' : str(item.description),
					'statut' : item.statut.__str__() if item.statut else '-',
					'etat' : str(item.etat),
					'societe' : item.societe.__str__() if item.societe else '-',
					'creation_date' : item.creation_date,
					'update_date' : item.update_date,
					'update_by' : item.update_by.__str__() if item.update_by else '-',
					'auteur' : item.auteur.__str__() if item.auteur else '-',
				}
				listes.append(element)
			return listes
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE UNITE_MESURE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', short_name = '', description = '', societe_id = None):
		try:
			unite_mesure = dao_unite_mesure()
			unite_mesure.name = name
			unite_mesure.short_name = short_name
			unite_mesure.description = description
			unite_mesure.societe_id = societe_id
			return unite_mesure
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA UNITE_MESURE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_unite_mesure, request_post = []):
		try:
			unite_mesure  = Model_Unite_mesure()
			if objet_dao_unite_mesure.name != None : unite_mesure.name = objet_dao_unite_mesure.name
			if objet_dao_unite_mesure.short_name != None : unite_mesure.short_name = objet_dao_unite_mesure.short_name
			if objet_dao_unite_mesure.description != None : unite_mesure.description = objet_dao_unite_mesure.description
			if objet_dao_unite_mesure.societe_id != None : unite_mesure.societe_id = objet_dao_unite_mesure.societe_id
			if auteur != None : unite_mesure.auteur_id = auteur.id

			unite_mesure.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Unité de mesure [Model_Unite_mesure]'
				utils.history_in_database(data)

			return True, unite_mesure, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA UNITE_MESURE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_unite_mesure, auteur = None, request_post = []):
		try:
			unite_mesure = Model_Unite_mesure.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_unite_mesure = model_to_dict(unite_mesure)

			unite_mesure.name = objet_dao_unite_mesure.name
			unite_mesure.short_name = objet_dao_unite_mesure.short_name
			unite_mesure.description = objet_dao_unite_mesure.description
			unite_mesure.societe_id = objet_dao_unite_mesure.societe_id
			if auteur != None : unite_mesure.update_by_id = auteur.id
			unite_mesure.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_unite_mesure, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Unité de mesure [Model_Unite_mesure]'
				utils.history_in_database(data)

			return True, unite_mesure, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA UNITE_MESURE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Unite_mesure.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Unite_mesure.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			unite_mesure = Model_Unite_mesure.objects.get(pk = id)
			unite_mesure.delete()
			return True
		except Exception as e:
			return False