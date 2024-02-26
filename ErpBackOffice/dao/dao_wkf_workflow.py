# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Wkf_Workflow
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

class dao_wkf_workflow(object):
    id = 0
    type_document	= ""
    content_type_id  = None
    

    @staticmethod
    def toListWorkflows():
        return Model_Wkf_Workflow.objects.all()
    
    @staticmethod
    def toListObjectContenType():
        return  ContentType.objects.all()
    

    @staticmethod
    def toCreateWorkflow(type_document, objet_id = None):        
        try:
            workflow = dao_wkf_workflow()
            workflow.type_document = type_document
            workflow.content_type_id = objet_id
            return workflow
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU WORKFLOW")
            #print(e)
            return None

    @staticmethod
    def toSaveWorkflow(auteur, object_dao_workflow):
        try:
            workflow = Model_Wkf_Workflow()
            workflow.type_document = object_dao_workflow.type_document
            workflow.content_type_id = object_dao_workflow.content_type_id
            workflow.save()
            return workflow
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DU WORKFLOW")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateWorkflow(id, object_dao_workflow):
        try:
            workflow = Model_Wkf_Workflow.objects.get(pk = id)
            workflow.type_document = object_dao_workflow.type_document
            workflow.content_type_id = object_dao_workflow.content_type_id
            workflow.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU WORKFLOW")
            #print(e)
            return False
  
    @staticmethod
    def toGetWorkflow(id):
        try:
            return Model_Wkf_Workflow.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetWorkflowFromTypeDoc(type_document):
        try:
            return Model_Wkf_Workflow.objects.get(type_document = type_document)
        except Exception as e:
            print("toGetWorkflowFromTypeDoc", e)
            return None


    @staticmethod
    def toGetWorkflowFromObject(objet_modele):
        try:
            content_type = ContentType.objects.get_for_model(objet_modele)
            #print(content_type)
            return Model_Wkf_Workflow.objects.filter(content_type_id= content_type.id).first()
        except Exception as e:
            print("toGetWorkflowFromObject", e)
            return None



    @staticmethod
    def toDeleteWorkflow(id):
        try:
            workflow = Model_Wkf_Workflow.objects.get(pk = id)
            workflow.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU WORKFLOW")
            #print(e)
            return False

      		
            