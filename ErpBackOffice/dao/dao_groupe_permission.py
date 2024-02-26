# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_GroupePermission, Model_GroupePermissionUtilisateur
from django.utils import timezone

class dao_groupe_permission(object):
    id = 0
    designation	= ""
    permissions = []
    

    @staticmethod
    def toListGroupePermissions():
        return Model_GroupePermission.objects.all()
    

    @staticmethod
    def toCreateGroupePermission(designation, permissions = []):        
        try:
            groupe_permission = dao_groupe_permission()
            groupe_permission.designation = designation
            groupe_permission.permissions = permissions
            
            return groupe_permission
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION Du GROUPE DE PERMISSION")
            #print(e)
            return None

    @staticmethod
    def toSaveGroupePermission(auteur, object_dao_groupe_permission):
        try:
            groupe_permission = Model_GroupePermission()
            groupe_permission.designation = object_dao_groupe_permission.designation
            for i in range(0, len(object_dao_groupe_permission.permissions)) :
                permission = object_dao_groupe_permission.permissions[i]
                groupe_permission.permissions.add(permission)
            groupe_permission.creation_date = timezone.now()
            groupe_permission.auteur_id = auteur.id 
            groupe_permission.save()
            return groupe_permission
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DU GROUPE DE  PERMISSION")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateGroupePermission(id, object_dao_groupe_permission):
        try:
            groupe_permission = Model_GroupePermission.objects.get(pk = id)
            groupe_permission.designation = object_dao_groupe_permission.designation
            for i in range(0, len(object_dao_groupe_permission.permissions)) :
                permission = object_dao_groupe_permission.permissions[i]
                groupe_permission.permissions.add(permission)
            groupe_permission.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU GROUPE DE PERMISSION")
            #print(e)
            return False
  
    @staticmethod
    def toGetGroupePermission(id):
        try:
            return Model_GroupePermission.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteGroupePermission(id):
        try:
            permission = Model_GroupePermission.objects.get(pk = id)
            permission.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU GROUPE DE PERMISSION")
            #print(e)
            return False
        

    @staticmethod
    def toGetGroupePermissionDeLaPersonne(personne_id):
        try:
            groupe_permission_utilisateur = Model_GroupePermissionUtilisateur.objects.get(utilisateur_id = personne_id)
            groupe_permission = Model_GroupePermission.objects.get(pk = groupe_permission_utilisateur.groupe_permission_id)
            return groupe_permission
        except Exception as e:
            #print("ERREUR toGetGroupePermissionDeLaPersonne")
            #print(e)
            return None
    
    @staticmethod
    def toListGroupePermissionDeLaPersonne(personne_id):
        try:
            liste = []
            groupe_permission_utilisateur = Model_GroupePermissionUtilisateur.objects.filter(utilisateur_id = personne_id)
            for item in groupe_permission_utilisateur:
                groupe_permission = Model_GroupePermission.objects.get(pk = item.groupe_permission_id)
                liste.append(groupe_permission)
            return liste
        except Exception as e:
            #print("ERREUR toListGroupePermissionDeLaPersonne")
            #print(e)
            return None
    
    @staticmethod
    def toAttributeGroupePermission(auteur, utilisateur_id, groupe_permission_id):
        try:
            groupe_permission_utilisateur = Model_GroupePermissionUtilisateur()
            groupe_permission_utilisateur.auteur_id = auteur.id
            groupe_permission_utilisateur.utilisateur_id = utilisateur_id
            groupe_permission_utilisateur.groupe_permission_id = groupe_permission_id
            groupe_permission_utilisateur.creation_date = timezone.now()
            groupe_permission_utilisateur.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU INSERT")
            #print(e)
            return False
    
    @staticmethod
    def toRetireGroupePermission(utilisateur_id, groupe_permission_id):
        try:
            groupe_permission_utilisateur = Model_GroupePermissionUtilisateur.objects.filter(groupe_permission_id= groupe_permission_id).filter(utilisateur_id = utilisateur_id).first()
            groupe_permission_utilisateur.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return False
                            
            
    @staticmethod
    def toAddPermission(groupe, permission_id):
        try:
            groupe.permissions.add(permission_id)
            return True
        except Exception as e:
            return False
        
    @staticmethod
    def toRemovePermission(groupe, permission_id):
        try:
            groupe.permissions.remove(permission_id)
            #print("%s Removed" % permission_id)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def toListGroupePermissionByDesignation(designation):
        try:
            groupe_permission = Model_GroupePermission.objects.get(designation = designation)
            groupe_permission_utilisateur = Model_GroupePermissionUtilisateur.objects.filter(groupe_permission_id = groupe_permission.id)
            return groupe_permission_utilisateur
        except Exception as e:
            #print("ERREUR LORS DE LA REQUETE")
            #print(e)
            return False
    

    @staticmethod
    def toGetPersonOfPermission(designation):
        try:
            groupe_permission_utilisateur = Model_GroupePermissionUtilisateur.objects.filter(groupe_permission__designation = designation).select_related()
            return groupe_permission_utilisateur
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return False