# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ErpBackOffice.models import Model_Personne
from django.db import models
# from ModuleAchat.models import *
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from django.db.models import Max,Sum
from ModuleConfiguration.models import *
# Create your models here.


class Model_Type_emplacement(models.Model):
    code = models.CharField(max_length = 20, null = True, blank=True, default = '', verbose_name = "Code", db_column='code')
    designation = models.CharField(max_length = 255, verbose_name = "Designation", db_column="name")
    societe  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut    = models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    = models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date =models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date = models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_type_emplacements', null = True, blank = True, db_column='updated_by')
    auteur =  models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_type_emplacements', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = "Type d'emplacement"
        verbose_name_plural = "Types d'emplacement"
        db_table = "stk_location_type"

class Model_Emplacement(models.Model):
    designation    =    models.CharField(max_length = 100, verbose_name = "Designation",db_column="name" , null = True, blank = True)
    designation_court    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Designation courte" ,db_column="short_name")
    code        = models.CharField(max_length = 20, null = True, blank=True, default = '', verbose_name = "Code", db_column='code')
    description    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Description", db_column="description")
    type_emplacement =    models.ForeignKey("Model_Type_emplacement", null = True, blank = True, on_delete=models.CASCADE, related_name='emplacements', verbose_name = "Type", db_column="location_type")
    defaut =    models.BooleanField(default=False,  verbose_name = "Est défaut", db_column="is_default")
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    visible  =    models.BooleanField(default=True,  verbose_name = "Est visible", db_column="is_visible")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_emplacements', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_emplacements', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.reference

    @property
    def reference(self):
        empl = self.designation
        try:
            ent = self.entrepot.designation_court
            empl = ent + '/' + empl
        except Exception as e:
            pass
        return empl

    class Meta:
        verbose_name = 'Emplacement'
        verbose_name_plural = 'Emplacements'
        db_table = 'stk_location'

class Model_Unite_mesure(models.Model):
    name    =    models.CharField(max_length = 100, verbose_name = "Designation", db_column="name" , null = True, blank = True)
    short_name    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Symbole", db_column="short_name" )
    description    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Description", db_column="description" )
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_unite_mesures', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_unite_mesures', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Unité de mesure'
        verbose_name_plural = 'Unités de mesure'
        db_table = 'stk_measure_unit'


class Model_Categorie(models.Model):
    name    =    models.CharField(max_length = 100, verbose_name = "Designation", db_column="name", null = True, blank = True)
    short_name    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Designation courte", db_column="short_name" )
    code        = models.CharField(max_length = 20, null = True, blank=True, default = '', verbose_name = "Code", db_column='code')
    description    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Description", db_column="description")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_categories', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_categories', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        db_table = 'stk_category'

    @property
    def nombre_articles(self):
        return Model_Article.objects.filter(category_id = self.pk).count()

class Model_Type_article(models.Model):
    designation =   models.CharField(max_length = 255, verbose_name = "Designation", db_column="name")
    est_service  =   models.BooleanField(default=False, verbose_name = "Est service", db_column="is_service")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_type_articles', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_type_articles', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = "Type d'Article"
        verbose_name_plural = "Types d'Articles"
        db_table = 'stk_product_type'


class Model_Article(models.Model):
    name    =    models.CharField(max_length = 100, verbose_name = "Designation", db_column="Désignation", null = True, blank = True)
    code = models.CharField(max_length = 20, null = True, blank=True, default = '', verbose_name = "Code", db_column='code')
    amount =    models.FloatField(default = 0.0, null = True, blank = True, verbose_name = "Prix unitaire", db_column="amount")
    devise    =    models.ForeignKey('ErpBackOffice.Model_Devise', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Devise", db_column="currency_id")
    type_article =   models.ForeignKey("Model_Type_Article", on_delete=models.CASCADE, blank=True, null=True, related_name="articles", verbose_name = "Type d'article", db_column="product_type")
    picture_icon    =    models.ImageField(null = True, blank = True, verbose_name = "Image", db_column="picture_icon")
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    quota_quantity            =    models.IntegerField(default = 0.0, null = True, blank = True, verbose_name = "Quantité seuil", db_column="quota_quantity")
    category    =    models.ForeignKey('Model_Categorie', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Catégorie", db_column="category")
    measure_unit    =    models.ForeignKey('Model_Unite_mesure', on_delete=models.SET_NULL, blank=True, null=True, related_name = 'produits_unit', verbose_name = "Unité de mesure", db_column="measure_unit")
    description    =    models.CharField(max_length = 500, null = True, blank = True, verbose_name = "Description", db_column="description")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_articles', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_articles', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return f"[{self.code}]/{self.name}"

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        db_table = 'stk_product'

    @property
    def disponible(self):
        dispo = Model_Stockage.objects.filter(article_id = self.id).aggregate(Sum('quantite'))
        dispo = dispo['quantite__sum']

        if dispo == None:
            return 0
        return dispo

    @property
    def disponible_emplacement(self, emplacement_id):
        dispo = Model_Stockage.objects.filter(article_id = self.id, emplacement_id = emplacement_id).aggregate(Max('quantite'))
        # e = Model_Stockage.objects.filter(article_id = self.id, emplacement_id = emplacement_id)

        dispo = dispo['quantite__max']

        if dispo == None:
            return 0
        return dispo

    @property
    def valeur_inventaire(self):
        return self.disponible * self.amount
    


    def checkAsset(self):
        Serie = Model_Actif.objects.filter(article_id = self.id)
        if Serie != None:
            return True
        else:
            return False

class Model_Actif(models.Model):
    article       =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, related_name="series_articles", verbose_name = "Article", db_column="product")
    numero_serie  =   models.CharField(max_length=50, verbose_name = "Numéro de série", db_column="code", null = True, blank = True)
    est_actif     =   models.BooleanField(default=True, verbose_name = "Est actif", db_column="is_active")
    emplacement   =   models.ForeignKey("Model_Emplacement", on_delete=models.SET_NULL, blank=True, null=True, related_name="series_articles", verbose_name = "Emplacement", db_column="location")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_actifs', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_actifs', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.article.name + ' / ' + self.numero_serie

    class Meta:
        verbose_name = 'Actif'
        verbose_name_plural = 'Actifs'
        db_table = 'stk_active'

class Model_Stockage(models.Model):
    emplacement =   models.ForeignKey(Model_Emplacement, on_delete=models.CASCADE, related_name="stockages", verbose_name = "Emplacement")
    article =   models.ForeignKey(Model_Article,on_delete=models.CASCADE, related_name="stockages", verbose_name = "Article")
    quantite  =   models.FloatField(default=0.0, verbose_name = "Quantité")
    unite  =   models.ForeignKey(Model_Unite_mesure,on_delete=models.SET_NULL, blank=True, null=True, related_name="stockages", verbose_name = "Unité de mesure")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_stockages', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_stockages', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.emplacement.designation + " / "+ self.article.name

    class Meta:
        verbose_name = "Stockage"
        verbose_name_plural = "Stockages"
        db_table = "stk_storage"

    @property
    def series_emplacement(self):
        return Model_Actif.objects.filter(est_actif=True, article_id = self.article.id, emplacement_id=self.emplacement.id)


class Model_Statut_operation_stock(models.Model):
    designation                     =   models.CharField(max_length = 50, verbose_name = "Designation", db_column="name", null = True, blank = True)
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_statut_operation_stocks', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_statut_operation_stocks', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = "Statut d'opération stock"
        verbose_name_plural = "Statuts d'opération stock"
        db_table = "stk_stock_transaction_status"

class Model_Operation_stock(models.Model):
    designation =   models.CharField(max_length = 50, verbose_name = "Designation", db_column="name", null = True, blank = True)
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_operation_stocks', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_operation_stocks', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = "Opération stock"
        verbose_name_plural = "Opérations stock"
        db_table = "stk_stock_transaction"

class Model_Type_mvt_stock(models.Model):
    designation  =   models.CharField(max_length = 50, verbose_name = "Designation", db_column="name", null = True, blank = True)
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_type_mvt_stocks', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_type_mvt_stocks', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = "Type de mouvement stock"
        verbose_name_plural = "Types de mouvement stock"
        db_table = "stk_stock_movement_type"

class Model_Rebut(models.Model):
    numero  =   models.CharField(max_length=25, verbose_name = "Numéro", db_column="code", null = True, blank = True)
    date      =   models.DateTimeField(auto_now_add=True, verbose_name = "Date", db_column="date")
    article =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, blank=True, null=True, related_name="rebuts", verbose_name = "Article", db_column="product")
    serie_article =   models.CharField(max_length=50, blank=True, null=True, verbose_name = "Numero Série", db_column="series")
    quantite  =   models.FloatField(default=0, verbose_name = "Quantité", db_column="quantity")
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    status =   models.ForeignKey(Model_Statut_operation_stock, null = True, blank = True, on_delete=models.SET_NULL, related_name="status_rebut", verbose_name = "Status", db_column="status_rebut")
    unite  =   models.ForeignKey(Model_Unite_mesure, on_delete=models.SET_NULL, blank=True, null=True, related_name="rebuts", verbose_name = "Unité de mesure", db_column="measure_unit")
    emplacement_origine  =   models.ForeignKey(Model_Emplacement, on_delete=models.CASCADE, blank=True, null=True, related_name="emplacement_rebut", verbose_name = "Emplacement d'origine", db_column="original_location")
    emplacement_rebut=   models.ForeignKey(Model_Emplacement, on_delete=models.CASCADE, blank=True, null=True, related_name="emplacement_rebut_destination", verbose_name = "Emplacement rébut", db_column="rebut_location")
    document =   models.CharField(max_length=500, blank=True, null=True, verbose_name = "Document d'origine", db_column="document")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_rebuts', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_rebuts', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = "Rebut"
        verbose_name_plural = "Rebuts"
        db_table = "stk_rebut"

class Model_Statut_ajustement(models.Model):
    designation                         =   models.CharField(max_length = 100, verbose_name = "Designation", db_column="code", null = True, blank = True)
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_statut_ajustements', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_statut_ajustements', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = "Statut inventaire"
        verbose_name_plural = "Statuts inventaire"
        db_table = "stk_inventory_status"

class Model_Ajustement(models.Model):
    reference  =   models.CharField(max_length = 100, verbose_name = "Référence", db_column="code", null = True, blank = True)
    date  =   models.DateTimeField(auto_now_add=True, verbose_name = "Date", db_column="date")
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    emplacement =   models.ForeignKey(Model_Emplacement, on_delete=models.CASCADE, related_name="ajustements", verbose_name = "Emplacement", db_column="location")
    status  =   models.ForeignKey(Model_Statut_ajustement, null = True, blank = True, on_delete=models.CASCADE, related_name="ajustements", verbose_name = "Status Ajustement", db_column="ajustment_status")
    inventaire_de =   models.IntegerField(blank=True, null=True, verbose_name = "Inventaire de", db_column="ajustment_inventory")
    document  =   models.CharField(max_length = 100, blank=True, null=True, verbose_name = "Document", db_column="document")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_ajustements', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_ajustements', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.reference

    @property
    def numero(self):
        return f"INV-{self.pk}"

    class Meta:
        verbose_name = "Inventaire"
        verbose_name_plural = "Inventaires"
        db_table = "stk_inventory"

class Model_Ligne_ajustement(models.Model):
    ajustement =   models.ForeignKey(Model_Ajustement, on_delete=models.CASCADE, related_name="ligne_ajustement", verbose_name = "Inventaire", db_column="ajustment")
    article  =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, blank=True, null=True, related_name="lignes_ajustements", verbose_name = "Article", db_column="product")
    series   =   models.ManyToManyField(Model_Actif, verbose_name = "Séries", db_column="series")
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    quantite_theorique =   models.FloatField(default=0, verbose_name = "Quantité théorique", db_column="quantity_theoretical")
    quantite_reelle =   models.FloatField(blank=True, null=True, default=0, verbose_name = "Quantité réelle", db_column="quantity_actual")
    unite  =   models.ForeignKey(Model_Unite_mesure, on_delete=models.SET_NULL,blank=True, null=True, related_name="lignes_ajustements", verbose_name = "Unité", db_column="unit")
    fait  =   models.BooleanField(default=False, verbose_name = "Est fait", db_column="is_done")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_ligne_ajustements', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_ligne_ajustements', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.ajustement.reference

    class Meta:
        verbose_name = "Ligne Inventaire"
        verbose_name_plural = "Lignes Inventaires"
        db_table = "stk_inventory_line"

class Model_Bon_reception(models.Model):
    code  =   models.CharField(max_length = 100, null = True, blank=True, default = '' , verbose_name = "Code reception", db_column="code")
    description  =    models.CharField(max_length = 300, null = True, blank=True, default = '', verbose_name = "Description", db_column="description")
    date_prevue  =   models.DateTimeField(auto_now_add=True, verbose_name = "Date", db_column="date")
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    emplacement_destination  = models.ForeignKey(Model_Emplacement,on_delete = models.SET_NULL, related_name="emplacement_destination_reception", null = True, blank = True, verbose_name = "Emplacement Destination", db_column="destination_location")
    emplacement_origine =  models.ForeignKey(Model_Emplacement,on_delete= models.SET_NULL, related_name="emplacement_origin_reception", null = True, blank = True, verbose_name = "Emplacement Origine", db_column="original_location")
    operation_stock  = models.ForeignKey(Model_Operation_stock, related_name="operration_stock_reception", null = True, blank = True, on_delete=models.SET_NULL, verbose_name = "Opération Stock", db_column="stock_operating") 
    status =   models.ForeignKey(Model_Statut_operation_stock, null = True, blank = True, on_delete=models.SET_NULL, related_name="operations_status_receipt", verbose_name = "Statut", db_column="operation_status")
    bon_livraison  =   models.FileField(upload_to="media",max_length = 25, blank=True, null=True, verbose_name = "Document d'Origine")
    employe  =  models.ForeignKey("ErpBackOffice.Model_Personne", related_name="employe_stock_receptions", null = True, blank = True, on_delete=models.SET_NULL, verbose_name = "Employé", db_column="employe")
    statut = models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat= models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date=  models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date  = models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by  =models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_bon_receptions', null = True, blank = True, db_column='updated_by')
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_bon_receptions', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Bon de Reception'
        verbose_name_plural = 'Bons de Receptions'
        db_table = 'stk_receipt_slip'


    @property
    def etat_livraison(self):
        reception_id = self.id
        demande = Model_Ligne_reception.objects.filter(bon_reception_id = reception_id).aggregate(Sum('quantite_demandee'))
        demande = makeFloat(demande['quantite_demandee__sum'])

        fait = Model_Ligne_reception.objects.filter(bon_reception_id = reception_id).aggregate(Sum('quantite_fait'))
        fait = makeFloat(fait['quantite_fait__sum'])

        if fait >= demande:
            return "Fini"
        else:
            return "Non fini"

class Model_Ligne_reception(models.Model):
    bon_reception   =   models.ForeignKey(Model_Bon_reception, on_delete=models.CASCADE, related_name="lignes_bon_reception", verbose_name = "Opération stock", db_column="inventory_operation")
    article =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, related_name="lignes_article_reception", verbose_name = "Article", db_column="product")
    series =   models.ManyToManyField(Model_Actif, verbose_name = "Numéros de serie", db_column="series")
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    quantite_demandee  =   models.FloatField(default=0, verbose_name = "Quantité demandée", db_column="quantity_requested")
    quantite_fait =   models.FloatField(blank=True, null=True, default=0, verbose_name = "Quantité réalisée", db_column="quantity_produced")
    quantite_reste =   models.FloatField(blank=True, null=True, default=0, verbose_name = "Quantité restante", db_column="quantity_rest")
    prix_unitaire =   models.FloatField(blank=True, null=True, default=0, verbose_name = "Prix Unitaire", db_column="price_unit")
    unite =   models.ForeignKey(Model_Unite_mesure, on_delete=models.SET_NULL,blank=True, null=True, related_name="lignes_bon_reception", verbose_name = "Unité de mesure", db_column="measure_unit")
    devise  =   models.ForeignKey("ErpBackOffice.Model_Devise", on_delete=models.SET_NULL, blank=True, null=True, related_name="lignes_bon_reception", verbose_name = "Devise", db_column="currency_id")
    description  =   models.CharField(max_length = 500, blank=True, null=True, verbose_name = "Description", db_column="description")
    fait  =   models.BooleanField(default=False, verbose_name = "Est réalisé", db_column="is_realised")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_ligne_receptions', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_ligne_ligne_receptions', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.bon_reception.code + " / " + self.article.name

    class Meta:
        verbose_name = 'Line Bon de Reception'
        verbose_name_plural = 'Lines Bons de Receptions'
        db_table = 'stk_line_receipt'

    @property
    def quantite_restante(self):
        return self.quantite_demandee - self.quantite_fait

    @property
    def total(self):
        return self.prix_unitaire * self.quantite


class Model_Bon_transfert(models.Model):
    code  =   models.CharField(max_length = 100, null = True, blank=True, default = '' , verbose_name = "Code transfert", db_column="code")
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    emplacement_origine =  models.ForeignKey(Model_Emplacement,on_delete= models.SET_NULL, related_name="emplacement_origin_transfert", null = True, blank = True, verbose_name = "Emplacement Origine", db_column="original_location")
    emplacement_destination  = models.ForeignKey(Model_Emplacement,on_delete = models.SET_NULL, related_name="emplacement_destination_transfert", null = True, blank = True, verbose_name = "Emplacement Destination", db_column="destination_location")   
    status =   models.ForeignKey(Model_Statut_operation_stock, null = True, blank = True, on_delete=models.SET_NULL, related_name="operations_status_transfert", verbose_name = "Statut", db_column="operation_status")
    operation_stock  = models.ForeignKey(Model_Operation_stock, related_name="operration_stock_transfert", null = True, blank = True, on_delete=models.SET_NULL, verbose_name = "Opération Stock", db_column="stock_operating")
    description  =    models.CharField(max_length = 300, null = True, blank=True, default = '', verbose_name = "Description", db_column="description")
    responsable_transfert =    models.ForeignKey(Model_Personne,on_delete = models.SET_NULL, related_name="demandeur_doing_bon_transfert", null = True, blank = True, verbose_name = "Responsable Transfert", db_column="Transfert_Manager")
    statut = models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status_wkf')
    etat  = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_ligne_transfert_stocks', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_ligne_transfert_stocks', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Bon de Transfert'
        verbose_name_plural = 'Bons de Transferts'
        db_table = 'stk_bon_transfer'

class Model_Ligne_bon_transfert(models.Model):
    quantite  =   models.FloatField(default=0, verbose_name = "Quantité fournie", db_column="quantity_requested")
    quantite_fait  =   models.FloatField(blank=True, null=True, default=0, verbose_name = "Quantité transferée", db_column="quantite_transfer")
    article =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, related_name="lignes_article_transfert", verbose_name = "Article", db_column="product")
    series =   models.ManyToManyField(Model_Actif, verbose_name = "Numéros de serie", db_column="series")
    description =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    fait  =   models.BooleanField(default=False, verbose_name = "Est réalisé", db_column="is_realised")
    bon_transfert  =    models.ForeignKey("Model_Bon_transfert",on_delete = models.SET_NULL, related_name="ligne_of_bon_commande", null = True, blank = True)
    stockage            =    models.ForeignKey("Model_Stockage",on_delete = models.SET_NULL, related_name="ligne_transfere_take_on_stockage", null = True, blank = True, verbose_name = "stockage", db_column="storage")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_ligne_ligne_transferts', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_ligne_ligne_transferts', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return 'ligne transfert {}'.format(self.article)

    class Meta:
        verbose_name = 'Line bon de Transfert'
        verbose_name_plural = 'Lines Bons de Transferts'
        db_table = 'stk_line_bon_transfer'

class Model_Bon_sortie(models.Model):
    code  =   models.CharField(max_length = 100, null = True, blank=True, default = '' , verbose_name = "Code Transfert", db_column="code")
    description  =    models.CharField(max_length = 300, null = True, blank=True, default = '', verbose_name = "Description", db_column="description")
    emplacement_destination  = models.ForeignKey(Model_Emplacement,on_delete = models.SET_NULL, related_name="emplacement_destination_bon_sorties", null = True, blank = True, verbose_name = "Emplacement Destination", db_column="destination_location")
    emplacement_origine =  models.ForeignKey(Model_Emplacement,on_delete= models.SET_NULL, related_name="emplacement_origin_bon_sorties", null = True, blank = True, verbose_name = "Emplacement Origine", db_column="original_location")
    operation_stock  = models.ForeignKey(Model_Operation_stock, related_name="operration_stock_sorties", null = True, blank = True, on_delete=models.SET_NULL, verbose_name = "Opération Stock", db_column="stock_operating") 
    status =   models.ForeignKey(Model_Statut_operation_stock, null = True, blank = True, on_delete=models.SET_NULL, related_name="operations_status_bon_sorties", verbose_name = "Statut", db_column="operation_status")
    employe  =  models.ForeignKey("ErpBackOffice.Model_Personne", related_name="employe_stock_bon_sorties", null = True, blank = True, on_delete=models.SET_NULL, verbose_name = "Employé", db_column="employe")
    statut = models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat= models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date=  models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date  = models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by  =models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_bon_sorties', null = True, blank = True, db_column='updated_by')
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_bon_sorties', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Bon de Sortie'
        verbose_name_plural = 'Bons de Sorties'
        db_table = 'stk_output'

class Model_Ligne_bon_sortie(models.Model):
    quantite_demandee  =  models.FloatField(default=0, blank=True, null=True, verbose_name = "Quantité", db_column="quantity")
    quantite_sortie  =   models.FloatField(blank=True, null=True, default=0, verbose_name = "Quantité Sortie", db_column="quantity_out")
    serie  =   models.ForeignKey(Model_Actif,on_delete=models.SET_NULL,blank=True, null=True, related_name = 'asset_line_sorties', verbose_name = "Numéros de serie", db_column="series")
    description  =    models.CharField(max_length = 100, null = True, blank=True, default = '', verbose_name = "description", db_column="description")
    bon_sortie  =    models.ForeignKey("Model_Bon_sortie",on_delete = models.CASCADE, related_name="bon_sortie_lines", null = True, blank = True, verbose_name = "Bon_transfert")
    article   =    models.ForeignKey('Model_Article', on_delete=models.SET_NULL, blank=True, null=True, related_name="article_lines_sortie", verbose_name = "Article", db_column="product")
    stockage  =    models.ForeignKey("Model_Stockage",on_delete = models.SET_NULL, related_name="ligne_bon_sortie_take_on_stockage", null = True, blank = True, verbose_name = "stockage", db_column="storage")    
    statut = models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat = models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    creation_date =  models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date  = models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by  =models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_line_sortie', null = True, blank = True, db_column='updated_by')
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_line_bon_sortie', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')

    def __str__(self):
        return 'ligne {}'.format(self.article)

    class Meta:
        verbose_name = 'Line Bon de Sortie'
        verbose_name_plural = 'Lines Bons de Sorties'
        db_table = 'stk_line_output'


class Model_Bon_retour(models.Model):
    code  =   models.CharField(max_length = 100, null = True, blank=True, default = '' , verbose_name = "Code Transfert", db_column="code")
    date_realisation =    models.DateTimeField(null = True, blank = True, verbose_name = "Date de retour", db_column="date_return")
    creation_date =  models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    est_realisee =    models.BooleanField(default = False, verbose_name = "Est realisee" , db_column='is_realise')
    quantite =    models.IntegerField(default = 0, verbose_name = "Quantité" , db_column='quantity')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    operation_stock  = models.ForeignKey(Model_Operation_stock, related_name="operation_stock_bon_retours", null = True, blank = True, on_delete=models.SET_NULL, verbose_name = "Opération Stock", db_column="stock_operating")
    status =   models.ForeignKey(Model_Statut_operation_stock, null = True, blank = True, on_delete=models.SET_NULL, related_name="operations_status_bon_retour", verbose_name = "Statut", db_column="operation_status")
    statut = models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat = models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    description  =    models.CharField(max_length = 100, null = True, blank=True, default = '', verbose_name = "description", db_column="description")
    agent  =    models.ForeignKey(Model_Personne,on_delete = models.SET_NULL, related_name="agent_charge_du_bon_retour", null = True, blank = True, verbose_name = "Agent", db_column="Agent")
    responsable_retour =    models.ForeignKey(Model_Personne,on_delete = models.SET_NULL, related_name="demandeur_doing_bon_retour", null = True, blank = True, verbose_name = "Responsable", db_column="Responsable")
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_bon_retour', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')
    emplacement_destination  = models.ForeignKey(Model_Emplacement,on_delete = models.SET_NULL, related_name="emplacement_destination_retours", null = True, blank = True, verbose_name = "Emplacement Destination", db_column="destination_location")
    emplacement_origine =  models.ForeignKey(Model_Emplacement,on_delete= models.SET_NULL, related_name="emplacement_origin_bon_retours", null = True, blank = True, verbose_name = "Emplacement Origine", db_column="original_location")
    update_date  = models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by  =models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_bon_retours', null = True, blank = True, db_column='updated_by', verbose_name = "Modifier par",)


    def __str__(self):
        return self.code


    class Meta:
        verbose_name = 'Bon de Retour'
        verbose_name_plural = 'Bons de Retours'
        db_table = 'stk_return_bon'

class Model_Ligne_bon_retour(models.Model):
    quantite_fournie  =    models.IntegerField(default = 0, verbose_name = "Quantité" , db_column='quantity')
    creation_date =  models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    numero_serie  =    models.CharField(max_length = 100, null = True, blank=True, default = '', verbose_name = "Numero Serie", db_column="numero_serie")
    description  =    models.CharField(max_length = 100, null = True, blank=True, default = '', verbose_name = "description", db_column="description")
    bon_retour =    models.ForeignKey("Model_Bon_retour",on_delete = models.SET_NULL, related_name="ligne_of_bon_retour", null = True, blank = True, verbose_name = "Bon de Retour" ,db_column="return_bon")
    article   =    models.ForeignKey('Model_Article', on_delete=models.CASCADE, blank=True, null=True, related_name="article_lines_retour", verbose_name = "Article", db_column="product")    
    stock_article =    models.ForeignKey("Model_Stockage",on_delete = models.SET_NULL, related_name="ligne_bon_retour_take_on_Stockage_article", null = True, blank = True, verbose_name = "Stockage" ,db_column="stockage")
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_line_bon_retour', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')
    statut = models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat = models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    update_date  = models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by  =models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateurs_line_retour', null = True, blank = True, db_column='updated_by', verbose_name = "Modifier par",)

    def __str__(self):
        return 'ligne {}'.format(self.article)


    class Meta:
        verbose_name = 'Bon de line Retour'
        verbose_name_plural = 'Lines Bons de Retours'
        db_table = 'stk_return_line_bon'

class Model_Mvt_stock(models.Model):
    date       =   models.DateTimeField(auto_now_add=True, verbose_name = "Date", db_column="date")
    type      =   models.ForeignKey(Model_Type_mvt_stock, on_delete=models.CASCADE, related_name='date_mvts_stocks', verbose_name = "Type mouvement", db_column="type")
    article    =   models.ForeignKey(Model_Article,on_delete=models.CASCADE, related_name="type_mvts_stocks", verbose_name = "Article", db_column="product")
    series       =   models.ManyToManyField(Model_Actif, verbose_name = "Numéros de serie", db_column="series")
    emplacement  =   models.ForeignKey(Model_Emplacement, on_delete=models.CASCADE, related_name="emplacement_mvts_stocks", verbose_name = "Emplacement", db_column="location")
    reception =   models.ForeignKey(Model_Bon_reception, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_mvts_stocks", verbose_name = "Réception", db_column="receipt")
    transfert =   models.ForeignKey(Model_Bon_transfert, on_delete=models.CASCADE, blank=True, null=True, related_name="transfert_mvts_stocks", verbose_name = "Transfert", db_column="transfer")
    sortie   =   models.ForeignKey(Model_Bon_sortie, on_delete=models.CASCADE, blank=True, null=True, related_name="sortie_mvts_stocks", verbose_name = "Sortie", db_column="output")
    retour   =   models.ForeignKey(Model_Bon_retour, on_delete=models.CASCADE, blank=True, null=True, related_name="retour_mvts_stocks", verbose_name = "Retour", db_column="return")
    ajustement   =   models.ForeignKey("Model_Ajustement", on_delete=models.CASCADE, blank=True, null=True, related_name="ajustement_mvts_stocks", verbose_name = "Inventaire", db_column="adjustment")
    rebut   =   models.ForeignKey("Model_Rebut", on_delete=models.CASCADE, blank=True, null=True, related_name="rebut_mvts_stocks", verbose_name = "Rebut", db_column="scum")
    quantite_initiale  =   models.FloatField(default=0, verbose_name = "Quantité Initiale", db_column="quantity_initial")
    unite_initiale =   models.ForeignKey(Model_Unite_mesure, on_delete=models.SET_NULL,blank=True, null=True, related_name="qte_mvts_stocks_unites_initials", verbose_name = "Unité de mesure initiale", db_column="unit_initial")
    quantite   =   models.FloatField(default=0, verbose_name = "Quantité finale", db_column="quantity_final")
    societe  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    unite    =   models.ForeignKey(Model_Unite_mesure, on_delete=models.SET_NULL,blank=True, null=True, related_name="unite_mvts_stocks_unites_finales", verbose_name = "Unité de mesure finale", db_column="unit_final")
    est_rebut  =   models.BooleanField(default=False, verbose_name = "Est rebut", db_column="is_scum")
    statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Statut", db_column='status')
    etat    =    models.CharField(max_length=50, blank=True, null=True, verbose_name = "Etat", db_column='state')
    creation_date    =    models.DateTimeField(auto_now_add = True, verbose_name = "Date de création" , db_column='created_date')
    update_date    =    models.DateTimeField(auto_now = True, verbose_name = "Date de dernière modification", db_column='updated_date')
    update_by    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'modificateur_mvt_stocks', null = True, blank = True, db_column='updated_by')
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_mvt_stocks', null = True, blank = True, verbose_name = "Créé par" , db_column='created_by')


    def __str__(self):
        return self.article.name + ' / ' + str(self.quantite)

    class Meta:
        verbose_name = "Mouvement stock"
        verbose_name_plural = "Mouvements stocks"
        db_table = "stk_stock_movement"
