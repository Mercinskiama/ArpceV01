from __future__ import unicode_literals
from ModuleArchivage.models import *
from ErpBackOffice.models import *
from django.utils import timezone
from django.forms import model_to_dict

class dao_tag(object):
	designation = ''
	code = ''
	categorie_id = None
	couleur = ''
	description = ''

	@staticmethod
	def toList(query=''):
		try:
			if query == '':
				return Model_Tag.objects.all().order_by('creation_date')

			return Model_Tag.objects.filter(Q(designation__icontains = query) | Q(code__icontains = query) | Q(couleur__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE TAG')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', code = '', categorie_id = None, couleur = '', description = ''):
		try:
			tag = dao_tag()
			tag.designation = designation
			tag.code = code
			tag.categorie_id = categorie_id
			tag.couleur = couleur
			tag.description = description
			return tag
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TAG')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_tag):
		try:
			tag  = Model_Tag()
			tag.designation = objet_dao_tag.designation
			if objet_dao_tag.code != None : tag.code = objet_dao_tag.code
			if objet_dao_tag.categorie_id != None : tag.categorie_id = objet_dao_tag.categorie_id
			if objet_dao_tag.couleur != None : tag.couleur = objet_dao_tag.couleur
			if objet_dao_tag.description != None : tag.description = objet_dao_tag.description
			if auteur != None : tag.auteur_id = auteur.id

			tag.save()

			return True, tag, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TAG')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_tag):
		try:
			tag = Model_Tag.objects.get(pk = id)
			# ON RECUPERE L'ANCIENNE VALEUR QUE JE TRANSFORMER EN OBJET
			before_tag = model_to_dict(tag)
			tag.designation = objet_dao_tag.designation
			tag.code = objet_dao_tag.code
			tag.categorie_id = objet_dao_tag.categorie_id
			tag.couleur = objet_dao_tag.couleur
			tag.description = objet_dao_tag.description
			tag.save()

			return True, tag, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TAG')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Tag.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Tag.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			tag = Model_Tag.objects.get(pk = id)
			tag.delete()
			return True
		except Exception as e:
			return False