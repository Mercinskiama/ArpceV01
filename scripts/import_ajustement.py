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
from ModuleStock.dao.dao_ajustement import dao_ajustement


def run():
	print('--- Execution script importation des ajustements ---')
	import_ajustement('liste_ajustements')

@transaction.atomic
def import_ajustement(file_name):
	print('import_ajustement() ...')
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
				reference = makeString(df['reference'][i])
				date = makeString(df['date'][i])
				if date in (None, '') : raise Exception('Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
			date = timezone.datetime(int(date[6:10]), int(date[3:5]), int(date[0:2]), int(date[11:13]), int(date[14:16]))
				societe_id = makeIntId(str(df['societe_id'][i]))
				emplacement_id = makeIntId(str(df['emplacement_id'][i]))
				if emplacement_id in (None, '') : raise Exception('Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')
				status_id = makeIntId(str(df['status_id'][i]))
				inventaire_de = makeInt(df['inventaire_de'][i])
				document = makeString(df['document'][i])

				ajustement = dao_ajustement.toCreate(reference = reference, date = date, societe_id = societe_id, emplacement_id = emplacement_id, status_id = status_id, inventaire_de = inventaire_de, document = document)
				saved, ajustement, message = dao_ajustement.toSave(auteur, ajustement)

				if saved == False: raise Exception(message)

				print('AJUSTEMENT ID {} cree '.format(ajustement.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT AJUSTEMENT')
		print(e)
		transaction.savepoint_rollback(sid)