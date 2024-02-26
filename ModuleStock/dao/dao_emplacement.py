from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_emplacement(object):
	designation = ''
	designation_court = ''
	code = ''
	description = ''
	type_emplacement_id = None
	defaut = False
	societe_id = None
	visible = False

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Emplacement.objects.filter(visible = True).order_by('-creation_date')
				return Model_Emplacement.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Emplacement.objects.filter(Q(designation__icontains = query) | Q(designation_court__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Emplacement.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(designation__icontains = query) | Q(designation_court__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE EMPLACEMENT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Emplacement.objects.all().order_by('-creation_date')

			return Model_Emplacement.objects.filter(Q(designation__icontains = query) | Q(designation_court__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE EMPLACEMENT')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'designation' : str(item.designation),
					'designation_court' : str(item.designation_court),
					'code' : str(item.code),
					'description' : str(item.description),
					'type_emplacement' : item.type_emplacement.__str__() if item.type_emplacement else '-',
					'defaut' : item.defaut,
					'societe' : item.societe.__str__() if item.societe else '-',
					'visible' : item.visible,
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE EMPLACEMENT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', designation_court = '', code = '', description = '', type_emplacement_id = None, defaut = False, societe_id = None, visible = False):
		try:
			emplacement = dao_emplacement()
			emplacement.designation = designation
			emplacement.designation_court = designation_court
			emplacement.code = code
			emplacement.description = description
			emplacement.type_emplacement_id = type_emplacement_id
			emplacement.defaut = defaut
			emplacement.societe_id = societe_id
			emplacement.visible = visible
			return emplacement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA EMPLACEMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_emplacement, request_post = []):
		try:
			emplacement  = Model_Emplacement()
			if objet_dao_emplacement.designation != None : emplacement.designation = objet_dao_emplacement.designation
			if objet_dao_emplacement.designation_court != None : emplacement.designation_court = objet_dao_emplacement.designation_court
			if objet_dao_emplacement.code != None : emplacement.code = objet_dao_emplacement.code
			if objet_dao_emplacement.description != None : emplacement.description = objet_dao_emplacement.description
			if objet_dao_emplacement.type_emplacement_id != None : emplacement.type_emplacement_id = objet_dao_emplacement.type_emplacement_id
			if objet_dao_emplacement.defaut != None : emplacement.defaut = objet_dao_emplacement.defaut
			if objet_dao_emplacement.societe_id != None : emplacement.societe_id = objet_dao_emplacement.societe_id
			if objet_dao_emplacement.visible != None : emplacement.visible = objet_dao_emplacement.visible
			if auteur != None : emplacement.auteur_id = auteur.id

			emplacement.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Emplacement [Model_Emplacement]'
				utils.history_in_database(data)

			return True, emplacement, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA EMPLACEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_emplacement, auteur = None, request_post = []):
		try:
			emplacement = Model_Emplacement.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_emplacement = model_to_dict(emplacement)

			emplacement.designation = objet_dao_emplacement.designation
			emplacement.designation_court = objet_dao_emplacement.designation_court
			emplacement.code = objet_dao_emplacement.code
			emplacement.description = objet_dao_emplacement.description
			emplacement.type_emplacement_id = objet_dao_emplacement.type_emplacement_id
			emplacement.defaut = objet_dao_emplacement.defaut
			emplacement.societe_id = objet_dao_emplacement.societe_id
			emplacement.visible = objet_dao_emplacement.visible
			if auteur != None : emplacement.update_by_id = auteur.id
			emplacement.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_emplacement, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Emplacement [Model_Emplacement]'
				utils.history_in_database(data)

			return True, emplacement, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA EMPLACEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Emplacement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Emplacement.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			emplacement = Model_Emplacement.objects.get(pk = id)
			emplacement.delete()
			return True
		except Exception as e:
			return False