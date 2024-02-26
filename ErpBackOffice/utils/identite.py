from __future__ import unicode_literals
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur, Model_Personne
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

class identite(object):
    @staticmethod
    def est_connecte(request):
        if request.user.is_authenticated == False : return False
        else: return True

    @staticmethod
    def utilisateur(request):
        if identite.est_connecte(request) == False: return None
        user = request.user
        """if user.username == "admin":
            utilisateur = Model_Personne()
            utilisateur.nom_complet = "SYSTEM"
            utilisateur.user = user
            utilisateur.id = None
            return utilisateur"""
        return dao_utilisateur.toGetUtilisateurDuProfil(user.id)

    @staticmethod
    def user(request):
        if identite.est_connecte(request) == False: return None
        return request.user



