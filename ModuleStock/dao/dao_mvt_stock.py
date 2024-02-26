from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_mvt_stock(object):
	date = None
	type_id = None
	article_id = None
	emplacement_id = None
	reception_id = None
	transfert_id = None
	sortie_id = None
	retour_id = None
	ajustement_id = None
	rebut_id = None
	quantite_initiale = 0.0
	unite_initiale_id = None
	quantite = 0.0
	societe_id = None
	unite_id = None
	est_rebut = False
	series = []

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Mvt_stock.objects.all().order_by('-creation_date')
				return Model_Mvt_stock.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Mvt_stock.objects.filter(Q(quantite_initiale__icontains = query) | Q(quantite__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Mvt_stock.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(quantite_initiale__icontains = query) | Q(quantite__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE MVT_STOCK')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Mvt_stock.objects.all().order_by('-creation_date')

			return Model_Mvt_stock.objects.filter(Q(quantite_initiale__icontains = query) | Q(quantite__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE MVT_STOCK')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'date' : item.date,
					'type' : item.type.__str__() if item.type else '-',
					'article' : item.article.__str__() if item.article else '-',
					'emplacement' : item.emplacement.__str__() if item.emplacement else '-',
					'reception' : item.reception.__str__() if item.reception else '-',
					'transfert' : item.transfert.__str__() if item.transfert else '-',
					'sortie' : item.sortie.__str__() if item.sortie else '-',
					'retour' : item.retour.__str__() if item.retour else '-',
					'ajustement' : item.ajustement.__str__() if item.ajustement else '-',
					'rebut' : item.rebut.__str__() if item.rebut else '-',
					'quantite_initiale' : makeFloat(item.quantite_initiale),
					'unite_initiale' : item.unite_initiale.__str__() if item.unite_initiale else '-',
					'quantite' : makeFloat(item.quantite),
					'societe' : item.societe.__str__() if item.societe else '-',
					'unite' : item.unite.__str__() if item.unite else '-',
					'est_rebut' : item.est_rebut,
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE MVT_STOCK  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(date = None, type_id = None, article_id = None, emplacement_id = None, reception_id = None, transfert_id = None, sortie_id = None, retour_id = None, ajustement_id = None, rebut_id = None, quantite_initiale = 0.0, unite_initiale_id = None, quantite = 0.0, societe_id = None, unite_id = None, est_rebut = False, series = []):
		try:
			mvt_stock = dao_mvt_stock()
			mvt_stock.date = date
			mvt_stock.type_id = type_id
			mvt_stock.article_id = article_id
			mvt_stock.emplacement_id = emplacement_id
			mvt_stock.reception_id = reception_id
			mvt_stock.transfert_id = transfert_id
			mvt_stock.sortie_id = sortie_id
			mvt_stock.retour_id = retour_id
			mvt_stock.ajustement_id = ajustement_id
			mvt_stock.rebut_id = rebut_id
			mvt_stock.quantite_initiale = quantite_initiale
			mvt_stock.unite_initiale_id = unite_initiale_id
			mvt_stock.quantite = quantite
			mvt_stock.societe_id = societe_id
			mvt_stock.unite_id = unite_id
			mvt_stock.est_rebut = est_rebut
			mvt_stock.series = series
			return mvt_stock
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA MVT_STOCK')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_mvt_stock, request_post = []):
		try:
			mvt_stock  = Model_Mvt_stock()
			mvt_stock.date = objet_dao_mvt_stock.date
			mvt_stock.type_id = objet_dao_mvt_stock.type_id
			mvt_stock.article_id = objet_dao_mvt_stock.article_id
			mvt_stock.emplacement_id = objet_dao_mvt_stock.emplacement_id
			if objet_dao_mvt_stock.reception_id != None : mvt_stock.reception_id = objet_dao_mvt_stock.reception_id
			if objet_dao_mvt_stock.transfert_id != None : mvt_stock.transfert_id = objet_dao_mvt_stock.transfert_id
			if objet_dao_mvt_stock.sortie_id != None : mvt_stock.sortie_id = objet_dao_mvt_stock.sortie_id
			if objet_dao_mvt_stock.retour_id != None : mvt_stock.retour_id = objet_dao_mvt_stock.retour_id
			if objet_dao_mvt_stock.ajustement_id != None : mvt_stock.ajustement_id = objet_dao_mvt_stock.ajustement_id
			if objet_dao_mvt_stock.rebut_id != None : mvt_stock.rebut_id = objet_dao_mvt_stock.rebut_id
			if objet_dao_mvt_stock.quantite_initiale != None : mvt_stock.quantite_initiale = objet_dao_mvt_stock.quantite_initiale
			if objet_dao_mvt_stock.unite_initiale_id != None : mvt_stock.unite_initiale_id = objet_dao_mvt_stock.unite_initiale_id
			if objet_dao_mvt_stock.quantite != None : mvt_stock.quantite = objet_dao_mvt_stock.quantite
			if objet_dao_mvt_stock.societe_id != None : mvt_stock.societe_id = objet_dao_mvt_stock.societe_id
			if objet_dao_mvt_stock.unite_id != None : mvt_stock.unite_id = objet_dao_mvt_stock.unite_id
			if objet_dao_mvt_stock.est_rebut != None : mvt_stock.est_rebut = objet_dao_mvt_stock.est_rebut
			if auteur != None : mvt_stock.auteur_id = auteur.id

			mvt_stock.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_mvt_stock.series)):
				try:
					objet = Model_Actif.objects.get(pk = objet_dao_mvt_stock.series[i])
					mvt_stock.series.add(objet)
				except Exception as e: pass

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Mouvement stock [Model_Mvt_stock]'
				utils.history_in_database(data)

			return True, mvt_stock, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA MVT_STOCK')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_mvt_stock, auteur = None, request_post = []):
		try:
			mvt_stock = Model_Mvt_stock.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_mvt_stock = model_to_dict(mvt_stock)

			mvt_stock.date = objet_dao_mvt_stock.date
			mvt_stock.type_id = objet_dao_mvt_stock.type_id
			mvt_stock.article_id = objet_dao_mvt_stock.article_id
			mvt_stock.emplacement_id = objet_dao_mvt_stock.emplacement_id
			mvt_stock.reception_id = objet_dao_mvt_stock.reception_id
			mvt_stock.transfert_id = objet_dao_mvt_stock.transfert_id
			mvt_stock.sortie_id = objet_dao_mvt_stock.sortie_id
			mvt_stock.retour_id = objet_dao_mvt_stock.retour_id
			mvt_stock.ajustement_id = objet_dao_mvt_stock.ajustement_id
			mvt_stock.rebut_id = objet_dao_mvt_stock.rebut_id
			mvt_stock.quantite_initiale = objet_dao_mvt_stock.quantite_initiale
			mvt_stock.unite_initiale_id = objet_dao_mvt_stock.unite_initiale_id
			mvt_stock.quantite = objet_dao_mvt_stock.quantite
			mvt_stock.societe_id = objet_dao_mvt_stock.societe_id
			mvt_stock.unite_id = objet_dao_mvt_stock.unite_id
			mvt_stock.est_rebut = objet_dao_mvt_stock.est_rebut
			if auteur != None : mvt_stock.update_by_id = auteur.id
			mvt_stock.save()

			#Mise à jour Champs (ManyToMany - Creation)
			series_old = mvt_stock.series.all()
			series_updated = []
			for i in range(0, len(objet_dao_mvt_stock.series)):
				try:
					objet = Model_Actif.objects.get(pk = objet_dao_mvt_stock.series[i])
					if objet not in series_old: mvt_stock.series.add(objet)
					series_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in series_old:
				if item.id not in series_updated: mvt_stock.series.remove(item)

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_mvt_stock, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Mouvement stock [Model_Mvt_stock]'
				utils.history_in_database(data)

			return True, mvt_stock, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA MVT_STOCK')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Mvt_stock.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Mvt_stock.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			mvt_stock = Model_Mvt_stock.objects.get(pk = id)
			mvt_stock.delete()
			return True
		except Exception as e:
			return False