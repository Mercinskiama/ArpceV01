from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_article(object):
	name = ''
	code = ''
	amount = 0.0
	devise_id = None
	type_article_id = None
	picture_icon = None
	societe_id = None
	quota_quantity = 0
	category_id = None
	measure_unit_id = None
	description = ''

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Article.objects.all().order_by('-creation_date')
				return Model_Article.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Article.objects.filter(Q(name__icontains = query) | Q(code__icontains = query) | Q(amount__icontains = query) | Q(quota_quantity__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Article.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(name__icontains = query) | Q(code__icontains = query) | Q(amount__icontains = query) | Q(quota_quantity__icontains = query) | Q(description__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ARTICLE')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Article.objects.all().order_by('-creation_date')

			return Model_Article.objects.filter(Q(name__icontains = query) | Q(code__icontains = query) | Q(amount__icontains = query) | Q(quota_quantity__icontains = query) | Q(description__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ARTICLE')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'name' : str(item.name),
					'code' : str(item.code),
					'amount' : makeFloat(item.amount),
					'devise' : item.devise.__str__() if item.devise else '-',
					'type_article' : item.type_article.__str__() if item.type_article else '-',
					'picture_icon' : item.picture_icon.url if item.picture_icon != None else None,
					'societe' : item.societe.__str__() if item.societe else '-',
					'quota_quantity' : makeInt(item.quota_quantity),
					'category' : item.category.__str__() if item.category else '-',
					'measure_unit' : item.measure_unit.__str__() if item.measure_unit else '-',
					'description' : str(item.description),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ARTICLE  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(name = '', code = '', amount = 0.0, devise_id = None, type_article_id = None, picture_icon = None, societe_id = None, quota_quantity = 0, category_id = None, measure_unit_id = None, description = ''):
		try:
			article = dao_article()
			article.name = name
			article.code = code
			article.amount = amount
			article.devise_id = devise_id
			article.type_article_id = type_article_id
			article.picture_icon = picture_icon
			article.societe_id = societe_id
			article.quota_quantity = quota_quantity
			article.category_id = category_id
			article.measure_unit_id = measure_unit_id
			article.description = description
			return article
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ARTICLE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_article, request_post = []):
		try:
			article  = Model_Article()
			if objet_dao_article.name != None : article.name = objet_dao_article.name
			if objet_dao_article.code != None : article.code = objet_dao_article.code
			if objet_dao_article.amount != None : article.amount = objet_dao_article.amount
			if objet_dao_article.devise_id != None : article.devise_id = objet_dao_article.devise_id
			if objet_dao_article.type_article_id != None : article.type_article_id = objet_dao_article.type_article_id
			if objet_dao_article.picture_icon != None : article.picture_icon = objet_dao_article.picture_icon
			if objet_dao_article.societe_id != None : article.societe_id = objet_dao_article.societe_id
			if objet_dao_article.quota_quantity != None : article.quota_quantity = objet_dao_article.quota_quantity
			if objet_dao_article.category_id != None : article.category_id = objet_dao_article.category_id
			if objet_dao_article.measure_unit_id != None : article.measure_unit_id = objet_dao_article.measure_unit_id
			if objet_dao_article.description != None : article.description = objet_dao_article.description
			if auteur != None : article.auteur_id = auteur.id

			article.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Article [Model_Article]'
				utils.history_in_database(data)

			return True, article, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ARTICLE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_article, auteur = None, request_post = []):
		try:
			article = Model_Article.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_article = model_to_dict(article)

			article.name = objet_dao_article.name
			article.code = objet_dao_article.code
			article.amount = objet_dao_article.amount
			article.devise_id = objet_dao_article.devise_id
			article.type_article_id = objet_dao_article.type_article_id
			if objet_dao_article.picture_icon != None : article.picture_icon = objet_dao_article.picture_icon
			article.societe_id = objet_dao_article.societe_id
			article.quota_quantity = objet_dao_article.quota_quantity
			article.category_id = objet_dao_article.category_id
			article.measure_unit_id = objet_dao_article.measure_unit_id
			article.description = objet_dao_article.description
			if auteur != None : article.update_by_id = auteur.id
			article.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_article, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Article [Model_Article]'
				utils.history_in_database(data)

			return True, article, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ARTICLE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Article.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Article.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			article = Model_Article.objects.get(pk = id)
			article.delete()
			return True
		except Exception as e:
			return False