from __future__ import unicode_literals
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
from django.urls import resolve
import datetime
import json

from ErpBackOffice.dao.dao_module import dao_module

from ErpBackOffice.utils.identite import identite
from ErpBackOffice.dao.dao_sous_module import dao_sous_module
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
from ErpBackOffice.dao.dao_groupe_menu import dao_groupe_menu
from ErpBackOffice.dao.dao_permission import dao_permission
from ErpBackOffice.dao.dao_operationnalisation_module import dao_operationnalisation_module
from ErpBackOffice.utils.utils import utils
from ErpBackOffice.models import Model_Permission, Model_ActionUtilisateur, Model_Regle
from django.db.models import Q
#POUR LOGGING
import logging, inspect, traceback
monLog = logging.getLogger('logger')
from ErpBackOffice.utils.utils import utils

class auth(object):

    @staticmethod
    def toPostValidityDate(module_id, date):
        #Test if a module Controle de Gestion exist and it is activate!
        if dao_module.toTestModuleInstalledByCode("CTRL"):        
            return dao_operationnalisation_module.toCheckValidity(module_id, date)
        else:
            return True

    @staticmethod
    def toReturnFailed(request, exception = "", traceback = "", redirect = None, msg = "Une erreur est survenue pendant l'exécution"):
        current_func = resolve(request.path_info).func
        module = current_func.__module__.split(".")[0]
        function = current_func.__name__
        monLog.error("{} :: {} :: ERREUR EFFECTUEE DANS LA FONCTION {} :: {} :: {}".format(identite.utilisateur(request), module, function.upper(), exception, traceback))
        monLog.debug("Error")
        print("ERREUR FONCTION {}() : {}".format(function, exception))
        if traceback != "":
            detail_error={}
            detail_error['auteur'] = identite.utilisateur(request).nom_complet
            detail_error['modele'] = f"Module: {module} || Fonction: {function}()"
            detail_error['erreur'] = f"\nException: {exception}\nTraceback: {traceback}"
            utils.write_log_in_database(detail_error)
        messages.add_message(request, messages.ERROR, msg)
        if redirect == None: redirect = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(redirect)
    
    @staticmethod
    def toReturnApiFailed(request, exception = "", traceback = "", msg = "Une erreur est survenue pendant l'exécution"):
        print(f'traceback: {traceback}')
        current_func = resolve(request.path_info).func
        module = current_func.__module__.split(".")[0]
        function = current_func.__name__
        monLog.error("{} :: {} :: ERREUR EFFECTUEE DANS LA FONCTION API {} :: {} :: {}".format("USER API", module, function.upper(), exception, traceback))
        monLog.debug("Error")
        print("ERREUR FONCTION API {}() : {}".format(function, exception))
        if traceback != "":
            detail_error={}
            detail_error['auteur'] = "USER API"
            detail_error['modele'] = f"Module: {module} || Fonction: {function}()"
            detail_error['erreur'] = f"Exception: {exception}\nTraceback: {traceback}"
            utils.write_log_in_database(detail_error)
        context = { "error" : True, "message" : msg}
        return JsonResponse(context, safe=False)

    @staticmethod
    def toGetAuth(requete):
        is_connect = identite.est_connecte(requete)
        if is_connect == False: return None, None, HttpResponseRedirect(reverse("backoffice_connexion"))
        #modules = []
        modules = dao_module.toListModulesInstalles()

        utilisateur = identite.utilisateur(requete)

        if utilisateur.user.username != "admin":
            #role = dao_role.toGetRoleDeLaPersonne(utilisateur.id)
            roles = dao_groupe_permission.toListGroupePermissionDeLaPersonne(utilisateur.id)
            #print(roles)
            modules = []
            if roles == []: return None, None, HttpResponseRedirect(reverse("backoffice_erreur_role"))
            else :
                for role in roles:
                    list_modules = dao_module.toListModulesByPermission(role)
                    for module in list_modules:
                        modules.append(module)
        modules = set(modules)
        modules = list(modules)

        return modules,utilisateur,None


    @staticmethod
    def toCheckAdmin(module_name,utilisateur):
        try: 
            is_checked = False
            module = dao_module.toGetModuleByName(module_name)
            permission = dao_permission.toGetPermissionOfAdmin(module.id)
            is_checked = auth.toCheckUserPerm(utilisateur, permission)
            return is_checked
        except Exception as e:
            print("ERREUR toCheckAdmin()")
            print(e)
            return  False
        
    @staticmethod
    def toCheckUserPerm(utilisateur, permission):
        try:
            if utilisateur.user.username == "admin": return True
            groupe_permissions = dao_groupe_permission.toListGroupePermissionDeLaPersonne(utilisateur.id)
            for groupe_permission in groupe_permissions:
                if dao_permission.toCheckPermission(groupe_permission.id, permission.id):
                    return True
            return False
        except Exception as e:
            print("ERREUR toCheckUserPerm()")
            print(e)
            return False

    @staticmethod
    def toGetAuthPerm(requete, same_perm_with = None):
        try:
            url_name = same_perm_with
            if same_perm_with == None: url_name = resolve(requete.path_info).url_name
            sous_modules = []
            modules = []
            permission = None
            groupe_permissions = []
            utilisateur = None

            actions = {
                'can_create' : False,
                'can_update' : False,
                'can_read' : False,
                'can_delete' : False
            }
            #print(f"actions 1: {actions}")

            is_connect = identite.est_connecte(requete)
            if is_connect == False: return modules, sous_modules, utilisateur, groupe_permissions, permission, actions, HttpResponseRedirect(reverse("backoffice_connexion"))
            
            utilisateur = identite.utilisateur(requete)
            groupe_permissions = dao_groupe_permission.toListGroupePermissionDeLaPersonne(utilisateur.id)
            action = Model_ActionUtilisateur.objects.filter(nom_action = url_name).first()
            permission = action.permission
            
            is_permissioned = False

            if utilisateur.user.username != "admin":
                permissions = dao_permission.toListPermissionsOfSousModule(permission.sous_module_id)
                print(f"permissions: {permissions}")
                for groupe_permission in groupe_permissions:
                    sous_modules.extend(dao_sous_module.toListSousModulesByPermission(permission, groupe_permission))
                    modules.extend(dao_module.toListModulesByPermission(groupe_permission))
                    
                    #On check si l'utilisateur a droit sur le lien
                    if dao_permission.toCheckPermission(groupe_permission.id, permission.id) == True: is_permissioned = True
                    
                    #On check également si l'utilisateur a droit sur les autres permissions CRUD du sous-modules
                    create_permission = permissions.filter(designation__startswith='CREER_').first()
                    if create_permission != None:
                        if dao_permission.toCheckPermission(groupe_permission.id, create_permission.id) == True: actions['can_create'] = True
                    update_permission = permissions.filter(designation__startswith='MODIFIER_').first()
                    if update_permission != None:
                        if dao_permission.toCheckPermission(groupe_permission.id, update_permission.id) == True: actions['can_update'] = True
                    read_permission = permissions.filter(designation__startswith='LISTER_').first()
                    if read_permission != None:
                        if dao_permission.toCheckPermission(groupe_permission.id, read_permission.id) == True: actions['can_read'] = True
                    delete_permission = permissions.filter(designation__startswith='SUPPRIMER_').first()
                    if delete_permission != None:
                        if dao_permission.toCheckPermission(groupe_permission.id, delete_permission.id) == True: actions['can_delete'] = True
                if not is_permissioned: 
                    return  modules, sous_modules, utilisateur, groupe_permissions, permission, actions, HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
                
                #print(f"actions 2: {actions}")
            else:
                actions = {'can_create' : True,'can_update' : True,'can_read' : True,'can_delete' : True}
                modules = dao_module.toListModulesInstalles()
                sous_modules = dao_sous_module.toListSousModulesByOfModuleByPermissionForAdmin(permission)

            modules = list(set(modules))
            modules = sorted(modules, key=lambda module: module.numero_ordre, reverse=False) 

            sous_modules = utils.remove_duplicate_in_list(sous_modules)
            sous_modules = sorted(sous_modules, key=lambda sous_module:  0 if sous_module.groupe_menu is None else sous_module.groupe_menu.numero_ordre, reverse=False)
                
            return  modules, sous_modules, utilisateur, groupe_permissions, permission, actions, None
        except Exception as e:
            print("ERREUR toGetAuthPerm()")
            print(e)
            return  [], [], None, [], None, {}, HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
        
    @staticmethod
    def toGetAuthentification(permission_number, requete, function_name=""):
        try:
            current_func = resolve(requete.path_info).func
            #print("kwargs : {}".format(resolve(requete.path_info).kwargs))
            #print("func : {}".format(current_func))
            #print("url_name : {}".format(resolve(requete.path_info).url_name))
            #print("current_func : {}".format(current_func.__name__))
            module_name = current_func.__module__.split(".")[0]
            module = dao_module.toGetModuleByAppName(module_name)
            auth.toCreateActionIfNotExist(permission_number, function_name, module.id)
            is_connect = identite.est_connecte(requete)
            if is_connect == False: return None, None, None, None, HttpResponseRedirect(reverse("backoffice_connexion"))
            utilisateur = identite.utilisateur(requete)
            groupe_permissions = dao_groupe_permission.toListGroupePermissionDeLaPersonne(utilisateur.id)
            #les cas avec les mêmes noms de fonction dans des modules différents sont gerés maintenant
            action = Model_ActionUtilisateur.objects.filter(nom_action = function_name, permission__sous_module__module_id = module.id).first() 
            #action = Model_ActionUtilisateur.objects.filter(nom_action = function_name).first()
            permission = action.permission
            sous_modules = []
            modules = []
            is_permissioned = False

            #if function_name == "": utilisateur.nom_complet = "SYSTEM"

            if utilisateur.user.username != "admin":
                for groupe_permission in groupe_permissions:
                    sous_modules.extend(dao_sous_module.toListSousModulesByPermission(permission, groupe_permission))
                    modules.extend(dao_module.toListModulesByPermission(groupe_permission))

                    if dao_permission.toCheckPermission(groupe_permission.id, permission.id) == True:
                        is_permissioned = True
                if not is_permissioned:
                    return  None, None, None, groupe_permissions, HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
            else:
                modules = dao_module.toListModulesInstalles()
                sous_modules = dao_sous_module.toListSousModulesByOfModuleByPermissionForAdmin(permission)

            modules = list(set(modules))
            modules = sorted(modules, key=lambda module: module.numero_ordre, reverse=False) 

            sous_modules = utils.remove_duplicate_in_list(sous_modules)
            sous_modules = sorted(sous_modules, key=lambda sous_module: 0 if sous_module.groupe_menu is None else sous_module.groupe_menu.numero_ordre, reverse=False)  
            return  modules,sous_modules, utilisateur, groupe_permissions, None
        except Exception as e:
            print("ERREUR toGetDashboardAuthentification()")
            print(e)
            return  None, None, None, [], HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))

    @staticmethod
    def toGetDashboardAuthentification(module_id, requete):
        try:
            is_connect = identite.est_connecte(requete)
            if is_connect == False: return None, None, None, None, HttpResponseRedirect(reverse("backoffice_connexion"))

            utilisateur = identite.utilisateur(requete)
            groupe_permissions = dao_groupe_permission.toListGroupePermissionDeLaPersonne(utilisateur.id)
            if module_id != 0: #erpbackoffice
                module = dao_module.toGetModule(module_id)
            sous_modules = []
            modules = []
            is_permissioned = False

            
            if utilisateur.user.username != "admin":
                for groupe_permission in groupe_permissions:
                    modules.extend(dao_module.toListModulesByPermission(groupe_permission))
                    if module_id != 0:
                        sous_modules.extend(dao_sous_module.toListSousModulesByGroupePermission(module, groupe_permission))
                        if module in modules:
                            is_permissioned = True
                if not is_permissioned:
                    if module_id != 0:      
                        return  None, None, None, groupe_permissions, HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
                    
            else:
                modules = dao_module.toListModulesInstalles()
                groupe_permission = dao_groupe_permission.toListGroupePermissions()
                if module_id != 0:
                    module = dao_module.toGetModule(module_id)
                    sous_modules = dao_sous_module.toListSousModulesByGroupePermissionForAdmin(module)
                    
            modules = list(set(modules))
            modules = sorted(modules, key=lambda module: module.numero_ordre, reverse=False) 
            
            sous_modules = utils.remove_duplicate_in_list(sous_modules)
            sous_modules = sorted(sous_modules, key=lambda sous_module: 0 if sous_module.groupe_menu is None else sous_module.groupe_menu.numero_ordre, reverse=False)             
            return  modules,sous_modules, utilisateur, groupe_permissions, None
        except Exception as e:
            #print("ERREUR toGetDashboardAuthentification()")
            #print(e)
            return  None, None, None, [], HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
    
    @staticmethod
    def toCreateActionIfNotExist(permission_number, function_name, module_id):
        try:
            if permission_number == 0: return False
            
            action = None
            permission = dao_permission.toGetPermissionByNumber(permission_number)
            if permission != None: action = Model_ActionUtilisateur.objects.filter(nom_action = function_name, permission_id = permission.id, permission__sous_module__module_id = module_id).first()

            if action == None and permission != None:
                action = Model_ActionUtilisateur()
                action.nom_action = function_name
                action.permission_id = permission.id
                action.save()
                #print("Nouvelle action creee")
            return True
        except Exception as e:
            return False
        
    @staticmethod
    def toListWithRules(results, permission, groupe_permissions, auteur):
        try:
            regle = auth.toGetRegleByPermissionAndRole(permission, groupe_permissions)
            if regle is None: return results
            if regle.lignes.count() == 0: return results
            expression = "results."

            for ligne in regle.lignes.all():
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
            data = eval(expression)
            return data
        except Exception as e:
            print("erreur toListWithRules() {}".format(e))
            return []
        
    @staticmethod
    def toGetWithRules(results, permission, groupe_permissions, auteur):
        try:
            regle = auth.toGetRegleByPermissionAndRole(permission, groupe_permissions)
            if regle is None: return results.first()
            if regle.lignes.count() == 0: return results.first()
            expression = "results."

            for ligne in regle.lignes.all():
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

            expression = "{}.first()".format(expression)            
            #print("expression {}".format(expression))
            object = eval(expression)
            return object
        except Exception as e:
            print("erreur toGetWithRules() {}".format(e))
            return None

        
    @staticmethod
    def toGetRegleByPermissionAndRole(permission, groupe_permissions):
        try:
            for groupe_permission in groupe_permissions:
                regle = Model_Regle.objects.filter(groupe_permission_id = groupe_permission.id, permissions__numero = permission.numero).first()
                if regle:
                    return regle
            return None
        except Exception as e:
            #print("erreur on regl", e)
            return None