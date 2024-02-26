from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_ajustement(object):
	reference = ''
	date = None
	societe_id = None
	emplacement_id = None
	status_id = None
	inventaire_de = 0
	document = ''

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Ajustement.objects.all().order_by('-creation_date')
				return Model_Ajustement.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Ajustement.objects.filter(Q(reference__icontains = query) | Q(inventaire_de__icontains = query) | Q(document__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Ajustement.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(reference__icontains = query) | Q(inventaire_de__icontains = query) | Q(document__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE AJUSTEMENT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Ajustement.objects.all().order_by('-creation_date')

			return Model_Ajustement.objects.filter(Q(reference__icontains = query) | Q(inventaire_de__icontains = query) | Q(document__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE AJUSTEMENT')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'reference' : str(item.reference),
					'date' : item.date,
					'societe' : item.societe.__str__() if item.societe else '-',
					'emplacement' : item.emplacement.__str__() if item.emplacement else '-',
					'status' : item.status.__str__() if item.status else '-',
					'inventaire_de' : makeInt(item.inventaire_de),
					'document' : str(item.document),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE AJUSTEMENT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(reference = '', date = None, societe_id = None, emplacement_id = None, status_id = None, inventaire_de = 0, document = ''):
		try:
			ajustement = dao_ajustement()
			ajustement.reference = reference
			ajustement.date = date
			ajustement.societe_id = societe_id
			ajustement.emplacement_id = emplacement_id
			ajustement.status_id = status_id
			ajustement.inventaire_de = inventaire_de
			ajustement.document = document
			return ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_ajustement, request_post = []):
		try:
			ajustement  = Model_Ajustement()
			if objet_dao_ajustement.reference != None : ajustement.reference = objet_dao_ajustement.reference
			ajustement.date = objet_dao_ajustement.date
			if objet_dao_ajustement.societe_id != None : ajustement.societe_id = objet_dao_ajustement.societe_id
			ajustement.emplacement_id = objet_dao_ajustement.emplacement_id
			if objet_dao_ajustement.status_id != None : ajustement.status_id = objet_dao_ajustement.status_id
			if objet_dao_ajustement.inventaire_de != None : ajustement.inventaire_de = objet_dao_ajustement.inventaire_de
			if objet_dao_ajustement.document != None : ajustement.document = objet_dao_ajustement.document
			if auteur != None : ajustement.auteur_id = auteur.id

			ajustement.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Inventaire [Model_Ajustement]'
				utils.history_in_database(data)

			return True, ajustement, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA AJUSTEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_ajustement, auteur = None, request_post = []):
		try:
			ajustement = Model_Ajustement.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_ajustement = model_to_dict(ajustement)

			ajustement.reference = objet_dao_ajustement.reference
			ajustement.date = objet_dao_ajustement.date
			ajustement.societe_id = objet_dao_ajustement.societe_id
			ajustement.emplacement_id = objet_dao_ajustement.emplacement_id
			ajustement.status_id = objet_dao_ajustement.status_id
			ajustement.inventaire_de = objet_dao_ajustement.inventaire_de
			ajustement.document = objet_dao_ajustement.document
			if auteur != None : ajustement.update_by_id = auteur.id
			ajustement.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_ajustement, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Inventaire [Model_Ajustement]'
				utils.history_in_database(data)

			return True, ajustement, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA AJUSTEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Ajustement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Ajustement.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			ajustement = Model_Ajustement.objects.get(pk = id)
			ajustement.delete()
			return True
		except Exception as e:
			return False


	@staticmethod
	def toGenerateNumeroInv():
		ajustement = dao_ajustement.toList().count()
		ajustement = ajustement + 1
		temp_numero = str(ajustement)

		for i in range(len(str(ajustement)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "INV-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero