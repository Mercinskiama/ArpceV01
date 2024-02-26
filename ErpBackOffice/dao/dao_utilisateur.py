# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.dao.dao_personne import dao_personne
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from ErpBackOffice.models import Model_Personne, Model_GroupePermissionUtilisateur, Model_UserSessions
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count

class dao_utilisateur(dao_personne):

    
    @staticmethod
    def toListUtilisateur():
        return Model_Personne.objects.order_by("-user__last_login")
    
    
    @staticmethod
    def toListSessionOfUtilisateur(user_id):
        return Model_UserSessions.objects.filter(user_id = user_id).order_by("-logout_date")

    @staticmethod
    def toListUtilisateursActifs():
        return Model_Personne.objects.filter(est_actif = True).order_by("-nom_complet")

    @staticmethod
    def toListUtilisateursInActifs():
        return Model_Personne.objects.filter(est_actif = False).order_by("-nom_complet")

    @staticmethod
    def toListUtilisateursDuRole(role_id):
        try:
            list = []
            collection = Model_GroupePermissionUtilisateur.objects.filter(groupe_permission_id = role_id)
            for item in collection :
                list.append(dao_utilisateur.toGetUtilisateur(item.utilisateur_id))
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
       
    @staticmethod
    def toSaveUtilisateur(auteur, objet_dao_personne):
        try:
            #print(objet_dao_personne.email)
            user = User.objects.create_user(
                username = objet_dao_personne.email,
				password = "password",
				email = objet_dao_personne.email
			)
            objet_dao_personne.user_id = user.id
            objet_dao_personne.type = "UTILISATEUR"
            return dao_personne.toSaveEmploye(auteur, objet_dao_personne)
        except Exception as e:
            #print("ERREUR LORS DE L'INSERT DU USER")
            #print(e)
            return None

    @staticmethod
    def toUpdateUtilisateur(id, objet_dao_personne):
        objet_dao_personne.id = id
        objet_dao_personne.type = "UTILISATEUR"
        return dao_personne.toUpdateEmploye(objet_dao_personne)
	
    @staticmethod
    def toActiveUtilisateur(id, est_actif):
        return dao_personne.toActiveEmploye(id, est_actif)
    
    @staticmethod
    def toGetUtilisateur(id):
        return dao_personne.toGetEmploye(id)
    
    @staticmethod
    def toGetUtilisateurDuProfil(user_id):
        try:
            user = Model_Personne.objects.get(user_id = user_id)
            print(f"user: {user.user.username}")
            return user
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None
        
    @staticmethod
    def toGetAdmin():
        try:
            return Model_Personne.objects.get(user__username = "admin")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toDeleteUtilisateur(id):
        return dao_personne.toDeleteEmploye(id) 

    @staticmethod
    def toListnombreEmployeConnecteRecement(today=timezone.now().year):
        try:
            list_nbre_employes = [0,0,0,0,0,0,0,0,0,0,0,0]
            list_employes = Model_Personne.objects.annotate(month=TruncMonth('user__last_login')).values('month').annotate(total=Count('user__last_login')).filter(user__last_login__year = today)
            for item in list_employes:
                if item["month"].month==1:
                    if item["total"] == 0:
                        list_nbre_employes[0] = 0
                    else:
                        list_nbre_employes[0] = item["total"]
                    continue
                elif item["month"].month==2:
                    if item["total"] == 0:
                        list_nbre_employes[1] = 0
                    else:
                        list_nbre_employes[1] = item["total"]
                    continue
                elif item["month"].month==3:
                    if item["total"] == 0:
                        list_nbre_employes[2] = 0
                    else:
                        list_nbre_employes[2] = item["total"]
                    continue
                elif item["month"].month==4:
                    if item["total"] == 0:
                        list_nbre_employes[3] = 0
                    else:
                        list_nbre_employes[3] = item["total"]
                    continue
                elif item["month"].month==5:
                    if item["total"] == 0:
                        list_nbre_employes[4] = 0
                    else:
                        list_nbre_employes[4] = item["total"]
                    continue
                elif item["month"].month==6:
                    if item["total"] == 0:
                        list_nbre_employes[5] = 0
                    else:
                        list_nbre_employes[5] = item["total"]
                    continue
                elif item["month"].month==7:
                    if item["total"] == 0:
                        list_nbre_employes[6] = 0
                    else:
                        list_nbre_employes[6] = item["total"]
                    continue
                elif item["month"].month==8:
                    if item["total"] == 0:
                        list_nbre_employes[7] = 0
                    else:
                        list_nbre_employes[7] = item["total"]
                    continue
                elif item["month"].month==9:
                    if item["total"] == 0:
                        list_nbre_employes[8] = 0
                    else:
                        list_nbre_employes[8] = item["total"]
                    continue
                elif item["month"].month==10:
                    if item["total"] == 0:
                        list_nbre_employes[9] = 0
                    else:
                        list_nbre_employes[9] = item["total"]
                    continue
                elif item["month"].month==11:
                    if item["total"] == 0:
                        list_nbre_employes[10] = 0
                    else:
                        list_nbre_employes[10] = item["total"]
                    continue
                elif item["month"].month==12:
                    if item["total"] == 0:
                        list_nbre_employes[11] = 0
                    else:
                        list_nbre_employes[11] = item["total"]
                    continue
                else:
                    pass
            return list_nbre_employes
        except Exception as e:
            print("ERRER LIST EMPLOYE BY MONTH WITHOUT USER ID")
            print(e)
            return []