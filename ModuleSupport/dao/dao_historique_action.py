from __future__ import unicode_literals
from ModuleSupport.models import *
from ErpBackOffice.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone

class dao_historique_action(object):
	valeur_avant = ''
	valeur_apres = ''
	modele = ''
	auteur = ''

	@staticmethod
	def toList(query=''):
		try:
			if query == '':
				return Model_Historique_action.objects.all().order_by('creation_date')

			return Model_Historique_action.objects.filter(Q(valeur_avant__icontains = query) | Q(valeur_apres__icontains = query) | Q(modele__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE HISTORIQUE_ACTION')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'valeur_avant' : str(item.valeur_avant),
					'valeur_apres' : str(item.valeur_apres),
					'modele' : str(item.modele),
					'auteur' : str(item.auteur),
					'etat' : str(item.etat),
					'creation_date' : item.creation_date,
					'update_date' : item.update_date,
				}
				listes.append(element)
			return listes
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE HISTORIQUE_ACTION  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(auteur = "", valeur_avant = '', valeur_apres = '', modele = ''):
		try:
			historique_action = dao_historique_action()
			historique_action.auteur = auteur
			historique_action.valeur_avant = valeur_avant
			historique_action.valeur_apres = valeur_apres
			historique_action.modele = modele
			return historique_action
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA HISTORIQUE_ACTION')
			#print(e)
			return None

	@staticmethod
	def toSave(objet_dao_historique_action):
		try:
			historique_action  = Model_Historique_action()
			if objet_dao_historique_action.auteur != None : historique_action.auteur = objet_dao_historique_action.auteur
			if objet_dao_historique_action.valeur_avant != None : historique_action.valeur_avant = objet_dao_historique_action.valeur_avant
			if objet_dao_historique_action.valeur_apres != None : historique_action.valeur_apres = objet_dao_historique_action.valeur_apres
			if objet_dao_historique_action.modele != None : historique_action.modele = objet_dao_historique_action.modele

			historique_action.save()

			return True, historique_action, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA HISTORIQUE_ACTION')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_historique_action, auteur = None):
		try:
			historique_action = Model_Historique_action.objects.get(pk = id)
			historique_action.valeur_avant = objet_dao_historique_action.valeur_avant
			historique_action.valeur_apres = objet_dao_historique_action.valeur_apres
			historique_action.modele = objet_dao_historique_action.modele
			if auteur != None : historique_action.update_by_id = auteur.id
			historique_action.save()

			return True, historique_action, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA HISTORIQUE_ACTION')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Historique_action.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Historique_action.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			historique_action = Model_Historique_action.objects.get(pk = id)
			historique_action.delete()
			return True
		except Exception as e:
			return False