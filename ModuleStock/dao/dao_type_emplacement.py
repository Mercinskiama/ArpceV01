from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_type_emplacement(object):
	code = ''
	designation = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Type_emplacement.objects.all().order_by('-creation_date')
				return Model_Type_emplacement.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Type_emplacement.objects.filter(Q(code__icontains = query) | Q(designation__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Type_emplacement.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(code__icontains = query) | Q(designation__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_EMPLACEMENT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Type_emplacement.objects.all().order_by('-creation_date')

			return Model_Type_emplacement.objects.filter(Q(code__icontains = query) | Q(designation__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_EMPLACEMENT')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'code' : str(item.code),
					'designation' : str(item.designation),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_EMPLACEMENT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(code = '', designation = '', societe_id = None):
		try:
			type_emplacement = dao_type_emplacement()
			type_emplacement.code = code
			type_emplacement.designation = designation
			type_emplacement.societe_id = societe_id
			return type_emplacement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPE_EMPLACEMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_type_emplacement, request_post = []):
		try:
			type_emplacement  = Model_Type_emplacement()
			if objet_dao_type_emplacement.code != None : type_emplacement.code = objet_dao_type_emplacement.code
			type_emplacement.designation = objet_dao_type_emplacement.designation
			if objet_dao_type_emplacement.societe_id != None : type_emplacement.societe_id = objet_dao_type_emplacement.societe_id
			if auteur != None : type_emplacement.auteur_id = auteur.id

			type_emplacement.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Type d\'emplacement [Model_Type_emplacement]'
				utils.history_in_database(data)

			return True, type_emplacement, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPE_EMPLACEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_type_emplacement, auteur = None, request_post = []):
		try:
			type_emplacement = Model_Type_emplacement.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_type_emplacement = model_to_dict(type_emplacement)

			type_emplacement.code = objet_dao_type_emplacement.code
			type_emplacement.designation = objet_dao_type_emplacement.designation
			type_emplacement.societe_id = objet_dao_type_emplacement.societe_id
			if auteur != None : type_emplacement.update_by_id = auteur.id
			type_emplacement.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_type_emplacement, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Type d\'emplacement [Model_Type_emplacement]'
				utils.history_in_database(data)

			return True, type_emplacement, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPE_EMPLACEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Type_emplacement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Type_emplacement.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			type_emplacement = Model_Type_emplacement.objects.get(pk = id)
			type_emplacement.delete()
			return True
		except Exception as e:
			return False