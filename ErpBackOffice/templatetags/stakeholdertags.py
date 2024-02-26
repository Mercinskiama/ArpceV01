from django import template
from ErpBackOffice.dao.dao_wkf_stakeholder import dao_wkf_stakeholder
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def transition_stakeholders(transition_id, content_type_id, objet_id):
    try:
        return dao_wkf_stakeholder.toListTransitionOfObject(transition_id, content_type_id, objet_id)        
    except Exception as e:
        print(e)
        return None