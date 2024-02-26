from __future__ import unicode_literals

from ErpBackOffice.models import Model_SousModule, Model_GroupePermission

class dao_sous_module(object):
    id = 0
    module_id = 0
    nom_sous_module = ""
    description = ""
    groupe = ""
    url_vers = ""
    numero_ordre = 1
    est_model = False
    model_principal_id = None
    groupe_menu_id = None
    permissions = []
    est_dashboard = False
    icon_menu = ""

    @staticmethod
    def toListSousModulesOfModule(module_id):
        try:
            sous_modules = Model_SousModule.objects.filter(module_id = module_id).order_by('est_dashboard').order_by('groupe_menu__numero_ordre').order_by('numero_ordre').distinct()
            sous_modules = sorted(sous_modules, key=lambda sous_module: 0 if sous_module.groupe_menu is None else sous_module.groupe_menu.id, reverse=False)  
            return sous_modules
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
        
    @staticmethod
    def toListSousModulesOf(module_id):
        try:
            sous_modules = Model_SousModule.objects.filter(est_actif = True, module_id = module_id).order_by("numero_ordre")
            return sous_modules
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
    
    @staticmethod
    def toListSousModule():
        return Model_SousModule.objects.filter(est_actif = True).order_by('est_dashboard').order_by('groupe_menu__numero_ordre').order_by('numero_ordre').distinct()


    @staticmethod
    def toListSousModulesByPermission(permission, groupe_permission):
        try:
            list = []

            module = permission.sous_module.module
            sous_modules_id = Model_GroupePermission.objects.filter(permissions__sous_module__est_actif = True, permissions__sous_module__module_id = module.id, pk=groupe_permission.id).order_by('permissions__sous_module__est_dashboard').order_by('permissions__sous_module__groupe_menu__numero_ordre').order_by('permissions__sous_module__numero_ordre').values('permissions__sous_module_id').distinct()
            for item in sous_modules_id:
                sous_module_id = item['permissions__sous_module_id']
                sous_module = Model_SousModule.objects.get(pk = sous_module_id)
                list.append(sous_module)

            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListSousModulesByOfModuleByPermission(permission):
        try:
            list = []

            module = permission.sous_module.module
            sous_modules_id = Model_GroupePermission.objects.filter(permissions__sous_module__est_actif = True, permissions__sous_module__module_id = module.id).order_by('permissions__sous_module__est_dashboard').order_by('permissions__sous_module__groupe_menu__numero_ordre').values('permissions__sous_module_id').distinct()

            for item in sous_modules_id:
                sous_module_id = item['permissions__sous_module_id']
                sous_module = Model_SousModule.objects.get(pk = sous_module_id)
                list.append(sous_module)

            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []


    @staticmethod
    def toListSousModulesByOfModuleByPermissionForAdmin(permission):
        try:

            module = permission.sous_module.module
            sous_modules = Model_SousModule.objects.filter(est_actif = True, module_id = module.id).order_by('est_dashboard').order_by('groupe_menu__numero_ordre').order_by('numero_ordre').distinct()

            return sous_modules
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
            
    @staticmethod
    def toListSousModulesByGroupePermission(module, groupe_permission):
        try:
            list = []
            sous_modules_id = Model_GroupePermission.objects.filter(permissions__sous_module__est_actif = True, permissions__sous_module__module_id = module.id, pk=groupe_permission.id).order_by('permissions__sous_module__est_dashboard').order_by('permissions__sous_module__groupe_menu__numero_ordre').order_by('permissions__sous_module__numero_ordre').values('permissions__sous_module_id').distinct()
            #print("mes sous GOOD", sous_modules_id)
            for item in sous_modules_id:
                sous_module_id = item['permissions__sous_module_id']
                sous_module = Model_SousModule.objects.get(pk = sous_module_id)
                list.append(sous_module)

            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListSousModulesByGroupePermissionForAdmin(module):
        try:
            list = []
            sous_modules_id = Model_SousModule.objects.filter(est_actif = True, module_id = module.id).order_by('est_dashboard').order_by('groupe_menu__numero_ordre').order_by('numero_ordre').values('id').distinct()

            for item in sous_modules_id:
                sous_module_id = item['id']
                sous_module = Model_SousModule.objects.get(pk = sous_module_id)
                list.append(sous_module)

            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []



    @staticmethod
    def toCreateSousModule(module_id, nom_sous_module, description, groupe = "", numero_ordre = 99, url_vers = "", est_model = False, model_principal_id = None, groupe_menu_id = None, permissions = [], est_dashboard = False, icon_menu = ""):
        try:
            sous_module = dao_sous_module()
            sous_module.module_id = module_id
            sous_module.nom_sous_module = nom_sous_module
            sous_module.description = description
            sous_module.groupe = groupe
            sous_module.numero_ordre = numero_ordre
            sous_module.url_vers = url_vers

            sous_module.est_model = est_model
            sous_module.model_principal_id = model_principal_id
            sous_module.groupe_menu_id = groupe_menu_id
            #sous_module.permissions = permissions
            sous_module.est_dashboard = est_dashboard
            sous_module.icon_menu = icon_menu
            return sous_module
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU SOUS-MODULE")
            #print(e)
            return None

    @staticmethod
    def toSaveSousModule(object_dao_sous_module):
        try:
            sous_module = Model_SousModule()
            sous_module.description = object_dao_sous_module.description
            sous_module.groupe = object_dao_sous_module.groupe
            sous_module.module_id = object_dao_sous_module.module_id
            sous_module.nom_sous_module = object_dao_sous_module.nom_sous_module
            sous_module.numero_ordre = object_dao_sous_module.numero_ordre
            sous_module.url_vers = object_dao_sous_module.url_vers

            sous_module.est_model = object_dao_sous_module.est_model
            sous_module.model_principal = object_dao_sous_module.model_principal_id
            sous_module.groupe_menu_id = object_dao_sous_module.groupe_menu_id
            '''for i in range(0, len(object_dao_sous_module.permissions)) :
                permission = object_dao_sous_module.permissions[i]
                sous_module.permissions.add(permission)'''
            sous_module.est_dashboard = object_dao_sous_module.est_dashboard
            sous_module.icon_menu = object_dao_sous_module.icon_menu

            sous_module.save()
            return sous_module
        except Exception as e:
            #print("ERREUR LORS DU SAVE DU SOUS-MODULE")
            #print(e)
            return None

    @staticmethod
    def toUpdateSousModule(id, object_dao_sous_module):
        try:
            sous_module = Model_SousModule.objects.get(pk = id)
            sous_module.description = object_dao_sous_module.description
            sous_module.groupe = object_dao_sous_module.groupe
            sous_module.module_id = object_dao_sous_module.module_id
            sous_module.nom_sous_module = object_dao_sous_module.nom_sous_module
            sous_module.numero_ordre = object_dao_sous_module.numero_ordre
            sous_module.url_vers = object_dao_sous_module.url_vers

            sous_module.est_model = object_dao_sous_module.est_model
            sous_module.model_principal = object_dao_sous_module.model_principal_id
            sous_module.groupe_menu_id = object_dao_sous_module.groupe_menu_id
            '''for i in range(0, len(object_dao_sous_module.permissions)) :
                permission = object_dao_sous_module.permissions[i]
                sous_module.permissions.add(permission)'''
            sous_module.est_dashboard = object_dao_sous_module.est_dashboard
            sous_module.icon_menu = object_dao_sous_module.icon_menu
            sous_module.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU SOUS-MODULE")
            #print(e)
            return False

    @staticmethod
    def toDeleteSousModule(id):
        try:
            sous_module = Model_SousModule.objects.get(pk = id)
            sous_module.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU SOUS-MODULE")
            #print(e)
            return False

    @staticmethod
    def toGetSousModule(id):
        try:
            return Model_SousModule.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetSousModuleDuModuleOf(module_id, numero_ordre):
        try:
            return Model_SousModule.objects.filter(est_actif = True, module_id = module_id).get(numero_ordre = numero_ordre)
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toCreateSousModuleGenerate(module_id, nom_sous_module,groupe,numero_ordre,url_vers):
        try:
            sous_module = dao_sous_module()
            sous_module.module_id = module_id
            sous_module.nom_sous_module = nom_sous_module
            sous_module.groupe = groupe
            sous_module.numero_ordre = numero_ordre
            sous_module.url_vers = url_vers
            return sous_module
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU SOUS-MODULE")
            #print(e)
            return None

    @staticmethod
    def toGetSousModuleDuModuleGroupeOf(module_id, groupe):
        try:
            return Model_SousModule.objects.filter(est_actif = True, module_id = module_id, groupe = groupe).order_by('numero_ordre')
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None


    @staticmethod
    def toGetSousModuleOfPermission(permission_id):
        try:
            #print("engendré", permission_id)
            ss = Model_SousModule.objects.filter(est_actif = True, permissions__pk = permission_id).order_by('numero_ordre')
            #print("ss", ss)
            return ss
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None