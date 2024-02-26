from __future__ import unicode_literals
from ModuleArchivage.models import *
from ErpBackOffice.models import *
from ModuleConfiguration.models import *
from django.utils import timezone
from ErpBackOffice.utils.utils import utils
import traceback

class dao_dossier(object):
	designation = ''
	sequence = ''
	parent_id = None
	description = ''
	owner_read = False
	est_racine = False
	est_archivage = False
	write_groups = []
	read_groups = []

	@staticmethod
	def toList(query='', auteur=None):
		try:
			if query == '':
				if auteur == None or auteur.societe_id == None: return Model_Dossier.objects.all().order_by('creation_date')
				else: return Model_Dossier.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('creation_date').distinct()
			else:
				if auteur == None or auteur.societe_id == None: return Model_Dossier.objects.filter(Q(designation__icontains = query) | Q(sequence__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
				else: return Model_Dossier.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (Q(designation__icontains = query) | Q(sequence__icontains = query) | Q(description__icontains = query))).order_by('creation_date').distinct()			  	
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DOSSIER')
			#print(e)
			return []

	@staticmethod
	def toListAll(query=''):
		try:
			if query == '': return Model_Dossier.objects.all().order_by('creation_date')

			return Model_Dossier.objects.filter(Q(designation__icontains = query) | Q(sequence__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DOSSIER')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', sequence = '', parent_id = None, description = '', owner_read = None, est_racine = None, est_archivage = None, write_groups = [], read_groups = []):
		try:
			dossier = dao_dossier()
			dossier.designation = designation
			dossier.sequence = sequence
			dossier.parent_id = parent_id
			dossier.description = description
			dossier.owner_read = owner_read
			dossier.est_racine = est_racine
			dossier.est_archivage = est_archivage
			dossier.write_groups = write_groups
			dossier.read_groups = read_groups
			return dossier
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA DOSSIER')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_dossier, request_post = []):
		try:
			dossier  = Model_Dossier()
			dossier.designation = objet_dao_dossier.designation
			if objet_dao_dossier.sequence != None : dossier.sequence = objet_dao_dossier.sequence
			if objet_dao_dossier.parent_id != None : dossier.parent_id = objet_dao_dossier.parent_id
			if objet_dao_dossier.description != None : dossier.description = objet_dao_dossier.description
			if objet_dao_dossier.owner_read != None : dossier.owner_read = objet_dao_dossier.owner_read
			if objet_dao_dossier.est_racine != None : dossier.est_racine = objet_dao_dossier.est_racine
			if objet_dao_dossier.est_archivage != None : dossier.est_archivage = objet_dao_dossier.est_archivage
			if auteur != None : dossier.auteur_id = auteur.id

			dossier.save()

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_dossier.read_groups)):
				try:
					objet = Model_GroupePermission.objects.get(pk = objet_dao_dossier.read_groups[i])
					dossier.read_groups.add(objet)
				except Exception as e: pass

			#Ajout Champs (ManyToMany - Creation)
			for i in range(0, len(objet_dao_dossier.read_groups)):
				try:
					objet = Model_GroupePermission.objects.get(pk = objet_dao_dossier.read_groups[i])
					dossier.read_groups.add(objet)
				except Exception as e: pass
    
			#HISTORIQUE AJOUT
			if request_post != []:
				data={}
				data['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet
				data['valeur_avant'] = ''
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = 'Model_Dossier'
				utils.history_in_database(data)

			return True, dossier, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA DOSSIER')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_dossier, auteur = None, request_post = []):
		try:
			dossier = Model_Dossier.objects.get(pk = id)
			before_dossier = model_to_dict(dossier)
			dossier.designation = objet_dao_dossier.designation
			dossier.sequence = objet_dao_dossier.sequence
			dossier.parent_id = objet_dao_dossier.parent_id
			dossier.description = objet_dao_dossier.description
			dossier.owner_read = objet_dao_dossier.owner_read
			dossier.est_racine = objet_dao_dossier.est_racine
			dossier.est_archivage = objet_dao_dossier.est_archivage
			if auteur != None : dossier.update_by_id = auteur.id
			dossier.save()

			#Mise à jour Champs (ManyToMany - Creation)
			read_groups_old = dossier.read_groups.all()
			read_groups_updated = []
			for i in range(0, len(objet_dao_dossier.read_groups)):
				try:
					objet = Model_GroupePermission.objects.get(pk = objet_dao_dossier.read_groups[i])
					if objet not in read_groups_old: dossier.read_groups.add(objet)
					read_groups_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in read_groups_old:
				if item.id not in read_groups_updated: dossier.read_groups.remove(item)

			#Mise à jour Champs (ManyToMany - Creation)
			read_groups_old = dossier.read_groups.all()
			read_groups_updated = []
			for i in range(0, len(objet_dao_dossier.read_groups)):
				try:
					objet = Model_GroupePermission.objects.get(pk = objet_dao_dossier.read_groups[i])
					if objet not in read_groups_old: dossier.read_groups.add(objet)
					read_groups_updated.append(objet.id)
				except Exception as e: pass
			# Suppression éléments qui n'existent plus
			for item in read_groups_old:
				if item.id not in read_groups_updated: dossier.read_groups.remove(item)

			#HISTORIQUE MISE A JOUR
			if request_post != []:
				data={}
				data['auteur'] = "Unknown" if auteur == None else auteur.nom_complet
				data['valeur_avant'] = json.dumps(before_dossier, indent=4, sort_keys=True, default=str)
				data['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)
				data['modele'] = "Model_Dossier"
				utils.history_in_database(data)
   
			return True, dossier, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DOSSIER')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Dossier.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Dossier.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			dossier = Model_Dossier.objects.get(pk = id)
			dossier.delete()
			return True
		except Exception as e:
			return False