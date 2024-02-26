# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ErpBackOffice.models import Model_Personne
from ErpBackOffice.models import Model_Wkf_Etape
import uuid

# Create your models here.
class Model_Log(models.Model):
	erreur   			= 	models.TextField(default='', verbose_name = "Erreur" ,db_column='error')
	modele   			= 	models.CharField(default='', max_length=1024, verbose_name = "Modele" ,db_column='model')
	auteur 	 			= 	models.CharField(default='', max_length=1024, verbose_name = "Auteur" ,db_column='autor')
	etat    			=   models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
	creation_date    	=   models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
	update_date    		=   models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = 'Log'
		verbose_name_plural = "Logs"
		db_table = 'sup_logs'


class Model_Historique_action(models.Model):
	valeur_avant 	 	= models.TextField(default='',blank=True, null=True, verbose_name = "Valeur Avant" ,db_column='Before_value')
	valeur_apres 	 	= models.TextField(default='',blank=True, null=True, verbose_name = "Valeur Apres" ,db_column='After_value')
	modele   			= models.CharField(default='', max_length=1024, verbose_name = "Modele" ,db_column='model')
	auteur 	 			= models.CharField(default='', max_length=1024, verbose_name = "Auteur" ,db_column='autor')
	etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
	creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
	update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = 'Historique Action'
		verbose_name_plural = "Historiques Actions"
		db_table = 'sup_action_story'