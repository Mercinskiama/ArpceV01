# -*- coding: utf-8 -*-
import os
import codecs
from ErpBackOffice.utils.generateur import *
from django.db import transaction

#python manage.py runscript test 
def run():
    print("Execution script ...")
    
    # VARIABLES A MODIFIER POUR GENERER
    #=================================

    model_contenttype_id = 58
    model_name = "Model_Actif"
    module_id = 9
    numero_ordre = 6
    groupe_menu_id = 59
    
    relateds = []    
    #C'est Content Type ID du modèle à lier. 
    #Ex.: Pour Model_Bon, ça peut être le Contenttyppe ID de Model_Ligne_bon qu'on peut ajouter dans le formulaire du Bon
    #related_id = "100"

    #C'est Le nom du champs du modèle à lier. 
    #Ex.: Pour le lien Model_Bon - Model_Ligne_bon, ça sera le nom du champs ForeignKey du Bon qui se retrouve sur la lien 
    #field_name = "billetterie" 

    #C'est le type de champ relationel. 
    #Ex.: ForeignKey ou ManyToManyRel  
    #field_type = "ForeignKey"
        
    #relateds.append(f"{related_id},{field_name},{field_type}")
        
    # FIN VARIABLES A MODIFIER POUR GENERER
    #=====================================
    
    #Pour tester la generation des fichiers python seulement
    #generatePy()

    #Pour tester la generation des fichiers html seulement    
    #generateHtml()
    
    #Pour tester la generation des fichiers CSS
    #generateCss()
    
    #Pour generer les fichier DAO dans un module spécifique
    # genDAOofModelContentType(model_contenttype_id, module_id)
    # print("FIN GENERATION DAO")

    #Pour generer les fichier CRUD du template
    # The code appears to be a Python function definition named `genTemplateOfContentType` that takes
    # three parameters: `model_contenttype_id`, `module_id`, and `relateds`. The function body seems
    # to be incomplete as it only contains a comment `p` and `
    # genTemplateOfContentType(model_contenttype_id, module_id, relateds)
    # print("FIN GENERATION TEMPLATE CRUD")
        
    #Pour generer les fichiers du reporting
    # genReportingOfContentType(model_contenttype_id, module_id)
    # print("FIN GENERATION TEMPLATE REPORTING")

    #Pour generer les fichiers du BI    
    # genBIOfContentType(model_contenttype_id, module_id) 
    # print("FIN GENERATION BI")
    
    #Pour generer les fichiers de l'API
    # genAPIOfContentType(model_contenttype_id, module_id)
    # print("FIN GENERATION API CRUD")
    
    #Pour generer les fichier python seulement    
    #url_vers = getUrlVersOfRelatedModel(model_name)
    #print("url_vers: {}".format(url_vers))

    #Pour generer les fichier python seulement
    #nom_pattern = getUrlOfRelatedModel(model_name)
    #print("nom_pattern: {}".format(nom_pattern))
    
    generate_menu_of_model_all(model_contenttype_id, module_id, numero_ordre, groupe_menu_id)

@transaction.atomic
def generate_menu_of_model_all(model_contenttype_id, module_id, numero_ordre = 1, groupe_menu_id = None, related_models = []):
    sid = transaction.savepoint()
    try:   
        module_id = int(module_id)
        moduleobject = dao_module.toGetModule(module_id)
        
        content_type = ContentType.objects.get(pk = model_contenttype_id)
        model_class = content_type.model_class()
        nom_modele_verbose_plural = model_class._meta.verbose_name_plural
        
        #Standardisation denomination modele
        nom_modele = content_type.model.replace("model_","").capitalize()
        nom_pattern = 'module_{0}'.format(unidecode.unidecode(moduleobject.nom_module.lower().replace(" ","_")))

        url_name_create = "{1}_add_{0}".format(nom_modele.lower(), nom_pattern)
        url_name_list = "{1}_list_{0}".format(nom_modele.lower(), nom_pattern)
        url_name_detail = "{1}_detail_{0}".format(nom_modele.lower(), nom_pattern)
        url_name_update = "{1}_update_{0}".format(nom_modele.lower(), nom_pattern)
        url_name_reporting = "{1}_get_generer_{0}".format(nom_modele.lower(), nom_pattern)
        
        nom_sous_module = nom_modele_verbose_plural
        description = f"Menu {nom_modele_verbose_plural}"
        groupe = ""
        numero_ordre = numero_ordre
        icon_menu = ""
        est_dashboard = False
        url_vers = url_name_list
        model_principal_id = model_contenttype_id
        groupe_menu_id = groupe_menu_id
        related_models  = related_models

        #On recupère l'utilisateur Admin
        auteur = Model_Personne()
        user = User.objects.get(id=1)
        auteur.user = user
        auteur.nom_complet = "SYSTEM"
        auteur.id = None

        #ACTIVER OU DESACTIVER LES OPTIONS ICI        
        est_actif = True        
        est_model = True        
        generate_dao = True        
        generate_template = True        
        generate_api = True        
        generate_reporting = False        
        generate_bi = True


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
            if groupe_menu_reporting == None: groupe_menu_id = None
            else: groupe_menu_id = groupe_menu_reporting.id
            numero_ordre = int(numero_ordre) + 20
            sousmodule_reporting = dao_sousmodule.toCreateSousmodule(module_id, "Rapport {}".format(nom_sous_module), "", "", "", url_name_reporting, numero_ordre, est_model = est_model, est_dashboard = False, est_actif = est_actif, model_principal_id = model_principal_id, groupe_menu_id = groupe_menu_id)
            sousmodule_reporting = dao_sousmodule.toSaveSousmodule(auteur, sousmodule_reporting)
            print("FIN CREATION SOUS MODULE")

        #GENERATION BI
        if est_model and generate_bi:
            url_name_bi = genBIOfContentType(model_principal_id, moduleobject.id) 
            print("FIN GENERATION BI")
            groupe_menu_bi = dao_groupe_menu.toGetGroupeAnalyseOfModule(module_id) 
            if groupe_menu_bi == None: groupe_menu_id = None
            else: groupe_menu_id = groupe_menu_bi.id
            numero_ordre = int(numero_ordre) + 30
            sousmodule_bi = dao_sousmodule.toCreateSousmodule(module_id, "Analyse {}".format(nom_sous_module), "", "", "", url_name_bi, numero_ordre, est_model = est_model, est_dashboard = False, est_actif = est_actif, model_principal_id = model_principal_id, groupe_menu_id = groupe_menu_id)
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
                
        transaction.savepoint_commit(sid)
        print("Operation effectuée avec succès!")
    except Exception as e:
        print('Erreur lors de l enregistrement')
        print(e)

   
def generatePy():
    print("generatePy() Run ...")
    path = os.path.abspath(os.path.curdir)
    path = path + "\\test.py"
    fichier = codecs.open(path,"w", encoding='utf-8')
    texte_a_ajouter_views_py_dossier_application = '# -*- coding: utf-8 -*-\nfrom __future__ import unicode_literals\nfrom django.shortcuts import render, redirect\nfrom django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse\nfrom django.template.response import SimpleTemplateResponse, TemplateResponse\nfrom django.contrib.auth import authenticate, login, logout\nfrom django.contrib.auth.models import User, Group\nfrom django.template import loader\nfrom django.views import generic\nfrom django.views.generic.edit import CreateView, UpdateView, DeleteView\nfrom django.urls import reverse_lazy, reverse\nfrom django.contrib import messages\nfrom django.utils import timezone\nfrom django.core import serializers\nfrom random import randint\nfrom django.core.mail import send_mail\nfrom django.conf import settings\nfrom django.core.files.storage import FileSystemStorage\nfrom django.core.files.base import ContentFile\nfrom django.core.files.storage import default_storage\nfrom ErpBackOffice.utils.identite import identite\nfrom ErpBackOffice.utils.tools import ErpModule\nimport datetime, calendar\nimport json\nimport pandas as pd\nfrom rest_framework.decorators import api_view\nimport base64, uuid\nfrom locale import atof, setlocale, LC_NUMERIC\nimport numpy as np\nfrom dateutil.relativedelta import relativedelta\nfrom ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId\nfrom django.db import transaction\nfrom ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation\nfrom ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow\nfrom ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape\nfrom ErpBackOffice.dao.dao_wkf_historique import dao_wkf_historique\nfrom ErpBackOffice.dao.dao_document import dao_document\nfrom ErpBackOffice import models\nfrom ErpBackOffice.dao.dao_model import dao_model\nfrom ErpBackOffice.dao.dao_personne import dao_personne\nfrom ErpBackOffice.dao.dao_place import dao_place\nfrom ErpBackOffice.dao.dao_compte import dao_compte\nfrom ErpBackOffice.dao.dao_module import dao_module\nfrom ErpBackOffice.dao.dao_devise import dao_devise\nfrom ModuleConversation.dao.dao_notification import dao_notification\nfrom ErpBackOffice.utils.pagination import pagination\nfrom ErpBackOffice.utils.auth import auth\nfrom ErpBackOffice.utils.wkf_task import wkf_task\nfrom ErpBackOffice.utils.endpoint import endpoint\n\n\n#LOGGING\nimport logging, inspect, unidecode\nmonLog = logging.getLogger("logger")\nmodule= "{2}"\nvar_module_id = {3}\n\n\ndef get_index(request):\n\ttry:\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(var_module_id, request)\n\t\tif response != None:\n\t\t\treturn response\n\n\t\tcontext = {{\n\t\t\t"title" : "Tableau de Bord",\n\t\t\t"utilisateur" : utilisateur,\n\t\t\t"sous_modules":sous_modules,\n\t\t\t"modules" : modules,\n\t\t\t"module" : ErpModule.{1}\n\t\t}}\n\n\t\ttemplate = loader.get_template("ErpProject/{2}/index.html")\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)'.format("","MODULE_TEST","ModuleTest",1)

    fichier.write(texte_a_ajouter_views_py_dossier_application)
    fichier.close()

def generatePy():
    print("generatePy() Run ...")
    path = os.path.abspath(os.path.curdir)
    path = path + "\\test.py"
    fichier = codecs.open(path,"w", encoding='utf-8')
    texte_a_ajouter_views_py_dossier_application = '# -*- coding: utf-8 -*-\nfrom __future__ import unicode_literals\nfrom django.shortcuts import render, redirect\nfrom django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse\nfrom django.template.response import SimpleTemplateResponse, TemplateResponse\nfrom django.contrib.auth import authenticate, login, logout\nfrom django.contrib.auth.models import User, Group\nfrom django.template import loader\nfrom django.views import generic\nfrom django.views.generic.edit import CreateView, UpdateView, DeleteView\nfrom django.urls import reverse_lazy, reverse\nfrom django.contrib import messages\nfrom django.utils import timezone\nfrom django.core import serializers\nfrom random import randint\nfrom django.core.mail import send_mail\nfrom django.conf import settings\nfrom django.core.files.storage import FileSystemStorage\nfrom django.core.files.base import ContentFile\nfrom django.core.files.storage import default_storage\nfrom ErpBackOffice.utils.identite import identite\nfrom ErpBackOffice.utils.tools import ErpModule\nimport datetime, calendar\nimport json\nimport pandas as pd\nfrom rest_framework.decorators import api_view\nimport base64, uuid\nfrom locale import atof, setlocale, LC_NUMERIC\nimport numpy as np\nfrom dateutil.relativedelta import relativedelta\nfrom ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId\nfrom django.db import transaction\nfrom ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation\nfrom ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow\nfrom ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape\nfrom ErpBackOffice.dao.dao_wkf_historique import dao_wkf_historique\nfrom ErpBackOffice.dao.dao_document import dao_document\nfrom ErpBackOffice import models\nfrom ErpBackOffice.dao.dao_model import dao_model\nfrom ErpBackOffice.dao.dao_personne import dao_personne\nfrom ErpBackOffice.dao.dao_place import dao_place\nfrom ErpBackOffice.dao.dao_compte import dao_compte\nfrom ErpBackOffice.dao.dao_module import dao_module\nfrom ErpBackOffice.dao.dao_devise import dao_devise\nfrom ModuleConversation.dao.dao_notification import dao_notification\nfrom ErpBackOffice.utils.pagination import pagination\nfrom ErpBackOffice.utils.auth import auth\nfrom ErpBackOffice.utils.wkf_task import wkf_task\nfrom ErpBackOffice.utils.endpoint import endpoint\n\n\n#LOGGING\nimport logging, inspect, unidecode\nmonLog = logging.getLogger("logger")\nmodule= "{2}"\nvar_module_id = {3}\n\n\ndef get_index(request):\n\ttry:\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(var_module_id, request)\n\t\tif response != None:\n\t\t\treturn response\n\n\t\tcontext = {{\n\t\t\t"title" : "Tableau de Bord",\n\t\t\t"utilisateur" : utilisateur,\n\t\t\t"sous_modules":sous_modules,\n\t\t\t"modules" : modules,\n\t\t\t"module" : ErpModule.{1}\n\t\t}}\n\n\t\ttemplate = loader.get_template("ErpProject/{2}/index.html")\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)'.format("","MODULE_TEST","ModuleTest",1)

    fichier.write(texte_a_ajouter_views_py_dossier_application)
    fichier.close()
    
def generateHtml():
    print("generateHtml() Run ...")
    path = os.path.abspath(os.path.curdir)
    path = path + "\\test.html"
    fichier = codecs.open(path,"w", encoding='utf-8')
    #texte_a_tester = genLayoutHtmlOfModule()
    #texte_a_tester = genDashBoardTemplate1("ModuleTest")
    texte_a_tester = genDashBoardTemplate2("ModuleTest")
    fichier.write(texte_a_tester)
    fichier.close()
    
def generateCss():
    print("generateCss() Run ...")
    path = os.path.abspath(os.path.curdir)
    path = path + "\\test.css"
    fichier = codecs.open(path,"w", encoding='utf-8')
    #texte_a_tester = genCssVertTemplate("achat")
    texte_a_tester = genCssOrangeTemplate("vente")
    #texte_a_tester = genCssPourpreTemplate("achat")
    #texte_a_tester = genCssBleuCielTemplate("achat")
    #texte_a_tester = genCssBleuTemplate("vente")
    #texte_a_tester = genCssMagentaTemplate("achat")

    fichier.write(texte_a_tester)
    fichier.close()