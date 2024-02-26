# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Wkf_Historique
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class dao_wkf_historique(object):
    id = 0
    employe_id = None
    etape_id = None
    content_type_id = None
    document_id = None

    @staticmethod
    def toListHistorique(objet_modele):
        content_type = ContentType.objects.get_for_model(objet_modele)
        return Model_Wkf_Historique.objects.filter(content_type_id = content_type.id, document_id = objet_modele.id)
    
    @staticmethod
    def toCreateHistoriqueWorkflow(employe_id , etape_id , objet_modele, notes = None):        
        try:
            content_type = ContentType.objects.get_for_model(objet_modele)
            historique_workflow = dao_wkf_historique()
            historique_workflow.employe_id = employe_id
            historique_workflow.etape_id = etape_id
            historique_workflow.content_type_id = content_type.id
            historique_workflow.document_id = objet_modele.id
            historique_workflow.notes = notes
            return historique_workflow
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE HISTORIQUE WORKFLOW")
            #print(e)
            return None

    @staticmethod
    def toSaveHistoriqueWorkflow(object_dao_wkf_historique):
        try:
            historique_workflow = Model_Wkf_Historique()
            historique_workflow.employe_id = object_dao_wkf_historique.employe_id
            historique_workflow.etape_id = object_dao_wkf_historique.etape_id
            historique_workflow.content_type_id = object_dao_wkf_historique.content_type_id
            historique_workflow.document_id  = object_dao_wkf_historique.document_id
            historique_workflow.notes = object_dao_wkf_historique.notes
            historique_workflow.save()
            return historique_workflow
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE HISTORIQUE WORKFLOW")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateHistoriqueWorkflow(id, object_dao_wkf_historique):
        try:
            historique_workflow = Model_Wkf_Historique.objects.get(pk = id)
            historique_workflow.employe_id = object_dao_wkf_historique.employe_id
            historique_workflow.etape_id = object_dao_wkf_historique.etape_id
            historique_workflow.content_type_id = object_dao_wkf_historique.content_type_id
            historique_workflow.document_id  = object_dao_wkf_historique.document_id
            historique_workflow.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE HISTORIQUE WORKFLOW")
            #print(e)
            return False
  
    @staticmethod
    def toGetHistoriqueWorkflow(id):
        try:
            
            return Model_Wkf_Historique.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteHistoriqueWorkflow(id):
        try:
            historique_workflow = Model_Wkf_Historique.objects.get(pk = id)
            historique_workflow.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE HISTORIQUE WORKFLOW")
            #print(e)
            return False


    @staticmethod
    def toGetIfSigned(etape_id, objet_modele, employe_id):
        try:
            content_type = ContentType.objects.get_for_model(objet_modele)
            historique_workflow = Model_Wkf_Historique.objects.filter(etape_id = etape_id, content_type_id = content_type.id, document_id = objet_modele.id, employe_id = employe_id) 
            if historique_workflow:
                return True
            else: return False           
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU WORKFLOW")
            #print(e)
            return False     
        					
            