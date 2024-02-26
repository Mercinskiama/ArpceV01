from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_ligne_ajustement(object):
	ajustement_id = None
	article_id = None
	societe_id = None
	quantite_theorique = 0.0
	quantite_reelle = 0.0
	unite_id = None
	fait = False
	series = []

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Ligne_ajustement.objects.all().order_by('-creation_date')
				return Model_Ligne_ajustement.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Ligne_ajustement.objects.filter(Q(quantite_theorique__icontains = query) | Q(quantite_reelle__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Ligne_ajustement.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(quantite_theorique__icontains = query) | Q(quantite_reelle__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_AJUSTEMENT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Ligne_ajustement.objects.all().order_by('-creation_date')

			return Model_Ligne_ajustement.objects.filter(Q(quantite_theorique__icontains = query) | Q(quantite_reelle__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_AJUSTEMENT')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'ajustement' : item.ajustement.__str__() if item.ajustement else '-',
					'article' : item.article.__str__() if item.article else '-',
					'societe' : item.societe.__str__() if item.societe else '-',
					'quantite_theorique' : makeFloat(item.quantite_theorique),
					'quantite_reelle' : makeFloat(item.quantite_reelle),
					'unite' : item.unite.__str__() if item.unite else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LIGNE_AJUSTEMENT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(ajustement_id = None, article_id = None, societe_id = None, quantite_theorique = 0.0, quantite_reelle = 0.0, unite_id = None, fait = False, series = []):
		try:
			ligne_ajustement = dao_ligne_ajustement()
			ligne_ajustement.ajustement_id = ajustement_id
			ligne_ajustement.article_id = article_id
			ligne_ajustement.societe_id = societe_id
			ligne_ajustement.quantite_theorique = quantite_theorique
			ligne_ajustement.quantite_reelle = quantite_reelle
			ligne_ajustement.unite_id = unite_id
			ligne_ajustement.fait = fait
			ligne_ajustement.series = series
			return ligne_ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_ligne_ajustement, request_post = []):
		try:
			ligne_ajustement  = Model_Ligne_ajustement()
			ligne_ajustement.ajustement_id = objet_dao_ligne_ajustement.ajustement_id
			if objet_dao_ligne_ajustement.article_id != None : ligne_ajustement.article_id = objet_dao_ligne_ajustement.article_id
			if objet_dao_ligne_ajustement.societe_id != None : ligne_ajustement.societe_id = objet_dao_ligne_ajustement.societe_id
			if objet_dao_ligne_ajustement.quantite_theorique != None : ligne_ajustement.quantite_theorique = objet_dao_ligne_ajustement.quantite_theorique
			if objet_dao_ligne_ajustement.quantite_reelle != None : ligne_ajustement.quantite_reelle = objet_dao_ligne_ajustement.quantite_reelle
			if objet_dao_ligne_ajustement.unite_id != None : ligne_ajustement.unite_id = objet_dao_ligne_ajustement.unite_id
			if objet_dao_ligne_ajustement.fait != None : ligne_ajustement.fait = objet_dao_ligne_ajustement.fait
			if auteur != None : ligne_ajustement.auteur_id = auteur.id

			ligne_ajustement.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_ligne_ajustement.series)):
				try:
					objet = Model_Actif.objects.get(pk = objet_dao_ligne_ajustement.series[i])
					ligne_ajustement.series.add(objet)
				except Exception as e: pass

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Ligne Inventaire [Model_Ligne_ajustement]'
				utils.history_in_database(data)

			return True, ligne_ajustement, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_AJUSTEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_ligne_ajustement, auteur = None, request_post = []):
		try:
			ligne_ajustement = Model_Ligne_ajustement.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_ligne_ajustement = model_to_dict(ligne_ajustement)

			ligne_ajustement.ajustement_id = objet_dao_ligne_ajustement.ajustement_id
			ligne_ajustement.article_id = objet_dao_ligne_ajustement.article_id
			ligne_ajustement.societe_id = objet_dao_ligne_ajustement.societe_id
			ligne_ajustement.quantite_theorique = objet_dao_ligne_ajustement.quantite_theorique
			ligne_ajustement.quantite_reelle = objet_dao_ligne_ajustement.quantite_reelle
			ligne_ajustement.unite_id = objet_dao_ligne_ajustement.unite_id
			ligne_ajustement.fait = objet_dao_ligne_ajustement.fait
			if auteur != None : ligne_ajustement.update_by_id = auteur.id
			ligne_ajustement.save()

			#Mise à jour Champs (ManyToMany - Creation)
			series_old = ligne_ajustement.series.all()
			series_updated = []
			for i in range(0, len(objet_dao_ligne_ajustement.series)):
				try:
					objet = Model_Actif.objects.get(pk = objet_dao_ligne_ajustement.series[i])
					if objet not in series_old: ligne_ajustement.series.add(objet)
					series_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in series_old:
				if item.id not in series_updated: ligne_ajustement.series.remove(item)

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_ligne_ajustement, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Ligne Inventaire [Model_Ligne_ajustement]'
				utils.history_in_database(data)

			return True, ligne_ajustement, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_AJUSTEMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Ligne_ajustement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Ligne_ajustement.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			ligne_ajustement = Model_Ligne_ajustement.objects.get(pk = id)
			ligne_ajustement.delete()
			return True
		except Exception as e:
			return False