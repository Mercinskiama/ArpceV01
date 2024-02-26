# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.models import Model_Regle
from django.utils import timezone

class dao_model(object):

    @staticmethod
    def toGetRegleByPermissionAndGroupePermission(permission_number, groupe_permissions):
        try:
            filtre = {}
            for groupe_permission in groupe_permissions:
                regle = Model_Regle.objects.filter(groupe_permission_id = groupe_permission.id, permissions__numero=permission_number).first()
                #regle = Model_Regle.objects.filter(permission__numero = permission_number, groupe_permission_id = groupe_permission.id).first()
                if regle:
                    return regle.filtre
                    #filtre.update(regle.filtre)
            return filtre
        except Exception as e:
            #print("erreur on regl", e)
            return None

    
    @staticmethod
    def toListModel(results, permission_number, groupe_permissions, auteur):
        filtre = dao_model.toGetRegleByPermissionAndGroupePermission(permission_number, groupe_permissions)
        if not filtre:
            return results
        else:
            kwargs = eval(filtre)
            return  results.filter(**kwargs)



    
                            
            