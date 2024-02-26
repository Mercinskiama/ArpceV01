from __future__ import unicode_literals
from ErpBackOffice.models import Model_GroupeMenu
from django.utils import timezone

class dao_groupemenu(object):
	id = 0
	designation = ''
	icon_menu = ''
	description = ''
	module = None
	numero_ordre = 0

	@staticmethod
	def toListGroupemenu():
		return Model_GroupeMenu.objects.all()

	@staticmethod
	def toCreateGroupemenu(designation,icon_menu,description,module_id,numero_ordre):
		try:
			groupemenu = dao_groupemenu()
			groupemenu.designation = designation
			groupemenu.icon_menu = icon_menu
			groupemenu.description = description
			groupemenu.module_id = module_id
			groupemenu.numero_ordre = numero_ordre
			return groupemenu
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA GROUPEMENU')
			#print(e)
			return None

	@staticmethod
	def toSaveGroupemenu(auteur, objet_dao_Groupemenu):
		try:
			groupemenu  = Model_GroupeMenu()
			groupemenu.designation = objet_dao_Groupemenu.designation
			groupemenu.icon_menu = objet_dao_Groupemenu.icon_menu
			groupemenu.description = objet_dao_Groupemenu.description
			groupemenu.module_id = objet_dao_Groupemenu.module_id
			groupemenu.numero_ordre = objet_dao_Groupemenu.numero_ordre
			groupemenu.auteur_id = auteur.id
			groupemenu.save()
			return groupemenu
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA GROUPEMENU')
			#print(e)
			return None

	@staticmethod
	def toUpdateGroupemenu(id, objet_dao_Groupemenu):
		try:
			groupemenu = Model_GroupeMenu.objects.get(pk = id)
			groupemenu.designation =objet_dao_Groupemenu.designation
			groupemenu.icon_menu =objet_dao_Groupemenu.icon_menu
			groupemenu.description =objet_dao_Groupemenu.description
			groupemenu.module_id =objet_dao_Groupemenu.module_id
			groupemenu.numero_ordre =objet_dao_Groupemenu.numero_ordre
			groupemenu.save()
			return groupemenu
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA GROUPEMENU')
			#print(e)
			return None
	@staticmethod
	def toGetGroupemenu(id):
		try:
			return Model_GroupeMenu.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteGroupemenu(id):
		try:
			groupemenu = Model_GroupeMenu.objects.get(pk = id)
			groupemenu.delete()
			return True
		except Exception as e:
			return False