# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Permission, Model_GroupePermission
from django.utils import timezone


class dao_permission(object):
    id = 0
    designation	= ""
    

    @staticmethod
    def toListPermissions():
        return Model_Permission.objects.all()
    
    @staticmethod
    def toListPermissionsOfModule(module_id):
        return Model_Permission.objects.filter(sous_module__module_id = module_id)
    
    
    @staticmethod
    def toListPermissionsNonAutorizeOfSousModule(groupe_id, sous_module_id):
        try:
            list = []
            permissions = Model_Permission.objects.filter(sous_module_id = sous_module_id)
            for item in permissions :
                
                if not Model_GroupePermission.objects.filter(permissions__id = item.id, pk=groupe_id).first():
                    list.append(item)
                
            return list
        except Exception as e:
            return []
    
    @staticmethod
    def toListPermissionsOfSousModule(sous_module_id):
        try:
            permissions = Model_Permission.objects.filter(sous_module_id = sous_module_id)
            return permissions
        except Exception as e:
            return []
        
    @staticmethod
    def toListPermissionsOfSousModuleOfrole(groupe_id, sous_module_id):
        try:
            permissions = Model_Permission.objects.filter(sous_module_id = sous_module_id)
            return permissions
        except Exception as e:
            return []
    

    @staticmethod
    def toCreatePermission(designation):        
        try:
            permission = dao_permission()
            permission.designation = designation
            return permission
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA PERMISSION")
            #print(e)
            return None

    @staticmethod
    def toSavePermission(auteur, object_dao_permission):
        try:
            permission = Model_Permission()
            permission.designation = object_dao_permission.designation
            permission.creation_date = timezone.now()
            permission.auteur_id = auteur.id 
            permission.save()
            return permission
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE LA PERMISSION")
            #print(e)
            return None
    
    @staticmethod
    def toUpdatePermission(id, object_dao_permission):
        try:
            permission = Model_Permission.objects.get(pk = id)
            permission.designation = object_dao_permission.designation
            permission.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE LA PERMISSION")
            #print(e)
            return False
  
    @staticmethod
    def toGetPermission(id):
        try:
            return Model_Permission.objects.get(pk = id)
        except Exception as e:
            return None
        
    @staticmethod
    def toGetPermissionByNumber(numero):
        try:
            return Model_Permission.objects.get(numero = numero)
        except Exception as e:
            return None
        
    @staticmethod
    def toGetPermissionByName(designation):
        try:
            return Model_Permission.objects.get(designation = designation)
        except Exception as e:
            return None
    
    @staticmethod
    def toGetPermissionOfAdmin(module_id):
        return Model_Permission.objects.filter(sous_module__module_id = module_id).filter(designation__icontains = "CREER_RAPPORT").first()
    
    @staticmethod
    def toCheckPermission(groupe_id, permission_id):
        try:
            Model_GroupePermission.objects.get(permissions__id = permission_id, pk=groupe_id)
            return True
        except Exception as e:
            return False

    @staticmethod
    def toDeletePermission(id):
        try:
            permission = Model_Permission.objects.get(pk = id)
            permission.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE LA PERMISSION")
            #print(e)
            return False
                            
            