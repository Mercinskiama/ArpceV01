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
from ModuleStock.dao.dao_statut_operation_stock import dao_statut_operation_stock


def run():
	print('--- Execution script importation des statut_operation_stocks ---')
	import_statut_operation_stock('liste_statut_operation_stocks')

@transaction.atomic
def import_statut_operation_stock(file_name):
	print('import_statut_operation_stock() ...')
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
				societe_id = makeIntId(str(df['societe_id'][i]))

				statut_operation_stock = dao_statut_operation_stock.toCreate(designation = designation, societe_id = societe_id)
				saved, statut_operation_stock, message = dao_statut_operation_stock.toSave(auteur, statut_operation_stock)

				if saved == False: raise Exception(message)

				print('STATUT_OPERATION_STOCK ID {} cree '.format(statut_operation_stock.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT STATUT_OPERATION_STOCK')
		print(e)
		transaction.savepoint_rollback(sid)