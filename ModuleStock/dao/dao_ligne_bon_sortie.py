from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_ligne_bon_sortie(object):
	quantite_demandee = 0.0
	quantite_sortie = 0.0
	serie_id = None
	description = ''
	bon_sortie_id = None
	article_id = None
	stockage_id = None
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Ligne_bon_sortie.objects.all().order_by('-creation_date')
				return Model_Ligne_bon_sortie.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Ligne_bon_sortie.objects.filter(Q(quantite_demandee__icontains = query) | Q(quantite_sortie__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Ligne_bon_sortie.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(quantite_demandee__icontains = query) | Q(quantite_sortie__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_BON_SORTIE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Ligne_bon_sortie.objects.all().order_by('-creation_date')

			return Model_Ligne_bon_sortie.objects.filter(Q(quantite_demandee__icontains = query) | Q(quantite_sortie__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_BON_SORTIE')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'quantite_demandee' : makeFloat(item.quantite_demandee),
					'quantite_sortie' : makeFloat(item.quantite_sortie),
					'serie' : item.serie.__str__() if item.serie else '-',
					'description' : str(item.description),
					'bon_sortie' : item.bon_sortie.__str__() if item.bon_sortie else '-',
					'article' : item.article.__str__() if item.article else '-',
					'stockage' : item.stockage.__str__() if item.stockage else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_BON_SORTIE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(quantite_demandee = 0.0, quantite_sortie = 0.0, serie_id = None, description = '', bon_sortie_id = None, article_id = None, stockage_id = None, societe_id = None):
		try:
			ligne_bon_sortie = dao_ligne_bon_sortie()
			ligne_bon_sortie.quantite_demandee = quantite_demandee
			ligne_bon_sortie.quantite_sortie = quantite_sortie
			ligne_bon_sortie.serie_id = serie_id
			ligne_bon_sortie.description = description
			ligne_bon_sortie.bon_sortie_id = bon_sortie_id
			ligne_bon_sortie.article_id = article_id
			ligne_bon_sortie.stockage_id = stockage_id
			ligne_bon_sortie.societe_id = societe_id
			return ligne_bon_sortie
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_BON_SORTIE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_ligne_bon_sortie, request_post = []):
		try:
			ligne_bon_sortie  = Model_Ligne_bon_sortie()
			if objet_dao_ligne_bon_sortie.quantite_demandee != None : ligne_bon_sortie.quantite_demandee = objet_dao_ligne_bon_sortie.quantite_demandee
			if objet_dao_ligne_bon_sortie.quantite_sortie != None : ligne_bon_sortie.quantite_sortie = objet_dao_ligne_bon_sortie.quantite_sortie
			if objet_dao_ligne_bon_sortie.serie_id != None : ligne_bon_sortie.serie_id = objet_dao_ligne_bon_sortie.serie_id
			if objet_dao_ligne_bon_sortie.description != None : ligne_bon_sortie.description = objet_dao_ligne_bon_sortie.description
			if objet_dao_ligne_bon_sortie.bon_sortie_id != None : ligne_bon_sortie.bon_sortie_id = objet_dao_ligne_bon_sortie.bon_sortie_id
			if objet_dao_ligne_bon_sortie.article_id != None : ligne_bon_sortie.article_id = objet_dao_ligne_bon_sortie.article_id
			if objet_dao_ligne_bon_sortie.stockage_id != None : ligne_bon_sortie.stockage_id = objet_dao_ligne_bon_sortie.stockage_id
			if objet_dao_ligne_bon_sortie.societe_id != None : ligne_bon_sortie.societe_id = objet_dao_ligne_bon_sortie.societe_id
			if auteur != None : ligne_bon_sortie.auteur_id = auteur.id

			ligne_bon_sortie.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Line Bon de Sortie [Model_Ligne_bon_sortie]'
				utils.history_in_database(data)

			return True, ligne_bon_sortie, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_BON_SORTIE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_ligne_bon_sortie, auteur = None, request_post = []):
		try:
			ligne_bon_sortie = Model_Ligne_bon_sortie.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_ligne_bon_sortie = model_to_dict(ligne_bon_sortie)

			ligne_bon_sortie.quantite_demandee = objet_dao_ligne_bon_sortie.quantite_demandee
			ligne_bon_sortie.quantite_sortie = objet_dao_ligne_bon_sortie.quantite_sortie
			ligne_bon_sortie.serie_id = objet_dao_ligne_bon_sortie.serie_id
			ligne_bon_sortie.description = objet_dao_ligne_bon_sortie.description
			ligne_bon_sortie.bon_sortie_id = objet_dao_ligne_bon_sortie.bon_sortie_id
			ligne_bon_sortie.article_id = objet_dao_ligne_bon_sortie.article_id
			ligne_bon_sortie.stockage_id = objet_dao_ligne_bon_sortie.stockage_id
			ligne_bon_sortie.societe_id = objet_dao_ligne_bon_sortie.societe_id
			if auteur != None : ligne_bon_sortie.update_by_id = auteur.id
			ligne_bon_sortie.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_ligne_bon_sortie, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Line Bon de Sortie [Model_Ligne_bon_sortie]'
				utils.history_in_database(data)

			return True, ligne_bon_sortie, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_BON_SORTIE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Ligne_bon_sortie.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Ligne_bon_sortie.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			ligne_bon_sortie = Model_Ligne_bon_sortie.objects.get(pk = id)
			ligne_bon_sortie.delete()
			return True
		except Exception as e:
			return False