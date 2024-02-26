# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_ModuleOverModel, Model_Module
from ErpBackOffice.dao.dao_module import dao_module
from django.utils import timezone

class dao_moduleovermodel(object):
    id = 0
    nom_modele = ""
    module_id = 0
    date_creation = ""
    state = ""
    
    @staticmethod
    def toCreateModuleOverModel(nom_modele,module_id):
        try:
            mod = dao_moduleovermodel()
            mod.nom_modele = nom_modele
            mod.module_id = module_id
            return mod
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSaveModuleOverModel(dao_moduleovermodel_object):
        try:
            mod = Model_ModuleOverModel()
            mod.nom_modele = dao_moduleovermodel_object.nom_modele
            mod.module_id = Model_Module.objects.get(pk = dao_moduleovermodel_object.module_id)
            mod.date_creation = timezone.now()
            mod.save()
            return mod
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdateModuleOverModel(id, dao_moduleovermodel_object):
        try:
            mod = Model_ModuleOverModel.objects.get(pk = id)
            mod.nom_modele = dao_moduleovermodel_object.nom_modele
            mod.module_id = dao_moduleovermodel_object.module_id
            mod.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDeleteModuleOverModel(dao_moduleovermodel_object):
        try:
            mod = Model_ModuleOverModel.objects.get(pk = dao_categorie_object.id)
            mod.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGetModuleOverModel(id):
        try:
            mod = Model_ModuleOverModel.objects.get(pk = id)
            return mod
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetModuleOverModelByRef(id):
        try:
            mod = Model_ModuleOverModel.objects.filter(module_id = id)
            return mod
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None