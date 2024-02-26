from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from datetime import time, timedelta, datetime, date
from django.utils import timezone
import json, random
from django.db import transaction
import pandas as pd
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId, makeString
from ErpBackOffice.models import Model_Personne

from ModuleStock.models import Model_Compte
from ModuleStock.dao.dao_ligne_ajustement import dao_ligne_ajustement


def run():
	print('--- Execution script importation des ligne_ajustements ---')
	import_ligne_ajustement('liste_ligne_ajustements')

@transaction.atomic
def import_ligne_ajustement(file_name):
	print('import_ligne_ajustement() ...')
	sid = transaction.savepoint()
	try:
		import_dir = settings.MEDIA_ROOT
		import_dir = import_dir + '/excel/'
		file_path = os.path.join(import_dir, str(file_name) + '.xlsx')
		if default_storage.exists(file_path):
			filename = default_storage.generate_filename(file_path)
			sheet = 'Sheet1'
			print('Sheet : {} file: {}'.format(sheet, filename))
			df = pd.read_excel(io=filename, sheet_name=sheet, engine='openpyxl')
			df = df.fillna('') #Replace all nan value

			auteur = Model_Personne.objects.get(pk = 7)

			for i in df.index:
				ajustement_id = makeIntId(str(df['ajustement_id'][i]))
				if ajustement_id in (None, '') : raise Exception('Le Champ \'Inventaire\' est obligatoire, Veuillez le renseigner SVP!')
				article_id = makeIntId(str(df['article_id'][i]))
				societe_id = makeIntId(str(df['societe_id'][i]))
				quantite_theorique = makeFloat(df['quantite_theorique'][i])
				quantite_reelle = makeFloat(df['quantite_reelle'][i])
				unite_id = makeIntId(str(df['unite_id'][i]))
				fait = True if str(df['fait'][i]) == 'True' else False

				ligne_ajustement = dao_ligne_ajustement.toCreate(ajustement_id = ajustement_id, article_id = article_id, societe_id = societe_id, quantite_theorique = quantite_theorique, quantite_reelle = quantite_reelle, unite_id = unite_id, fait = fait)
				saved, ligne_ajustement, message = dao_ligne_ajustement.toSave(auteur, ligne_ajustement)

				if saved == False: raise Exception(message)

				print('LIGNE_AJUSTEMENT ID {} cree '.format(ligne_ajustement.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT LIGNE_AJUSTEMENT')
		print(e)
		transaction.savepoint_rollback(sid)