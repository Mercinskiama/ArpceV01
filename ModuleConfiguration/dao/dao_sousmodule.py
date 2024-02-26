from __future__ import unicode_literals
from ErpBackOffice.models import Model_SousModule
from django.utils import timezone

class dao_sousmodule(object):
	id = 0
	module = None
	nom_sous_module = ''
	description = ''
	groupe = None
	icon_menu = ''
	url_vers = ''
	numero_ordre = ''
	est_model = False
	est_dashboard = False
	est_actif = False
	model_principal = None
	groupe_menu = None

	@staticmethod
	def toListSousmodule():
		return Model_SousModule.objects.all().order_by("-id")

	@staticmethod
	def toListSousmoduleActif():
		return Model_SousModule.objects.filter(est_actif = True).order_by("-id")

	@staticmethod
	def toCreateSousmodule(module_id, nom_sous_module, description, groupe, icon_menu, url_vers, numero_ordre, est_model, est_dashboard, est_actif, model_principal_id, groupe_menu_id):
		try:
			sousmodule = dao_sousmodule()
			sousmodule.module_id = module_id
			sousmodule.nom_sous_module = nom_sous_module
			sousmodule.description = description
			sousmodule.groupe = groupe
			sousmodule.icon_menu = icon_menu
			sousmodule.url_vers = url_vers
			sousmodule.numero_ordre = numero_ordre
			sousmodule.est_model = est_model
			sousmodule.est_dashboard = est_dashboard
			sousmodule.est_actif = est_actif
			sousmodule.model_principal_id = model_principal_id
			sousmodule.groupe_menu_id = groupe_menu_id
			return sousmodule
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA SOUSMODULE')
			print(e)
			return None

	@staticmethod
	def toSaveSousmodule(auteur, objet_dao_Sousmodule):
		try:
			sousmodule  = Model_SousModule()
			sousmodule.module_id = objet_dao_Sousmodule.module_id
			sousmodule.nom_sous_module = objet_dao_Sousmodule.nom_sous_module
			sousmodule.description = objet_dao_Sousmodule.description
			sousmodule.groupe = objet_dao_Sousmodule.groupe
			sousmodule.icon_menu = objet_dao_Sousmodule.icon_menu
			sousmodule.url_vers = objet_dao_Sousmodule.url_vers
			sousmodule.numero_ordre = objet_dao_Sousmodule.numero_ordre
			sousmodule.est_model = objet_dao_Sousmodule.est_model
			sousmodule.est_dashboard = objet_dao_Sousmodule.est_dashboard
			sousmodule.est_actif = objet_dao_Sousmodule.est_actif
			sousmodule.model_principal_id = objet_dao_Sousmodule.model_principal_id
			sousmodule.groupe_menu_id = objet_dao_Sousmodule.groupe_menu_id
			sousmodule.auteur_id = auteur.id
			sousmodule.save()
			return sousmodule
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA SOUSMODULE')
			print(e)
			return None

	@staticmethod
	def toUpdateSousmodule(id, objet_dao_Sousmodule):
		try:
			sousmodule = Model_SousModule.objects.get(pk = id)
			sousmodule.module_id =objet_dao_Sousmodule.module_id
			sousmodule.nom_sous_module =objet_dao_Sousmodule.nom_sous_module
			sousmodule.description =objet_dao_Sousmodule.description
			sousmodule.groupe =objet_dao_Sousmodule.groupe
			sousmodule.icon_menu =objet_dao_Sousmodule.icon_menu
			sousmodule.url_vers =objet_dao_Sousmodule.url_vers
			sousmodule.numero_ordre =objet_dao_Sousmodule.numero_ordre
			sousmodule.est_model =objet_dao_Sousmodule.est_model
			sousmodule.est_dashboard =objet_dao_Sousmodule.est_dashboard
			sousmodule.est_actif =objet_dao_Sousmodule.est_actif
			sousmodule.model_principal_id =objet_dao_Sousmodule.model_principal_id
			sousmodule.groupe_menu_id =objet_dao_Sousmodule.groupe_menu_id
			sousmodule.save()
			return sousmodule
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SOUSMODULE')
			#print(e)
			return None
	@staticmethod
	def toGetSousmodule(id):
		try:
			return Model_SousModule.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteSousmodule(id):
		try:
			sousmodule = Model_SousModule.objects.get(pk = id)
			sousmodule.delete()
			return True
		except Exception as e:
			return False