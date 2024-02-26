from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_bon_transfert(object):
	code = ''
	societe_id = None
	emplacement_origine_id = None
	emplacement_destination_id = None
	status_id = None
	operation_stock_id = None
	description = ''
	responsable_transfert_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Bon_transfert.objects.all().order_by('-creation_date')
				return Model_Bon_transfert.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Bon_transfert.objects.filter(Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Bon_transfert.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(code__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE BON_TRANSFERT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Bon_transfert.objects.all().order_by('-creation_date')

			return Model_Bon_transfert.objects.filter(Q(code__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE BON_TRANSFERT')
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
					'societe' : item.societe.__str__() if item.societe else '-',
					'emplacement_origine' : item.emplacement_origine.__str__() if item.emplacement_origine else '-',
					'emplacement_destination' : item.emplacement_destination.__str__() if item.emplacement_destination else '-',
					'status' : item.status.__str__() if item.status else '-',
					'operation_stock' : item.operation_stock.__str__() if item.operation_stock else '-',
					'description' : str(item.description),
					'responsable_transfert' : item.responsable_transfert.__str__() if item.responsable_transfert else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE BON_TRANSFERT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(code = '', societe_id = None, emplacement_origine_id = None, emplacement_destination_id = None, status_id = None, operation_stock_id = None, description = '', responsable_transfert_id = None):
		try:
			bon_transfert = dao_bon_transfert()
			bon_transfert.code = code
			bon_transfert.societe_id = societe_id
			bon_transfert.emplacement_origine_id = emplacement_origine_id
			bon_transfert.emplacement_destination_id = emplacement_destination_id
			bon_transfert.status_id = status_id
			bon_transfert.operation_stock_id = operation_stock_id
			bon_transfert.description = description
			bon_transfert.responsable_transfert_id = responsable_transfert_id
			return bon_transfert
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA BON_TRANSFERT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_bon_transfert, request_post = []):
		try:
			bon_transfert  = Model_Bon_transfert()
			if objet_dao_bon_transfert.code != None : bon_transfert.code = objet_dao_bon_transfert.code
			if objet_dao_bon_transfert.societe_id != None : bon_transfert.societe_id = objet_dao_bon_transfert.societe_id
			if objet_dao_bon_transfert.emplacement_origine_id != None : bon_transfert.emplacement_origine_id = objet_dao_bon_transfert.emplacement_origine_id
			if objet_dao_bon_transfert.emplacement_destination_id != None : bon_transfert.emplacement_destination_id = objet_dao_bon_transfert.emplacement_destination_id
			if objet_dao_bon_transfert.status_id != None : bon_transfert.status_id = objet_dao_bon_transfert.status_id
			if objet_dao_bon_transfert.operation_stock_id != None : bon_transfert.operation_stock_id = objet_dao_bon_transfert.operation_stock_id
			if objet_dao_bon_transfert.description != None : bon_transfert.description = objet_dao_bon_transfert.description
			if objet_dao_bon_transfert.responsable_transfert_id != None : bon_transfert.responsable_transfert_id = objet_dao_bon_transfert.responsable_transfert_id
			if auteur != None : bon_transfert.auteur_id = auteur.id

			bon_transfert.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Bon de Transfert [Model_Bon_transfert]'
				utils.history_in_database(data)

			return True, bon_transfert, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA BON_TRANSFERT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_bon_transfert, auteur = None, request_post = []):
		try:
			bon_transfert = Model_Bon_transfert.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_bon_transfert = model_to_dict(bon_transfert)

			bon_transfert.code = objet_dao_bon_transfert.code
			bon_transfert.societe_id = objet_dao_bon_transfert.societe_id
			bon_transfert.emplacement_origine_id = objet_dao_bon_transfert.emplacement_origine_id
			bon_transfert.emplacement_destination_id = objet_dao_bon_transfert.emplacement_destination_id
			bon_transfert.status_id = objet_dao_bon_transfert.status_id
			bon_transfert.operation_stock_id = objet_dao_bon_transfert.operation_stock_id
			bon_transfert.description = objet_dao_bon_transfert.description
			bon_transfert.responsable_transfert_id = objet_dao_bon_transfert.responsable_transfert_id
			if auteur != None : bon_transfert.update_by_id = auteur.id
			bon_transfert.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_bon_transfert, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Bon de Transfert [Model_Bon_transfert]'
				utils.history_in_database(data)

			return True, bon_transfert, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA BON_TRANSFERT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Bon_transfert.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Bon_transfert.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			bon_transfert = Model_Bon_transfert.objects.get(pk = id)
			bon_transfert.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroBonTransfert():
		sortie = dao_bon_transfert.toList().count()
		sortie = sortie + 1
		temp_numero = str(sortie)
		for i in range(len(str(sortie)), 4):
			temp_numero = "0" + temp_numero
		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois
		temp_numero = f"BN-TRFT-{timezone.now().year}{mois}{temp_numero}"
		return temp_numero