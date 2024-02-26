from __future__ import unicode_literals

from ErpBackOffice.models import Model_Module, Model_GroupePermission
import unidecode

class dao_module(object):
    id = 0
    nom_module = ""
    description = ""
    est_installe = False
    url_vers = ""
    numero_ordre = 1
    icon_module = ""
    couleur = ""

    @staticmethod
    def toListModules():
        return Model_Module.objects.all().order_by("numero_ordre")

    @staticmethod
    def toListModulesInstalles():
        return Model_Module.objects.filter(est_installe = True).order_by("numero_ordre")
               
    @staticmethod
    def toListModulesByPermission(groupe_permission):
        try:
            list = []
            
            modules_id = Model_GroupePermission.objects.filter(pk=groupe_permission.id).order_by('permissions__sous_module__module__numero_ordre').values('permissions__sous_module__module_id').distinct()
            
            for item in modules_id:
                module_id = item['permissions__sous_module__module_id']
                module = Model_Module.objects.get(pk = module_id)
                list.append(module)
                            
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    
    
    @staticmethod
    def toCreateModule(nom_module, description, url_vers, numero_ordre, icon_module, couleur = "Orange", est_installe = False):
        try:
            module = dao_module()
            module.nom_module = nom_module
            module.description = description
            module.est_installe = est_installe
            module.icon_module = icon_module
            module.couleur = couleur
            module.numero_ordre = numero_ordre
            module.numero_ordre = numero_ordre
            module.url_vers = url_vers
            return module
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU MODULE")
            #print(e)
            return None

    @staticmethod
    def toSaveModule(object_dao_module):
        try:
            module = Model_Module()
            module.description = object_dao_module.description
            module.est_installe = object_dao_module.est_installe
            module.icon_module = object_dao_module.icon_module
            module.nom_module = object_dao_module.nom_module
            module.numero_ordre = object_dao_module.numero_ordre
            module.url_vers = object_dao_module.url_vers
            module.couleur = object_dao_module.couleur
            #On met à jour le nom de application django du module
            nom_modules = module.nom_module.split(" ")
            name_module = ""
            for item in nom_modules: 
                name_module = '{}{}'.format(name_module, unidecode.unidecode(item.lower().capitalize()))
            nom_application = 'Module{0}'.format(name_module)
            module.nom_application = nom_application
            module.save()
            return module
        except Exception as e:
            #print("ERREUR LORS DU SAVE DU MODULE")
            #print(e)
            return None        

    @staticmethod
    def toUpdateModule(id, object_dao_module):
        try:
            module = Model_Module.objects.get(pk = id)
            module.description = object_dao_module.description
            module.est_installe = object_dao_module.est_installe
            module.icon_module = object_dao_module.icon_module
            module.nom_module = object_dao_module.nom_module
            module.numero_ordre = object_dao_module.numero_ordre
            module.url_vers = object_dao_module.url_vers
            module.couleur = object_dao_module.couleur
            module.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU MODULE")
            #print(e)
            return False        

    @staticmethod
    def toInstallModule(id, est_installe):
        try:
            module = Model_Module.objects.get(pk = id)
            module.est_installe = est_installe
            module.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE L'INSALLATION / DESINSTALLATION DU MODULE")
            #print(e)
            return False

    @staticmethod
    def toDeleteModule(id):
        try:
            module = Model_Module.objects.get(pk = id)
            module.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU MODULE")
            #print(e)
            return False
  
    @staticmethod
    def toGetModule(id):
        try:
            return Model_Module.objects.get(pk = id)
        except Exception as e:
            return None
  
    @staticmethod
    def toGetModuleOf(numero_ordre):
        try:
            return Model_Module.objects.get(numero_ordre = numero_ordre)
        except Exception as e:
            return None
    
        
    @staticmethod
    def toGetModuleByNumOrder(num):
        try:
            return Model_Module.objects.get(numero_ordre = num)
        except Exception as e:
            return None
    
    @staticmethod
    def toGetModuleByName(module_name):
        try:
            return Model_Module.objects.filter(nom_module = module_name).first()
        except Exception as e:
            return None
        
    @staticmethod
    def toGetModuleByAppName(nom_application):
        try:
            return Model_Module.objects.filter(nom_application = nom_application).first()
        except Exception as e:
            return None
    
    @staticmethod
    def toTestModuleInstalledByCode(module_code):
        try:
            is_installed = False
            module = Model_Module.objects.filter(code = module_code).first()
            if module:
                is_installed = module.est_installe
            return is_installed
        except Exception as e:
            return False