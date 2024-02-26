from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_societe(object):
	code = ''
	name = ''
	picture_icon = None
	type = ''
	societe_id = None
	devise_id = None
	type_periode_id = None
	adress_email = ''
	siteweb = ''
	pays_id = None
	pays_adress = ''
	province_id = None
	province_adress = ''
	ville_id = None
	ville_adress = ''
	commune_id = None
	adresse_line1 = ''
	adresse_line2 = ''
	telephone_1 = ''
	telephone_2 = ''
	nbr_periode_gl = 0
	nbr_periode_ar = 0
	nbr_periode_ap = 0
	nbr_periode_cm = 0
	nbr_periode_fa = 0
	nbr_periode_bgt = 0
	nbr_periode_py = 0
	period_begin_date = None
	period_end_date = None
	description = ''
	autres_adresses = []
	contacts = []

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Societe.objects.all().order_by('-creation_date')
				return Model_Societe.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Societe.objects.filter(Q(code__icontains = query) | Q(name__icontains = query) | Q(type__icontains = query) | Q(adress_email__icontains = query) | Q(siteweb__icontains = query) | Q(pays_adress__icontains = query) | Q(province_adress__icontains = query) | Q(ville_adress__icontains = query) | Q(adresse_line1__icontains = query) | Q(adresse_line2__icontains = query) | Q(telephone_1__icontains = query) | Q(telephone_2__icontains = query) | Q(nbr_periode_gl__icontains = query) | Q(nbr_periode_ar__icontains = query) | Q(nbr_periode_ap__icontains = query) | Q(nbr_periode_cm__icontains = query) | Q(nbr_periode_fa__icontains = query) | Q(nbr_periode_bgt__icontains = query) | Q(nbr_periode_py__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Societe.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(code__icontains = query) | Q(name__icontains = query) | Q(type__icontains = query) | Q(adress_email__icontains = query) | Q(siteweb__icontains = query) | Q(pays_adress__icontains = query) | Q(province_adress__icontains = query) | Q(ville_adress__icontains = query) | Q(adresse_line1__icontains = query) | Q(adresse_line2__icontains = query) | Q(telephone_1__icontains = query) | Q(telephone_2__icontains = query) | Q(nbr_periode_gl__icontains = query) | Q(nbr_periode_ar__icontains = query) | Q(nbr_periode_ap__icontains = query) | Q(nbr_periode_cm__icontains = query) | Q(nbr_periode_fa__icontains = query) | Q(nbr_periode_bgt__icontains = query) | Q(nbr_periode_py__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE SOCIETE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Societe.objects.all().order_by('-creation_date')

			return Model_Societe.objects.filter(Q(code__icontains = query) | Q(name__icontains = query) | Q(type__icontains = query) | Q(adress_email__icontains = query) | Q(siteweb__icontains = query) | Q(pays_adress__icontains = query) | Q(province_adress__icontains = query) | Q(ville_adress__icontains = query) | Q(adresse_line1__icontains = query) | Q(adresse_line2__icontains = query) | Q(telephone_1__icontains = query) | Q(telephone_2__icontains = query) | Q(nbr_periode_gl__icontains = query) | Q(nbr_periode_ar__icontains = query) | Q(nbr_periode_ap__icontains = query) | Q(nbr_periode_cm__icontains = query) | Q(nbr_periode_fa__icontains = query) | Q(nbr_periode_bgt__icontains = query) | Q(nbr_periode_py__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE SOCIETE')
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
					'name' : str(item.name),
					'picture_icon' : item.picture_icon.url if item.picture_icon != None else None,
					'type' : str(item.type),
					'societe' : item.societe.__str__() if item.societe else '-',
					'devise' : item.devise.__str__() if item.devise else '-',
					'type_periode' : item.type_periode.__str__() if item.type_periode else '-',
					'adress_email' : str(item.adress_email),
					'siteweb' : str(item.siteweb),
					'pays' : item.pays.__str__() if item.pays else '-',
					'pays_adress' : str(item.pays_adress),
					'province' : item.province.__str__() if item.province else '-',
					'province_adress' : str(item.province_adress),
					'ville' : item.ville.__str__() if item.ville else '-',
					'ville_adress' : str(item.ville_adress),
					'commune' : item.commune.__str__() if item.commune else '-',
					'adresse_line1' : str(item.adresse_line1),
					'adresse_line2' : str(item.adresse_line2),
					'telephone_1' : str(item.telephone_1),
					'telephone_2' : str(item.telephone_2),
					'nbr_periode_gl' : makeInt(item.nbr_periode_gl),
					'nbr_periode_ar' : makeInt(item.nbr_periode_ar),
					'nbr_periode_ap' : makeInt(item.nbr_periode_ap),
					'nbr_periode_cm' : makeInt(item.nbr_periode_cm),
					'nbr_periode_fa' : makeInt(item.nbr_periode_fa),
					'nbr_periode_bgt' : makeInt(item.nbr_periode_bgt),
					'nbr_periode_py' : makeInt(item.nbr_periode_py),
					'period_begin_date' : item.period_begin_date,
					'period_end_date' : item.period_end_date,
					'description' : str(item.description),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE SOCIETE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(code = '', name = '', picture_icon = None, type = '', societe_id = None, devise_id = None, type_periode_id = None, adress_email = '', siteweb = '', pays_id = None, pays_adress = '', province_id = None, province_adress = '', ville_id = None, ville_adress = '', commune_id = None, adresse_line1 = '', adresse_line2 = '', telephone_1 = '', telephone_2 = '', nbr_periode_gl = 0, nbr_periode_ar = 0, nbr_periode_ap = 0, nbr_periode_cm = 0, nbr_periode_fa = 0, nbr_periode_bgt = 0, nbr_periode_py = 0, period_begin_date = None, period_end_date = None, description = '', autres_adresses = [], contacts = []):
		try:
			societe = dao_societe()
			societe.code = code
			societe.name = name
			societe.picture_icon = picture_icon
			societe.type = type
			societe.societe_id = societe_id
			societe.devise_id = devise_id
			societe.type_periode_id = type_periode_id
			societe.adress_email = adress_email
			societe.siteweb = siteweb
			societe.pays_id = pays_id
			societe.pays_adress = pays_adress
			societe.province_id = province_id
			societe.province_adress = province_adress
			societe.ville_id = ville_id
			societe.ville_adress = ville_adress
			societe.commune_id = commune_id
			societe.adresse_line1 = adresse_line1
			societe.adresse_line2 = adresse_line2
			societe.telephone_1 = telephone_1
			societe.telephone_2 = telephone_2
			societe.nbr_periode_gl = nbr_periode_gl
			societe.nbr_periode_ar = nbr_periode_ar
			societe.nbr_periode_ap = nbr_periode_ap
			societe.nbr_periode_cm = nbr_periode_cm
			societe.nbr_periode_fa = nbr_periode_fa
			societe.nbr_periode_bgt = nbr_periode_bgt
			societe.nbr_periode_py = nbr_periode_py
			societe.period_begin_date = period_begin_date
			societe.period_end_date = period_end_date
			societe.description = description
			societe.autres_adresses = autres_adresses
			societe.contacts = contacts
			return societe
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA SOCIETE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_societe, request_post = []):
		try:
			societe  = Model_Societe()
			societe.code = objet_dao_societe.code
			societe.name = objet_dao_societe.name
			if objet_dao_societe.picture_icon != None : societe.picture_icon = objet_dao_societe.picture_icon
			if objet_dao_societe.type != None : societe.type = objet_dao_societe.type
			if objet_dao_societe.societe_id != None : societe.societe_id = objet_dao_societe.societe_id
			if objet_dao_societe.devise_id != None : societe.devise_id = objet_dao_societe.devise_id
			if objet_dao_societe.type_periode_id != None : societe.type_periode_id = objet_dao_societe.type_periode_id
			if objet_dao_societe.adress_email != None : societe.adress_email = objet_dao_societe.adress_email
			if objet_dao_societe.siteweb != None : societe.siteweb = objet_dao_societe.siteweb
			if objet_dao_societe.pays_id != None : societe.pays_id = objet_dao_societe.pays_id
			if objet_dao_societe.pays_adress != None : societe.pays_adress = objet_dao_societe.pays_adress
			if objet_dao_societe.province_id != None : societe.province_id = objet_dao_societe.province_id
			if objet_dao_societe.province_adress != None : societe.province_adress = objet_dao_societe.province_adress
			if objet_dao_societe.ville_id != None : societe.ville_id = objet_dao_societe.ville_id
			if objet_dao_societe.ville_adress != None : societe.ville_adress = objet_dao_societe.ville_adress
			if objet_dao_societe.commune_id != None : societe.commune_id = objet_dao_societe.commune_id
			if objet_dao_societe.adresse_line1 != None : societe.adresse_line1 = objet_dao_societe.adresse_line1
			if objet_dao_societe.adresse_line2 != None : societe.adresse_line2 = objet_dao_societe.adresse_line2
			if objet_dao_societe.telephone_1 != None : societe.telephone_1 = objet_dao_societe.telephone_1
			if objet_dao_societe.telephone_2 != None : societe.telephone_2 = objet_dao_societe.telephone_2
			if objet_dao_societe.nbr_periode_gl != None : societe.nbr_periode_gl = objet_dao_societe.nbr_periode_gl
			if objet_dao_societe.nbr_periode_ar != None : societe.nbr_periode_ar = objet_dao_societe.nbr_periode_ar
			if objet_dao_societe.nbr_periode_ap != None : societe.nbr_periode_ap = objet_dao_societe.nbr_periode_ap
			if objet_dao_societe.nbr_periode_cm != None : societe.nbr_periode_cm = objet_dao_societe.nbr_periode_cm
			if objet_dao_societe.nbr_periode_fa != None : societe.nbr_periode_fa = objet_dao_societe.nbr_periode_fa
			if objet_dao_societe.nbr_periode_bgt != None : societe.nbr_periode_bgt = objet_dao_societe.nbr_periode_bgt
			if objet_dao_societe.nbr_periode_py != None : societe.nbr_periode_py = objet_dao_societe.nbr_periode_py
			if objet_dao_societe.period_begin_date != None : societe.period_begin_date = objet_dao_societe.period_begin_date
			if objet_dao_societe.period_end_date != None : societe.period_end_date = objet_dao_societe.period_end_date
			if objet_dao_societe.description != None : societe.description = objet_dao_societe.description
			if auteur != None : societe.auteur_id = auteur.id

			societe.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_societe.autres_adresses)):
				try:
					objet = Model_Adresse.objects.get(pk = objet_dao_societe.autres_adresses[i])
					societe.autres_adresses.add(objet)
				except Exception as e: pass

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_societe.contacts)):
				try:
					objet = Model_Contact.objects.get(pk = objet_dao_societe.contacts[i])
					societe.contacts.add(objet)
				except Exception as e: pass

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Société [Model_Societe]'
				utils.history_in_database(data)

			return True, societe, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SOCIETE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_societe, auteur = None, request_post = []):
		try:
			societe = Model_Societe.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_societe = model_to_dict(societe)

			societe.code = objet_dao_societe.code
			societe.name = objet_dao_societe.name
			if objet_dao_societe.picture_icon != None : societe.picture_icon = objet_dao_societe.picture_icon
			societe.type = objet_dao_societe.type
			societe.societe_id = objet_dao_societe.societe_id
			societe.devise_id = objet_dao_societe.devise_id
			societe.type_periode_id = objet_dao_societe.type_periode_id
			societe.adress_email = objet_dao_societe.adress_email
			societe.siteweb = objet_dao_societe.siteweb
			societe.pays_id = objet_dao_societe.pays_id
			societe.pays_adress = objet_dao_societe.pays_adress
			societe.province_id = objet_dao_societe.province_id
			societe.province_adress = objet_dao_societe.province_adress
			societe.ville_id = objet_dao_societe.ville_id
			societe.ville_adress = objet_dao_societe.ville_adress
			societe.commune_id = objet_dao_societe.commune_id
			societe.adresse_line1 = objet_dao_societe.adresse_line1
			societe.adresse_line2 = objet_dao_societe.adresse_line2
			societe.telephone_1 = objet_dao_societe.telephone_1
			societe.telephone_2 = objet_dao_societe.telephone_2
			societe.nbr_periode_gl = objet_dao_societe.nbr_periode_gl
			societe.nbr_periode_ar = objet_dao_societe.nbr_periode_ar
			societe.nbr_periode_ap = objet_dao_societe.nbr_periode_ap
			societe.nbr_periode_cm = objet_dao_societe.nbr_periode_cm
			societe.nbr_periode_fa = objet_dao_societe.nbr_periode_fa
			societe.nbr_periode_bgt = objet_dao_societe.nbr_periode_bgt
			societe.nbr_periode_py = objet_dao_societe.nbr_periode_py
			societe.period_begin_date = objet_dao_societe.period_begin_date
			societe.period_end_date = objet_dao_societe.period_end_date
			societe.description = objet_dao_societe.description
			if auteur != None : societe.update_by_id = auteur.id
			societe.save()

			#Mise à jour Champs (ManyToMany - Creation)
			contacts_old = societe.contacts.all()
			contacts_updated = []
			for i in range(0, len(objet_dao_societe.contacts)):
				try:
					objet = Model_Adresse.objects.get(pk = objet_dao_societe.contacts[i])
					if objet not in contacts_old: societe.contacts.add(objet)
					contacts_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in contacts_old:
				if item.id not in contacts_updated: societe.contacts.remove(item)

			#Mise à jour Champs (ManyToMany - Creation)
			contacts_old = societe.contacts.all()
			contacts_updated = []
			for i in range(0, len(objet_dao_societe.contacts)):
				try:
					objet = Model_Contact.objects.get(pk = objet_dao_societe.contacts[i])
					if objet not in contacts_old: societe.contacts.add(objet)
					contacts_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in contacts_old:
				if item.id not in contacts_updated: societe.contacts.remove(item)

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_societe, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Société [Model_Societe]'
				utils.history_in_database(data)

			return True, societe, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SOCIETE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Societe.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Societe.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			societe = Model_Societe.objects.get(pk = id)
			societe.delete()
			return True
		except Exception as e:
			return False