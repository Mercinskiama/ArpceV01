# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Wkf_Transition, Model_Wkf_Etape
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow

#from ErpBackOffice.dao.dao_etape_workflow import dao_etape_workflow
from django.utils import timezone

class dao_wkf_transition(object):
    id = 0
    etape_source_id	= None
    etape_destination_id = None
    groupe_permission_id = None
    condition_id = None
    url = ""
    operateur = ""
    traitement = ""
    unite_fonctionnelle_id = None
    est_decisive = False
    est_configurable = False
    est_delegable = False
    est_filtrable = False
    filtre = ""
    

    @staticmethod
    def toListTransitions():
        return Model_Wkf_Transition.objects.all()

    @staticmethod
    def toListTransitionsOfWorkflow(workflow_id):
        #print(workflow_id)  
        return Model_Wkf_Transition.objects.filter(etape_destination__workflow_id = workflow_id).order_by('id')

    @staticmethod
    def toListTransitionsOfSource(etape_id,service_referent_id=0):
        try:
            if service_referent_id == 0:
                return Model_Wkf_Transition.objects.filter(etape_source_id = etape_id)
            else:
                return Model_Wkf_Transition.objects.filter(etape_source_id = etape_id).filter(unite_fonctionnelle_id = service_referent_id)
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE TRANSITION WORKFLOW")
            #print(e)
            return None

    """
    @staticmethod
    def toListTransitionsOfWorkflow(workflow_id):
        workflow = dao_wkf_workflow.toGetWorkflow(pk = workflow_id)
        etapes = dao_wkf_etape.toListEtapeOfWorkflows(workflow.id)

        data = []

        for etape in etapes:

            """

    @staticmethod
    def toCreateTransition(etape_source_id , etape_destination_id, groupe_permission_id, condition_id, url, operateur, traitement = "", unite_fonctionnelle_id = None, est_decisive = False, est_configurable = False, est_delegable = False, est_filtrable = False, filtre = ""):        
        try:
            transition = dao_wkf_transition()
            transition.etape_source_id = etape_source_id
            transition.etape_destination_id = etape_destination_id
            transition.groupe_permission_id = groupe_permission_id
            transition.condition_id = condition_id
            transition.url = url
            transition.traitement = traitement
            transition.unite_fonctionnelle_id = unite_fonctionnelle_id
            transition.operateur = operateur
            transition.est_decisive = est_decisive
            transition.est_configurable = est_configurable
            transition.est_delegable = est_delegable
            transition.est_filtrable = est_filtrable
            transition.filtre = filtre
            return transition
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE TRANSITION WORKFLOW")
            #print(e)
            return None

    @staticmethod
    def toSaveTransition(auteur, object_dao_wkf_transition):
        try:
            transition = Model_Wkf_Transition()
            transition.etape_source_id = object_dao_wkf_transition.etape_source_id
            transition.etape_destination_id = object_dao_wkf_transition.etape_destination_id
            transition.groupe_permission_id = object_dao_wkf_transition.groupe_permission_id
            transition.condition_id = object_dao_wkf_transition.condition_id
            transition.url = object_dao_wkf_transition.url
            transition.traitement  = object_dao_wkf_transition.traitement
            transition.unite_fonctionnelle_id = object_dao_wkf_transition.unite_fonctionnelle_id
            transition.operateur = object_dao_wkf_transition.operateur
            transition.est_decisive = object_dao_wkf_transition.est_decisive
            transition.est_configurable = object_dao_wkf_transition.est_configurable
            transition.est_delegable = object_dao_wkf_transition.est_delegable
            transition.est_filtrable = object_dao_wkf_transition.est_filtrable
            transition.filtre = object_dao_wkf_transition.filtre
            transition.save()
            return transition
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE TRANSITION WORKFLOW")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateTransition(id, object_dao_wkf_transition):
        try:
            transition = Model_Wkf_Transition.objects.get(pk = id)
            transition.etape_source_id = object_dao_wkf_transition.etape_source_id
            transition.etape_destination_id = object_dao_wkf_transition.etape_destination_id
            transition.groupe_permission_id = object_dao_wkf_transition.groupe_permission_id
            transition.condition_id = object_dao_wkf_transition.condition_id
            transition.url = object_dao_wkf_transition.url
            transition.traitement  = object_dao_wkf_transition.traitement
            transition.unite_fonctionnelle_id = object_dao_wkf_transition.unite_fonctionnelle_id
            transition.operateur = object_dao_wkf_transition.operateur
            transition.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE TRANSITION WORKFLOW")
            #print(e)
            return False
  
    @staticmethod
    def toGetTransition(id):
        try:
            return Model_Wkf_Transition.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetTransitionsOfSource(etape_id, service_referent_id=0):
        if service_referent_id == 0:
            return Model_Wkf_Transition.objects.filter(etape_source_id = etape_id).first()
        else:
            return Model_Wkf_Transition.objects.filter(etape_source_id = etape_id).filter(unite_fonctionnelle_id = service_referent_id)
    
    @staticmethod
    def toGetNextEtapeFromTransitionsOfSource(etape_id, numero_ordre = None):
        return Model_Wkf_Transition.objects.filter(etape_source_id = etape_id).first()

    @staticmethod
    def toGetEtapeDestinationOfTRansition(transition_id):
        try:
            trans = Model_Wkf_Transition.objects.get(pk = transition_id)
            #print("TRANS ID %s" % trans)
            etape = Model_Wkf_Etape.objects.get(pk = trans.etape_destination_id)
            #print("ETAPE SUI %s" % etape)
            return etape
        except Exception as e:
            #print("ERREUR LOG")
            #print(e)
            return False
    
    
    @staticmethod
    def toListTransitionsGenerateDocByEtapeSource(etape_id):
        return Model_Wkf_Transition.objects.filter(etape_source_id = etape_id, est_generate_doc = True)
        
    
    @staticmethod
    def toListTransitionOfContentType(content_type):
        try:
            return Model_Wkf_Transition.objects.filter(etape_source__workflow__content_type  = content_type)           
        except Exception as e:
            return []
    
    @staticmethod
    def toListTranstionOfContentTypeFiltered(content_type, etape_id, condition_name):
        try:
            return Model_Wkf_Transition.objects.filter(etape_source__workflow__content_type  = content_type,etape_source_id = etape_id, condition__designation = condition_name)           
            
        except Exception as e:
            return []



    @staticmethod
    def toDeleteTransition(id):
        try:
            transition = Model_Wkf_Transition.objects.get(pk = id)
            transition.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE TRANSITION WORKFLOW")
            #print(e)
            return False
        					
    