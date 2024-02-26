from __future__ import unicode_literals

from ErpBackOffice.models import Model_Civilite

class dao_civilite(object):
    id = 0
    designation = ""
    designation_court = ""

    @staticmethod
    def toCreateCivilite(designation,designation_court):
        try:
            civilite = dao_civilite()
            civilite.designation = designation
            civilite.designation_court = designation_court
            return civilite
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None
        
    @staticmethod
    def toSaveCivilite(dao_civilite_object):
        try:
            civilite = Model_Civilite()
            civilite.designation = dao_civilite_object.designation
            civilite.designation_court = dao_civilite_object.designation_court
            civilite.save()
            return civilite
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    @staticmethod
    def toUpdateCivilite(id,dao_civilite_object):
        try:
            civilite = Model_Civilite.objects.get(pk = id)
            civilite.designation = dao_civilite_object.designation
            civilite.designation_court = dao_civilite_object.designation_court
            civilite.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR")
            #print(e)
            return False

    @staticmethod
    def toDeleteCivilite(id,dao_civilite_object):
        try:
            civilite = Model_Civilite.objects.get(pk=id)
            civilite.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return None

    @staticmethod
    def toListCivilite():
        try:
            return Model_Civilite.objects.all().order_by("designation")
        except Exception as e:
            #print("ERREUR LORS DE L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetCivilite(id):
        try:
            return Model_Civilite.objects.get(pk = id)
        except Exception as e:
            #print("ERR")
            #print(e)
            return None
       
        
        


    