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
from ModuleStock.dao.dao_categorie import dao_categorie


def run():
	print('--- Execution script importation des categories ---')
	import_categorie('liste_categories')

@transaction.atomic
def import_categorie(file_name):
	print('import_categorie() ...')
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
				name = makeString(df['name'][i])
				short_name = makeString(df['short_name'][i])
				code = makeString(df['code'][i])
				description = makeString(df['description'][i])
				societe_id = makeIntId(str(df['societe_id'][i]))

				categorie = dao_categorie.toCreate(name = name, short_name = short_name, code = code, description = description, societe_id = societe_id)
				saved, categorie, message = dao_categorie.toSave(auteur, categorie)

				if saved == False: raise Exception(message)

				print('CATEGORIE ID {} cree '.format(categorie.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT CATEGORIE')
		print(e)
		transaction.savepoint_rollback(sid)