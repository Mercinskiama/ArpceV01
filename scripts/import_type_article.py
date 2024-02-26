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
from ModuleStock.dao.dao_type_article import dao_type_article


def run():
	print('--- Execution script importation des type_articles ---')
	import_type_article('liste_type_articles')

@transaction.atomic
def import_type_article(file_name):
	print('import_type_article() ...')
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
				if designation in (None, '') : raise Exception('Le Champ \'Designation\' est obligatoire, Veuillez le renseigner SVP!')
				est_service = True if str(df['est_service'][i]) == 'True' else False
				societe_id = makeIntId(str(df['societe_id'][i]))

				type_article = dao_type_article.toCreate(designation = designation, est_service = est_service, societe_id = societe_id)
				saved, type_article, message = dao_type_article.toSave(auteur, type_article)

				if saved == False: raise Exception(message)

				print('TYPE_ARTICLE ID {} cree '.format(type_article.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT TYPE_ARTICLE')
		print(e)
		transaction.savepoint_rollback(sid)