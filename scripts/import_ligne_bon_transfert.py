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
from ModuleStock.dao.dao_ligne_bon_transfert import dao_ligne_bon_transfert


def run():
	print('--- Execution script importation des ligne_bon_transferts ---')
	import_ligne_bon_transfert('liste_ligne_bon_transferts')

@transaction.atomic
def import_ligne_bon_transfert(file_name):
	print('import_ligne_bon_transfert() ...')
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
				quantite = makeFloat(df['quantite'][i])
				quantite_fait = makeFloat(df['quantite_fait'][i])
				article_id = makeIntId(str(df['article_id'][i]))
				if article_id in (None, '') : raise Exception('Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
				description = makeString(df['description'][i])
				societe_id = makeIntId(str(df['societe_id'][i]))
				fait = True if str(df['fait'][i]) == 'True' else False
				bon_transfert_id = makeIntId(str(df['bon_transfert_id'][i]))
				stockage_id = makeIntId(str(df['stockage_id'][i]))

				ligne_bon_transfert = dao_ligne_bon_transfert.toCreate(quantite = quantite, quantite_fait = quantite_fait, article_id = article_id, description = description, societe_id = societe_id, fait = fait, bon_transfert_id = bon_transfert_id, stockage_id = stockage_id)
				saved, ligne_bon_transfert, message = dao_ligne_bon_transfert.toSave(auteur, ligne_bon_transfert)

				if saved == False: raise Exception(message)

				print('LIGNE_BON_TRANSFERT ID {} cree '.format(ligne_bon_transfert.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT LIGNE_BON_TRANSFERT')
		print(e)
		transaction.savepoint_rollback(sid)