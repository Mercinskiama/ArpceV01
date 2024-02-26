from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_statut_ajustement(object):
	designation = ''
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Statut_ajustement.objects.all().order_by('-creation_date')
				return Model_Statut_ajustement.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Statut_ajustement.objects.filter(Q(designation__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Statut_ajustement.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(designation__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE STATUT_AJUSTEMENT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Statut_ajustement.objects.all().order_by('-creation_date')

			return Model_Statut_ajustement.objects.filter(Q(designation__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE STATUT_AJUSTEMENT')
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
					'statut' : item.statut.__str__() if item.statut else '-',
					'etat' : str(item.etat),
					'societe' : item.societe.__str__() if item.societe else '-',
					'creation_date' : item.creation_date,
					'update_date' : item.update_date,
					'update_by' : item.update_by.__str__() if item.update_by else '-',
					'auteur' : item.auteur.__str__() if item.auteur else '-',
				}
				listes.append(element)
			return listes
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE STATUT_AJUSTEMENT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', societe_id = None):
		try:
			statut_ajustement = dao_statut_ajustement()
			statut_ajustement.designation = designation
			statut_ajustement.societe_id = societe_id
			return statut_ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA STATUT_AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_statut_ajustement, request_post = []):
		try:
			statut_ajustement  = Model_Statut_ajustement()
			if objet_dao_statut_ajustement.designation != None : statut_ajustement.designation = objet_dao_statut_ajustement.designation
			if objet_dao_statut_ajustement.societe_id != None : statut_ajustement.societe_id = objet_dao_statut_ajustement.societe_id
			if auteur != None : statut_ajustement.auteur_id = auteur.id

			statut_ajustement.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Statut inventaire [Model_Statut_ajustement]'
				utils.history_in_database(data)

			return True, statut_ajustement, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA STATUT_AJUSTEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_statut_ajustement, auteur = None, request_post = []):
		try:
			statut_ajustement = Model_Statut_ajustement.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_statut_ajustement = model_to_dict(statut_ajustement)

			statut_ajustement.designation = objet_dao_statut_ajustement.designation
			statut_ajustement.societe_id = objet_dao_statut_ajustement.societe_id
			if auteur != None : statut_ajustement.update_by_id = auteur.id
			statut_ajustement.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_statut_ajustement, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Statut inventaire [Model_Statut_ajustement]'
				utils.history_in_database(data)

			return True, statut_ajustement, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA STATUT_AJUSTEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Statut_ajustement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Statut_ajustement.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			statut_ajustement = Model_Statut_ajustement.objects.get(pk = id)
			statut_ajustement.delete()
			return True
		except Exception as e:
			return False