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
from ModuleStock.dao.dao_rebut import dao_rebut


def run():
	print('--- Execution script importation des rebuts ---')
	import_rebut('liste_rebuts')

@transaction.atomic
def import_rebut(file_name):
	print('import_rebut() ...')
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
				numero = makeString(df['numero'][i])
				date = makeString(df['date'][i])
				if date in (None, '') : raise Exception('Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
			date = timezone.datetime(int(date[6:10]), int(date[3:5]), int(date[0:2]), int(date[11:13]), int(date[14:16]))
				article_id = makeIntId(str(df['article_id'][i]))
				serie_article = makeString(df['serie_article'][i])
				quantite = makeFloat(df['quantite'][i])
				societe_id = makeIntId(str(df['societe_id'][i]))
				status_id = makeIntId(str(df['status_id'][i]))
				unite_id = makeIntId(str(df['unite_id'][i]))
				emplacement_origine_id = makeIntId(str(df['emplacement_origine_id'][i]))
				emplacement_rebut_id = makeIntId(str(df['emplacement_rebut_id'][i]))
				document = makeString(df['document'][i])

				rebut = dao_rebut.toCreate(numero = numero, date = date, article_id = article_id, serie_article = serie_article, quantite = quantite, societe_id = societe_id, status_id = status_id, unite_id = unite_id, emplacement_origine_id = emplacement_origine_id, emplacement_rebut_id = emplacement_rebut_id, document = document)
				saved, rebut, message = dao_rebut.toSave(auteur, rebut)

				if saved == False: raise Exception(message)

				print('REBUT ID {} cree '.format(rebut.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT REBUT')
		print(e)
		transaction.savepoint_rollback(sid)