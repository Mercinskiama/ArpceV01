from __future__ import unicode_literals
from ModuleArchivage.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_categorie_tag(object):
	designation = ''
	code = ''
	description = ''
	dossier_id = None

	@staticmethod
	def toList(query=''):
		try:
			if query == '':
				return Model_Categorie_tag.objects.all().order_by('creation_date')

			return Model_Categorie_tag.objects.filter(Q(designation__icontains = query) | Q(code__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE CATEGORIE_TAG')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', code = '', description = '', dossier_id = None):
		try:
			categorie_tag = dao_categorie_tag()
			categorie_tag.designation = designation
			categorie_tag.code = code
			categorie_tag.description = description
			categorie_tag.dossier_id = dossier_id
			return categorie_tag
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CATEGORIE_TAG')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_categorie_tag):
		try:
			categorie_tag  = Model_Categorie_tag()
			categorie_tag.designation = objet_dao_categorie_tag.designation
			if objet_dao_categorie_tag.code != None : categorie_tag.code = objet_dao_categorie_tag.code
			if objet_dao_categorie_tag.description != None : categorie_tag.description = objet_dao_categorie_tag.description
			if objet_dao_categorie_tag.dossier_id != None : categorie_tag.dossier_id = objet_dao_categorie_tag.dossier_id
			if auteur != None : categorie_tag.auteur_id = auteur.id

			categorie_tag.save()

			return True, categorie_tag, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA CATEGORIE_TAG')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_categorie_tag):
		try:
			categorie_tag = Model_Categorie_tag.objects.get(pk = id)
			categorie_tag.designation = objet_dao_categorie_tag.designation
			categorie_tag.code = objet_dao_categorie_tag.code
			categorie_tag.description = objet_dao_categorie_tag.description
			categorie_tag.dossier_id = objet_dao_categorie_tag.dossier_id
			categorie_tag.save()

			return True, categorie_tag, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CATEGORIE_TAG')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Categorie_tag.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Categorie_tag.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			categorie_tag = Model_Categorie_tag.objects.get(pk = id)
			categorie_tag.delete()
			return True
		except Exception as e:
			return False