from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_type_periode(object):
	name = ''
	periodicite = ''
	nombre_par_exercice = 0
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Type_periode.objects.all().order_by('-creation_date')
				return Model_Type_periode.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Type_periode.objects.filter(Q(name__icontains = query) | Q(periodicite__icontains = query) | Q(nombre_par_exercice__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Type_periode.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(periodicite__icontains = query) | Q(nombre_par_exercice__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_PERIODE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Type_periode.objects.all().order_by('-creation_date')

			return Model_Type_periode.objects.filter(Q(name__icontains = query) | Q(periodicite__icontains = query) | Q(nombre_par_exercice__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_PERIODE')
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
					'periodicite' : str(item.value_periodicite),
					'nombre_par_exercice' : makeInt(item.nombre_par_exercice),
					'description' : str(item.description),
					'statut' : item.statut.__str__() if item.statut else '-',
					'societe' : item.societe.__str__() if item.societe else '-',
					'etat' : str(item.etat),
					'creation_date' : item.creation_date,
					'update_date' : item.update_date,
					'update_by' : item.update_by.__str__() if item.update_by else '-',
					'auteur' : item.auteur.__str__() if item.auteur else '-',
				}
				listes.append(element)
			return listes
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_PERIODE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', periodicite = '', nombre_par_exercice = 0, description = '', societe_id = None):
		try:
			type_periode = dao_type_periode()
			type_periode.name = name
			type_periode.periodicite = periodicite
			type_periode.nombre_par_exercice = nombre_par_exercice
			type_periode.description = description
			type_periode.societe_id = societe_id
			return type_periode
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPE_PERIODE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_type_periode, request_post = []):
		try:
			type_periode  = Model_Type_periode()
			type_periode.name = objet_dao_type_periode.name
			if objet_dao_type_periode.periodicite != None : type_periode.periodicite = objet_dao_type_periode.periodicite
			if objet_dao_type_periode.nombre_par_exercice != None : type_periode.nombre_par_exercice = objet_dao_type_periode.nombre_par_exercice
			if objet_dao_type_periode.description != None : type_periode.description = objet_dao_type_periode.description
			if objet_dao_type_periode.societe_id != None : type_periode.societe_id = objet_dao_type_periode.societe_id
			if auteur != None : type_periode.auteur_id = auteur.id

			type_periode.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Type Période [Model_Type_periode]'
				utils.history_in_database(data)

			return True, type_periode, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPE_PERIODE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_type_periode, auteur = None, request_post = []):
		try:
			type_periode = Model_Type_periode.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_type_periode = model_to_dict(type_periode)

			type_periode.name = objet_dao_type_periode.name
			type_periode.periodicite = objet_dao_type_periode.periodicite
			type_periode.nombre_par_exercice = objet_dao_type_periode.nombre_par_exercice
			type_periode.description = objet_dao_type_periode.description
			type_periode.societe_id = objet_dao_type_periode.societe_id
			if auteur != None : type_periode.update_by_id = auteur.id
			type_periode.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_type_periode, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Type Période [Model_Type_periode]'
				utils.history_in_database(data)

			return True, type_periode, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPE_PERIODE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Type_periode.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Type_periode.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			type_periode = Model_Type_periode.objects.get(pk = id)
			type_periode.delete()
			return True
		except Exception as e:
			return False