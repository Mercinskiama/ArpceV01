from __future__ import unicode_literals

from ErpBackOffice.models import Model_ActionUtilisateur, Model_ActionSousModule, Model_RoleAction

class dao_action_utilisateur(object):
    id = 0
    action_id = 0
    sous_module_id = 0
    role_id = 0
    auteur_id = 0

    @staticmethod
    def toListActionsAutorisees(sous_module_id, role_id):
        try:
            list = []
            actions_autorisees = Model_RoleAction.objects.filter(role_id = role_id)
            actions_du_sous_module = Model_ActionSousModule.objects.filter(sous_module_id = sous_module_id)
            for item in actions_autorisees:
                for action in actions_du_sous_module:
                    if item.action_id == action.id:
                        list.append(action)
                        break
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListActionsSousModuleNonAutrosees(sous_module_id, role_id):
        try:
            list = []
            actions_autorisees_au_sous_module = dao_action_utilisateur.toListActionsAutorisees(sous_module_id, role_id)
            actions_du_sous_module = dao_action_utilisateur.toListActionsOf(sous_module_id)

            for action in actions_du_sous_module:
                action_existant = False
                for item in actions_autorisees_au_sous_module:
                    if item.id == action.id:
                        action_existant = True
                        break
                if action_existant == False:
                    list.append(action)
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListActionsOf(sous_module_id):
        try:
            return Model_ActionSousModule.objects.filter(sous_module_id = sous_module_id)
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
    
    @staticmethod
    def toCreateRoleActionInSousModule(action_id, sous_module_id, role_id):
        try:
            action = dao_action_utilisateur()
            action.action_id = action_id
            action.role_id = role_id
            action.sous_module_id = sous_module_id
            return action
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ACTION")
            #print(e)
            return None

    @staticmethod
    def toSaveRoleActionInSousModule(auteur, object_dao_action_utilisateur):
        try:
            action_sous_module = Model_ActionSousModule.objects.filter(sous_module_id = object_dao_action_utilisateur.sous_module_id).get(action_id = object_dao_action_utilisateur.action_id)
            if action_sous_module == None :
                action_sous_module = Model_ActionSousModule()
                action_sous_module.action_id = object_dao_action_utilisateur.action_id
                action_sous_module.sous_module_id == object_dao_action_utilisateur.sous_module_id
                action_sous_module.save()
            role_action = Model_RoleAction()
            role_action.action_id = action_sous_module.id
            role_action.auteur_id = auteur.id
            role_action.role_id = object_dao_action_utilisateur.role_id
            role_action.save()
            return role_action
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    @staticmethod
    def toDeleteRoleActionInSousModule(id):
        try:
            role_action = Model_RoleAction.objects.get(pk = id)
            role_action.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False
  
    @staticmethod
    def toGetRoleActionInSousModule(id):
        try:
            return Model_RoleAction.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetActionDuSousModule(ref_action, sous_module_id):
        try:
            action = Model_ActionUtilisateur.objects.get(ref_action = ref_action.upper())
            return Model_ActionSousModule.objects.filter(action_id = action.id).get(sous_module_id = sous_module_id)
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None
        					
            