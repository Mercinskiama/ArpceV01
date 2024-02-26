from __future__ import unicode_literals
from ErpBackOffice.models import Model_Notification, Model_Temp_Notification
from django.utils import timezone

class dao_notification(object):
	id = 0
	user_id = None
	est_lu = False
	message_id = None
	text = ''
	url_piece_concernee = ''

	@staticmethod
	def toListNotification():
		return Model_Notification.objects.all().order_by('-id')
	@staticmethod
	def toListAllReceiverOfAMessage(message__id):
		return Model_Notification.objects.filter(message__id = message__id)
	@staticmethod
	def toListNotificationByUser(user_id):
		return Model_Notification.objects.filter(user_id=user_id).order_by('-created_at')[:3]
	@staticmethod
	def toListMessageByUserFull(destinataire_id):
		#print(destinataire_id)
		model = Model_Notification.objects.all().prefetch_related('message')
		return model

	@staticmethod
	def toCreateNotification(user_id,est_lu,message_id,text,url_piece_concernee):
		try:
			notification = dao_notification()
			notification.user_id = user_id
			notification.est_lu = est_lu
			notification.message_id = message_id
			notification.text = text
			notification.url_piece_concernee = url_piece_concernee
			return notification
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA NOTIFICATION')
			#print(e)
			return None

	@staticmethod
	def toSaveNotification(auteur, objet_dao_Notification):
		try:
			#print(auteur.id)
			#print(objet_dao_Notification)

			notification  = Model_Notification()
			notification.user_id = objet_dao_Notification.user_id
			notification.est_lu = objet_dao_Notification.est_lu
			notification.message_id = objet_dao_Notification.message_id
			notification.text = objet_dao_Notification.text
			notification.url_piece_concernee = objet_dao_Notification.url_piece_concernee
			notification.created_at = timezone.now()
			notification.updated_at = timezone.now()
			notification.auteur_id = auteur.id

			notification.save()
			return notification
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA NOTIFICATION')
			#print(e)
			return None

	@staticmethod
	def toUpdateNotification(id, objet_dao_Notification):
		try:
			notification = Model_Notification.objects.get(pk = id)
			notification.user_id =objet_dao_Notification.user_id
			notification.est_lu =objet_dao_Notification.est_lu
			notification.message_id =objet_dao_Notification.message_id
			notification.text =objet_dao_Notification.text
			notification.url_piece_concernee =objet_dao_Notification.url_piece_concernee
			notification.updated_at = timezone.now()
			notification.save()
			return notification
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA NOTIFICATION')
			#print(e)
			return None
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
	@staticmethod
	def toCountNotificationUnread(user_id):
		try:
			notif = Model_Notification.objects.filter(user_id = user_id).filter(est_lu = False).exclude(auteur_id = None)
			return notif.count()
		except Exception as e:
			return None
	@staticmethod
	def toGetListNotificationHeader(user_id):
		try:
			return Model_Notification.objects.filter(user_id = user_id).filter(est_lu = False).exclude(auteur_id = None).order_by('-created_at')[:3]
		except Exception as e:
			return None
	#SIGNAL NOTIFICATION
	@staticmethod
	def toCountSystemNotificationUnread(user_id):
		try:
			notif = Model_Notification.objects.filter(auteur_id = None).filter(user_id = user_id)
			return notif.count()
		except Exception as e:
			return None
	@staticmethod
	def toGetListSystemNotificationHeader(user_id):
		try:
			return Model_Notification.objects.filter(user_id = None).filter(est_lu = False).filter(user_id = user_id).order_by('-created_at')[:3]
		except Exception as e:
			return None
	@staticmethod
	def toUpdateMessageRead(user_id,message_id):
		try:
			notification = Model_Notification.objects.filter(user_id=user_id).get(message__id = message_id)
			#print(notification.est_lu)
			notification.est_lu = True
			notification.save()
			#print(notification.est_lu)
			#print(notification.text)
			return notification
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA NOTIFICATION')
			#print(e)
			return None