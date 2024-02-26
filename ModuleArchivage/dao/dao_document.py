from __future__ import unicode_literals
from ModuleArchivage.models import *
from ErpBackOffice.models import *
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import os
from django.core.files.storage import default_storage

class dao_document(object):
	designation = ''
	type = 0
	taille = 0
	type_mime = 0
	mime = ''
	dossier_id = None
	res_model_id = None
	res_field = ''
	res_id = 0
	est_public = False
	est_archive = False
	est_bloque = False
	auteur_blocage_id = None
	access_token = ''
	url = ''
	description = ''
	indexation = ''
	fichier = None
	miniature = None
	tags = []
	favoris = []

	@staticmethod
	def toList(query=''):
		try:
			if query == '':
				return Model_Document.objects.all().order_by('creation_date')

			return Model_Document.objects.filter(Q(designation__icontains = query) | Q(type__icontains = query) | Q(taille__icontains = query) | Q(type_mime__icontains = query) | Q(mime__icontains = query) | Q(res_field__icontains = query) | Q(res_id__icontains = query) | Q(access_token__icontains = query) | Q(url__icontains = query) | Q(description__icontains = query) | Q(indexation__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DOCUMENT')
			#print(e)
			return []

	@staticmethod
	def toListDocumentbyObjetModele(objet_modele):
		try:
			content_type = ContentType.objects.get_for_model(objet_modele)
			return Model_Document.objects.filter(res_model_id = content_type.id, res_id = objet_modele.id)
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DOCUMENT')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', type = None, taille = None, type_mime = None, mime = '', dossier_id = None, res_model_id = None, res_field = '', res_id = None, est_public = None, est_archive = None, est_bloque = None, auteur_blocage_id = None, access_token = '', url = '', description = '', indexation = '', fichier = None, miniature = None, tags = [], favoris = []):
		try:
			document = dao_document()
			document.designation = designation
			document.type = type
			document.taille = taille
			document.type_mime = type_mime
			document.mime = mime
			document.dossier_id = dossier_id
			document.res_model_id = res_model_id
			document.res_field = res_field
			document.res_id = res_id
			document.est_public = est_public
			document.est_archive = est_archive
			document.est_bloque = est_bloque
			document.auteur_blocage_id = auteur_blocage_id
			document.access_token = access_token
			document.url = url
			document.description = description
			document.indexation = indexation
			document.fichier = fichier
			document.miniature = miniature
			document.tags = tags
			document.favoris = favoris
			return document
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA DOCUMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_document):
		try:
			document  = Model_Document()
			document.designation = objet_dao_document.designation
			if objet_dao_document.type != None : document.type = objet_dao_document.type
			if objet_dao_document.taille != None : document.taille = objet_dao_document.taille
			if objet_dao_document.type_mime != None : document.type_mime = objet_dao_document.type_mime
			document.mime = objet_dao_document.mime
			if objet_dao_document.dossier_id != None : document.dossier_id = objet_dao_document.dossier_id
			if objet_dao_document.res_model_id != None : document.res_model_id = objet_dao_document.res_model_id
			if objet_dao_document.res_field != None : document.res_field = objet_dao_document.res_field
			if objet_dao_document.res_id != None : document.res_id = objet_dao_document.res_id
			if objet_dao_document.est_public != None : document.est_public = objet_dao_document.est_public
			if objet_dao_document.est_archive != None : document.est_archive = objet_dao_document.est_archive
			if objet_dao_document.est_bloque != None : document.est_bloque = objet_dao_document.est_bloque
			if objet_dao_document.auteur_blocage_id != None : document.auteur_blocage_id = objet_dao_document.auteur_blocage_id
			if objet_dao_document.access_token != None : document.access_token = objet_dao_document.access_token
			if objet_dao_document.url != None : document.url = objet_dao_document.url
			if objet_dao_document.description != None : document.description = objet_dao_document.description
			if objet_dao_document.indexation != None : document.indexation = objet_dao_document.indexation
			if objet_dao_document.fichier != None : document.fichier = objet_dao_document.fichier
			if objet_dao_document.miniature != None : document.miniature = objet_dao_document.miniature
			if auteur != None : document.auteur_id = auteur.id

			document.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_document.favoris)):
				try:
					objet = Model_Tag.objects.get(pk = objet_dao_document.favoris[i])
					document.favoris.add(objet)
				except Exception as e: pass

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_document.favoris)):
				try:
					objet = Model_Personne.objects.get(pk = objet_dao_document.favoris[i])
					document.favoris.add(objet)
				except Exception as e: pass

			return True, document, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA DOCUMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_document):
		try:
			document = Model_Document.objects.get(pk = id)
			document.designation = objet_dao_document.designation
			document.type = objet_dao_document.type
			document.taille = objet_dao_document.taille
			document.type_mime = objet_dao_document.type_mime
			document.mime = objet_dao_document.mime
			document.dossier_id = objet_dao_document.dossier_id
			document.res_model_id = objet_dao_document.res_model_id
			document.res_field = objet_dao_document.res_field
			document.res_id = objet_dao_document.res_id
			document.est_public = objet_dao_document.est_public
			document.est_archive = objet_dao_document.est_archive
			document.est_bloque = objet_dao_document.est_bloque
			document.auteur_blocage_id = objet_dao_document.auteur_blocage_id
			document.access_token = objet_dao_document.access_token
			document.url = objet_dao_document.url
			document.description = objet_dao_document.description
			document.indexation = objet_dao_document.indexation
			if objet_dao_document.fichier != None : document.fichier = objet_dao_document.fichier
			if objet_dao_document.miniature != None : document.miniature = objet_dao_document.miniature
			document.save()

			#Mise à jour Champs (ManyToMany - Creation)
			favoris_old = document.favoris.all()
			favoris_updated = []
			for i in range(0, len(objet_dao_document.favoris)):
				try:
					objet = Model_Tag.objects.get(pk = objet_dao_document.favoris[i])
					if objet not in favoris_old: document.favoris.add(objet)
					favoris_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in favoris_old:
				if item.id not in favoris_updated: document.favoris.remove(item)

			#Mise à jour Champs (ManyToMany - Creation)
			favoris_old = document.favoris.all()
			favoris_updated = []
			for i in range(0, len(objet_dao_document.favoris)):
				try:
					objet = Model_Personne.objects.get(pk = objet_dao_document.favoris[i])
					if objet not in favoris_old: document.favoris.add(objet)
					favoris_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in favoris_old:
				if item.id not in favoris_updated: document.favoris.remove(item)

			return True, document, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DOCUMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Document.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Document.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			document = Model_Document.objects.get(pk = id)
			document.delete()
			return True
		except Exception as e:
			return False