from django.contrib import admin
from . import models

admin.site.register(models.Model_Emplacement)
admin.site.register(models.Model_Type_emplacement)

admin.site.register(models.Model_Unite_mesure)
admin.site.register(models.Model_Categorie)

admin.site.register(models.Model_Type_article)
admin.site.register(models.Model_Article)
admin.site.register(models.Model_Actif)
admin.site.register(models.Model_Stockage)
admin.site.register(models.Model_Statut_operation_stock)

admin.site.register(models.Model_Operation_stock)
admin.site.register(models.Model_Type_mvt_stock)
admin.site.register(models.Model_Rebut)
admin.site.register(models.Model_Statut_ajustement)
admin.site.register(models.Model_Ajustement)
admin.site.register(models.Model_Ligne_ajustement)

admin.site.register(models.Model_Bon_reception)
admin.site.register(models.Model_Ligne_reception)
admin.site.register(models.Model_Bon_transfert)
admin.site.register(models.Model_Ligne_bon_transfert)
admin.site.register(models.Model_Bon_sortie)
admin.site.register(models.Model_Ligne_bon_sortie)

admin.site.register(models.Model_Mvt_stock)

