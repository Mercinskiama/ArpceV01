from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_ligne_bon_transfert(object):
	quantite = 0.0
	quantite_fait = 0.0
	article_id = None
	description = ''
	societe_id = None
	fait = False
	bon_transfert_id = None
	stockage_id = None
	series = []

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Ligne_bon_transfert.objects.all().order_by('-creation_date')
				return Model_Ligne_bon_transfert.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Ligne_bon_transfert.objects.filter(Q(quantite__icontains = query) | Q(quantite_fait__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Ligne_bon_transfert.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(quantite__icontains = query) | Q(quantite_fait__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_BON_TRANSFERT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Ligne_bon_transfert.objects.all().order_by('-creation_date')

			return Model_Ligne_bon_transfert.objects.filter(Q(quantite__icontains = query) | Q(quantite_fait__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_BON_TRANSFERT')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'quantite' : makeFloat(item.quantite),
					'quantite_fait' : makeFloat(item.quantite_fait),
					'article' : item.article.__str__() if item.article else '-',
					'description' : str(item.description),
					'societe' : item.societe.__str__() if item.societe else '-',
					'fait' : item.fait,
					'bon_transfert' : item.bon_transfert.__str__() if item.bon_transfert else '-',
					'stockage' : item.stockage.__str__() if item.stockage else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_BON_TRANSFERT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(quantite = 0.0, quantite_fait = 0.0, article_id = None, description = '', societe_id = None, fait = False, bon_transfert_id = None, stockage_id = None, series = []):
		try:
			ligne_bon_transfert = dao_ligne_bon_transfert()
			ligne_bon_transfert.quantite = quantite
			ligne_bon_transfert.quantite_fait = quantite_fait
			ligne_bon_transfert.article_id = article_id
			ligne_bon_transfert.description = description
			ligne_bon_transfert.societe_id = societe_id
			ligne_bon_transfert.fait = fait
			ligne_bon_transfert.bon_transfert_id = bon_transfert_id
			ligne_bon_transfert.stockage_id = stockage_id
			ligne_bon_transfert.series = series
			return ligne_bon_transfert
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_BON_TRANSFERT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_ligne_bon_transfert, request_post = []):
		try:
			ligne_bon_transfert  = Model_Ligne_bon_transfert()
			if objet_dao_ligne_bon_transfert.quantite != None : ligne_bon_transfert.quantite = objet_dao_ligne_bon_transfert.quantite
			if objet_dao_ligne_bon_transfert.quantite_fait != None : ligne_bon_transfert.quantite_fait = objet_dao_ligne_bon_transfert.quantite_fait
			ligne_bon_transfert.article_id = objet_dao_ligne_bon_transfert.article_id
			if objet_dao_ligne_bon_transfert.description != None : ligne_bon_transfert.description = objet_dao_ligne_bon_transfert.description
			if objet_dao_ligne_bon_transfert.societe_id != None : ligne_bon_transfert.societe_id = objet_dao_ligne_bon_transfert.societe_id
			if objet_dao_ligne_bon_transfert.fait != None : ligne_bon_transfert.fait = objet_dao_ligne_bon_transfert.fait
			if objet_dao_ligne_bon_transfert.bon_transfert_id != None : ligne_bon_transfert.bon_transfert_id = objet_dao_ligne_bon_transfert.bon_transfert_id
			if objet_dao_ligne_bon_transfert.stockage_id != None : ligne_bon_transfert.stockage_id = objet_dao_ligne_bon_transfert.stockage_id
			if auteur != None : ligne_bon_transfert.auteur_id = auteur.id

			ligne_bon_transfert.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_ligne_bon_transfert.series)):
				try:
					objet = Model_Actif.objects.get(pk = objet_dao_ligne_bon_transfert.series[i])
					ligne_bon_transfert.series.add(objet)
				except Exception as e: pass

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Line bon de Transfert [Model_Ligne_bon_transfert]'
				utils.history_in_database(data)

			return True, ligne_bon_transfert, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_BON_TRANSFERT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_ligne_bon_transfert, auteur = None, request_post = []):
		try:
			ligne_bon_transfert = Model_Ligne_bon_transfert.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_ligne_bon_transfert = model_to_dict(ligne_bon_transfert)

			ligne_bon_transfert.quantite = objet_dao_ligne_bon_transfert.quantite
			ligne_bon_transfert.quantite_fait = objet_dao_ligne_bon_transfert.quantite_fait
			ligne_bon_transfert.article_id = objet_dao_ligne_bon_transfert.article_id
			ligne_bon_transfert.description = objet_dao_ligne_bon_transfert.description
			ligne_bon_transfert.societe_id = objet_dao_ligne_bon_transfert.societe_id
			ligne_bon_transfert.fait = objet_dao_ligne_bon_transfert.fait
			ligne_bon_transfert.bon_transfert_id = objet_dao_ligne_bon_transfert.bon_transfert_id
			ligne_bon_transfert.stockage_id = objet_dao_ligne_bon_transfert.stockage_id
			if auteur != None : ligne_bon_transfert.update_by_id = auteur.id
			ligne_bon_transfert.save()

			#Mise à jour Champs (ManyToMany - Creation)
			series_old = ligne_bon_transfert.series.all()
			series_updated = []
			for i in range(0, len(objet_dao_ligne_bon_transfert.series)):
				try:
					objet = Model_Actif.objects.get(pk = objet_dao_ligne_bon_transfert.series[i])
					if objet not in series_old: ligne_bon_transfert.series.add(objet)
					series_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in series_old:
				if item.id not in series_updated: ligne_bon_transfert.series.remove(item)

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_ligne_bon_transfert, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Line bon de Transfert [Model_Ligne_bon_transfert]'
				utils.history_in_database(data)

			return True, ligne_bon_transfert, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_BON_TRANSFERT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Ligne_bon_transfert.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Ligne_bon_transfert.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			ligne_bon_transfert = Model_Ligne_bon_transfert.objects.get(pk = id)
			ligne_bon_transfert.delete()
			return True
		except Exception as e:
			return False