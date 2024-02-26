from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_actif(object):
	article_id = None
	numero_serie = ''
	est_actif = False
	emplacement_id = None
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Actif.objects.all().order_by('-creation_date')
				return Model_Actif.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Actif.objects.filter(Q(numero_serie__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Actif.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(numero_serie__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ACTIF')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Actif.objects.all().order_by('-creation_date')

			return Model_Actif.objects.filter(Q(numero_serie__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ACTIF')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'article' : item.article.__str__() if item.article else '-',
					'numero_serie' : str(item.numero_serie),
					'est_actif' : item.est_actif,
					'emplacement' : item.emplacement.__str__() if item.emplacement else '-',
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ACTIF  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(article_id = None, numero_serie = '', est_actif = False, emplacement_id = None, societe_id = None):
		try:
			actif = dao_actif()
			actif.article_id = article_id
			actif.numero_serie = numero_serie
			actif.est_actif = est_actif
			actif.emplacement_id = emplacement_id
			actif.societe_id = societe_id
			return actif
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ACTIF')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_actif, request_post = []):
		try:
			actif  = Model_Actif()
			actif.article_id = objet_dao_actif.article_id
			if objet_dao_actif.numero_serie != None : actif.numero_serie = objet_dao_actif.numero_serie
			if objet_dao_actif.est_actif != None : actif.est_actif = objet_dao_actif.est_actif
			if objet_dao_actif.emplacement_id != None : actif.emplacement_id = objet_dao_actif.emplacement_id
			if objet_dao_actif.societe_id != None : actif.societe_id = objet_dao_actif.societe_id
			if auteur != None : actif.auteur_id = auteur.id

			actif.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Actif [Model_Actif]'
				utils.history_in_database(data)

			return True, actif, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ACTIF')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_actif, auteur = None, request_post = []):
		try:
			actif = Model_Actif.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_actif = model_to_dict(actif)

			actif.article_id = objet_dao_actif.article_id
			actif.numero_serie = objet_dao_actif.numero_serie
			actif.est_actif = objet_dao_actif.est_actif
			actif.emplacement_id = objet_dao_actif.emplacement_id
			actif.societe_id = objet_dao_actif.societe_id
			if auteur != None : actif.update_by_id = auteur.id
			actif.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_actif, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Actif [Model_Actif]'
				utils.history_in_database(data)

			return True, actif, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ACTIF')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Actif.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Actif.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			actif = Model_Actif.objects.get(pk = id)
			actif.delete()
			return True
		except Exception as e:
			return False