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
from ModuleStock.dao.dao_ligne_reception import dao_ligne_reception


def run():
	print('--- Execution script importation des ligne_receptions ---')
	import_ligne_reception('liste_ligne_receptions')

@transaction.atomic
def import_ligne_reception(file_name):
	print('import_ligne_reception() ...')
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
				bon_reception_id = makeIntId(str(df['bon_reception_id'][i]))
				if bon_reception_id in (None, '') : raise Exception('Le Champ \'Opération stock\' est obligatoire, Veuillez le renseigner SVP!')
				article_id = makeIntId(str(df['article_id'][i]))
				if article_id in (None, '') : raise Exception('Le Champ \'Article\' est obligatoire, Veuillez le renseigner SVP!')
				societe_id = makeIntId(str(df['societe_id'][i]))
				quantite_demandee = makeFloat(df['quantite_demandee'][i])
				quantite_fait = makeFloat(df['quantite_fait'][i])
				quantite_reste = makeFloat(df['quantite_reste'][i])
				prix_unitaire = makeFloat(df['prix_unitaire'][i])
				unite_id = makeIntId(str(df['unite_id'][i]))
				devise_id = makeIntId(str(df['devise_id'][i]))
				description = makeString(df['description'][i])
				fait = True if str(df['fait'][i]) == 'True' else False

				ligne_reception = dao_ligne_reception.toCreate(bon_reception_id = bon_reception_id, article_id = article_id, societe_id = societe_id, quantite_demandee = quantite_demandee, quantite_fait = quantite_fait, quantite_reste = quantite_reste, prix_unitaire = prix_unitaire, unite_id = unite_id, devise_id = devise_id, description = description, fait = fait)
				saved, ligne_reception, message = dao_ligne_reception.toSave(auteur, ligne_reception)

				if saved == False: raise Exception(message)

				print('LIGNE_RECEPTION ID {} cree '.format(ligne_reception.id))
			transaction.savepoint_commit(sid)
		else: print('Fichier Excel non trouvé')
	except Exception as e:
		print('ERREUR IMPORT LIGNE_RECEPTION')
		print(e)
		transaction.savepoint_rollback(sid)