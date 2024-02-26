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
from ModuleStock.dao.dao_emplacement import dao_emplacement


def run():
	print('--- Execution script importation des emplacements ---')
	import_emplacement('liste_emplacements')

@transaction.atomic
def import_emplacement(file_name):
	print('import_emplacement() ...')
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
				designation = makeString(df['designation'][i])
				designation_court = makeString(df['designation_court'][i])
				code = makeString(df['code'][i])
				description = makeString(df['description'][i])
				type_emplacement_id = makeIntId(str(df['type_emplacement_id'][i]))
				defaut = True if str(df['defaut'][i]) == 'True' else False
				societe_id = makeIntId(str(df['societe_id'][i]))
				visible = True if str(df['visible'][i]) == 'True' else False

				emplacement = dao_emplacement.toCreate(designation = designation, designation_court = designation_court, code = code, description = description, type_emplacement_id = type_emplacement_id, defaut = defaut, societe_id = societe_id, visible = visible)
				saved, emplacement, message = dao_emplacement.toSave(auteur, emplacement)

				if saved == False: raise Exception(message)

				print('EMPLACEMENT ID {} cree '.format(emplacement.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT EMPLACEMENT')
		print(e)
		transaction.savepoint_rollback(sid)