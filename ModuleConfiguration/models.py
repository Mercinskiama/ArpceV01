# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ErpBackOffice.models import Model_Personne
from django.contrib.contenttypes.models import ContentType

# Create your models here.
TypeView = (
    ("List", "List"),
    ("Chart", "Chart"),
    ("Card", "Card"),
    ("Pivot", "Pivot")
)
TypeVisibilite = (
    (1, "Partager avec tous les utilisateurs"),
    (2, "Partager pour mon rôle utilisateur"),
    (3, "Moi uniquement")
)
class Model_Query(models.Model):
    numero    =    models.CharField(max_length = 100, default="", verbose_name = "Numéro")
    designation    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Désignation")
    role    =    models.ForeignKey('ErpBackOffice.Model_GroupePermission', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Rôle utilisateur")
    query    =    models.TextField(null = True, blank = True, verbose_name = "Requête")
    description    =    models.TextField(null = True, blank = True, verbose_name = "Description")
    champs_afficher    =    models.TextField(null = True, blank = True, verbose_name = "Champs à afficher")
    visibilite    =    models.IntegerField(choices=TypeVisibilite, default=1, verbose_name = "Visibilité")
    type_view    =    models.CharField(max_length = 100, choices=TypeView, default="List", verbose_name = "Type de vue")
    est_regroupe    =    models.BooleanField(default = False, verbose_name = "Est défaut")
    regr_count    =    models.IntegerField(default = -1, verbose_name = "Numéro regroupement")
    chart_view    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Type de vue graphique")
    chart_type    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Type graphique")
    legend_dataset    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Légende Dataset")
    title_card    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Titre Card")
    model         =    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut")
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat")
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création")
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification")
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteurs_queries', null = True, blank = True, verbose_name = "Auteur")

    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = 'Requête BI'
        verbose_name_plural = 'Requêtes BI'
        db_table = 'query'

    @property
    def value_type_view(self):
        if self.type_view: return dict(TypeView)[str(self.type_view)]
        
    @property
    def list_type_view(self):
        list = []
        for key, value in TypeView:
            item = {'id' : key,'designation' : value}
            list.append(item)
        return list
    
    @property
    def value_visibilite(self):
        if self.visibilite: return dict(TypeVisibilite)[int(self.visibilite)]
        
    @property
    def list_visibilite(self):
        list = []
        for key, value in TypeVisibilite:
            item = {'id' : key,'designation' : value}
            list.append(item)
        return list

class Model_Societe(models.Model):
    code        = models.CharField(max_length = 20, verbose_name = "Code", db_column='code')
    name    =    models.CharField(max_length = 100, verbose_name = "Nom de la société", db_column='name')
    picture_icon    =    models.ImageField(null = True, blank = True, verbose_name = "Logo de la société",db_column='picture_icon' )
    type    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Type",db_column='type')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société mère",db_column='parent_id')
    devise    =    models.ForeignKey('ErpBackOffice.Model_Devise', on_delete=models.SET_NULL, related_name = 'societes', blank=True, null=True, verbose_name = "Devise de référence",db_column='currency_id')
    type_periode    =    models.ForeignKey('ModuleConfiguration.Model_Type_periode', on_delete=models.SET_NULL, related_name = 'societes', blank=True, null=True, verbose_name = "Type de période",db_column='period_type_id')
    adress_email    =    models.EmailField(max_length = 100, null = True, blank = True, verbose_name = "Email", db_column='email')
    siteweb    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Genre", db_column='website')
    pays    =    models.ForeignKey('Model_Pays', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Pays", db_column='country_id')
    pays_adress    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Nom Pays", db_column='adress_country')
    province    =    models.ForeignKey('Model_Province', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Province", db_column='province_id')
    province_adress    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Nom Province", db_column='adress_state')
    ville    =    models.ForeignKey('Model_Ville', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Ville", db_column='city_id')
    ville_adress    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Nom Ville", db_column='adress_city')
    commune    =    models.ForeignKey('Model_Commune', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Commune", db_column='township_id')
    adresse_line1    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Adresse ligne 1", db_column='adress_line1')
    adresse_line2    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Adresse ligne 2", db_column='adress_line2')
    telephone_1            =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Téléphone 1", db_column='phone_number1')
    telephone_2            =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Téléphone 2", db_column='phone_number2')
    autres_adresses    			=    models.ManyToManyField('Model_Adresse', verbose_name = "Autres adresse", db_column='others_adresses')
    contacts    			=    models.ManyToManyField('Model_Contact', verbose_name = "Contacts", db_column='contacts')
    nbr_periode_gl            =    models.IntegerField(default = 12, null = True, blank = True, verbose_name = "Nombre période Comptabilité",db_column='nbr_periode_gl')
    nbr_periode_ar            =    models.IntegerField(default = 12, null = True, blank = True, verbose_name = "Nombre période Comptabilité Client",db_column='nbr_periode_ar')
    nbr_periode_ap            =    models.IntegerField(default = 12, null = True, blank = True, verbose_name = "Nombre période Comptabilité Fournisseur",db_column='nbr_periode_ap')
    nbr_periode_cm            =    models.IntegerField(default = 12, null = True, blank = True, verbose_name = "Nombre période Comptabilité Trésorerie ",db_column='nbr_periode_cm')
    nbr_periode_fa            =    models.IntegerField(default = 12, null = True, blank = True, verbose_name = "Nombre période Comptabilité Immobilisation",db_column='nbr_periode_fa')
    nbr_periode_bgt            =    models.IntegerField(default = 12, null = True, blank = True, verbose_name = "Nombre période Budget",db_column='nbr_periode_bgt')
    nbr_periode_py            =    models.IntegerField(default = 12, null = True, blank = True, verbose_name = "Nombre période Paie",db_column='nbr_periode_py')
    period_begin_date    =    models.DateTimeField(null = True, blank = True, verbose_name = "Début exercice en cours" , db_column='period_begin_date')
    period_end_date    =    models.DateTimeField(null = True, blank = True, verbose_name = "Fin Exercice en cours" , db_column='period_end_date')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Description",db_column='description')
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_societes', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_societes', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Société'
        verbose_name_plural = 'Sociétés'
        db_table = 'cnf_company'

    @property
    def fille(self):
        return Model_Societe.objects.filter(parent_id=self.id)   
    
class Model_Pays(models.Model):
    name    =    models.CharField(max_length = 100, verbose_name = "Nom", db_column='name')
    code        = models.CharField(max_length = 20, verbose_name = "Code", db_column='code')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Description",db_column='description')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_pays', null = True, blank = True, verbose_name = "modifié par" , db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_pays', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'
        db_table = 'cnf_country'

class Model_Province(models.Model):
    name    =    models.CharField(max_length = 100, verbose_name = "Nom", db_column='name')
    country    =    models.ForeignKey('Model_Pays', on_delete=models.CASCADE, related_name = 'provinces', blank=True, null=True, verbose_name = "Pays",db_column='country')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Description",db_column='description')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_provinces', null = True, blank = True, verbose_name = "modifié par" , db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_provinces', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        db_table = 'cnf_state'
        
class Model_District(models.Model):
    name    =    models.CharField(max_length = 100, verbose_name = "Nom", db_column='name')
    province    =    models.ForeignKey('Model_Province', on_delete=models.CASCADE, related_name = 'districts', blank=True, null=True, verbose_name = "Province",db_column='province')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Description",db_column='description')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_districts', null = True, blank = True, verbose_name = "modifié par" , db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_districts', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        db_table = 'cnf_district'
        
class Model_Ville(models.Model):
    name    =    models.CharField(max_length = 100, verbose_name = "Nom", db_column='name')
    province    =    models.ForeignKey('Model_Province', on_delete=models.CASCADE, related_name = 'villes', blank=True, null=True, verbose_name = "Province",db_column='province')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Description",db_column='description')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_villes', null = True, blank = True, verbose_name = "modifié par" , db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_villes', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'
        db_table = 'cnf_city'
        
class Model_Commune(models.Model):
    name    =    models.CharField(max_length = 100, verbose_name = "Nom", db_column='name')
    ville    =    models.ForeignKey('Model_Ville', on_delete=models.CASCADE, related_name = 'communes', blank=True, null=True, verbose_name = "Ville",db_column='city')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Description",db_column='description')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_communes', null = True, blank = True, verbose_name = "modifié par" , db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_communes', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Commune'
        verbose_name_plural = 'Communes'
        db_table = 'cnf_township'

        
TypeAdresse  =  ((1, 'Contact'),(2, 'Adresse personnelle'),(2, 'Adresse de facturation'),(2, 'Adresse de livraison'),(2, 'Autre adresse'))
class Model_Adresse(models.Model):
    name    =    models.CharField(max_length = 250, verbose_name = "Nom", db_column='name')
    type_adresse    	=    models.IntegerField(default= 1, choices = TypeAdresse, verbose_name = "Type", db_column='type')
    country    =    models.ForeignKey('Model_Pays', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Pays", db_column='country')
    adress_state    =    models.ForeignKey('Model_Province', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Province", db_column='province')
    adress_city    =    models.ForeignKey('Model_Ville', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Ville", db_column='city')
    adress_township    =    models.ForeignKey('Model_Commune', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Commune", db_column='township')
    adress_line1    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Adresse ligne 1", db_column='street')
    adress_line2    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Adresse ligne 2", db_column='street2')
    code_postal            =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Code Postal", db_column='zip_code')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Autres informations",db_column='description')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_adresses', null = True, blank = True, verbose_name = "modifié par" , db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_adresses', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'
        db_table = 'cnf_address'
        
    @property
    def value_type_adresse(self):
        if self.type_adresse: return dict(TypeAdresse)[int(self.type_adresse)]

    @property
    def list_type_adresse(self):
        list = []
        for key, value in TypeAdresse:
            item = {'id' : key,'designation' : value}
            list.append(item)
        return list
    

TypeContact  =  ((1, 'Individu'),(2, 'Société'))
class Model_Contact(models.Model):
    name    =    models.CharField(max_length = 250, verbose_name = "Noms", db_column='name')
    type    	=    models.IntegerField(default= 1, choices = TypeContact, verbose_name = "Type Personne", db_column='company_type')
    nature    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Nature", db_column='nature')
    email    =    models.EmailField(max_length = 250, null = True, blank = True, verbose_name = "Courriel", db_column='email')
    siteweb    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Site web", db_column='website')
    function    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Fonction", db_column='function')
    country    =    models.ForeignKey('Model_Pays', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Pays", db_column='country')
    adress_state    =    models.ForeignKey('Model_Province', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Province", db_column='province')
    adress_city    =    models.ForeignKey('Model_Ville', on_delete=models.SET_NULL, null = True, blank = True, verbose_name = "Ville", db_column='city')
    adress_line1    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Adresse ligne 1", db_column='street')
    adress_line2    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Adresse ligne 2", db_column='street2')
    phone_number            =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Téléphone", db_column='phone')
    phone_number_2            =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Mobile", db_column='mobile')
    code_postal            =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Code Postal", db_column='zip_code')
    autres_adresses    			=    models.ManyToManyField('Model_Adresse', verbose_name = "Autres adresse", db_column='others_adresses')
	#res_model         	=    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Modèle Ressource", db_column='res_model')
	#res_id    			=    models.IntegerField(blank=True, null=True, verbose_name = "Id Ressource", db_column='res_id')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Autres informations",db_column='description')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_contacts', null = True, blank = True, verbose_name = "modifié par" , db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_contacts', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        db_table = 'cnf_contact'
    
    @property
    def value_type(self):
        if self.type: return dict(TypeContact)[int(self.type)]

    @property
    def list_type(self):
        list = []
        for key, value in TypeContact:
            item = {'id' : key,'designation' : value}
            list.append(item)
        return list

Periodicite  =  (('Week', 'Hebdomadaire'),('Month', 'Mensuelle'),('Quarter', 'Trimestrielle'),('Year', 'Annuelle'),('Other', 'Autre'))    
class Model_Type_periode(models.Model):
    name =    models.CharField(max_length = 250,verbose_name = "Désignation", db_column='name')
    periodicite         =    models.CharField(max_length = 100, choices = Periodicite, null = True, blank = True, default="", verbose_name = "Périodicité", db_column='periodicity')
    nombre_par_exercice = models.IntegerField(null = True, blank = True, verbose_name = "Nombre par exercice", db_column='number_per_fiscal_year')
    description    =    models.TextField(null = True, blank = True, verbose_name = "Description", db_column='description' )
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    societe    =    models.ForeignKey('Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société", db_column='company')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey("ErpBackOffice.Model_Personne", on_delete = models.SET_NULL, related_name = 'modificateur_type_periodes', null = True, blank = True, verbose_name = "modifié par" , db_column='updated_by')
    auteur    =    models.ForeignKey("ErpBackOffice.Model_Personne", on_delete = models.SET_NULL, related_name = 'auteur_type_periodes', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Type Période'
        verbose_name_plural = 'Types Période'
        db_table = 'cnf_type_period'
        
    @property
    def value_periodicite(self):
        if self.periodicite: return dict(Periodicite)[str(self.periodicite)]

    @property
    def list_periodicite(self):
        list = []
        for key, value in Periodicite:
            item = {'id' : key,'designation' : value}
            list.append(item)
        return list
