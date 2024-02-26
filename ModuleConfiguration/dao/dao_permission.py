from __future__ import unicode_literals
from ErpBackOffice.models import Model_Permission, Model_GroupePermission
from django.utils import timezone

class dao_permission(object):
	id = 0
	sous_module = None
	designation = ''
	numero = 0

	@staticmethod
	def toListPermission():
		return Model_Permission.objects.filter(sous_module__module__id=12).order_by("-id")

	
	@staticmethod
	def toListPermissions():
		return Model_Permission.objects.all().order_by("-id")

	@staticmethod
	def toGetLatestNumeroOrdre():
		return Model_Permission.objects.last().numero
    
	@staticmethod
	def toListPermissionsOfModule(module_id):
		return Model_Permission.objects.filter(sous_module__module_id = module_id)
    
    
	@staticmethod
	def toListPermissionsNonAutorizeOfSousModule(groupe_id, sous_module_id):
		try:
			list = []
			permissions = Model_Permission.objects.filter(sous_module_id = sous_module_id)
			for item in permissions :
                
				if not Model_GroupePermission.objects.filter(permissions__id = item.id, pk=groupe_id).first():
					list.append(item)
                
			return list
		except Exception as e:
			return []
    
	@staticmethod
	def toListPermissionsOfSousModule(sous_module_id):
		try:
			permissions = Model_Permission.objects.filter(sous_module_id = sous_module_id)
			return permissions
		except Exception as e:
			return []


	@staticmethod
	def toCreatePermission(sous_module_id,designation,numero):
		try:
			permission = dao_permission()
			permission.sous_module_id = sous_module_id
			permission.designation = designation
			permission.numero = numero
			return permission
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PERMISSION')
			#print(e)
			return None

	@staticmethod
	def toSavePermission(auteur, objet_dao_Permission):
		try:
			permission  = Model_Permission()
			permission.sous_module_id = objet_dao_Permission.sous_module_id
			permission.designation = objet_dao_Permission.designation
			permission.numero = objet_dao_Permission.numero
			permission.auteur_id = auteur.id
			permission.save()
			return permission
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PERMISSION')
			#print(e)
			return None

	@staticmethod
	def toUpdatePermission(id, objet_dao_Permission):
		try:
			permission = Model_Permission.objects.get(pk = id)
			permission.sous_module_id =objet_dao_Permission.sous_module_id
			permission.designation =objet_dao_Permission.designation
			permission.numero =objet_dao_Permission.numero
			permission.save()
			return permission
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PERMISSION')
			#print(e)
			return None
	@staticmethod
	def toGetPermission(id):
		try:
			return Model_Permission.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeletePermission(id):
		try:
			permission = Model_Permission.objects.get(pk = id)
			permission.delete()
			return True
		except Exception as e:
			return False