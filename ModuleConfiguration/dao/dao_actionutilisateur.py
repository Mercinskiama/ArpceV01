from __future__ import unicode_literals
from ErpBackOffice.models import Model_ActionUtilisateur
from django.utils import timezone

class dao_actionutilisateur(object):
	id = 0
	nom_action = ''
	ref_action = ''
	description = ''
	permission = None

	@staticmethod
	def toListActionutilisateur():
		return Model_ActionUtilisateur.objects.all().order_by("-id")

	@staticmethod
	def toCreateActionutilisateur(nom_action,ref_action,description,permission_id):
		try:
			actionutilisateur = dao_actionutilisateur()
			actionutilisateur.nom_action = nom_action
			actionutilisateur.ref_action = ref_action
			actionutilisateur.description = description
			actionutilisateur.permission_id = permission_id
			return actionutilisateur
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ACTIONUTILISATEUR')
			#print(e)
			return None

	@staticmethod
	def toSaveActionutilisateur(auteur, objet_dao_Actionutilisateur):
		try:
			actionutilisateur  = Model_ActionUtilisateur()
			actionutilisateur.nom_action = objet_dao_Actionutilisateur.nom_action
			actionutilisateur.ref_action = objet_dao_Actionutilisateur.ref_action
			actionutilisateur.description = objet_dao_Actionutilisateur.description
			actionutilisateur.permission_id = objet_dao_Actionutilisateur.permission_id
			actionutilisateur.auteur_id = auteur.id
			actionutilisateur.save()
			return actionutilisateur
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ACTIONUTILISATEUR')
			#print(e)
			return None

	@staticmethod
	def toUpdateActionutilisateur(id, objet_dao_Actionutilisateur):
		try:
			actionutilisateur = Model_ActionUtilisateur.objects.get(pk = id)
			actionutilisateur.nom_action =objet_dao_Actionutilisateur.nom_action
			actionutilisateur.ref_action =objet_dao_Actionutilisateur.ref_action
			actionutilisateur.description =objet_dao_Actionutilisateur.description
			actionutilisateur.permission_id =objet_dao_Actionutilisateur.permission_id
			actionutilisateur.save()
			return actionutilisateur
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ACTIONUTILISATEUR')
			#print(e)
			return None

	@staticmethod
	def toGetActionutilisateur(id):
		try:
			return Model_ActionUtilisateur.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetActionByName(nom_action):
		try:
			return Model_ActionUtilisateur.objects.filter(nom_action = nom_action).first()
		except Exception as e:
			return None

	@staticmethod
	def toDeleteActionutilisateur(id):
		try:
			actionutilisateur = Model_ActionUtilisateur.objects.get(pk = id)
			actionutilisateur.delete()
			return True
		except Exception as e:
			return False