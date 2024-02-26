from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_type_article(object):
	designation = ''
	est_service = False
	societe_id = None

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Type_article.objects.all().order_by('-creation_date')
				return Model_Type_article.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Type_article.objects.filter(Q(designation__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Type_article.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(designation__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_ARTICLE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Type_article.objects.all().order_by('-creation_date')

			return Model_Type_article.objects.filter(Q(designation__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_ARTICLE')
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
					'est_service' : item.est_service,
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TYPE_ARTICLE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', est_service = False, societe_id = None):
		try:
			type_article = dao_type_article()
			type_article.designation = designation
			type_article.est_service = est_service
			type_article.societe_id = societe_id
			return type_article
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPE_ARTICLE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_type_article, request_post = []):
		try:
			type_article  = Model_Type_article()
			type_article.designation = objet_dao_type_article.designation
			if objet_dao_type_article.est_service != None : type_article.est_service = objet_dao_type_article.est_service
			if objet_dao_type_article.societe_id != None : type_article.societe_id = objet_dao_type_article.societe_id
			if auteur != None : type_article.auteur_id = auteur.id

			type_article.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Type d\'Article [Model_Type_article]'
				utils.history_in_database(data)

			return True, type_article, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPE_ARTICLE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_type_article, auteur = None, request_post = []):
		try:
			type_article = Model_Type_article.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_type_article = model_to_dict(type_article)

			type_article.designation = objet_dao_type_article.designation
			type_article.est_service = objet_dao_type_article.est_service
			type_article.societe_id = objet_dao_type_article.societe_id
			if auteur != None : type_article.update_by_id = auteur.id
			type_article.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_type_article, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Type d\'Article [Model_Type_article]'
				utils.history_in_database(data)

			return True, type_article, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPE_ARTICLE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Type_article.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Type_article.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			type_article = Model_Type_article.objects.get(pk = id)
			type_article.delete()
			return True
		except Exception as e:
			return False