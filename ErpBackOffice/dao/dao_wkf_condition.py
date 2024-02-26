# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Wkf_Condition
from django.utils import timezone

class dao_wkf_condition(object):
    id = 0
    designation	= ""
    

    @staticmethod
    def toListConditions():
        return Model_Wkf_Condition.objects.all()
    

    @staticmethod
    def toCreateCondition(designation):        
        try:
            condition = dao_wkf_condition()
            condition.designation = designation
            return condition
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA CONDITION DE TRANSITION DE LA CONDITION DE TRANSITION ")
            #print(e)
            return None

    @staticmethod
    def toSaveCondition(auteur, object_dao_condition):
        try:
            condition = Model_Wkf_Condition()
            condition.designation = object_dao_condition.designation
            condition.save()
            return condition
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE LA CONDITION DE TRANSITION ")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateCondition(id, object_dao_condition):
        try:
            condition = Model_Wkf_Condition.objects.get(pk = id)
            condition.designation = object_dao_condition.designation
            condition.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE LA CONDITION DE TRANSITION ")
            #print(e)
            return False
  
    @staticmethod
    def toGetCondition(id):
        try:
            return Model_Wkf_Condition.objects.get(pk = id)
        except Exception as e:
            return None      

    @staticmethod
    def toDeleteCondition(id):
        try:
            condition = Model_Wkf_Condition.objects.get(pk = id)
            condition.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE LA CONDITION DE TRANSITION ")
            #print(e)
            return False
        					
            