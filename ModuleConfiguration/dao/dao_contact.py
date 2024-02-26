from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_contact(object):
	name = ''
	type = 0
	nature = ''
	email = ''
	siteweb = ''
	function = ''
	country_id = None
	adress_state_id = None
	adress_city_id = None
	adress_line1 = ''
	adress_line2 = ''
	phone_number = ''
	phone_number_2 = ''
	code_postal = ''
	description = ''
	societe_id = None
	autres_adresses = []

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Contact.objects.all().order_by('-creation_date')
				return Model_Contact.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Contact.objects.filter(Q(name__icontains = query) | Q(type__icontains = query) | Q(nature__icontains = query) | Q(email__icontains = query) | Q(siteweb__icontains = query) | Q(function__icontains = query) | Q(adress_line1__icontains = query) | Q(adress_line2__icontains = query) | Q(phone_number__icontains = query) | Q(phone_number_2__icontains = query) | Q(code_postal__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Contact.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(type__icontains = query) | Q(nature__icontains = query) | Q(email__icontains = query) | Q(siteweb__icontains = query) | Q(function__icontains = query) | Q(adress_line1__icontains = query) | Q(adress_line2__icontains = query) | Q(phone_number__icontains = query) | Q(phone_number_2__icontains = query) | Q(code_postal__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE CONTACT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Contact.objects.all().order_by('-creation_date')

			return Model_Contact.objects.filter(Q(name__icontains = query) | Q(type__icontains = query) | Q(nature__icontains = query) | Q(email__icontains = query) | Q(siteweb__icontains = query) | Q(function__icontains = query) | Q(adress_line1__icontains = query) | Q(adress_line2__icontains = query) | Q(phone_number__icontains = query) | Q(phone_number_2__icontains = query) | Q(code_postal__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE CONTACT')
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
					'type' : makeInt(item.value_type),
					'nature' : str(item.nature),
					'email' : str(item.email),
					'siteweb' : str(item.siteweb),
					'function' : str(item.function),
					'country' : item.country.__str__() if item.country else '-',
					'adress_state' : item.adress_state.__str__() if item.adress_state else '-',
					'adress_city' : item.adress_city.__str__() if item.adress_city else '-',
					'adress_line1' : str(item.adress_line1),
					'adress_line2' : str(item.adress_line2),
					'phone_number' : str(item.phone_number),
					'phone_number_2' : str(item.phone_number_2),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE CONTACT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', type = 0, nature = '', email = '', siteweb = '', function = '', country_id = None, adress_state_id = None, adress_city_id = None, adress_line1 = '', adress_line2 = '', phone_number = '', phone_number_2 = '', code_postal = '', description = '', societe_id = None, autres_adresses = []):
		try:
			contact = dao_contact()
			contact.name = name
			contact.type = type
			contact.nature = nature
			contact.email = email
			contact.siteweb = siteweb
			contact.function = function
			contact.country_id = country_id
			contact.adress_state_id = adress_state_id
			contact.adress_city_id = adress_city_id
			contact.adress_line1 = adress_line1
			contact.adress_line2 = adress_line2
			contact.phone_number = phone_number
			contact.phone_number_2 = phone_number_2
			contact.code_postal = code_postal
			contact.description = description
			contact.societe_id = societe_id
			contact.autres_adresses = autres_adresses
			return contact
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CONTACT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_contact, request_post = []):
		try:
			contact  = Model_Contact()
			contact.name = objet_dao_contact.name
			if objet_dao_contact.type != None : contact.type = objet_dao_contact.type
			if objet_dao_contact.nature != None : contact.nature = objet_dao_contact.nature
			if objet_dao_contact.email != None : contact.email = objet_dao_contact.email
			if objet_dao_contact.siteweb != None : contact.siteweb = objet_dao_contact.siteweb
			if objet_dao_contact.function != None : contact.function = objet_dao_contact.function
			if objet_dao_contact.country_id != None : contact.country_id = objet_dao_contact.country_id
			if objet_dao_contact.adress_state_id != None : contact.adress_state_id = objet_dao_contact.adress_state_id
			if objet_dao_contact.adress_city_id != None : contact.adress_city_id = objet_dao_contact.adress_city_id
			if objet_dao_contact.adress_line1 != None : contact.adress_line1 = objet_dao_contact.adress_line1
			if objet_dao_contact.adress_line2 != None : contact.adress_line2 = objet_dao_contact.adress_line2
			if objet_dao_contact.phone_number != None : contact.phone_number = objet_dao_contact.phone_number
			if objet_dao_contact.phone_number_2 != None : contact.phone_number_2 = objet_dao_contact.phone_number_2
			if objet_dao_contact.code_postal != None : contact.code_postal = objet_dao_contact.code_postal
			if objet_dao_contact.description != None : contact.description = objet_dao_contact.description
			if objet_dao_contact.societe_id != None : contact.societe_id = objet_dao_contact.societe_id
			if auteur != None : contact.auteur_id = auteur.id

			contact.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_contact.autres_adresses)):
				try:
					objet = Model_Adresse.objects.get(pk = objet_dao_contact.autres_adresses[i])
					contact.autres_adresses.add(objet)
				except Exception as e: pass

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Contact [Model_Contact]'
				utils.history_in_database(data)

			return True, contact, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA CONTACT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_contact, auteur = None, request_post = []):
		try:
			contact = Model_Contact.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_contact = model_to_dict(contact)

			contact.name = objet_dao_contact.name
			contact.type = objet_dao_contact.type
			contact.nature = objet_dao_contact.nature
			contact.email = objet_dao_contact.email
			contact.siteweb = objet_dao_contact.siteweb
			contact.function = objet_dao_contact.function
			contact.country_id = objet_dao_contact.country_id
			contact.adress_state_id = objet_dao_contact.adress_state_id
			contact.adress_city_id = objet_dao_contact.adress_city_id
			contact.adress_line1 = objet_dao_contact.adress_line1
			contact.adress_line2 = objet_dao_contact.adress_line2
			contact.phone_number = objet_dao_contact.phone_number
			contact.phone_number_2 = objet_dao_contact.phone_number_2
			contact.code_postal = objet_dao_contact.code_postal
			contact.description = objet_dao_contact.description
			contact.societe_id = objet_dao_contact.societe_id
			if auteur != None : contact.update_by_id = auteur.id
			contact.save()

			#Mise à jour Champs (ManyToMany - Creation)
			autres_adresses_old = contact.autres_adresses.all()
			autres_adresses_updated = []
			for i in range(0, len(objet_dao_contact.autres_adresses)):
				try:
					objet = Model_Adresse.objects.get(pk = objet_dao_contact.autres_adresses[i])
					if objet not in autres_adresses_old: contact.autres_adresses.add(objet)
					autres_adresses_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in autres_adresses_old:
				if item.id not in autres_adresses_updated: contact.autres_adresses.remove(item)

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_contact, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Contact [Model_Contact]'
				utils.history_in_database(data)

			return True, contact, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CONTACT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Contact.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Contact.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			contact = Model_Contact.objects.get(pk = id)
			contact.delete()
			return True
		except Exception as e:
			return False