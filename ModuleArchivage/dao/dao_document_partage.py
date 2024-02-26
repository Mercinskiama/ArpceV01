from __future__ import unicode_literals
from ModuleArchivage.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_document_partage(object):
	designation = ''
	type = 0
	url = ''
	date_echeance = '2010-01-01 00:00:00'
	description = ''
	documents = []

	@staticmethod
	def toList(query=''):
		try:
			if query == '':
				return Model_Document_partage.objects.all().order_by('creation_date')

			return Model_Document_partage.objects.filter(Q(designation__icontains = query) | Q(type__icontains = query) | Q(url__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DOCUMENT_PARTAGE')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', type = None, url = '', date_echeance = None, description = '', documents = []):
		try:
			document_partage = dao_document_partage()
			document_partage.designation = designation
			document_partage.type = type
			document_partage.url = url
			document_partage.date_echeance = date_echeance
			document_partage.description = description
			document_partage.documents = documents
			return document_partage
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA DOCUMENT_PARTAGE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_document_partage):
		try:
			document_partage  = Model_Document_partage()
			document_partage.designation = objet_dao_document_partage.designation
			if objet_dao_document_partage.type != None : document_partage.type = objet_dao_document_partage.type
			if objet_dao_document_partage.url != None : document_partage.url = objet_dao_document_partage.url
			if objet_dao_document_partage.date_echeance != None : document_partage.date_echeance = objet_dao_document_partage.date_echeance
			if objet_dao_document_partage.description != None : document_partage.description = objet_dao_document_partage.description
			if auteur != None : document_partage.auteur_id = auteur.id

			document_partage.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_document_partage.documents)):
				try:
					objet = Model_Document.objects.get(pk = objet_dao_document_partage.documents[i])
					document_partage.documents.add(objet)
				except Exception as e: pass

			return True, document_partage, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA DOCUMENT_PARTAGE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_document_partage):
		try:
			document_partage = Model_Document_partage.objects.get(pk = id)
			document_partage.designation = objet_dao_document_partage.designation
			document_partage.type = objet_dao_document_partage.type
			document_partage.url = objet_dao_document_partage.url
			document_partage.date_echeance = objet_dao_document_partage.date_echeance
			document_partage.description = objet_dao_document_partage.description
			document_partage.save()

			#Mise à jour Champs (ManyToMany - Creation)
			documents_old = document_partage.documents.all()
			documents_updated = []
			for i in range(0, len(objet_dao_document_partage.documents)):
				try:
					objet = Model_Document.objects.get(pk = objet_dao_document_partage.documents[i])
					if objet not in documents_old: document_partage.documents.add(objet)
					documents_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in documents_old:
				if item.id not in documents_updated: document_partage.documents.remove(item)

			return True, document_partage, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DOCUMENT_PARTAGE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Document_partage.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Document_partage.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			document_partage = Model_Document_partage.objects.get(pk = id)
			document_partage.delete()
			return True
		except Exception as e:
			return False