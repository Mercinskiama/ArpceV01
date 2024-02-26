from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_ligne_reception(object):
	bon_reception_id = None
	article_id = None
	societe_id = None
	quantite_demandee = 0.0
	quantite_fait = 0.0
	quantite_reste = 0.0
	prix_unitaire = 0.0
	unite_id = None
	devise_id = None
	description = ''
	fait = False
	series = []

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Ligne_reception.objects.all().order_by('-creation_date')
				return Model_Ligne_reception.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Ligne_reception.objects.filter(Q(quantite_demandee__icontains = query) | Q(quantite_fait__icontains = query) | Q(quantite_reste__icontains = query) | Q(prix_unitaire__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Ligne_reception.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(quantite_demandee__icontains = query) | Q(quantite_fait__icontains = query) | Q(quantite_reste__icontains = query) | Q(prix_unitaire__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_RECEPTION')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Ligne_reception.objects.all().order_by('-creation_date')

			return Model_Ligne_reception.objects.filter(Q(quantite_demandee__icontains = query) | Q(quantite_fait__icontains = query) | Q(quantite_reste__icontains = query) | Q(prix_unitaire__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_RECEPTION')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'bon_reception' : item.bon_reception.__str__() if item.bon_reception else '-',
					'article' : item.article.__str__() if item.article else '-',
					'societe' : item.societe.__str__() if item.societe else '-',
					'quantite_demandee' : makeFloat(item.quantite_demandee),
					'quantite_fait' : makeFloat(item.quantite_fait),
					'quantite_reste' : makeFloat(item.quantite_reste),
					'prix_unitaire' : makeFloat(item.prix_unitaire),
					'unite' : item.unite.__str__() if item.unite else '-',
					'devise' : item.devise.__str__() if item.devise else '-',
					'description' : str(item.description),
					'fait' : item.fait,
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_RECEPTION  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(bon_reception_id = None, article_id = None, societe_id = None, quantite_demandee = 0.0, quantite_fait = 0.0, quantite_reste = 0.0, prix_unitaire = 0.0, unite_id = None, devise_id = None, description = '', fait = False, series = []):
		try:
			ligne_reception = dao_ligne_reception()
			ligne_reception.bon_reception_id = bon_reception_id
			ligne_reception.article_id = article_id
			ligne_reception.societe_id = societe_id
			ligne_reception.quantite_demandee = quantite_demandee
			ligne_reception.quantite_fait = quantite_fait
			ligne_reception.quantite_reste = quantite_reste
			ligne_reception.prix_unitaire = prix_unitaire
			ligne_reception.unite_id = unite_id
			ligne_reception.devise_id = devise_id
			ligne_reception.description = description
			ligne_reception.fait = fait
			ligne_reception.series = series
			return ligne_reception
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_RECEPTION')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_ligne_reception, request_post = []):
		try:
			ligne_reception  = Model_Ligne_reception()
			ligne_reception.bon_reception_id = objet_dao_ligne_reception.bon_reception_id
			ligne_reception.article_id = objet_dao_ligne_reception.article_id
			if objet_dao_ligne_reception.societe_id != None : ligne_reception.societe_id = objet_dao_ligne_reception.societe_id
			if objet_dao_ligne_reception.quantite_demandee != None : ligne_reception.quantite_demandee = objet_dao_ligne_reception.quantite_demandee
			if objet_dao_ligne_reception.quantite_fait != None : ligne_reception.quantite_fait = objet_dao_ligne_reception.quantite_fait
			if objet_dao_ligne_reception.quantite_reste != None : ligne_reception.quantite_reste = objet_dao_ligne_reception.quantite_reste
			if objet_dao_ligne_reception.prix_unitaire != None : ligne_reception.prix_unitaire = objet_dao_ligne_reception.prix_unitaire
			if objet_dao_ligne_reception.unite_id != None : ligne_reception.unite_id = objet_dao_ligne_reception.unite_id
			if objet_dao_ligne_reception.devise_id != None : ligne_reception.devise_id = objet_dao_ligne_reception.devise_id
			if objet_dao_ligne_reception.description != None : ligne_reception.description = objet_dao_ligne_reception.description
			if objet_dao_ligne_reception.fait != None : ligne_reception.fait = objet_dao_ligne_reception.fait
			if auteur != None : ligne_reception.auteur_id = auteur.id

			ligne_reception.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_ligne_reception.series)):
				try:
					objet = Model_Actif.objects.get(pk = objet_dao_ligne_reception.series[i])
					ligne_reception.series.add(objet)
				except Exception as e: pass

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Line Bon de Reception [Model_Ligne_reception]'
				utils.history_in_database(data)

			return True, ligne_reception, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_RECEPTION')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_ligne_reception, auteur = None, request_post = []):
		try:
			ligne_reception = Model_Ligne_reception.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_ligne_reception = model_to_dict(ligne_reception)

			ligne_reception.bon_reception_id = objet_dao_ligne_reception.bon_reception_id
			ligne_reception.article_id = objet_dao_ligne_reception.article_id
			ligne_reception.societe_id = objet_dao_ligne_reception.societe_id
			ligne_reception.quantite_demandee = objet_dao_ligne_reception.quantite_demandee
			ligne_reception.quantite_fait = objet_dao_ligne_reception.quantite_fait
			ligne_reception.quantite_reste = objet_dao_ligne_reception.quantite_reste
			ligne_reception.prix_unitaire = objet_dao_ligne_reception.prix_unitaire
			ligne_reception.unite_id = objet_dao_ligne_reception.unite_id
			ligne_reception.devise_id = objet_dao_ligne_reception.devise_id
			ligne_reception.description = objet_dao_ligne_reception.description
			ligne_reception.fait = objet_dao_ligne_reception.fait
			if auteur != None : ligne_reception.update_by_id = auteur.id
			ligne_reception.save()

			#Mise à jour Champs (ManyToMany - Creation)
			series_old = ligne_reception.series.all()
			series_updated = []
			for i in range(0, len(objet_dao_ligne_reception.series)):
				try:
					objet = Model_Actif.objects.get(pk = objet_dao_ligne_reception.series[i])
					if objet not in series_old: ligne_reception.series.add(objet)
					series_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in series_old:
				if item.id not in series_updated: ligne_reception.series.remove(item)

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_ligne_reception, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Line Bon de Reception [Model_Ligne_reception]'
				utils.history_in_database(data)

			return True, ligne_reception, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_RECEPTION')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Ligne_reception.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Ligne_reception.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			ligne_reception = Model_Ligne_reception.objects.get(pk = id)
			ligne_reception.delete()
			return True
		except Exception as e:
			return False