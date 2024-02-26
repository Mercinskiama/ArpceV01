from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_stockage(object):
	emplacement_id = None
	article_id = None
	quantite = 0.0
	unite_id = None
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Stockage.objects.all().order_by('-creation_date')
				return Model_Stockage.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Stockage.objects.filter(Q(quantite__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Stockage.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(quantite__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE STOCKAGE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Stockage.objects.all().order_by('-creation_date')

			return Model_Stockage.objects.filter(Q(quantite__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE STOCKAGE')
			#print(e)
			return []

	@staticmethod
	def toListStock():
		try:
			return Model_Emplacement.objects.filter(Q(visible = True) | Q(type_emplacement_id = 2)).order_by('creation_date')
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE EMPLACEMENT')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'emplacement' : item.emplacement.__str__() if item.emplacement else '-',
					'article' : item.article.__str__() if item.article else '-',
					'quantite' : makeFloat(item.quantite),
					'unite' : item.unite.__str__() if item.unite else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE STOCKAGE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(emplacement_id = None, article_id = None, quantite = 0.0, unite_id = None, societe_id = None):
		try:
			stockage = dao_stockage()
			stockage.emplacement_id = emplacement_id
			stockage.article_id = article_id
			stockage.quantite = quantite
			stockage.unite_id = unite_id
			stockage.societe_id = societe_id
			return stockage
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA STOCKAGE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_stockage, request_post = []):
		try:
			stockage  = Model_Stockage()
			stockage.emplacement_id = objet_dao_stockage.emplacement_id
			stockage.article_id = objet_dao_stockage.article_id
			if objet_dao_stockage.quantite != None : stockage.quantite = objet_dao_stockage.quantite
			if objet_dao_stockage.unite_id != None : stockage.unite_id = objet_dao_stockage.unite_id
			if objet_dao_stockage.societe_id != None : stockage.societe_id = objet_dao_stockage.societe_id
			if auteur != None : stockage.auteur_id = auteur.id

			stockage.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Stockage [Model_Stockage]'
				utils.history_in_database(data)

			return True, stockage, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA STOCKAGE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_stockage, auteur = None, request_post = []):
		try:
			stockage = Model_Stockage.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_stockage = model_to_dict(stockage)

			stockage.emplacement_id = objet_dao_stockage.emplacement_id
			stockage.article_id = objet_dao_stockage.article_id
			stockage.quantite = objet_dao_stockage.quantite
			stockage.unite_id = objet_dao_stockage.unite_id
			stockage.societe_id = objet_dao_stockage.societe_id
			if auteur != None : stockage.update_by_id = auteur.id
			stockage.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_stockage, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Stockage [Model_Stockage]'
				utils.history_in_database(data)

			return True, stockage, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA STOCKAGE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Stockage.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Stockage.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			stockage = Model_Stockage.objects.get(pk = id)
			stockage.delete()
			return True
		except Exception as e:
			return False