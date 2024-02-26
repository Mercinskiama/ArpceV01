from __future__ import unicode_literals
from ErpBackOffice.models import Model_Temp_Notification
from django.utils import timezone

class dao_temp_notification(object):
	id = 0
	user_id = None
	notification_id = None
	est_lu = False

	@staticmethod
	def toListTempNotification():
		return Model_Temp_Notification.objects.all().order_by('-id')


	@staticmethod
	def toGetTempNotification(id):
		try:
			return Model_Temp_Notification.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteTempNotification(id):
		try:
			notification = Model_Temp_Notification.objects.get(pk = id)
			notification.delete()
			return True
		except Exception as e:
			return False
	#NOTIF FROM MESSAGES
	@staticmethod
	def toCountTempNotificationUnread(user_id, module_name):
		try:
			notif_count = Model_Temp_Notification.objects.filter(user_id = user_id, notification__module_source = module_name, est_lu = False).count()
			return notif_count
		except Exception as e:
			return 0

	@staticmethod
	def toGetListTempNotificationUnread(user_id, module_name):
		try:
			return Model_Temp_Notification.objects.filter(user_id = user_id, notification__module_source = module_name, est_lu = False).order_by('-created_at')[:3]
		except Exception as e:
			return []

	@staticmethod
	def toGetListTempNotificationRead(user_id, module_name):
		try:
			return Model_Temp_Notification.objects.filter(user_id = user_id, notification__module_source = module_name, est_lu = True).order_by('-created_at')
		except Exception as e:
			return []

	@staticmethod
	def toGetListTempNotification(user_id, module_name):
		try:
			return Model_Temp_Notification.objects.filter(user_id = user_id, notification__module_source = module_name).order_by('-created_at')
		except Exception as e:
			return []

	@staticmethod
	def toCountNotificationUnread(user_id):
		try:
			notif_count = Model_Temp_Notification.objects.filter(user_id = user_id, est_lu = False).count()
			return notif_count
		except Exception as e:
			return 0

	@staticmethod
	def toListNotificationUnread(user_id):
		try:
			return Model_Temp_Notification.objects.filter(user_id = user_id, est_lu = False).order_by('-created_at')
		except Exception as e:
			return []

	@staticmethod
	def toListNotification(user_id):
		try:
			return Model_Temp_Notification.objects.filter(user_id = user_id).order_by('-created_at')
		except Exception as e:
			return []

	@staticmethod
	def toCountNotification(user_id):
		try:
			notif_count = Model_Temp_Notification.objects.filter(user_id = user_id).count()
			return notif_count
		except Exception as e:
			return 0

	@staticmethod
	def toUpdateTempNotificationRead(id):
		try:
			temp_notification = Model_Temp_Notification.objects.get(pk = id)
			temp_notification.est_lu = True
			temp_notification.save()
			return temp_notification
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA NOTIFICATION')
			#print(e)
			return None