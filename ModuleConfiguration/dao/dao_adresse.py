from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_adresse(object):
	name = ''
	type_adresse = 0
	country_id = None
	adress_state_id = None
	adress_city_id = None
	adress_township_id = None
	adress_line1 = ''
	adress_line2 = ''
	code_postal = ''
	description = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Adresse.objects.all().order_by('-creation_date')
				return Model_Adresse.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Adresse.objects.filter(Q(name__icontains = query) | Q(type_adresse__icontains = query) | Q(adress_line1__icontains = query) | Q(adress_line2__icontains = query) | Q(code_postal__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Adresse.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(type_adresse__icontains = query) | Q(adress_line1__icontains = query) | Q(adress_line2__icontains = query) | Q(code_postal__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ADRESSE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Adresse.objects.all().order_by('-creation_date')

			return Model_Adresse.objects.filter(Q(name__icontains = query) | Q(type_adresse__icontains = query) | Q(adress_line1__icontains = query) | Q(adress_line2__icontains = query) | Q(code_postal__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ADRESSE')
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
					'type_adresse' : makeInt(item.value_type_adresse),
					'country' : item.country.__str__() if item.country else '-',
					'adress_state' : item.adress_state.__str__() if item.adress_state else '-',
					'adress_city' : item.adress_city.__str__() if item.adress_city else '-',
					'adress_township' : item.adress_township.__str__() if item.adress_township else '-',
					'adress_line1' : str(item.adress_line1),
					'adress_line2' : str(item.adress_line2),
					'code_postal' : str(item.code_postal),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ADRESSE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', type_adresse = 0, country_id = None, adress_state_id = None, adress_city_id = None, adress_township_id = None, adress_line1 = '', adress_line2 = '', code_postal = '', description = '', societe_id = None):
		try:
			adresse = dao_adresse()
			adresse.name = name
			adresse.type_adresse = type_adresse
			adresse.country_id = country_id
			adresse.adress_state_id = adress_state_id
			adresse.adress_city_id = adress_city_id
			adresse.adress_township_id = adress_township_id
			adresse.adress_line1 = adress_line1
			adresse.adress_line2 = adress_line2
			adresse.code_postal = code_postal
			adresse.description = description
			adresse.societe_id = societe_id
			return adresse
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ADRESSE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_adresse, request_post = []):
		try:
			adresse  = Model_Adresse()
			adresse.name = objet_dao_adresse.name
			if objet_dao_adresse.type_adresse != None : adresse.type_adresse = objet_dao_adresse.type_adresse
			if objet_dao_adresse.country_id != None : adresse.country_id = objet_dao_adresse.country_id
			if objet_dao_adresse.adress_state_id != None : adresse.adress_state_id = objet_dao_adresse.adress_state_id
			if objet_dao_adresse.adress_city_id != None : adresse.adress_city_id = objet_dao_adresse.adress_city_id
			if objet_dao_adresse.adress_township_id != None : adresse.adress_township_id = objet_dao_adresse.adress_township_id
			if objet_dao_adresse.adress_line1 != None : adresse.adress_line1 = objet_dao_adresse.adress_line1
			if objet_dao_adresse.adress_line2 != None : adresse.adress_line2 = objet_dao_adresse.adress_line2
			if objet_dao_adresse.code_postal != None : adresse.code_postal = objet_dao_adresse.code_postal
			if objet_dao_adresse.description != None : adresse.description = objet_dao_adresse.description
			if objet_dao_adresse.societe_id != None : adresse.societe_id = objet_dao_adresse.societe_id
			if auteur != None : adresse.auteur_id = auteur.id

			adresse.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Adresse [Model_Adresse]'
				utils.history_in_database(data)

			return True, adresse, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ADRESSE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_adresse, auteur = None, request_post = []):
		try:
			adresse = Model_Adresse.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_adresse = model_to_dict(adresse)

			adresse.name = objet_dao_adresse.name
			adresse.type_adresse = objet_dao_adresse.type_adresse
			adresse.country_id = objet_dao_adresse.country_id
			adresse.adress_state_id = objet_dao_adresse.adress_state_id
			adresse.adress_city_id = objet_dao_adresse.adress_city_id
			adresse.adress_township_id = objet_dao_adresse.adress_township_id
			adresse.adress_line1 = objet_dao_adresse.adress_line1
			adresse.adress_line2 = objet_dao_adresse.adress_line2
			adresse.code_postal = objet_dao_adresse.code_postal
			adresse.description = objet_dao_adresse.description
			adresse.societe_id = objet_dao_adresse.societe_id
			if auteur != None : adresse.update_by_id = auteur.id
			adresse.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_adresse, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Adresse [Model_Adresse]'
				utils.history_in_database(data)

			return True, adresse, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ADRESSE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Adresse.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Adresse.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			adresse = Model_Adresse.objects.get(pk = id)
			adresse.delete()
			return True
		except Exception as e:
			return False