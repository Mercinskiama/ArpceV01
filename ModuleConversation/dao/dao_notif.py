from __future__ import unicode_literals
from ErpBackOffice.models import Model_Notification
from django.utils import timezone

class dao_notif(object):
	id = 0
	text = ''
	url_piece_concernee = ''
	module_source = ''

	@staticmethod
	def toListNotification():
		return Model_Notification.objects.all().order_by('-id')
	@staticmethod

	@staticmethod
	def toGetNotification(id):
		try:
			return Model_Notification.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteNotification(id):
		try:
			notification = Model_Notification.objects.get(pk = id)
			notification.delete()
			return True
		except Exception as e:
			return False
	#NOTIF FROM MESSAGES
