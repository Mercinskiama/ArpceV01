from __future__ import unicode_literals
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
import datetime
import json
import os
from django.conf import settings
from django.core.files.storage import default_storage

from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_wkf_historique import dao_wkf_historique
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ModuleArchivage.dao.dao_document import dao_document
from ErpBackOffice.dao.dao_wkf_stakeholder import dao_wkf_stakeholder
from django.db import transaction

from ErpBackOffice.utils.identite import identite
from django.contrib.contenttypes.models import ContentType

class wkf_task(object):
    
    @staticmethod
    def initializeWorkflow(auteur,objet_modele,type_document = None):
        try:
            #Initialisation du workflow à l'etat initial
            #si la designation du document n'est pas fourni, on recupère le workflow par le content type
            if type_document != None:
                workflow = dao_wkf_workflow.toGetWorkflowFromTypeDoc(type_document)
            else:
                workflow = dao_wkf_workflow.toGetWorkflowFromObject(objet_modele)

            etape = dao_wkf_etape.toGetEtapeInitialWorkflow(workflow.id)
            objet_modele.statut_id = etape.id
            objet_modele.etat = etape.designation
            objet_modele.save()#TODO C'est ce 2è save quicrée le doublons dans la notification
            wkf_task.generateDocWorkflow(auteur, objet_modele)           

            #Enregistrement de l'opération dans la table historique (pour une traçabilité)
            historique = dao_wkf_historique.toCreateHistoriqueWorkflow(auteur.id, etape.id, objet_modele)
            historique = dao_wkf_historique.toSaveHistoriqueWorkflow(historique)
        except Exception as e:
            #print("Erreur",e)
            pass

    
    @staticmethod
    def getDetailObject(utilisateur,objet_modele):

        #recuperation du content type à partir du modele 
        content_type = ContentType.objects.get_for_model(objet_modele)
        historique = dao_wkf_historique.toListHistorique(objet_modele)
        #recuperation des transitions des étapes suivantes
        #Test prioritaire sur l'existence d'un service référent influencant les transitions d'étapes à suivre
        try:
            transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id, objet_modele.services_ref.id)
            #print("transition_etape_suivant", transition_etape_suivant)
            if transition_etape_suivant.count() == 0:
                transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id)
        except Exception as e:
            #print("Erreur",e)
            #L'objet n'a pas de services referents
            transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id)

        #listage des documents relatif à l'objet
        #documents = dao_document.toListDocumentbyObjetModele(objet_modele)
        documents = []
        signee = False
        
        return historique, transition_etape_suivant, signee, content_type.id, documents


    @staticmethod
    def get_details(utilisateur, objet_modele):
        try:
            #recuperation du content type à partir du modele 
            content_type = ContentType.objects.get_for_model(objet_modele)
            
            #recuperation de l'historique du workflow de ce modèle
            historique = dao_wkf_historique.toListHistorique(objet_modele)
            
            #recuperation des transitions des étapes suivantes
            transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id)

            #recuperation des documents relatif à l'objet
            documents = dao_document.toListDocumentbyObjetModele(objet_modele)
            
            return historique, transitions_etapes_suivantes, content_type.id, documents
        except Exception as e:            
            return [], [], None, []
    
        
    @staticmethod
    def postworkflow(objet_id,content_type_id,employe,etape_id, url_detail,request):
        '''fonction chargée d'assurer le traitement du passage d'un état à un autre pour un document-workflow donné'''
        
        try:
            base_dir = settings.BASE_DIR
            media_dir = settings.MEDIA_ROOT
            media_url = settings.MEDIA_URL
            
            etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
            
            #recuperation du modele de l'objet à partir de l'identifiant du content type
            model_objet = ContentType.objects.get(pk = content_type_id).model_class()
            #recuperation de l'instance du modèle concerné par le traitement à partir de son id
            objet_modele = model_objet.objects.get(pk = objet_id)
            #print(objet_modele)
            #print("on est la 565")
            #print(bzba)
            
            
            #liste des transitions
            try:
                transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id, objet_modele.services_ref.id)
                if transition_etape_suivant.count() == 0:
                    transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id)
            except Exception as e:
                #L'objet n'a pas de services referents
                transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id)
            
            #print("Finir sur mes lèvres", transition_etape_suivant)

            for item in transition_etape_suivant:
                if item.condition.designation == "Upload":
                    
                    #print("Upload")
                    #print(request)
                    #print(request.FILES)
                    if 'file_upload' in request.FILES:
                        nom_fichier = request.FILES['file_upload'].name

                        #print(nom_fichier)
                        #print("Debut file ")
                        files = request.FILES.getlist("file_upload",None)
                        
                        #On affecte le chemin de l'Image

                        objet_modele.statut_id = etape.id
                        objet_modele.etat = etape.designation
                        objet_modele.save()

                        docs_dir = 'documents/'
                        media_dir = media_dir + '/' + docs_dir

                        for fichier in files:                    
                            #print("fichier", fichier)
                            nom_fichier = fichier.name
                            nom_fichier = nom_fichier[:75]
                            #print(nom_fichier)
                            
                            #save_path = os.path.join(media_dir, str(nom_fichier))
                            #path = default_storage.save(save_path, fichier)
                            #url = media_url + docs_dir + str(nom_fichier)
                            #print(url)

                            #document = dao_document.toCreateDocument(str(objet_modele._meta),url,nom_fichier, objet_modele)
                            #document = dao_document.toSaveDocument(employe, document)
                            #'''archiver.delay(path, url, str(nom_fichier),str(objet_modele._meta),"",employe.id,objet_modele.etat,None, True)'''
                            
                            #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                            #archive.archiver(document, str(nom_fichier),None,None,employe.id,nom_fichier,None, True)  
                            content_type = ContentType.objects.get_for_model(objet_modele)
                            document = dao_document.toCreate(designation = nom_fichier, type = 1, type_mime = 2, mime = "PDF", dossier_id = 1, res_model_id = content_type.id, res_id = objet_modele.id, description = nom_fichier, indexation = nom_fichier, fichier = fichier)
                            saved, document, message = dao_document.toSave(employe, document)

                        #print("docu saved")
                    else:
                        return None
                else:
                    #print("mama")
                    objet_modele.statut_id = etape.id
                    objet_modele.etat = etape.designation
                    objet_modele.save()
                
                if item.traitement  != None:
                    #print("on est ensemble")
                    try:
                        exec(item.traitement)
                    except Exception as e:
                        #print("Erreur on traitement", e)
                        pass

            #print("lalana")
            historique = dao_wkf_historique.toCreateHistoriqueWorkflow(employe.id, etape.id, objet_modele)
            historique = dao_wkf_historique.toSaveHistoriqueWorkflow(historique)
            
            return historique
        except Exception as e:
            #print("Erreur", e)
            return None


	
    @staticmethod
    def cancelWorkflow(auteur,objet_id,content_type_id, notes = None, type_document = None, etape_id = None):
        '''Fonction permettant de passer à l'étape annuler du workflow ou de faire un rollback à une étape précise'''
        try:
            model_objet = ContentType.objects.get(pk = content_type_id).model_class()
            objet_modele = model_objet.objects.get(pk = objet_id)            
            workflow = dao_wkf_workflow.toGetWorkflowFromObject(objet_modele)
            if not workflow:
                if type_document != None:
                    workflow = dao_wkf_workflow.toGetWorkflowFromTypeDoc(type_document)
            
            
            
            #Si ce n'est pas un rollback
            if not etape_id: 
                print("cas 1")
                etape = dao_wkf_etape.toGetEtapeEchecWorkflow(workflow.id)
            else: 
                print("cas 2")
                etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
            print("au sortir, erreur", etape)
            objet_modele.statut_id = etape.id
            objet_modele.etat = etape.designation
            objet_modele.save()            

            historique = dao_wkf_historique.toCreateHistoriqueWorkflow(auteur.id, etape.id, objet_modele, notes)
            historique = dao_wkf_historique.toSaveHistoriqueWorkflow(historique)
            
            return historique
        except Exception as e:
            print("Erreur on cancelWorkflow", e)
            return None
	

    
    @staticmethod
    def passingStepWorkflow(auteur, objet_modele, etape_id = None):
        '''Passage d'une étape à une autre'''
        
        #print("passing")
        if etape_id != None:
            #print("hhhh")
            etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
            try:
                transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id, objet_modele.services_ref.id)
            except Exception as e:
                #L'objet n'a pas de services referents
                transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(objet_modele.statut_id)
            #print(objet_modele)
            #print(transition_etape_suivant)
            for item in transition_etape_suivant:
                # Gestion des transitions dans le document
                objet_modele.statut_id = etape.id
                objet_modele.etat = etape.designation
                objet_modele.save()
            
        else:
            #print("passing 2")
            
            item = dao_wkf_transition.toGetTransitionsOfSource(objet_modele.statut_id)
            '''for item in transition:'''
            #print("item",item)
            objet_modele.statut_id = item.etape_destination_id
            objet_modele.etat = item.etape_destination.designation
            objet_modele.save()
        
        historique = dao_wkf_historique.toCreateHistoriqueWorkflow(auteur.id, objet_modele.statut_id, objet_modele)
        historique = dao_wkf_historique.toSaveHistoriqueWorkflow(historique)



    @staticmethod
    def generateDocWorkflow(auteur, objet_modele):
        try:
            #Get ContentType of all FK
            for f in objet_modele._meta.get_fields():
                if f.many_to_one:#Si c'est un champ FK
                    #Manoeuvre pour récuperer l'objet avec valeur de la classe dans objet_related
                    modele = objet_modele._meta.get_field(f.name).related_model
                    model_content_type = ContentType.objects.get_for_model(modele)
                    pk_related = objet_modele._meta.get_field(f.name).value_from_object(objet_modele)
                    objet_related = model_content_type.model_class().objects.get(pk = pk_related)

                    #Cherchons les transitions ayant comme étape de depart, le statut_id de notre objet_related
                    transitions = dao_wkf_transition.toListTransitionsGenerateDocByEtapeSource(objet_related.statut_id)
                    for transition in transitions:
                        wkf_task.passingStepWorkflow(auteur,objet_related, transition.etape_destination_id)
                else:#Si c'est un champ ManyToMany or OneToMany
                    pass
            return True
        except Exception as e:
            print(f'Exception generateDocWorflow {e}')
            return False


    @staticmethod
    def postStakeHolder(transition_id, objet_id,content_type_id, employes, carbon_copies, est_delegation, comments, url_detail, module_source, auteur):
        '''fonction chargée d'assurer le traitement de StakeHolder'''
        try:
            base_dir = settings.BASE_DIR
            media_dir = settings.MEDIA_ROOT
            media_url = settings.MEDIA_URL

            #recuperation du modele de l'objet à partir de l'identifiant du content type
            model_objet = ContentType.objects.get(pk = content_type_id).model_class()
            #recuperation de l'instance du modèle concerné par le traitement à partir de son id
            objet_modele = model_objet.objects.get(pk = objet_id)

            stakeholder  = dao_wkf_stakeholder.toCreateStakeHolderWorkflow(transition_id, objet_modele, employes, carbon_copies, est_delegation, comments, url_detail, module_source)
            stakeholder  = dao_wkf_stakeholder.toSaveStakeHolderWorkflow(auteur, stakeholder)
            
            #historique = dao_wkf_historique.toCreateHistoriqueWorkflow(auteur.id, etape.id, objet_modele)
            #historique = dao_wkf_historique.toSaveHistoriqueWorkflow(historique)
            
            return stakeholder
        except Exception as e:
            print("Erreur", e)
            return None


    
