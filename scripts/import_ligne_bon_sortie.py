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
from ModuleStock.dao.dao_ligne_bon_sortie import dao_ligne_bon_sortie


def run():
	print('--- Execution script importation des ligne_bon_sorties ---')
	import_ligne_bon_sortie('liste_ligne_bon_sorties')

@transaction.atomic
def import_ligne_bon_sortie(file_name):
	print('import_ligne_bon_sortie() ...')
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
				quantite_demandee = makeFloat(df['quantite_demandee'][i])
				quantite_sortie = makeFloat(df['quantite_sortie'][i])
				serie_id = makeIntId(str(df['serie_id'][i]))
				description = makeString(df['description'][i])
				bon_sortie_id = makeIntId(str(df['bon_sortie_id'][i]))
				article_id = makeIntId(str(df['article_id'][i]))
				stockage_id = makeIntId(str(df['stockage_id'][i]))
				societe_id = makeIntId(str(df['societe_id'][i]))

				ligne_bon_sortie = dao_ligne_bon_sortie.toCreate(quantite_demandee = quantite_demandee, quantite_sortie = quantite_sortie, serie_id = serie_id, description = description, bon_sortie_id = bon_sortie_id, article_id = article_id, stockage_id = stockage_id, societe_id = societe_id)
				saved, ligne_bon_sortie, message = dao_ligne_bon_sortie.toSave(auteur, ligne_bon_sortie)

				if saved == False: raise Exception(message)

				print('LIGNE_BON_SORTIE ID {} cree '.format(ligne_bon_sortie.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT LIGNE_BON_SORTIE')
		print(e)
		transaction.savepoint_rollback(sid)