from __future__ import unicode_literals
from ErpBackOffice.models import Model_Devise
from django.utils import timezone
from ErpBackOffice.models import Model_Taux


class dao_devise(object):
    id = 0
    symbole_devise = ""
    code_iso = ""
    designation = ""
    est_reference = False
    est_active = False
    auteur_id = 0

    @staticmethod
    def toListDevises():
        return Model_Devise.objects.all().order_by("designation")

    @staticmethod
    def toListDevisesActives():
        return Model_Devise.objects.filter(est_active = True).order_by("designation")

    @staticmethod
    def toCreateDevise(symbole_devise, code_iso, designation):
        try:
            devise = dao_devise()
            devise.symbole_devise = symbole_devise
            devise.code_iso = code_iso
            devise.designation = designation
            devise.est_active = False
            devise.est_reference = False
            devise.est_virtuelle = False
            return devise
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA DEVISE")
            #print(e)
            return None

    @staticmethod
    def toSaveDevise(auteur, objet_dao_devise):
        try:
            devise  = Model_Devise()
            devise.symbole_devise = objet_dao_devise.symbole_devise
            devise.code_iso = objet_dao_devise.code_iso
            devise.designation = objet_dao_devise.designation
            devise.est_active = objet_dao_devise.est_active
            devise.est_reference = objet_dao_devise.est_reference
            devise.auteur_id = auteur.id
            devise.creation_date = timezone.now()
            devise.save()
            return devise
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toUpdateDevise(id, objet_dao_devise):
        try:
            devise = Model_Devise.objects.get(pk = id)
            devise.symbole_devise = objet_dao_devise.symbole_devise
            devise.code_iso = objet_dao_devise.code_iso
            devise.designation = objet_dao_devise.designation
            devise.est_active = objet_dao_devise.est_active
            devise.est_reference = objet_dao_devise.est_reference
            devise.save()
            return devise
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toActiveDevise(id, est_active):
        try:
            devise = Model_Devise.objects.get(pk = id)
            devise.est_active = est_active
            devise.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetDevise(id):
        try:
            return Model_Devise.objects.get(pk = id)
        except Exception as e:
            return None
        
    @staticmethod
    def toGetDeviseByCode(code):
        try:
            return Model_Devise.objects.get(code_iso = code)
        except Exception as e:
            return None
        
    @staticmethod
    def toGetDeviseVirtuelle():
        return Model_Devise.objects.filter(est_virtuelle = True).first()

    @staticmethod
    def toGetDeviseReference():
        try:
            return Model_Devise.objects.get(est_reference = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetTauxByDeviseReference():
        try:
            devise = Model_Devise.objects.get(est_reference = True)
            taux_ref = Model_Taux.objects.filter(devise_depart_id = devise.id).filter(est_courant=True).first()
            #print('**Le taux de reference ** %s' %taux_ref.montant)
            return taux_ref.montant
        except Exception as e:
            return 0

    @staticmethod
    def toDeleteDevise(id):
        try:
            devise = Model_Devise.objects.get(pk = id)
            devise.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toReferenceDevise(id):
        try:
            Model_Devise.objects.all().update(est_reference = False)

            devise = dao_devise.toGetDevise(id)
            devise.est_reference = True
            devise.save()
            return True
        except Exception as e:
            #print("ERREUR DU UPDATE")
            #print(e)
            return False
