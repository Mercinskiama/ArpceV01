from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from datetime import time, timedelta, datetime, date
from django.utils import timezone
import json
from django.db import transaction
from django.db.models import Q
import pandas as pd
import requests
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import time
from requests.auth import HTTPBasicAuth,HTTPDigestAuth
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from ErpBackOffice.utils.auth import auth
import random

#-----------------------------------------------
from ErpBackOffice.utils.separateur import AfficheEntier
#-----------------------------------------------

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ErpBackOffice.utils.generateur import *

def run():
    print("--- Execution script generer menu ---")
    generer_menu("Liste_modeles3")

@transaction.atomic
def generer_menu(file_name):
    print(" ... generer menu ...")
    sid = transaction.savepoint()
    try:
        import_dir = settings.MEDIA_ROOT
        file_dir = 'excel/'
        import_dir = import_dir + '/' + file_dir
        file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
        if default_storage.exists(file_path):
            filename = default_storage.generate_filename(file_path)
            sheet = "Sheet"
            print("Sheet : {} file: {}".format(sheet, filename))
            df = pd.read_excel(io=file_path, sheet_name=sheet, engine='openpyxl')


            for i in df.index:
                print("MODELE: {}".format(df['modele_name'][i]))
                module_id = makeInt(df['module_id'][i])
                modele_id = makeIntId(df['modele_id'][i])
                groupe_menu_id = makeIntId(df['groupe_menu_id'][i])
                groupe_menu_name = makeString(df['groupe_menu_name'][i])
                numero_ordre = makeInt(df['numero_ordre'][i])
                relateds = makeString(df['related_models'][i]) # Ex.: 1,2

                generate_reporting_value = makeString(df['generate_reporting'][i])
                generate_bi_value = makeString(df['generate_bi'][i])
                est_actif_value = makeString(df['est_actif'][i])

                moduleobject = dao_module.toGetModule(module_id)
                
                #Standardisation denomination modele
                
                content_type = ContentType.objects.get(pk = modele_id)
                model_class = content_type.model_class()
                nom_modele_verbose_plural = model_class._meta.verbose_name_plural
                nom_modele = content_type.model.replace("model_","").capitalize()
                nom_pattern = 'module_{0}'.format(unidecode.unidecode(moduleobject.nom_module.lower().replace(" ","_")))

                url_name_create = "{1}_add_{0}".format(nom_modele.lower(), nom_pattern)
                url_name_list = "{1}_list_{0}".format(nom_modele.lower(), nom_pattern)
                url_name_detail = "{1}_detail_{0}".format(nom_modele.lower(), nom_pattern)
                url_name_update = "{1}_update_{0}".format(nom_modele.lower(), nom_pattern)
                url_name_reporting = "{1}_get_generer_{0}".format(nom_modele.lower(), nom_pattern)
                
                nom_sous_module = nom_modele_verbose_plural
                description = f"Menu {nom_modele_verbose_plural}"
                                
                url_vers = url_name_list
                groupe = ""
                icon_menu = ""
                est_dashboard = False
                model_principal_id = modele_id
                relateds = relateds.split(".")
                                
                related_models = []
                for i in range(0, len(relateds)) :
                    related_id = makeInt(relateds[i])
                    element = get_related_models(modele_id, related_id)                
                    if element != None: related_models.append(element)
                    else: related_models.append("")
                
                #On recupère l'utilisateur Admin
                auteur = Model_Personne.objects.get(pk = 7)
                
                est_actif = False
                if est_actif_value == 'Oui' : est_actif = True
                
                generate_reporting = False
                if generate_reporting_value == "Oui" : generate_reporting = True
                
                generate_bi = False
                if generate_bi_value == "Oui" : generate_bi = True
                
                est_model = True               
                generate_dao = True                
                generate_template = True                
                generate_api = True


                if groupe_menu_id in (0, None):
                    groupe_menu = dao_groupe_menu.toGetGroupeByNameOfModule(module_id, groupe_menu_name)
                    if groupe_menu  == None:
                        #On crée le groupe menu
                        groupe_menu = dao_groupemenu.toCreateGroupemenu(groupe_menu_name, "achats.svg", "Groupe Menu {}".format(groupe_menu_name), moduleobject.id, 2)
                        groupe_menu = dao_groupemenu.toSaveGroupemenu(auteur, groupe_menu) 
                        print(f"Groupe Menu {groupe_menu_name} cree") 
                    groupe_menu_id = groupe_menu.id 
                            
                
                sousmodule = dao_sousmodule.toCreateSousmodule(module_id, nom_sous_module, description, groupe, icon_menu, url_vers, numero_ordre, est_model = est_model, est_dashboard = est_dashboard, est_actif = est_actif, model_principal_id = model_principal_id, groupe_menu_id = groupe_menu_id)
                sousmodule = dao_sousmodule.toSaveSousmodule(auteur, sousmodule)
                print("FIN CREATION SOUS MODULE")
                        
                #GENERATION DAO
                if est_model and generate_dao :
                    genDAOofModelContentType(model_principal_id, moduleobject.id)
                    print("FIN GENERATION DAO")
                
                #GENERATION TEMPLATE
                if est_model and generate_template:
                    nom_modele = genTemplateOfContentType(model_principal_id, moduleobject.id, related_models)
                    print("FIN GENERATION TEMPLATE")
                    permission = dao_permission.toCreatePermission(sousmodule.id, f"SUPPRIMER_{nom_modele.upper()}", dao_permission.toGetLatestNumeroOrdre() + 1)
                    permission = dao_permission.toSavePermission(auteur, permission)
                    print("FIN CREATION PERMISSION SUPPRIMER")
                
                #GENERATION REPORTING
                if est_model and generate_reporting:
                    url_name_reporting = genReportingOfContentType(model_principal_id, moduleobject.id) 
                    print("FIN GENERATION REPORTING")
                    groupe_menu_reporting = dao_groupe_menu.toGetGroupeRapportOfModule(module_id) 
                    if groupe_menu_reporting == None: 
                        #On crée le groupe menu reporting
                        designation = "Rapports"
                        groupe_menu_reporting = dao_groupemenu.toCreateGroupemenu(designation,"file.svg", "Groupe Menu {}".format(designation), moduleobject.id, 8)
                        groupe_menu_reporting = dao_groupemenu.toSaveGroupemenu(auteur, groupe_menu_reporting) 
                        print("Groupe Menu 2 cree")
                    sousmodule_reporting = dao_sousmodule.toCreateSousmodule(module_id, "Rapport {}".format(nom_sous_module), "", "", "", url_name_reporting, numero_ordre, est_model = est_model, est_dashboard = False, est_actif = est_actif, model_principal_id = model_principal_id, groupe_menu_id = groupe_menu_reporting.id)
                    sousmodule_reporting = dao_sousmodule.toSaveSousmodule(auteur, sousmodule_reporting)
                    print("FIN CREATION SOUS MODULE")

                #GENERATION BI
                if est_model and generate_bi:
                    url_name_bi = genBIOfContentType(model_principal_id, moduleobject.id) 
                    print("FIN GENERATION BI")
                    groupe_menu_bi = dao_groupe_menu.toGetGroupeAnalyseOfModule(module_id) 
                    if groupe_menu_bi == None: 
                        #On crée le groupe menu Analyses
                        designation = "Analyses"
                        groupe_menu_bi = dao_groupemenu.toCreateGroupemenu(designation,"line-chart-for-business.svg", "Groupe Menu {}".format(designation), moduleobject.id, 9)
                        groupe_menu_bi = dao_groupemenu.toSaveGroupemenu(auteur, groupe_menu_bi) 
                        print("Groupe Menu 3 cree")
                    numero_ordre = int(numero_ordre) + 60
                    sousmodule_bi = dao_sousmodule.toCreateSousmodule(module_id, "Analyse {}".format(nom_sous_module), "", "", "", url_name_bi, numero_ordre, est_model = est_model, est_dashboard = False, est_actif = est_actif, model_principal_id = model_principal_id, groupe_menu_id = groupe_menu_bi.id)
                    sousmodule_bi = dao_sousmodule.toSaveSousmodule(auteur, sousmodule_bi)
                    print("FIN CREATION SOUS MODULE")
                            
                #GENERATION API
                if est_model and generate_api:
                    genAPIOfContentType(model_principal_id, moduleobject.id)            
                    print("FIN GENERATION API")
                

                #GESTION PERMISSION ET ACTION
                list_permission = []
                list_permission.append(f"LISTER_{nom_modele}")
                list_permission.append(f"CREER_{nom_modele}")
                list_permission.append(f"MODIFIER_{nom_modele}")
                list_permission.append(f"ANALYSER_{nom_modele}")
                
                list_action = []
                list_action.append(f"{url_name_list},{url_name_detail}")
                list_action.append(url_name_create)
                list_action.append(url_name_update)
                list_action.append(url_name_reporting)

                for i in range(0, len(list_permission)) :
                    sous_module_id = sousmodule.id
                    if est_model and generate_reporting and list_permission[i].startswith("ANALYSER_"):
                        sous_module_id = sousmodule_reporting.id
                    permission = dao_permission.toCreatePermission(sous_module_id, list_permission[i], dao_permission.toGetLatestNumeroOrdre() + 1)
                    permission = dao_permission.toSavePermission(auteur, permission)
                    action_string = list_action[i]
                    list_action_string = action_string.split(",")
                    for uneaction in list_action_string:
                        action = dao_actionutilisateur.toCreateActionutilisateur(uneaction,"", "", permission.id)
                        action = dao_actionutilisateur.toSaveActionutilisateur(auteur, action)
                print("FIN GESTION PERMISSION ET ACTION")

                print("Menu généré")
            transaction.savepoint_commit(sid)
        else: print("Fichier Excel non trouvé")
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print("ERREUR generer menu")
        print(e)
        
def get_related_models(model_id, related_id):
    try:             
        model = ContentType.objects.get(pk = model_id)
        nom_modele_class = model.model_class().__name__
        
        models = ContentType.objects.all()

        for item in models:
            model_class = item.model_class()
            if model_class != None:
                for field in model_class._meta.get_fields(include_parents=False, include_hidden=False):
                    if field.related_model != None and field.__class__.__name__ not in  ("ManyToManyField", "ManyToOneRel", "ManyToManyRel") and field.related_model.__name__ == nom_modele_class:
                        if related_id == item.id:
                            return f"{item.id},{field.name},{field.__class__.__name__}"            
        return None
    except Exception as e:
        return None
