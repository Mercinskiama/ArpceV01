from __future__ import unicode_literals
from ModuleStock.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict
import traceback
from ErpBackOffice.utils.utils import utils

class dao_rebut(object):
	numero = ''
	date = None
	article_id = None
	serie_article = ''
	quantite = 0.0
	societe_id = None
	status_id = None
	unite_id = None
	emplacement_origine_id = None
	emplacement_rebut_id = None
	document = ''

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Rebut.objects.all().order_by('-creation_date')
				return Model_Rebut.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Rebut.objects.filter(Q(numero__icontains = query) | Q(serie_article__icontains = query) | Q(quantite__icontains = query) | Q(document__icontains = query)).order_by('-creation_date').distinct()
				else: return Model_Rebut.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(numero__icontains = query) | Q(serie_article__icontains = query) | Q(quantite__icontains = query) | Q(document__icontains = query))).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE REBUT')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '':
				return Model_Rebut.objects.all().order_by('-creation_date')

			return Model_Rebut.objects.filter(Q(numero__icontains = query) | Q(serie_article__icontains = query) | Q(quantite__icontains = query) | Q(document__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE REBUT')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'numero' : str(item.numero),
					'date' : item.date,
					'article' : item.article.__str__() if item.article else '-',
					'serie_article' : str(item.serie_article),
					'quantite' : makeFloat(item.quantite),
					'societe' : item.societe.__str__() if item.societe else '-',
					'status' : item.status.__str__() if item.status else '-',
					'unite' : item.unite.__str__() if item.unite else '-',
					'emplacement_origine' : item.emplacement_origine.__str__() if item.emplacement_origine else '-',
					'emplacement_rebut' : item.emplacement_rebut.__str__() if item.emplacement_rebut else '-',
					'document' : str(item.document),
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
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE REBUT  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(numero = '', date = None, article_id = None, serie_article = '', quantite = 0.0, societe_id = None, status_id = None, unite_id = None, emplacement_origine_id = None, emplacement_rebut_id = None, document = ''):
		try:
			rebut = dao_rebut()
			rebut.numero = numero
			rebut.date = date
			rebut.article_id = article_id
			rebut.serie_article = serie_article
			rebut.quantite = quantite
			rebut.societe_id = societe_id
			rebut.status_id = status_id
			rebut.unite_id = unite_id
			rebut.emplacement_origine_id = emplacement_origine_id
			rebut.emplacement_rebut_id = emplacement_rebut_id
			rebut.document = document
			return rebut
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA REBUT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_rebut, request_post = []):
		try:
			rebut  = Model_Rebut()
			if objet_dao_rebut.numero != None : rebut.numero = objet_dao_rebut.numero
			rebut.date = objet_dao_rebut.date
			if objet_dao_rebut.article_id != None : rebut.article_id = objet_dao_rebut.article_id
			if objet_dao_rebut.serie_article != None : rebut.serie_article = objet_dao_rebut.serie_article
			if objet_dao_rebut.quantite != None : rebut.quantite = objet_dao_rebut.quantite
			if objet_dao_rebut.societe_id != None : rebut.societe_id = objet_dao_rebut.societe_id
			if objet_dao_rebut.status_id != None : rebut.status_id = objet_dao_rebut.status_id
			if objet_dao_rebut.unite_id != None : rebut.unite_id = objet_dao_rebut.unite_id
			if objet_dao_rebut.emplacement_origine_id != None : rebut.emplacement_origine_id = objet_dao_rebut.emplacement_origine_id
			if objet_dao_rebut.emplacement_rebut_id != None : rebut.emplacement_rebut_id = objet_dao_rebut.emplacement_rebut_id
			if objet_dao_rebut.document != None : rebut.document = objet_dao_rebut.document
			if auteur != None : rebut.auteur_id = auteur.id

			rebut.save()

			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Rebut [Model_Rebut]'
				utils.history_in_database(data)

			return True, rebut, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA REBUT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_rebut, auteur = None, request_post = []):
		try:
			rebut = Model_Rebut.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR DE OBJET
			before_rebut = model_to_dict(rebut)

			rebut.numero = objet_dao_rebut.numero
			rebut.date = objet_dao_rebut.date
			rebut.article_id = objet_dao_rebut.article_id
			rebut.serie_article = objet_dao_rebut.serie_article
			rebut.quantite = objet_dao_rebut.quantite
			rebut.societe_id = objet_dao_rebut.societe_id
			rebut.status_id = objet_dao_rebut.status_id
			rebut.unite_id = objet_dao_rebut.unite_id
			rebut.emplacement_origine_id = objet_dao_rebut.emplacement_origine_id
			rebut.emplacement_rebut_id = objet_dao_rebut.emplacement_rebut_id
			rebut.document = objet_dao_rebut.document
			if auteur != None : rebut.update_by_id = auteur.id
			rebut.save()

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_rebut, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Rebut [Model_Rebut]'
				utils.history_in_database(data)

			return True, rebut, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA REBUT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Rebut.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Rebut.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			rebut = Model_Rebut.objects.get(pk = id)
			rebut.delete()
			return True
		except Exception as e:
			return False



	@staticmethod
	def toGenerateNumeroRebut():
		rebut = dao_rebut.toList().count()
		rebut = rebut + 1
		temp_numero = str(rebut)
		for i in range(len(str(rebut)), 4):
			temp_numero = "0" + temp_numero
		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois
		temp_numero = f"BN_REBUT-{timezone.now().year}{mois}{temp_numero}"
		return temp_numero