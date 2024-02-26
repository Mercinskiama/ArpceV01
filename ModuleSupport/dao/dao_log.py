from __future__ import unicode_literals
from ModuleSupport.models import *
from ErpBackOffice.models import *
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from django.utils import timezone
from django.forms import model_to_dict

class dao_log(object):
	erreur = ''
	modele = ''
	auteur = ''

	@staticmethod
	def toList(query=''):
		try:
			if query == '':
				return Model_Log.objects.all().order_by('-creation_date')

			return Model_Log.objects.filter(Q(erreur__icontains = query) | Q(modele__icontains = query)).order_by('-creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LOG')
			#print(e)
			return []

	@staticmethod
	def toListJson(model=[]):
		try:
			listes = []
			for item in model: 
				element = {
					'id' : item.id,
					'erreur' : str(item.erreur),
					'modele' : str(item.modele),
					'auteur' : str(item.auteur),
					'etat' : str(item.etat),
					'creation_date' : item.creation_date,
					'update_date' : item.update_date,
				}
				listes.append(element)
			return listes
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE LOG  EN JSON')
			#print(e)
			return []

	@staticmethod
	def toCreate(erreur = '', modele = '', auteur = ''):
		try:
			log = dao_log()
			log.erreur = erreur
			log.modele = modele
			log.auteur = auteur
			return log
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LOG')
			#print(e)
			return None

	@staticmethod
	def toSave(objet_dao_log):
		try:
			log  = Model_Log()
			if objet_dao_log.erreur != None : log.erreur = objet_dao_log.erreur
			if objet_dao_log.modele != None : log.modele = objet_dao_log.modele
			if objet_dao_log.auteur != None : log.auteur = objet_dao_log.auteur
			log.save()

			return True, log, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LOG')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_log, auteur = None):
		try:
			log = Model_Log.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR QUE JE TRANSFORMER EN OBJET
			before_log = model_to_dict(log)
			log.erreur = objet_dao_log.erreur
			log.modele = objet_dao_log.modele
			if auteur != None : log.update_by_id = auteur.id
			log.save()

			return True, log, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LOG')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Log.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Log.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			log = Model_Log.objects.get(pk = id)
			log.delete()
			return True
		except Exception as e:
			return False