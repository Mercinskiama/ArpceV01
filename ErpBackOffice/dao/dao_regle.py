# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Regle
from django.utils import timezone

class dao_regle(object):
    id = 0
    designation	= ""
    filtre = ""
    permissions = []
    groupe_permission_id = None   

    @staticmethod
    def toListRegles():
        return Model_Regle.objects.all()
    

    @staticmethod
    def toCreateRegle(designation, filtre, groupe_permission_id, permissions):        
        try:
            regle = dao_regle()
            regle.designation = designation
            regle.filtre = filtre
            regle.permissions = permissions
            regle.groupe_permission_id =groupe_permission_id
            
            return regle
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA REGLE")
            #print(e)
            return None

    @staticmethod
    def toSaveRegle(auteur, object_dao_regle):
        try:
            regle = Model_Regle()
            regle.designation = object_dao_regle.designation
            regle.filtre = object_dao_regle.filtre
            #regle.permissions = object_dao_regle.permissions
            regle.groupe_permission_id = object_dao_regle.groupe_permission_id
            regle.creation_date = timezone.now()
            regle.auteur_id = auteur.id 
            regle.save()
            return regle
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE LA REGLE")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateRegle(id, object_dao_regle):
        try:
            regle = Model_Regle.objects.get(pk = id)
            regle.designation = object_dao_regle.designation
            regle.filtre  = object_dao_regle.filtre
            regle.permissions = object_dao_regle.permissions
            regle.groupe_permission_id = object_dao_regle.groupe_permission_id
            regle.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE LA REGLE")
            #print(e)
            return False
  
    @staticmethod
    def toGetRegle(id):
        try:
            return Model_Regle.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteRegle(id):
        try:
            regle = Model_Regle.objects.get(pk = id)
            regle.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE LA REGLE")
            #print(e)
            return False
    

    @staticmethod
    def toGetRegleByPermissionAndGroupePermission(permission_number, groupe_permissions):
        try:
            for groupe_permission in groupe_permissions:
                regle = Model_Regle.objects.filter(permission__numero = permission_number, groupe_permission_id = groupe_permission.id).first()
                #print("unos regle", regle)
                if regle:
                    return regle.filtre
            return None
        except Exception as e:
            #print("erreur on regl", e)
            return None
    
    @staticmethod
    def toListModulesOfRegle(regle_id):
        try:
            list_module = []
            list_sous_module = []
            
            regle = Model_Regle.objects.get(pk = regle_id)
            #print("regle", regle.permissions.all())
            
            for permission in regle.permissions.all():
                #print("permission", permission)
                list_module.append(permission.sous_module.module)
                list_sous_module.append(permission.sous_module)
                            
            list_module = list(set(list_module))
            list_sous_module = list(set(list_sous_module))
            #print("list stous ",list_sous_module )
            return list_module, list_sous_module
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return [], []
    
    

                            
            