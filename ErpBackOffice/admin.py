from django.contrib import admin
from django import forms

# Register your models here.
from . import models

# Register your models here.
admin.site.register(models.Model_Personne)
admin.site.register(models.Model_Module)
admin.site.register(models.Model_SousModule)
admin.site.register(models.Model_ActionUtilisateur)
admin.site.register(models.Model_Devise)
admin.site.register(models.Model_Taux)
admin.site.register(models.Model_Place)
admin.site.register(models.Model_Wkf_Workflow)
admin.site.register(models.Model_Wkf_Etape)
admin.site.register(models.Model_Wkf_Condition)
admin.site.register(models.Model_Wkf_Transition)
admin.site.register(models.Model_Wkf_Historique)
admin.site.register(models.Model_Wkf_Approbation)
admin.site.register(models.Model_Wkf_Stakeholder)
admin.site.register(models.Model_Notification)
admin.site.register(models.Model_Temp_Notification)
admin.site.register(models.Model_Message)
admin.site.register(models.Model_ModuleOverModel)
admin.site.register(models.Model_Organisation)
admin.site.register(models.Model_Civilite)
admin.site.register(models.Model_GroupeMenu)
admin.site.register(models.Model_GroupePermission)
admin.site.register(models.Model_Permission)
admin.site.register(models.Model_Regle)
admin.site.register(models.Model_LigneRegle)
admin.site.register(models.Model_GroupePermissionUtilisateur)
admin.site.register(models.Model_Operationnalisation_module)