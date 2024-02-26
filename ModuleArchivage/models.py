# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ErpBackOffice.models import Model_Personne
import base64, uuid
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Model_Categorie_tag(models.Model):
	designation    =    models.CharField(max_length = 250, verbose_name = "Désignation" )
	code    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Code" )
	description    =    models.CharField(max_length = 550, null = True, blank = True, verbose_name = "Description" )
	dossier    =    models.ForeignKey("Model_Dossier", related_name = "categorie_tags", on_delete=models.CASCADE, null = True, blank = True, verbose_name = "Dossier")
	societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_categorie_tags', null = True, blank = True)

	def __str__(self):
		return self.designation


	class Meta:
		verbose_name = 'Catégorie d\'étiquette'
		verbose_name_plural = 'Catégories d\'étiquette'
		db_table = 'categorie_tag'


class Model_Tag(models.Model):
	designation    =    models.CharField(max_length = 250, verbose_name = "Désignation" )
	code    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Code" )
	categorie    =    models.ForeignKey("Model_Categorie_tag", related_name = "tags_categorie", on_delete=models.CASCADE, null = True, blank = True, verbose_name = "Catégorie")
	couleur    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Couleur" )
	societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
	description    =    models.CharField(max_length = 550, null = True, blank = True, verbose_name = "Description" )
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_tags', null = True, blank = True)

	def __str__(self):
		return self.designation

	class Meta:
		verbose_name = "Etiquette"
		verbose_name_plural = "Etiquettes"
		db_table = "tag"
  
class Model_Dossier(models.Model):
	designation    =    models.CharField(max_length = 250, verbose_name = "Désignation")
	sequence    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Séquence")
	parent    =    models.ForeignKey("Model_Dossier", related_name = "dossiers_fils", on_delete=models.CASCADE, null = True, blank = True, verbose_name = "Dossier parent")
	description    =    models.CharField(max_length = 550, null = True, blank = True, verbose_name = "Description")
	write_groups    =    models.ManyToManyField('ErpBackOffice.Model_GroupePermission', related_name = 'dossiers_writes', verbose_name = "Accès en écriture")
	read_groups    =    models.ManyToManyField('ErpBackOffice.Model_GroupePermission', related_name = 'dossiers_reads', verbose_name = "Accès en lecture")
	owner_read         =    models.BooleanField(default = True, verbose_name = "Lire Documents personnels seulement")
	est_racine          =    models.BooleanField(default = False, verbose_name = "Est dossier racine")
	est_archivage       =    models.BooleanField(default = False, verbose_name = "Est dossier archivage")
	societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_dossiers', null = True, blank = True)

	def __str__(self):
		if self.parent_id != None:
			return "{}/{}".format(self.parent, self.designation)
		else: return "{}".format(self.designation)

	class Meta:
		verbose_name = "Dossier"
		verbose_name_plural = "Dossiers"
		db_table = "dossier"
  
	@property
	def nombre_dossiers(self):
		try:
			nombre = self.dossiers_fils.count()
			return nombre
		except Exception as e:
			return 0

	@property
	def nombre_documents(self):
		try:
			nombre = self.documents.count()
			return nombre
		except Exception as e:
			return 0


TypeMime  =  ((1, 'txt'),(2, 'pdf'),(3, 'word'),(4, 'pptx'),(5, 'image'))
TypeDocument  =  ((1, 'Fichier'),(2, 'URL'))
  
class Model_Document(models.Model):
	designation    		=    models.CharField(max_length = 250, verbose_name = "Désignation")
	type    			=    models.IntegerField(choices = TypeDocument, default = 1, verbose_name = "Type")
	taille    			=    models.IntegerField(null = True, blank = True, verbose_name = "Taille de Fichier")
	type_mime    		=    models.IntegerField(choices = TypeMime, default = 1, verbose_name = "Type Mime")
	mime    			=    models.CharField(max_length = 250, verbose_name = "Mime")
	dossier    			=    models.ForeignKey("Model_Dossier", related_name = "documents", on_delete=models.CASCADE, null = True, blank = True, verbose_name = "Dossier")
	tags    			=    models.ManyToManyField('Model_Tag', verbose_name = "Etiquettes")
	res_model         	=    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Modèle Ressource")
	res_field    		=    models.CharField(max_length = 250, blank=True, null=True, verbose_name = "Champs Ressource")
	res_id    			=    models.IntegerField(blank=True, null=True, verbose_name = "Id Ressource")
	est_public          =    models.BooleanField(default = True, verbose_name = "Est public")
	est_archive         =    models.BooleanField(default = False, verbose_name = "Est archivé")
	est_bloque          =    models.BooleanField(default = False, verbose_name = "Est bloqué ")
	auteur_blocage      =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'documents_bloques', null = True, blank = True, verbose_name = "Bloqué par")
	favoris             =    models.ManyToManyField(Model_Personne, verbose_name = "Favoris")
	access_token        =    models.CharField(max_length = 250, blank=True, null=True, default="", verbose_name = "Token accès")
	url                 =    models.CharField(max_length = 250, blank=True, null=True, verbose_name = "URL")
	description    		=    models.CharField(max_length = 550, null = True, blank = True, verbose_name = "Description")
	indexation    		=    models.CharField(max_length = 4000, null = True, blank = True, verbose_name = "Contenu indexé")
	fichier 			=    models.FileField(upload_to ='uploads/%Y/%m/%d/', verbose_name = "Fichier")
	miniature 			=    models.FileField(upload_to ='uploads/%Y/%m/%d/', verbose_name = "Miniature")
	societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
	statut    			=    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    			=    models.CharField(max_length=50, blank=True, null=True)
	creation_date    	=    models.DateTimeField(auto_now_add = True)
	update_date    		=    models.DateTimeField(auto_now = True)
	auteur    			=    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_documents', null = True, blank = True)

	def __str__(self):
		return self.designation

	class Meta:
		verbose_name = "Document"
		verbose_name_plural = "Documents"
		db_table = "document"

	@property
	def value_type_question(self):
		if self.type_mime: return dict(TypeMime)[int(self.type_mime)]

	@property
	def list_type_mime(self):
		list = []
		for key, value in TypeMime:
			item = {'id' : key,'designation' : value}
			list.append(item)
		return list

	@property
	def value_type(self):
		if self.type: return dict(TypeDocument)[int(self.type)]

	@property
	def list_type(self):
		list = []
		for key, value in TypeDocument:
			item = {'id' : key,'designation' : value}
			list.append(item)
		return list

TypePartage  =  ((1, 'Liste de documents'),(2, 'Domaine'))
  
class Model_Document_partage(models.Model):
	designation    		=    models.CharField(max_length = 250, verbose_name = "Désignation")
	type    			=    models.IntegerField(choices = TypePartage, default = 1, verbose_name = "Type de partage")
	documents    	    =    models.ManyToManyField("Model_Document", verbose_name = "Documents")
	url                 =    models.CharField(max_length = 250, blank=True, null=True, verbose_name = "URL")
	date_echeance    	=    models.DateTimeField(blank=True, null=True, verbose_name = "Date d'échéance")
	societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
	description    		=    models.CharField(max_length = 550, null = True, blank = True, verbose_name = "Description")
	statut    			=    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    			=    models.CharField(max_length=50, blank=True, null=True)
	creation_date    	=    models.DateTimeField(auto_now_add = True)
	update_date    		=    models.DateTimeField(auto_now = True)
	auteur    			=    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_partages', null = True, blank = True)

	def __str__(self):
		return self.url

	class Meta:
		verbose_name = "Lien partagé"
		verbose_name_plural = "Liens partagés"
		db_table = "document_partage"

	@property
	def value_type(self):
		if self.type: return dict(TypePartage)[int(self.type)]

	@property
	def list_type(self):
		list = []
		for key, value in TypePartage:
			item = {'id' : key,'designation' : value}
			list.append(item)
		return list
  
class Model_Document_archivage(models.Model):
	document    	    =    models.ForeignKey("Model_Document", related_name = "archivages", on_delete=models.CASCADE, null = True, blank = True, verbose_name = "Document")
	societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
	creation_date    	=    models.DateTimeField(auto_now_add = True)
	auteur    			=    models.ForeignKey(Model_Personne, on_delete = models.CASCADE, related_name = 'auteur_archivages', null = True, blank = True)

	def __str__(self):
		return "{} aime {}".format(self.document, self.auteur.nom_complet)

	class Meta:
		db_table = "document_archivage"
