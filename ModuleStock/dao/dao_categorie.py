from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_categorie(object):
	name = ''
	short_name = ''
	code = ''
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Categorie.objects.all().order_by('-creation_date')
				return Model_Categorie.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Categorie.objects.filter(Q(name__icontains = query) | Q(short_name__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Categorie.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(short_name__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE CATEGORIE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Categorie.objects.all().order_by('-creation_date')

			return Model_Categorie.objects.filter(Q(name__icontains = query) | Q(short_name__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE CATEGORIE')
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
					'code' : str(item.code),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE CATEGORIE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', short_name = '', code = '', description = '', societe_id = None):
		try:
			categorie = dao_categorie()
			categorie.name = name
			categorie.short_name = short_name
			categorie.code = code
			categorie.description = description
			categorie.societe_id = societe_id
			return categorie
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CATEGORIE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_categorie, request_post = []):
		try:
			categorie  = Model_Categorie()
			if objet_dao_categorie.name != None : categorie.name = objet_dao_categorie.name
			if objet_dao_categorie.short_name != None : categorie.short_name = objet_dao_categorie.short_name
			if objet_dao_categorie.code != None : categorie.code = objet_dao_categorie.code
			if objet_dao_categorie.description != None : categorie.description = objet_dao_categorie.description
			if objet_dao_categorie.societe_id != None : categorie.societe_id = objet_dao_categorie.societe_id
			if auteur != None : categorie.auteur_id = auteur.id

			categorie.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Catégorie [Model_Categorie]'
				utils.history_in_database(data)

			return True, categorie, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA CATEGORIE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_categorie, auteur = None, request_post = []):
		try:
			categorie = Model_Categorie.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_categorie = model_to_dict(categorie)

			categorie.name = objet_dao_categorie.name
			categorie.short_name = objet_dao_categorie.short_name
			categorie.code = objet_dao_categorie.code
			categorie.description = objet_dao_categorie.description
			categorie.societe_id = objet_dao_categorie.societe_id
			if auteur != None : categorie.update_by_id = auteur.id
			categorie.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_categorie, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Catégorie [Model_Categorie]'
				utils.history_in_database(data)

			return True, categorie, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CATEGORIE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Categorie.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Categorie.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			categorie = Model_Categorie.objects.get(pk = id)
			categorie.delete()
			return True
		except Exception as e:
			return False