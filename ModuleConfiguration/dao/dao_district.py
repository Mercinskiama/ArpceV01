from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_district(object):
	name = ''
	province_id = None
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_District.objects.all().order_by('-creation_date')
				return Model_District.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_District.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_District.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DISTRICT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_District.objects.all().order_by('-creation_date')

			return Model_District.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DISTRICT')
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DISTRICT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', province_id = None, description = '', societe_id = None):
		try:
			district = dao_district()
			district.name = name
			district.province_id = province_id
			district.description = description
			district.societe_id = societe_id
			return district
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA DISTRICT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_district, request_post = []):
		try:
			district  = Model_District()
			district.name = objet_dao_district.name
			if objet_dao_district.province_id != None : district.province_id = objet_dao_district.province_id
			if objet_dao_district.description != None : district.description = objet_dao_district.description
			if objet_dao_district.societe_id != None : district.societe_id = objet_dao_district.societe_id
			if auteur != None : district.auteur_id = auteur.id

			district.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'District [Model_District]'
				utils.history_in_database(data)

			return True, district, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA DISTRICT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_district, auteur = None, request_post = []):
		try:
			district = Model_District.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_district = model_to_dict(district)

			district.name = objet_dao_district.name
			district.province_id = objet_dao_district.province_id
			district.description = objet_dao_district.description
			district.societe_id = objet_dao_district.societe_id
			if auteur != None : district.update_by_id = auteur.id
			district.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_district, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'District [Model_District]'
				utils.history_in_database(data)

			return True, district, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DISTRICT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_District.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_District.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			district = Model_District.objects.get(pk = id)
			district.delete()
			return True
		except Exception as e:
			return False