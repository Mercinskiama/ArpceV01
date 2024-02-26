from __future__ import unicode_literals
from ErpBackOffice.models import Model_Taux

class dao_taux(object):
    id = 0
    devise_depart_id = 0
    devise_arrive_id = 0
    montant = 0
    est_courant = False

    @staticmethod
    def toListTaux():
        return Model_Taux.objects.all()

    @staticmethod
    def toListTauxCourants():
        return Model_Taux.objects.filter(est_courant = True)

    @staticmethod
    def toCreateTaux(devise_arrive, devise_depart, montant):
        try:
            taux = dao_taux()
            taux.devise_arrive_id = devise_arrive.id
            taux.devise_depart_id = devise_depart.id
            taux.montant = montant
            taux.est_courant = False
            return taux
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU TAUX")
            #print(e)
            return None
			
    @staticmethod
    def toSaveTaux(auteur, objet_dao_taux):
        try:
            taux  = Model_Taux()
            taux.devise_arrive_id = objet_dao_taux.devise_arrive_id
            taux.devise_depart_id = objet_dao_taux.devise_depart_id
            taux.montant = objet_dao_taux.montant
            taux.est_courant = False
            taux.auteur_id = auteur.id
            taux.save()
            return taux
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toUpdateTaux(id, objet_dao_taux):
        try:
            taux = Model_Taux.objects.get(pk = id)
            taux.devise_arrive_id = objet_dao_taux.devise_arrive_id
            taux.devise_depart_id = objet_dao_taux.devise_depart_id
            taux.montant = objet_dao_taux.montant
            devise.save()
            return devise
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None
	
    @staticmethod
    def toActiveTaux(id, est_courant):
        try:
            taux = Model_Taux.objects.get(pk = id)
            taux.est_courant = est_courant
            taux.save()
            return True
        except Exception as e:
            return False
  
    @staticmethod
    def toGetTaux(id):
        try:
            return Model_Taux.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetTauxbyDeviseDepart(devise_id):
        return Model_Taux.objects.filter(devise_depart_id = devise_id).first()
  
    @staticmethod
    def toGetTauxbyDeviseArrive(devise_id):
        return Model_Taux.objects.filter(devise_arrive_id = devise_id).first()
  
    @staticmethod
    def toDeleteTaux(id):
        try:
            taux = Model_Taux.objects.get(pk = id)
            taux.delete()
            return True
        except Exception as e:
            return False