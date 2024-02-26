from __future__ import unicode_literals
from ErpBackOffice.models import Model_Operationnalisation_module
from django.utils import timezone
import datetime


class dao_operationnalisation_module(object):
		
	@staticmethod
	def toCheckValidity(module_id, date_operation):
		date_operation = date_operation[6:10] + '-' + date_operation[3:5] + '-' + date_operation[0:2]
		mdate = datetime.datetime.strptime(date_operation, "%Y-%m-%d").date()
		is_exist = Model_Operationnalisation_module.objects.filter(module_id = module_id).filter(est_active = True).filter(date_debut__lt=mdate, date_fin__gt=mdate).exists()
		return is_exist