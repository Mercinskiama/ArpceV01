from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_bon_reception(object):
	code = ''
	description = ''
	date_prevue = None
	societe_id = None
	emplacement_destination_id = None
	emplacement_origine_id = None
	operation_stock_id = None
	status_id = None
	bon_livraison = None
	employe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Bon_reception.objects.all().order_by('-creation_date')
				return Model_Bon_reception.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Bon_reception.objects.filter(Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Bon_reception.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(code__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE BON_RECEPTION')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Bon_reception.objects.all().order_by('-creation_date')

			return Model_Bon_reception.objects.filter(Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE BON_RECEPTION')
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
					'description' : str(item.description),
					'date_prevue' : item.date_prevue,
					'societe' : item.societe.__str__() if item.societe else '-',
					'emplacement_destination' : item.emplacement_destination.__str__() if item.emplacement_destination else '-',
					'emplacement_origine' : item.emplacement_origine.__str__() if item.emplacement_origine else '-',
					'operation_stock' : item.operation_stock.__str__() if item.operation_stock else '-',
					'status' : item.status.__str__() if item.status else '-',
					'bon_livraison' : item.bon_livraison.url if item.bon_livraison != None else None,
					'employe' : item.employe.__str__() if item.employe else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE BON_RECEPTION  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(code = '', description = '', date_prevue = None, societe_id = None, emplacement_destination_id = None, emplacement_origine_id = None, operation_stock_id = None, status_id = None, bon_livraison = None, employe_id = None):
		try:
			bon_reception = dao_bon_reception()
			bon_reception.code = code
			bon_reception.description = description
			bon_reception.date_prevue = date_prevue
			bon_reception.societe_id = societe_id
			bon_reception.emplacement_destination_id = emplacement_destination_id
			bon_reception.emplacement_origine_id = emplacement_origine_id
			bon_reception.operation_stock_id = operation_stock_id
			bon_reception.status_id = status_id
			bon_reception.bon_livraison = bon_livraison
			bon_reception.employe_id = employe_id
			return bon_reception
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA BON_RECEPTION')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_bon_reception, request_post = []):
		try:
			bon_reception  = Model_Bon_reception()
			if objet_dao_bon_reception.code != None : bon_reception.code = objet_dao_bon_reception.code
			if objet_dao_bon_reception.description != None : bon_reception.description = objet_dao_bon_reception.description
			bon_reception.date_prevue = objet_dao_bon_reception.date_prevue
			if objet_dao_bon_reception.societe_id != None : bon_reception.societe_id = objet_dao_bon_reception.societe_id
			if objet_dao_bon_reception.emplacement_destination_id != None : bon_reception.emplacement_destination_id = objet_dao_bon_reception.emplacement_destination_id
			if objet_dao_bon_reception.emplacement_origine_id != None : bon_reception.emplacement_origine_id = objet_dao_bon_reception.emplacement_origine_id
			if objet_dao_bon_reception.operation_stock_id != None : bon_reception.operation_stock_id = objet_dao_bon_reception.operation_stock_id
			if objet_dao_bon_reception.status_id != None : bon_reception.status_id = objet_dao_bon_reception.status_id
			if objet_dao_bon_reception.bon_livraison != None : bon_reception.bon_livraison = objet_dao_bon_reception.bon_livraison
			if objet_dao_bon_reception.employe_id != None : bon_reception.employe_id = objet_dao_bon_reception.employe_id
			if auteur != None : bon_reception.auteur_id = auteur.id

			bon_reception.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Bon de Reception [Model_Bon_reception]'
				utils.history_in_database(data)

			return True, bon_reception, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA BON_RECEPTION')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_bon_reception, auteur = None, request_post = []):
		try:
			bon_reception = Model_Bon_reception.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_bon_reception = model_to_dict(bon_reception)

			bon_reception.code = objet_dao_bon_reception.code
			bon_reception.description = objet_dao_bon_reception.description
			bon_reception.date_prevue = objet_dao_bon_reception.date_prevue
			bon_reception.societe_id = objet_dao_bon_reception.societe_id
			bon_reception.emplacement_destination_id = objet_dao_bon_reception.emplacement_destination_id
			bon_reception.emplacement_origine_id = objet_dao_bon_reception.emplacement_origine_id
			bon_reception.operation_stock_id = objet_dao_bon_reception.operation_stock_id
			bon_reception.status_id = objet_dao_bon_reception.status_id
			if objet_dao_bon_reception.bon_livraison != None : bon_reception.bon_livraison = objet_dao_bon_reception.bon_livraison
			bon_reception.employe_id = objet_dao_bon_reception.employe_id
			if auteur != None : bon_reception.update_by_id = auteur.id
			bon_reception.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_bon_reception, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Bon de Reception [Model_Bon_reception]'
				utils.history_in_database(data)

			return True, bon_reception, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA BON_RECEPTION')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Bon_reception.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Bon_reception.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			bon_reception = Model_Bon_reception.objects.get(pk = id)
			bon_reception.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroBonReception():
		reception = dao_bon_reception.toList().count()
		reception = reception + 1
		temp_numero = str(reception)

		for i in range(len(str(reception)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = f"BN-RECEPTION-{timezone.now().year}{mois}{temp_numero}"
		return temp_numero