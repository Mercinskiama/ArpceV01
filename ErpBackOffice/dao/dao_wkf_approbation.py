# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Wkf_Approbation
from django.utils import timezone

class dao_wkf_approbation(object):
    id = 0
    designation	= ""
    transition_id = None
    
    @staticmethod
    def toListApprobations():
        return Model_Wkf_Approbation.objects.all()
    

    @staticmethod
    def toCreateApprobation(designation, transition_id = None):        
        try:
            approbation = dao_wkf_approbation()
            approbation.designation = designation
            approbation.transition_id = transition_id
            return approbation
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA approbation")
            #print(e)
            return None

    @staticmethod
    def toSaveApprobation(auteur, object_dao_approbation):
        try:
            approbation = Model_Wkf_Approbation()
            approbation.designation = object_dao_approbation.designation
            approbation.transition_id = object_dao_approbation.transition_id
            approbation.save()
            return approbation
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE LA approbation")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateApprobation(id, object_dao_approbation):
        try:
            approbation = Model_Wkf_Approbation.objects.get(pk = id)
            approbation.designation = object_dao_approbation.designation
            approbation.transition_id = object_dao_approbation.transition_id
            approbation.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE LA approbation ")
            #print(e)
            return False
  
    @staticmethod
    def toGetApprobation(id):
        try:
            return Model_Wkf_Approbation.objects.get(pk = id)
        except Exception as e:
            return None      

    @staticmethod
    def toDeleteApprobation(id):
        try:
            approbation = Model_Wkf_Approbation.objects.get(pk = id)
            approbation.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE LA approbation")
            #print(e)
            return False
        					
            