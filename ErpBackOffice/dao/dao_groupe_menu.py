from __future__ import unicode_literals
from ErpBackOffice.models import Model_GroupeMenu
from django.utils import timezone


class dao_groupe_menu(object):
    id = 0
    designation = ""
    icon_menu = ""
    description = ""
    module_id = None

    @staticmethod
    def toListGroupeMenus():
        return Model_GroupeMenu.objects.all().order_by("numero_ordre")
    
    @staticmethod
    def toListGroupeOfModule(module_id):
        try:
            groupe_menu = Model_GroupeMenu.objects.filter(module_id = module_id).order_by("numero_ordre")
            return groupe_menu
        except Exception as e:
            #print("ERREUR LORS DE LA RECUPERATION DU GROUPE MENU")
            #print(e)
            return []

    @staticmethod
    def toGetGroupeRapportOfModule(module_id):
        try:
            groupe_menu = Model_GroupeMenu.objects.filter(module_id = module_id, designation = "Rapports").first()
            return groupe_menu
        except Exception as e:
            #print("ERREUR LORS DE LA RECUPERATION DU GROUPE MENU")
            #print(e)
            return None
        
    @staticmethod
    def toGetGroupeAnalyseOfModule(module_id):
        try:
            groupe_menu = Model_GroupeMenu.objects.filter(module_id = module_id, designation = "Analyses").first()
            return groupe_menu
        except Exception as e:
            #print("ERREUR LORS DE LA RECUPERATION DU GROUPE MENU")
            #print(e)
            return None

    @staticmethod
    def toGetGroupeConfigOfModule(module_id):
        try:
            groupe_menu = Model_GroupeMenu.objects.filter(module_id = module_id, designation = "Configurations").first()
            return groupe_menu
        except Exception as e:
            #print("ERREUR LORS DE LA RECUPERATION DU GROUPE MENU")
            #print(e)
            return None
        
    @staticmethod
    def toGetGroupeByNameOfModule(module_id, designation):
        try:
            groupe_menu = Model_GroupeMenu.objects.filter(module_id = module_id, designation = designation).first()
            return groupe_menu
        except Exception as e:
            #print("ERREUR LORS DE LA RECUPERATION DU GROUPE MENU")
            #print(e)
            return None
        
    @staticmethod
    def toCreateGroupeMenu(designation, icon_menu, description, module_id):
        try:
            groupe_menu = dao_groupe_menu()
            groupe_menu.designation = designation
            groupe_menu.icon_menu = icon_menu
            groupe_menu.description = description
            groupe_menu.module_id = module_id
            return groupe_menu
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU GROUPE MENU")
            #print(e)
            return None

    @staticmethod
    def toSaveGroupeMenu(auteur, objet_dao_groupe_menu):
        try:
            groupe_menu  = Model_GroupeMenu()
            groupe_menu.designation = objet_dao_groupe_menu.designation
            groupe_menu.icon_menu = objet_dao_groupe_menu.icon_menu
            groupe_menu.description = objet_dao_groupe_menu.description
            groupe_menu.module_id = objet_dao_groupe_menu.module_id
            groupe_menu.auteur_id = auteur.id
            groupe_menu.creation_date = timezone.now()
            groupe_menu.save()
            return groupe_menu
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toUpdateGroupeMenu(id, objet_dao_groupe_menu):
        try:
            groupe_menu = Model_GroupeMenu.objects.get(pk = id)
            groupe_menu.designation = objet_dao_groupe_menu.designation
            groupe_menu.icon_menu = objet_dao_groupe_menu.icon_menu
            groupe_menu.description = objet_dao_groupe_menu.description
            groupe_menu.module_id = objet_dao_groupe_menu.module_id
            groupe_menu.save()
            return groupe_menu
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toGetGroupeMenu(id):
        try:
            return Model_GroupeMenu.objects.get(pk = id)
        except Exception as e:
            return None
    

    @staticmethod
    def toDeleteGroupeMenu(id):
        try:
            groupe_menu = Model_GroupeMenu.objects.get(pk = id)
            groupe_menu.delete()
            return True
        except Exception as e:
            return False