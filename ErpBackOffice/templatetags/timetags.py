from django import template
from datetime import datetime

register = template.Library()

@register.filter(name="timestamp_to_datetime")
def timestamp_to_datetime(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    date = datetime.fromtimestamp(ts)
    return date.strftime("%d/%m/%Y %H:%M:%S")

@register.filter(name="timestamp_to_date")
def timestamp_to_date(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    date = datetime.fromtimestamp(ts)
    return date.strftime("%d/%m/%Y")

