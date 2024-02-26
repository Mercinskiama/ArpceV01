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
from ModuleStock.dao.dao_article import dao_article


def run():
	print('--- Execution script importation des articles ---')
	import_article('liste_articles')

@transaction.atomic
def import_article(file_name):
	print('import_article() ...')
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
				code = makeString(df['code'][i])
				amount = makeFloat(df['amount'][i])
				devise_id = makeIntId(str(df['devise_id'][i]))
				type_article_id = makeIntId(str(df['type_article_id'][i]))
				societe_id = makeIntId(str(df['societe_id'][i]))
				quota_quantity = makeInt(df['quota_quantity'][i])
				category_id = makeIntId(str(df['category_id'][i]))
				measure_unit_id = makeIntId(str(df['measure_unit_id'][i]))
				description = makeString(df['description'][i])

				article = dao_article.toCreate(name = name, code = code, amount = amount, devise_id = devise_id, type_article_id = type_article_id, societe_id = societe_id, quota_quantity = quota_quantity, category_id = category_id, measure_unit_id = measure_unit_id, description = description)
				saved, article, message = dao_article.toSave(auteur, article)

				if saved == False: raise Exception(message)

				print('ARTICLE ID {} cree '.format(article.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT ARTICLE')
		print(e)
		transaction.savepoint_rollback(sid)