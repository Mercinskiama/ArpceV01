# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Wkf_Etape
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from django.utils import timezone


class dao_wkf_etape(object):
    id = 0
    designation	= ""
    label = ""
    workflow_id = None
    est_initiale = False
    est_echec = False
    est_succes = False

    @staticmethod
    def toListEtapeWorkflows():
        return Model_Wkf_Etape.objects.all()

    @staticmethod
    def toListEtapeOfWorkflows(workflow_id):
        return Model_Wkf_Etape.objects.filter(workflow_id = workflow_id)
        
    
    @staticmethod
    def toListEtapeSuivante(etape_actuel_id, service_referent_id=0):
        try:
            actuel = Model_Wkf_Etape.objects.get(pk = etape_actuel_id)
            #print("actual %s" % actuel.id)
            objet =  dao_wkf_transition.toListTransitionsOfSource(actuel.id, service_referent_id)
            if not objet:
                objet =  dao_wkf_transition.toListTransitionsOfSource(actuel.id)
            return objet
        except Exception as e:
            return []



    @staticmethod
    def toCreateEtapeWorkflow(designation , label , workflow_id, est_initiale, est_echec, est_succes):        
        try:
            etape_workflow = dao_wkf_etape()
            etape_workflow.designation = designation
            etape_workflow.label = label
            etape_workflow.workflow_id = workflow_id
            etape_workflow.est_initiale = est_initiale
            etape_workflow.est_succes = est_succes
            etape_workflow.est_echec = est_echec
            return etape_workflow
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE ETAPE WORKFLOW")
            #print(e)
            return None

    @staticmethod
    def toSaveEtapeWorkflow(auteur, object_dao_wkf_etape):
        try:
            etape_workflow = Model_Wkf_Etape()
            etape_workflow.designation = object_dao_wkf_etape.designation
            etape_workflow.label = object_dao_wkf_etape.label
            etape_workflow.workflow_id = object_dao_wkf_etape.workflow_id
            etape_workflow.est_initiale = object_dao_wkf_etape.est_initiale
            etape_workflow.est_succes = object_dao_wkf_etape.est_succes
            etape_workflow.est_echec = object_dao_wkf_etape.est_echec
            etape_workflow.save()
            return etape_workflow
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE ETAPE WORKFLOW")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateEtapeWorkflow(id, object_dao_wkf_etape):
        try:
            etape_workflow = Model_Wkf_Etape.objects.get(pk = id)
            etape_workflow.designation = object_dao_wkf_etape.designation
            etape_workflow.label = object_dao_wkf_etape.label
            etape_workflow.workflow_id = object_dao_wkf_etape.workflow_id
            etape_workflow.est_initiale = object_dao_wkf_etape.est_initiale
            etape_workflow.est_succes = object_dao_wkf_etape.est_succes
            etape_workflow.est_echec = object_dao_wkf_etape.est_echec
            etape_workflow.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE ETAPE WORKFLOW")
            #print(e)
            return False
  
    @staticmethod
    def toGetEtapeWorkflow(id):
        try:
            return Model_Wkf_Etape.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetEtapeInitialWorkflow(workflow_id):
        try:
            return Model_Wkf_Etape.objects.filter(workflow_id = workflow_id , est_initiale = True).first()
        except Exception as e:
            return None
    
    @staticmethod
    def toGetEtapeFinalWorkflow(workflow_id):
        try:
            return Model_Wkf_Etape.objects.filter(workflow_id = workflow_id , est_succes = True).first()
        except Exception as e:
            return None
    
    @staticmethod
    def toGetEtapeEchecWorkflow(workflow_id):
        try:
            etape = Model_Wkf_Etape.objects.filter(workflow_id = workflow_id , est_echec = True).first()
            if not etape:
                etape = dao_wkf_etape()
                etape.toCreateEtapeWorkflow("Annulé", "Annuler", workflow_id, est_echec=True)
                etape.toSaveEtapeWorkflow(None, etape)
            return etape
        except Exception as e:
            return None

    @staticmethod
    def toGetEtapeSuivante(etape_actuel_id, service_referent_id=0):
        actuel = Model_Wkf_Etape.objects.get(pk = etape_actuel_id)
        #print("actual %s" % actuel.id)
        return dao_wkf_transition.toGetTransitionsOfSource(actuel.id, service_referent_id)


    @staticmethod
    def toDeleteEtapeWorkflow(id):
        try:
            etape_workflow = Model_Wkf_Etape.objects.get(pk = id)
            etape_workflow.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE ETAPE WORKFLOW")
            #print(e)
            return False
    

    @staticmethod
    def toGetNextStep(etape_actuel_id):
        actuel = Model_Wkf_Etape.objects.get(pk = etape_actuel_id)
        #print("actual %s" % actuel.id)
        return dao_wkf_transition.toGetNextEtapeFromTransitionsOfSource(actuel.id, actuel.num_ordre)

    @staticmethod
    def toGetEtapeByDesignation(designation):
        return Model_Wkf_Etape.objects.filter(designation__contains = designation).first()
        
        					
            