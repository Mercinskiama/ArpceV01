from __future__ import unicode_literals
from ModuleConfiguration.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_query(object):
	numero = ''
	designation = ''
	role_id = None
	slq_query = ''
	description = ''
	champs_afficher = ''
	visibilite = ''
	type_view = ''
	est_regroupe = False
	regr_count = 0
	chart_type = ''
	chart_view = ''
	legend_dataset = ''
	title_card = ''
	model_id = None

	@staticmethod
	def toList(query=''):
		try:
			if query == '':
				return Model_Query.objects.all().order_by('creation_date')

			return Model_Query.objects.filter(Q(numero__icontains = query) | Q(designation__icontains = query) | Q(query__icontains = query) | Q(description__icontains = query) | Q(champs_afficher__icontains = query) | Q(visibilite__icontains = query) | Q(type_view__icontains = query) | Q(regr_count__icontains = query) | Q(chart_type__icontains = query) | Q(legend_dataset__icontains = query) | Q(title_card__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE QUERY')
			#print(e)
			return []

	@staticmethod
	def toCreate(numero = '', designation = '', role_id = None, slq_query = '', description = '', champs_afficher = '', visibilite = 1, type_view = '', est_regroupe = None, regr_count = None, chart_type = '', chart_view = '', legend_dataset = '', title_card = '', model_id = None):
		try:
			query = dao_query()
			query.numero = numero
			query.designation = designation
			query.role_id = role_id
			query.slq_query = slq_query
			query.description = description
			query.champs_afficher = champs_afficher
			query.visibilite = visibilite
			query.type_view = type_view
			query.chart_view = chart_view
			query.est_regroupe = est_regroupe
			query.regr_count = regr_count
			query.chart_type = chart_type
			query.legend_dataset = legend_dataset
			query.title_card = title_card
			query.model_id = model_id
			return query
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA QUERY')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_query):
		try:
			query  = Model_Query()
			if objet_dao_query.numero != None : query.numero = objet_dao_query.numero
			if objet_dao_query.designation != None : query.designation = objet_dao_query.designation
			if objet_dao_query.role_id != None : query.role_id = objet_dao_query.role_id
			if objet_dao_query.slq_query != None : query.query = objet_dao_query.slq_query
			if objet_dao_query.description != None : query.description = objet_dao_query.description
			if objet_dao_query.champs_afficher != None : query.champs_afficher = objet_dao_query.champs_afficher
			if objet_dao_query.visibilite != None : query.visibilite = objet_dao_query.visibilite
			if objet_dao_query.type_view != None : query.type_view = objet_dao_query.type_view
			if objet_dao_query.est_regroupe != None : query.est_regroupe = objet_dao_query.est_regroupe
			if objet_dao_query.regr_count != None : query.regr_count = objet_dao_query.regr_count
			if objet_dao_query.chart_type != None : query.chart_type = objet_dao_query.chart_type
			if objet_dao_query.chart_view != None : query.chart_view = objet_dao_query.chart_view
			if objet_dao_query.legend_dataset != None : query.legend_dataset = objet_dao_query.legend_dataset
			if objet_dao_query.title_card != None : query.title_card = objet_dao_query.title_card
			if objet_dao_query.model_id != None : query.model_id = objet_dao_query.model_id
			if auteur != None : query.auteur_id = auteur.id

			query.save()

			return True, query, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA QUERY')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_query):
		try:
			query = Model_Query.objects.get(pk = id)
			query.numero = objet_dao_query.numero
			query.designation = objet_dao_query.designation
			query.role_id = objet_dao_query.role_id
			query.query = objet_dao_query.slq_query
			query.description = objet_dao_query.description
			query.champs_afficher = objet_dao_query.champs_afficher
			query.visibilite = objet_dao_query.visibilite
			query.type_view = objet_dao_query.type_view
			query.est_regroupe = objet_dao_query.est_regroupe
			query.regr_count = objet_dao_query.regr_count
			query.chart_type = objet_dao_query.chart_type
			query.chart_view = objet_dao_query.chart_view
			query.legend_dataset = objet_dao_query.legend_dataset
			query.title_card = objet_dao_query.title_card
			query.model_id = objet_dao_query.model_id
			query.save()

			return True, query, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA QUERY')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Query.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Query.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			query = Model_Query.objects.get(pk = id)
			query.delete()
			return True
		except Exception as e:
			return False