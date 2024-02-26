# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Wkf_Stakeholder
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class dao_wkf_stakeholder(object):
    id = 0
    transition_id = None
    content_type_id = None
    document_id = None
    employes = []
    carbon_copies = []
    est_delegation = True
    comments = None
    url_detail = None
    module_source = None
    
    
        
    @staticmethod
    def toCreateStakeHolderWorkflow(transition_id , objet_modele, employes, carbon_copies, est_delegation, comments = None, url_detail = None, module_source = None):        
        try:
            content_type = ContentType.objects.get_for_model(objet_modele)
            stakeholder_workflow = dao_wkf_stakeholder()
            stakeholder_workflow.transition_id = transition_id
            stakeholder_workflow.content_type_id = content_type.id
            stakeholder_workflow.document_id = objet_modele.id
            stakeholder_workflow.employes = employes
            stakeholder_workflow.carbon_copies = carbon_copies
            stakeholder_workflow.est_delegation = est_delegation
            stakeholder_workflow.comments = comments
            stakeholder_workflow.url_detail = url_detail
            stakeholder_workflow. module_source = module_source
            return stakeholder_workflow
        except Exception as e:
            print("ERREUR LORS DE LA CREATION DE HISTORIQUE WORKFLOW")
            print(e)
            return None

    @staticmethod
    def toSaveStakeHolderWorkflow(auteur, object_dao_wkf_stakeholder):
        try:
            stakeholder_workflow = Model_Wkf_Stakeholder()
            stakeholder_workflow.transition_id = object_dao_wkf_stakeholder.transition_id
            stakeholder_workflow.content_type_id = object_dao_wkf_stakeholder.content_type_id
            stakeholder_workflow.document_id  = object_dao_wkf_stakeholder.document_id
            stakeholder_workflow.comments = object_dao_wkf_stakeholder.comments
            stakeholder_workflow.est_delegation = object_dao_wkf_stakeholder.est_delegation
            stakeholder_workflow.url_detail = object_dao_wkf_stakeholder.url_detail
            stakeholder_workflow. module_source = object_dao_wkf_stakeholder.module_source
            stakeholder_workflow.created_at = timezone.now()
            stakeholder_workflow.updated_at = timezone.now()
            stakeholder_workflow.auteur_id = auteur.id
            stakeholder_workflow.save()

            if isinstance(object_dao_wkf_stakeholder.employes, list):
                for item in object_dao_wkf_stakeholder.employes:
                    stakeholder_workflow.employes.add(item)

            if isinstance(object_dao_wkf_stakeholder.carbon_copies, list):
                for item in object_dao_wkf_stakeholder.carbon_copies:
                    stakeholder_workflow.carbon_copies.add(item)
            stakeholder_workflow.save()

            return stakeholder_workflow
        except Exception as e:
            print("ERREUR LORS DE L'ENREGISTREMENT DE HISTORIQUE WORKFLOW")
            print(e)
            return None
    
    @staticmethod
    def toUpdateStakeHolderWorkflow(id, object_dao_wkf_stakeholder):
        try:
            stakeholder_workflow = Model_Wkf_Stakeholder.objects.get(pk = id)
            stakeholder_workflow.transition_id = object_dao_wkf_stakeholder.transition_id
            stakeholder_workflow.employes = object_dao_wkf_stakeholder.employes
            stakeholder_workflow.content_type_id = object_dao_wkf_stakeholder.content_type_id
            stakeholder_workflow.document_id  = object_dao_wkf_stakeholder.document_id
            stakeholder_workflow.comments = object_dao_wkf_stakeholder.comments
            stakeholder_workflow.employes = object_dao_wkf_stakeholder.employes
            stakeholder_workflow.carbon_copies = object_dao_wkf_stakeholder.carbon_copies
            stakeholder_workflow.est_delegation = object_dao_wkf_stakeholder.est_delegation
            stakeholder_workflow.url_detail = object_dao_wkf_stakeholder.url_detail
            stakeholder_workflow.module_source = object_dao_wkf_stakeholder.module_source
            stakeholder_workflow.updated_at = timezone.now()
            stakeholder_workflow.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE HISTORIQUE WORKFLOW")
            #print(e)
            return False
  
    @staticmethod
    def toGetStakeHolderWorkflow(id):
        try:
            
            return Model_Wkf_Stakeholder.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteStakeHolderWorkflow(id):
        try:
            stakeholder_workflow = Model_Wkf_Stakeholder.objects.get(pk = id)
            stakeholder_workflow.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE HISTORIQUE WORKFLOW")
            #print(e)
            return False
    

    @staticmethod
    def toListTransitionOfObject(transition_id, content_type_id, objet_id):
        try:
            content_type = ContentType.objects.get(pk = content_type_id)
            return Model_Wkf_Stakeholder.objects.filter(transition_id = transition_id, content_type = content_type, document_id = objet_id)        
        except Exception as e:
            print(e)
            return None


    
        					
            