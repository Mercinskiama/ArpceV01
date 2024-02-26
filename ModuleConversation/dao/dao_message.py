from __future__ import unicode_literals
from ErpBackOffice.models import Model_Message
from django.utils import timezone
from ModuleConversation.dao.dao_notification import dao_notification

class dao_message(object):
	id = 0
	objet = ''
	corps = ''
	type = ''
	destinataire_id = None
	expediteur_id = None
	status = ''
	document_id = None

	@staticmethod
	def toListMessage():
		return Model_Message.objects.all().order_by('-id')
	@staticmethod
	def toListMessageByUser(destinataire_id):
		#print(destinataire_id)
		return Model_Message.objects.filter(model_notification__user_id=destinataire_id).order_by('-created_at')[:3]
	@staticmethod
	def toListMessageByUserFull(destinataire_id):
		#print(destinataire_id)
		return Model_Message.objects.filter(model_notification__user_id=destinataire_id).order_by('-created_at')
	@staticmethod
	def toListMessageSentByUserFull(expediteur_id):
		#print(expediteur_id)
		return Model_Message.objects.filter(expediteur_id=expediteur_id).order_by('-created_at')

	@staticmethod
	def toCreateMessage(objet,corps,type,destinataire_id,expediteur_id,status,document_id):
		try:
			message = dao_message()
			message.objet = objet
			message.corps = corps
			message.type = type
			message.destinataire_id = destinataire_id
			message.expediteur_id = expediteur_id
			message.status = status
			#message.document_id = document_id
			return message
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA MESSAGE')
			#print(e)
			return None

	@staticmethod
	def toSaveMessage(auteur, objet_dao_Message):
		try:
			#print(auteur.id)
			#print("dao_message")
			message  = Model_Message()
			message.objet = objet_dao_Message.objet
			message.corps = objet_dao_Message.corps
			message.type = objet_dao_Message.type
			message.destinataire_id = objet_dao_Message.destinataire_id
			message.expediteur_id = objet_dao_Message.expediteur_id
			message.status = objet_dao_Message.status
			#message.document_id = objet_dao_Message.document_id
			message.created_at = timezone.now()
			message.updated_at = timezone.now()
			message.auteur_id = auteur.id

			message.save()
			#Creation d'une notification
			notification = dao_notification()
			unenotification = notification.toCreateNotification(message.destinataire_id,False,message.id,message.corps[:90],None)
			unenotification = notification.toSaveNotification(auteur,unenotification)
			return message
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA MESSAGE')
			#print(e)
			return None

	@staticmethod
	def toUpdateMessage(id, objet_dao_Message):
		try:
			message = Model_Message.objects.get(pk = id)
			message.objet =objet_dao_Message.objet
			message.corps =objet_dao_Message.corps
			message.type =objet_dao_Message.type
			message.destinataire_id =objet_dao_Message.destinataire_id
			message.expediteur_id =objet_dao_Message.expediteur_id
			message.status =objet_dao_Message.status
			#message.document_id =objet_dao_Message.document_id
			message.updated_at = timezone.now()
			message.save()
			return message
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA MESSAGE')
			#print(e)
			return None
	@staticmethod
	def toGetMessage(id):
		try:
			return Model_Message.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteMessage(id):
		try:
			message = Model_Message.objects.get(pk = id)
			message.delete()
			return True
		except Exception as e:
			return False
	@staticmethod
	def toGetMessageOfEmploye(destinataire_id):
		try:
			return Model_Message.objects.filter(model_notification__user_id = destinataire_id)
		except Exception as e:
			return None
