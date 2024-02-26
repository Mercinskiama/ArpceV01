from __future__ import unicode_literals

from ErpBackOffice.models import Model_UserSessions, Model_Personne
from django.contrib.sessions.models import Session
from django.utils import timezone

class dao_session(object):
    
    @staticmethod
    def processingUniqueSession(request):
        session = Session.objects.get(session_key=request.session.session_key)
        usings = Model_UserSessions.objects.filter(user = request.user, is_active = True).exclude(session = session)
        #On efface les sessions anterieurs de ce gars
        for using in usings:
            session = using.session
            session.delete() #ceci efface en cascade le model user session too
    
    
    @staticmethod
    def toListUtilisateurConnected():
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []
        # Build a list of user ids from that query
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))

        # Query all logged in users based on id list
        return Model_Personne.objects.filter(user_id__in=uid_list).order_by("-user__last_login")
        #queryset2 =  Model_Personne.objects.exclude(user_id__in=uid_list).order_by("-user__last_login")