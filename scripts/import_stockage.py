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
from ModuleStock.dao.dao_stockage import dao_stockage


def run():
	print('--- Execution script importation des stockages ---')
	import_stockage('liste_stockages')

@transaction.atomic
def import_stockage(file_name):
	print('import_stockage() ...')
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
				emplacement_id = makeIntId(str(df['emplacement_id'][i]))
				if emplacement_id in (None, '') : raise Exception('Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')
				article_id = makeIntId(str(df['article_id'][i]))
				if article_id in (None, '') : raise Exception('Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
				quantite = makeFloat(df['quantite'][i])
				unite_id = makeIntId(str(df['unite_id'][i]))
				societe_id = makeIntId(str(df['societe_id'][i]))

				stockage = dao_stockage.toCreate(emplacement_id = emplacement_id, article_id = article_id, quantite = quantite, unite_id = unite_id, societe_id = societe_id)
				saved, stockage, message = dao_stockage.toSave(auteur, stockage)

				if saved == False: raise Exception(message)

				print('STOCKAGE ID {} cree '.format(stockage.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT STOCKAGE')
		print(e)
		transaction.savepoint_rollback(sid)