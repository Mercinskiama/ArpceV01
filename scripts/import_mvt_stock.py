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
from ModuleStock.dao.dao_mvt_stock import dao_mvt_stock


def run():
	print('--- Execution script importation des mvt_stocks ---')
	import_mvt_stock('liste_mvt_stocks')

@transaction.atomic
def import_mvt_stock(file_name):
	print('import_mvt_stock() ...')
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
				date = makeString(df['date'][i])
				if date in (None, '') : raise Exception('Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
			date = timezone.datetime(int(date[6:10]), int(date[3:5]), int(date[0:2]), int(date[11:13]), int(date[14:16]))
				type_id = makeIntId(str(df['type_id'][i]))
				if type_id in (None, '') : raise Exception('Le Champ \'Type mouvement\' est obligatoire, Veuillez le renseigner SVP!')
				article_id = makeIntId(str(df['article_id'][i]))
				if article_id in (None, '') : raise Exception('Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
				emplacement_id = makeIntId(str(df['emplacement_id'][i]))
				if emplacement_id in (None, '') : raise Exception('Le Champ \'Emplacement\' est obligatoire, Veuillez le renseigner SVP!')
				reception_id = makeIntId(str(df['reception_id'][i]))
				transfert_id = makeIntId(str(df['transfert_id'][i]))
				sortie_id = makeIntId(str(df['sortie_id'][i]))
				retour_id = makeIntId(str(df['retour_id'][i]))
				ajustement_id = makeIntId(str(df['ajustement_id'][i]))
				rebut_id = makeIntId(str(df['rebut_id'][i]))
				quantite_initiale = makeFloat(df['quantite_initiale'][i])
				unite_initiale_id = makeIntId(str(df['unite_initiale_id'][i]))
				quantite = makeFloat(df['quantite'][i])
				societe_id = makeIntId(str(df['societe_id'][i]))
				unite_id = makeIntId(str(df['unite_id'][i]))
				est_rebut = True if str(df['est_rebut'][i]) == 'True' else False

				mvt_stock = dao_mvt_stock.toCreate(date = date, type_id = type_id, article_id = article_id, emplacement_id = emplacement_id, reception_id = reception_id, transfert_id = transfert_id, sortie_id = sortie_id, retour_id = retour_id, ajustement_id = ajustement_id, rebut_id = rebut_id, quantite_initiale = quantite_initiale, unite_initiale_id = unite_initiale_id, quantite = quantite, societe_id = societe_id, unite_id = unite_id, est_rebut = est_rebut)
				saved, mvt_stock, message = dao_mvt_stock.toSave(auteur, mvt_stock)

				if saved == False: raise Exception(message)

				print('MVT_STOCK ID {} cree '.format(mvt_stock.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT MVT_STOCK')
		print(e)
		transaction.savepoint_rollback(sid)