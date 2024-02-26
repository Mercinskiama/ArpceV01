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
from ModuleStock.dao.dao_type_mvt_stock import dao_type_mvt_stock


def run():
	print('--- Execution script importation des type_mvt_stocks ---')
	import_type_mvt_stock('liste_type_mvt_stocks')

@transaction.atomic
def import_type_mvt_stock(file_name):
	print('import_type_mvt_stock() ...')
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

				type_mvt_stock = dao_type_mvt_stock.toCreate(designation = designation, societe_id = societe_id)
				saved, type_mvt_stock, message = dao_type_mvt_stock.toSave(auteur, type_mvt_stock)

				if saved == False: raise Exception(message)

				print('TYPE_MVT_STOCK ID {} cree '.format(type_mvt_stock.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT TYPE_MVT_STOCK')
		print(e)
		transaction.savepoint_rollback(sid)