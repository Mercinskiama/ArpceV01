# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from email.policy import default

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Max, Sum, Q, Count
from datetime import time, timedelta, datetime, date
import calendar
import json
from random import randint
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ErpBackOffice.utils.separateur import AfficheEntier
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in, user_logged_out
from dateutil.relativedelta import relativedelta
from django.forms import model_to_dict


PlaceType =	(
    (1, "Pays"),
    (2, "Etat / Province"),
    (3, "Ville"),
    (4, "Commune"),
    (5, "Quartier")
)
JoursDelaSemaine = (
    ('1', 'Lundi'),
    ('2', 'Mardi'),
    ('3', 'Mercredi'),
    ('4', 'Jeudi'),
    ('5', 'Vendredi'),
    ('6', 'Samedi'),
    ('7', 'Dimanche')
)

# WORKFLOW
TypeOperateur = (
    (1, "OR"),
    (2, "AND")
)
TypeOperationTest = (
    (1, "<"),
    (2, "<="),
    (3, ">"),
    (4, ">="),
    (5, "=="),
    (6, "!=")
)
TypeConditionTest = (
    (1, "Début"),
    (2, "Ou"),
    (3, "Et"),
    (4, "sauf")
)


# COMMON MODEL
class Model_Personne(models.Model):
    #Propriete commune à toutes personnes
    prenom                    =    models.CharField(max_length = 250, null = True, blank = True)
    nom                        =    models.CharField(max_length = 250, null = True, blank = True)
    nom_complet                =    models.CharField(max_length = 400, null = True, blank = True)
    image                    =    models.CharField(max_length = 700, null = True, blank = True, default="")
    email                    =    models.CharField(max_length = 150, null = True, blank = True, default="")
    phone                    =    models.CharField(max_length = 100, null = True, blank = True, default="")
    adresse                    =    models.CharField(max_length = 500, null = True, blank = True, default="")
    commune_quartier           =    models.ForeignKey("Model_Place", on_delete = models.SET_NULL, related_name="personnes", null = True, blank = True)
    est_actif                 =    models.BooleanField(default = True)
    creation_date            =     models.DateTimeField(auto_now_add = True,null=True,blank=True)
    auteur                    =     models.ForeignKey("Model_Personne", on_delete = models.SET_NULL, related_name="personnes_creees", null = True, blank = True)
    est_particulier            =    models.BooleanField(default=False)
    societe                  =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    update_date              =    models.DateTimeField(auto_now=True)
    user                     =    models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name="users_employes")

    @property
    def all_users(self):
        return Model_Personne.objects.all()
        
    @property
    def is_connected(self):
        try:
            employe = Model_UserSessions.objects.filter(user = self.user, is_active = True, logout_date = None)
            if employe:
                return True
            return False
        except Exception as e:
            return False

    def __str__(self):
        if self.nom_complet != None and self.nom_complet != "":
            return self.nom_complet
        else: return "%s %s" % (self.prenom, self.nom)

    @property
    def adresse_complete(self):
        place = Model_Place.objects.get(pk = self.commune_quartier_id)
        adresse = place.designation
        i = 1
        while place.parent_id != None and place.parent_id != 0:
            place = Model_Place.objects.get(pk = place.parent_id)
            if i % 2 == 0 : adresse = adresse + ', \n' + place.designation
            else : adresse = adresse + ', \n' + place.designation
        return self.adresse + ', \n' + adresse

    @property
    def utilisateur(self):
        if self.user_id == None: return None

        user = User.objects.get(pk = self.user_id)
        return user

class Model_Civilite(models.Model):
    designation                =    models.CharField(max_length = 20, verbose_name = "Montant")
    designation_court        =    models.CharField(max_length = 5, verbose_name = "Montant")
    societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut                  =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', related_name="civilites", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    update_date             =    models.DateTimeField(auto_now = True)
    auteur                    =    models.ForeignKey(Model_Personne, related_name="auteur_civilite", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = 'Civilité'
        verbose_name_plural = 'Civilités'


class Model_Place(models.Model):
    designation                =    models.CharField(max_length = 50, null = True, blank = True)
    code_telephone            =    models.CharField(max_length = 5, null = True, blank = True)
    place_type                =    models.IntegerField(choices = PlaceType)
    code_pays                =    models.CharField(max_length=3, null = True, blank = True, default="")
    parent                    =    models.ForeignKey("Model_Place", null = True, blank = True, on_delete = models.CASCADE, related_name="fils")
    societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    url                    =     models.CharField(max_length = 250, blank=True, null=True)
    auteur                    =    models.ForeignKey(Model_Personne, related_name="auteur_place", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.designation

    @property
    def places_filles(self):
        return Model_Place.objects.filter(parent_id = self.id)

#New way Of droit

class Model_Module(models.Model):
    nom_module                =    models.CharField(max_length = 50, null = True, blank = True)
    nom_application           =    models.CharField(max_length = 100, null = True, blank = True)
    code                    =    models.CharField(max_length = 5, null = True, blank = True)
    description                =    models.TextField(null = True, blank = True)
    est_installe            =    models.BooleanField(default = False)
    url_vers                =    models.CharField(max_length = 100, null = True, blank = True)
    numero_ordre            =    models.IntegerField()
    icon_module                =    models.CharField(max_length = 50, default = "", null = True, blank = True)
    couleur                    =    models.CharField(max_length = 15, default = "", null = True, blank = True)
    url =     models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                                                                                                                                              =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_module", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Module %s" % self.nom_module

    @property
    def nombre_periode(self):
        return Model_Operationnalisation_module.objects.filter(module_id = self.id).count()
    
    @property
    def periode_active(self):
        return Model_Operationnalisation_module.objects.filter(module_id = self.id).filter(est_active = True).count()

    @property
    def periode_cloture(self):
        return Model_Operationnalisation_module.objects.filter(module_id = self.id).filter(est_cloture = True).count()
    
class Model_Operationnalisation_module(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    est_active = models.BooleanField(default = False)
    est_cloture = models.BooleanField(default = False)
    observation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    module      = models.ForeignKey(Model_Module, on_delete = models.SET_NULL, related_name = 'module_fk_xdu', null = True, blank = True)
    statut      =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now = True)
    auteur      = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_operationnalisation_module_pyz', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_GroupeMenu(models.Model):
    designation        = models.CharField(max_length = 50, null = True, blank = True)
    icon_menu          = models.CharField(max_length = 150, null = True, blank = True)
    description        = models.CharField(max_length = 250, null = True, blank = True)
    module             = models.ForeignKey(Model_Module, related_name="module_of_groupemenu", on_delete=models.CASCADE)
    url                = models.CharField(max_length = 250, blank=True, null=True)
    numero_ordre       =    models.IntegerField()
    creation_date      =    models.DateTimeField(auto_now=True)
    auteur             = models.ForeignKey(Model_Personne, related_name="auteur_of_groupe_menu", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Groupe %s / %s" % (self.designation, self.module.nom_module)


class Model_SousModule(models.Model):
    module                    =    models.ForeignKey(Model_Module, related_name="sous_modules", on_delete=models.CASCADE)
    nom_sous_module            =    models.CharField(max_length = 50, null = True, blank = True)
    description                =    models.TextField(null = True, blank = True)
    groupe                    =    models.CharField(max_length = 50, null = True, blank = True)
    icon_menu          = models.CharField(max_length = 150, null = True, blank = True)
    url_vers                =    models.CharField(max_length = 100, null = True, blank = True)
    numero_ordre            =    models.IntegerField()
    est_model               =    models.BooleanField(default = False)
    est_dashboard            =      models.BooleanField(default = False)
    est_actif            =      models.BooleanField(default = True)
    model_principal            =    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    groupe_menu               =    models.ForeignKey(Model_GroupeMenu, related_name="groupe_menu",  blank=True, null=True, on_delete=models.SET_NULL)
    update_date                 =    models.DateTimeField(auto_now_add = True)
    #permissions        =    models.ManyToManyField("Model_Permission", related_name="permission_related_to_sous_module", blank = True)
    url                    =     models.CharField(max_length = 250, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now=True)
    auteur                    =    models.ForeignKey(Model_Personne, related_name="auteur_sous_module", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Module %s / %s" % (self.module.nom_module, self.nom_sous_module)

#Ex Equivalent à Model_Droit
class Model_Permission(models.Model):
    sous_module              =    models.ForeignKey(Model_SousModule, on_delete = models.CASCADE, related_name="permission_of_sous_module", null = True, blank = True)
    designation              =    models.CharField(max_length = 50, null = True, blank = True)
    numero                   =    models.IntegerField(null = True, blank = True, unique = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_permission", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.sous_module:
            name = self.sous_module.module.nom_module
        else:
            name = "Rien"
        return "Permission %s / %s" % (self.designation, name)


#Ex Equivalent à Model_Role
class Model_GroupePermission(models.Model):
    designation              =    models.CharField(max_length = 100, null = True, blank = True)
    permissions              =    models.ManyToManyField("Model_Permission", related_name="permission_related_to_a_group", blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_groupe", null = True, blank = True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


    def stat(self):
        stat = {}
        modules = []
        sous_modules = []
        try:
            permissions = self.permissions.all()
            for permission in permissions:
                if permission.sous_module:
                    sous_modules.append(permission.sous_module)
                    if permission.sous_module.module:
                        modules.append(permission.sous_module.module)
            modules = set(modules)
            modules = list(modules)
            sous_modules = set(sous_modules)
            sous_modules = list(sous_modules)
            stat["nombre_module"] = len(modules)
            stat["nombre_sous_module"] = len(sous_modules)
            return stat

        except Exception as e:
            #print("ERREUR")
            #print(e)
            return 0

class Model_GroupePermissionUtilisateur(models.Model):
    groupe_permission        =    models.ForeignKey(Model_GroupePermission, related_name="groupe_permission", null = True, blank = True, on_delete=models.CASCADE)
    utilisateur              =    models.ForeignKey(Model_Personne, on_delete=models.CASCADE)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_groupe_permission_utilisateur", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.utilisateur.nom_complet + " / " + self.groupe_permission.designation

class Model_Regle(models.Model):
    designation             =    models.CharField(max_length = 100, null = True, blank = True)
    filtre                  =    models.CharField(max_length = 250, null = True, blank = True)
    #permission             =    models.ForeignKey(Model_Permission, related_name="regle_link_to_permission", on_delete=models.CASCADE,  blank = True, null = True)
    permissions             =    models.ManyToManyField(Model_Permission, related_name="regle_link_to_all_permission")
    groupe_permission       =    models.ForeignKey(Model_GroupePermission, related_name="regle_link_to_a_group", on_delete=models.CASCADE, null = True, blank = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_regle", null = True, blank = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add=True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return " %s / %s" % (self.groupe_permission.designation, self.designation)
    
    @property
    def expression(self):
        try:
            if self.lignes.count() == 0: return ""
            expression = "results."

            for ligne in self.lignes.all():
                # On récupère le code et la valeur du test
                code = ligne.code
                valeur = ligne.valeur
                operation = "="
                if ligne.type_operation == 1: operation = "__lt="
                elif ligne.type_operation == 2: operation = "__lte="
                elif ligne.type_operation == 3: operation = "__gt="
                elif ligne.type_operation == 4: operation = "__gte="

                if ligne.type_condition == 1: 
                    expression = "{}).filter(".format(expression)
                elif ligne.type_condition == 4:
                    expression = "{}).exclude(".format(expression)
                elif ligne.type_condition == 2:
                    expression = "{}|".format(expression)    
                elif ligne.type_condition == 3:
                    expression = "{}&".format(expression)

                if ligne.type_operation == 6: expression = "{}~Q({}{}{})".format(expression, code, operation, valeur)
                else: expression = "{}Q({}{}{})".format(expression, code, operation, valeur)
                
            expression = "{})".format(expression)
            expression = expression.replace(".).", ".")
            
            print("expression {}".format(expression))
            return expression
        except Exception as e:
            return ""
    
class Model_LigneRegle(models.Model):
    sequence                =    models.IntegerField(default = 99)
    regle                   =    models.ForeignKey(Model_Regle, on_delete=models.CASCADE, related_name="lignes")
    type_operation          =    models.IntegerField(choices = TypeOperationTest, default= 1)
    type_condition          =    models.IntegerField(choices = TypeConditionTest, default= 1)
    valeur                  =    models.CharField(max_length = 500, null = True, blank = True)
    code                    =    models.CharField(max_length = 500, null = True, blank = True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    update_date             =    models.DateTimeField(auto_now = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="auteur_lignes", null = True, blank = True)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return "Ligne Règle No {} - {}".format(self.sequence, self.regle.designation)

    @property
    def value_type_operation(self):
        try:
            return dict(TypeOperationTest)[int(self.type_operation)]
        except Exception as e:
            return ""

    @property
    def value_type_condition(self):
        try:
            return dict(TypeConditionTest)[int(self.type_condition)]
        except Exception as e:
            return ""

#End new way of droit

class Model_ActionUtilisateur(models.Model):
    nom_action               =    models.CharField(max_length = 200, null = True, blank = True)
    ref_action               =    models.CharField(max_length = 200, default = "", null = True, blank = True)
    description              =    models.TextField()
    permission               =    models.ForeignKey(Model_Permission, on_delete = models.CASCADE, related_name="actions", null = True, blank = True)
    url                      =     models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_action_utilisation", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "ACTION %s" % self.nom_action


class Model_ModuleOverModel(models.Model):
    nom_modele               =    models.CharField(max_length = 100)
    module_id                =    models.ForeignKey(Model_Module, on_delete=models.SET_NULL, null=True)
    model_id                 =    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_moduleovermodel", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s" % (self.nom_modele)

class Model_Devise(models.Model):
    symbole_devise           =    models.CharField(max_length = 5, null = True, blank = True, verbose_name = "Symbole")
    code_iso                 =    models.CharField(max_length = 5, null = True, blank = True, verbose_name = "Code ISO")
    designation              =    models.CharField(max_length = 200, null = True, blank = True, verbose_name = "Designation")
    est_reference            =    models.BooleanField(default = False, verbose_name = "Est référence")
    est_active               =    models.BooleanField(default = False, verbose_name = "Est active")
    est_locale               =    models.BooleanField(default = False, verbose_name = "Est monnaie locale")
    sous_unite               =    models.BooleanField(default = False, verbose_name = "A un sous unité")
    num_decimale             =    models.IntegerField(default = 0, blank=True, null=True, verbose_name = "Nombre de décimale")
    designation_sous_unite   =    models.CharField(max_length = 200, null = True, blank = True, verbose_name = "Designation sous unité")
    code_sous_unite          =    models.CharField(max_length = 20, null = True, blank = True, verbose_name = "Code sous unité")
    societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut                   =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', related_name="devises", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now_add = True)
    update_date              =    models.DateTimeField(auto_now = True)
    auteur                   =    models.ForeignKey(Model_Personne, default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name="auteur_devises")

    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = 'Devise'
        verbose_name_plural = 'Devises'

class Model_Taux(models.Model):
    devise_depart            =    models.ForeignKey("Model_Devise", on_delete = models.SET_NULL, related_name="taux_lies", null = True, blank = True, verbose_name = "Devise de départ")
    devise_arrive            =    models.ForeignKey("Model_Devise",on_delete = models.SET_NULL,  related_name="taux_subits", null = True, blank = True, verbose_name = "Devise arrivé")
    montant                  =    models.FloatField(verbose_name = "Montant")
    est_courant              =    models.BooleanField(default = True, verbose_name = "Est taux encours")
    societe                         =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    statut                   =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', related_name="taux", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now_add = True)
    update_date              =    models.DateTimeField(auto_now = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_taux", null = True, blank = True)
    
    
    def __str__(self):
        return "Taux du {} : 1 {} vaut {} {}".format(self.creation_date.strftime("%d/%m/%Y"), self.devise_depart.symbole_devise, self.montant, self.devise_arrive.symbole_devise)

    @property
    def designation(self):
        return "{} {} (1 {})".format(self.montant, self.devise_arrive.symbole_devise, self.devise_depart.symbole_devise)
    
    class Meta:
        verbose_name = 'Taux'
        verbose_name_plural = 'Taux'

class Model_TypeOrganisation(models.Model):
    designation              =    models.CharField(max_length = 50)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="types_organisations", null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_Organisation(models.Model):
    nom                      =    models.CharField(max_length = 150)
    slogan                   =    models.CharField(max_length = 150, null = True, blank = True, default="")
    email                    =    models.CharField(max_length = 150, null = True, blank = True, default="")
    image                    =    models.CharField(max_length = 500, null = True, blank = True, default="")
    icon                     =    models.CharField(max_length = 500, null = True, blank = True, default="")
    image_cover              =    models.CharField(max_length = 500, null = True, blank = True, default="")
    phone                    =    models.CharField(max_length = 50, null = True, blank = True, default="")
    boite_postal             =    models.CharField(max_length = 50, null = True, blank = True, default="")
    fax                      =    models.CharField(max_length = 50, null = True, blank = True, default="")
    numero_fiscal            =    models.CharField(max_length = 50, null = True, blank = True, default="")
    site_web                 =    models.CharField(max_length = 100, null = True, blank = True, default="")
    type_organisation        =    models.ForeignKey(Model_TypeOrganisation, on_delete = models.SET_NULL, related_name = "organisations", null = True, blank = True)
    commune_quartier         =    models.ForeignKey(Model_Place, on_delete = models.SET_NULL, related_name = "organisations", null = True, blank = True)
    adresse                  =    models.CharField(max_length = 100, null = True, blank = True, default="")
    devise                   =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="organisations", null = True, blank = True)
    nom_application          =    models.CharField(max_length = 50, null = True, blank = True, default="")
    est_active               =    models.BooleanField(default = False)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="organisations", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.nom

#Model utilisé pour assurer une seule connexion à un instant T sur un seul compte
class Model_UserSessions(models.Model):
    user = models.ForeignKey(User, related_name='user_of_usersession', on_delete = models.CASCADE)
    session = models.ForeignKey(Session, related_name='session_of_usersession',on_delete=models.SET_NULL, null = True, blank=True)
    session_key = models.CharField(max_length = 100, null = True, blank=True, default = '')
    login_date = models.DateTimeField(blank=True, null=True)
    logout_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default = False)

    def __str__(self):
        return '%s - %s' % (self.user, self.session.session_key)

@receiver(user_logged_in)
def concurrent_logins(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')
    if user is not None and request is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        user_session = Model_UserSessions.objects.filter(session = session, is_active = True)
        if not user_session:
            #print("abbah")
            Model_UserSessions.objects.create(user=user, session=session, session_key=request.session.session_key, is_active = True, login_date = timezone.now())
    if user is not None:
        request.session['LOGIN_COUNT'] = user.user_of_usersession.count()

@receiver(user_logged_out)
def performing_logout(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')
    if user is not None and request is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        user_sessions = Model_UserSessions.objects.filter(session = session, is_active = True)
        if user_sessions:
            for session in user_sessions:
                user_session = Model_UserSessions.objects.get(pk = session.id)
                user_session.is_active = False
                user_session.logout_date = timezone.now()
                user_session.save()

# MODEL WORKFLOW

class Model_Wkf_Workflow(models.Model):
    type_document           =    models.CharField(max_length=30, unique=True)
    content_type            =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    societe                 =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkfs', null = True, blank = True)

    def __str__(self):
        return self.type_document

class Model_Wkf_Etape(models.Model):
    designation             =    models.CharField(max_length=50)
    label                   =    models.CharField(max_length=50, blank=True, null=True)
    workflow                =    models.ForeignKey(Model_Wkf_Workflow, on_delete=models.CASCADE, related_name="etapes_workflows")
    est_initiale            =    models.BooleanField(default=False)
    est_succes              =    models.BooleanField(default=False)
    est_echec               =    models.BooleanField(default = False)
    num_ordre               =    models.IntegerField(blank=True, null=True)
    societe                 =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_etapes', null = True, blank = True)


    def __str__(self):
        return self.workflow.type_document +' / '+ self.designation

    def etat_initial(self):
        if self.est_initiale == True : return "Initiale"
        else : return "Non initiale"

class Model_Wkf_Condition(models.Model):
    designation             =    models.CharField(max_length=50)
    societe                 =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_conditions', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_Wkf_Transition(models.Model):
    etape_source            =    models.ForeignKey(Model_Wkf_Etape, on_delete=models.CASCADE, related_name="transitions_etapes_source")
    etape_destination       =    models.ForeignKey(Model_Wkf_Etape, on_delete=models.CASCADE, related_name="transitions_etapes_destination")
    groupe_permission       =    models.ForeignKey(Model_GroupePermission, on_delete=models.SET_NULL, blank=True, null=True ,related_name="transition_groupe_permission")
    #unite_fonctionnelle     =    models.ForeignKey("Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="unite_fonctionnelle_of_transition")
    condition               =    models.ForeignKey(Model_Wkf_Condition, on_delete=models.SET_NULL, blank=True, null=True , related_name="conditions_transitions")
    url                     =    models.CharField(max_length = 250, blank=True, null=True)
    operateur               =    models.IntegerField(choices = TypeOperateur, default=1) #Dans le cas de plusieurs transitions, ca peut avoir son importance
    traitement              =    models.CharField(max_length=250, blank=True, null=True)
    est_decisive            =    models.BooleanField(default = False)
    est_configurable        =    models.BooleanField(default = False)
    est_delegable           =    models.BooleanField(default=False)
    est_filtrable           =    models.BooleanField(default = False)
    est_generate_doc        =    models.BooleanField(default = False) #Action generer document
    filtre                  =    models.CharField(max_length=50, blank=True, null=True)#Champ Utilisable dans le cas ou la condition est GenerateDoc
    societe                 =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_transitions', null = True, blank = True)


    def __str__(self):
        return self.etape_source.workflow.type_document + ': ' + self.etape_source.designation + ' > ' + self.etape_destination.designation

    def value_operateur(self):
        return dict(TypeOperateur)[int(self.operateur)]

    @property
    def transitions_suivantes(self):
        return Model_Wkf_Transition.objects.filter(etape_source = self.etape_destination)

class Model_Wkf_Stakeholder(models.Model):
    '''Modèle utilisé si et seulement si la transition est configurable ou delegable, Ca permet à l'utilisateur de fixer la suite du traitement'''
    transition              =    models.ForeignKey(Model_Wkf_Transition, on_delete=models.CASCADE, related_name="transitions_stakeholder")
    content_type            =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    document_id             =    models.PositiveIntegerField(blank=True, null=True)
    #condition              =    models.ForeignKey(Model_Wkf_Condition, on_delete=models.SET_NULL, blank=True, null=True) #A utiliser si l'utilisaeur peut mm rédéfinir l'action
    employes                =    models.ManyToManyField("Model_Personne", related_name="destinataires")
    carbon_copies           =    models.ManyToManyField("Model_Personne", related_name="copie_information")
    est_delegation          =    models.BooleanField(default= False)
    comments                =    models.CharField(max_length=500, blank=True, null=True)
    url_detail              =    models.CharField(max_length=100, blank=True, null=True) # Usefull for Notification
    module_source           =    models.CharField(max_length= 100, blank=True, null=True) # Usefull for Notification
    societe                 =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    created_at              =   models.DateTimeField(auto_now_add = True)
    updated_at              =   models.DateTimeField(auto_now = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_stakeholder', null = True, blank = True)

class Model_Wkf_Historique(models.Model):
    employe                 =    models.ForeignKey(Model_Personne,on_delete=models.SET_NULL, related_name="workflow_utilisateurs", blank=True, null=True)
    etape                   =    models.ForeignKey(Model_Wkf_Etape,on_delete=models.SET_NULL, related_name="workflow_etapes",null = True, blank = True)
    timestamp               =    models.DateTimeField(auto_now_add=True)
    content_type            =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    document_id             =    models.PositiveIntegerField(blank=True, null=True)
    content_object          =    GenericForeignKey('content_type', 'document_id')
    notes                   =    models.CharField(max_length=500, blank=True, null=True)
    societe                 =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_historiques', null = True, blank = True)

    def __str__(self):
        return self.etape.designation

class Model_Wkf_Approbation(models.Model):
    designation             =   models.CharField(max_length = 500)
    transition              =   models.ForeignKey(Model_Wkf_Transition, on_delete=models.SET_NULL, blank=True, null=True ,related_name="approbations")
    societe                 =    models.ForeignKey('ModuleConfiguration.Model_Societe', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Société",db_column='company_id')
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_appros', null = True, blank = True)

    def __str__(self):
        return self.designation


#CONVERSATION
class Model_Message(models.Model):
    objet                   =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    corps                   =   models.CharField(max_length = 500, null = True, blank=True, default = '')
    type                    =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    destinataire            =   models.ManyToManyField(Model_Personne)
    expediteur              =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'expediteur_fk_ezk', null = True, blank = True)
    status                  =   models.CharField(max_length = 200, null = True, blank=True, default = '')
    #document                =   models.ForeignKey(Model_Document, on_delete = models.SET_NULL, related_name = 'document_fk_odz', null = True, blank = True)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_message_zam', null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.objet

    @property
    def hisexpediteur(self):
        cont = Model_Personne.objects.get(pk = self.expediteur_id)
        return cont.nom_complet

class Model_Notification(models.Model):
    text                    =   models.CharField(max_length = 500, null = True, blank=True, default = '')
    url_piece_concernee     =   models.CharField(max_length = 300, null = True, blank=True, default = '')
    module_source           =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    #res_model         	    =    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Modèle Ressource")
    #res_id    			    =    models.IntegerField(blank=True, null=True, verbose_name = "Id Ressource")
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_notification_dmj', null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.text

    @property
    def hismessageexpediteur(self):
        #print("allo")
        cont = Model_Message.objects.get(pk = self.auteur_id)
        return cont.hisexpediteur

class Model_Temp_Notification(models.Model):
    user                    =  models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'user_fk_koy', null = True, blank = True)
    notification            =   models.ForeignKey(Model_Notification, on_delete = models.CASCADE, related_name='notif_fk_sk', null = True, blank = True)
    type_action             =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    lien_action             =   models.CharField(max_length = 300, null = True, blank=True, default = '')
    source_identifiant      =   models.IntegerField(null=True,blank=True)
    est_lu                  =   models.BooleanField(default = False)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, related_name="auteur_temp_notification", null = True, blank = True, on_delete=models.SET_NULL)
