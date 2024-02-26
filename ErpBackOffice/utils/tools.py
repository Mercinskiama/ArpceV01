from __future__ import unicode_literals
from enum import Enum

class ModuleAchatSousModule(Enum):
    SM_HOME = 0
    SM_FOURNITURE = 1
    SM_BON_ACHAT = 2
    SM_FOURNISSEUR = 3
    SM_FACTURE = 4
    SM_ARTICLE = 5
    SM_RAPPORT = 6
    SM_CATEGORIE_ARTICLE = 7
    SM_UNITE_MESURE = 8
    SM_CATEGORIE_UNITE_MESURE = 9
    SM_CONDITION_REGLEMENT = 10
    SM_PARAMETRAGE = 11
    #SM_PAIEMENT_FACTURE = 12

class ModuleVenteSousModule(Enum):
    SM_HOME = 0
    SM_COMMANDE = 1
    SM_BON_COMMANDE = 2
    SM_CLIENT = 3
    SM_ARTICLE = 4
    SM_FACTURE = 5
    SM_RAPPORT = 6
    SM_CATEGORIE_CLIENT = 7
    SM_CATEGORIE_ARTICLE = 8
    SM_CIVILITE = 9
    SM_PARAMETRAGE = 10
    SM_PAIEMENT_FACTURE = 11
    SM_LIVRAISON = 12

class ModuleRessourcesHumainesSousModule(Enum):
    SM_HOME = 0
    SM_EMPLOYES = 1
    SM_DEPARTEMENTS = 2
    SM_REQUETES = 3
    SM_PRESENCES = 4
    SM_POSTES = 5
    SM_PARAMETRAGE = 6


class ModuleComptabiliteSousModule(Enum):
    SM_HOME = 0
    SM_COMPTE = 1
    SM_ECRITURE = 2
    SM_PIECE = 3
    SM_RAPPORT_JOURNAL = 4
    SM_RAPPORT_GRAND_LIVRE = 5
    SM_RAPPORT_BALANCE = 6


class ModuleInventaireSousModule(Enum):
    SM_HOME = 0
    SM_DASHBOARD = 1
    SM_TRANSFERT = 2
    SM_ARTICLES = 3
    SM_AJUSTEMENT_STOCK = 4
    SM_MOUVEMENT_STOCK = 5
    SM_ENTREPOT = 6
    SM_EMPLACEMENT = 7
    SM_TYPE_OPERATION = 8

class DataConfig(Enum):
    FCM_API_ACCESS_KEY = "AIzaSyAS6HSifTqrk5WT0Qt2SRhYPW2rZb4gVoM"

class ErpModule(Enum):
    MODULE_ACCUEIL = 0
    MODULE_CONFIGURATION = 99
    MODULE_APPLICATION = 98
    MODULE_ARCHIVAGE = 97
    MODULE_CONVERSATION = 100