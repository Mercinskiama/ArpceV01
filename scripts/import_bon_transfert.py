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
from ModuleStock.dao.dao_bon_transfert import dao_bon_transfert


def run():
	print('--- Execution script importation des bon_transferts ---')
	import_bon_transfert('liste_bon_transferts')

@transaction.atomic
def import_bon_transfert(file_name):
	print('import_bon_transfert() ...')
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
				code = makeString(df['code'][i])
				societe_id = makeIntId(str(df['societe_id'][i]))
				emplacement_origine_id = makeIntId(str(df['emplacement_origine_id'][i]))
				emplacement_destination_id = makeIntId(str(df['emplacement_destination_id'][i]))
				status_id = makeIntId(str(df['status_id'][i]))
				operation_stock_id = makeIntId(str(df['operation_stock_id'][i]))
				description = makeString(df['description'][i])
				responsable_transfert_id = makeIntId(str(df['responsable_transfert_id'][i]))

				bon_transfert = dao_bon_transfert.toCreate(code = code, societe_id = societe_id, emplacement_origine_id = emplacement_origine_id, emplacement_destination_id = emplacement_destination_id, status_id = status_id, operation_stock_id = operation_stock_id, description = description, responsable_transfert_id = responsable_transfert_id)
				saved, bon_transfert, message = dao_bon_transfert.toSave(auteur, bon_transfert)

				if saved == False: raise Exception(message)

				print('BON_TRANSFERT ID {} cree '.format(bon_transfert.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT BON_TRANSFERT')
		print(e)
		transaction.savepoint_rollback(sid)