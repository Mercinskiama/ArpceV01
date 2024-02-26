from django.utils import timezone
from ErpBackOffice.models import Model_Temp_Notification, Model_Notification
from ErpBackOffice.models import Model_Wkf_Etape, Model_Wkf_Transition, Model_Wkf_Workflow
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from ErpBackOffice import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
#from ErpBackOffice.utils.sending_email import sending_email
from ErpBackOffice.utils.EmailThread import send_async_mail
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
#from ModuleComptabilites.models import *


'''def signal_engagement(sender,instance,created,**kwargs):
    if instance.statut: #C'est pour ne pas envoyer 2 notifications après l'etape initiale       
        auteur = "Admin"
        if instance.auteur: auteur = instance.auteur.nom_complet
        texte = "Le Bon d'Engagement N° {0} initié par {1} en date du {2} vous est envoyé pour traitement".format(instance.numero, auteur, instance.creation_date)
        lien_action = 'module_comptabilites_detail_engagements'
        sending_notification(instance,"MODULE_COMPTABILITES",texte,lien_action)
   
#Connection avec le Model
post_save.connect(signal_engagement,sender=Model_Engagements)'''


############################ CODE D'ENVOI DES NOTIFICATION #################################
def sending_notification(instance,module_source,texte,lien_action, superieur_hierarchique = None):
    try:
        #print("im inside bitch")
        recipient_list = []
        #recuperation des transitions
        transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = instance.statut)
        #print("inst", instance.statut)

        #Si premier enregistrement
        if not instance.statut:
            etape_initial = retrieving_etape_initiale(instance)
            transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = etape_initial)
            if transitions_concernees.count() > 1:
                transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = etape_initial).filter(unite_fonctionnelle = instance.services_ref)
                
        #création de la notification
        notif = Model_Notification.objects.create(module_source = module_source,text=texte,created_at = timezone.now())
        
        #Constitution du role utilisateur des etapes concernées
        role_users = []
        print(transitions_concernees)
        for transition in transitions_concernees:
            if transition.groupe_permission:
                list_roles = dao_groupe_permission.toListGroupePermissionByDesignation(transition.groupe_permission.designation)
                for un_role in list_roles:
                    role_users.append(un_role)
        
        #Elimination des doublons
        role_users = set(role_users)
        role_users = list(role_users)

        #Envoi des notifications aux utilisateurs concernées
        print(role_users)
        for item in role_users:
            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #conservation mail
            if item.utilisateur.email != "" and item.utilisateur.email != None:
                recipient_list.append(item.utilisateur.email)
               
        #Envoi des mails au concerné
        #send_async_mail('Notification Système ERP',texte,recipient_list,False,module_source,'')
        #recipient_list.clear()
    except Exception as e:
        print("Erreur on sub function")
        print("Erreur",e)


############################ CODE D'ENVOI DES NOTIFICATION #################################
def sending_stakeholder_notification(instance,texte):
    try:
        recipient_list = []
        module_source = instance.module_source
        lien_action = instance.url_detail
        users = instance.employes
        Cc = instance.carbon_copies
        
        #création de la notification
        notif = Model_Notification.objects.create(module_source = module_source,text=texte,created_at = timezone.now())
        
        #Envoi des notifications aux utilisateurs concernées
        #print("role",role_users)
        for item in users.all():
            Model_Temp_Notification.objects.create(user_id=item.id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.document_id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #conservation mail
            if item.email != "" and item.email != None:
                recipient_list.append(item.email)
        
        for item in Cc.all():
            #Model_Temp_Notification.objects.create(user_id=item.id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #conservation mail
            if item.email != "" and item.email != None:
                recipient_list.append(item.email)
        
        #Envoi des mails au concerné
        send_async_mail('Notification Système',texte,recipient_list,False,module_source,'')
        recipient_list.clear()
    except Exception as e:
        #print("Erreur on sub function")
        #print("Erreur",e)
        pass

def retrieving_etape_initiale(objet_modele):
    content_type = ContentType.objects.get_for_model(objet_modele)
    workflow = Model_Wkf_Workflow.objects.filter(content_type_id= content_type.id).first()
    return Model_Wkf_Etape.objects.get(workflow_id = workflow.id , est_initiale = True)

