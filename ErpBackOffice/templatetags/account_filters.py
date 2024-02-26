from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId

register = template.Library()

@register.filter(name='monetary_rounded')
def monetary_rounded(amount):
    amount = makeFloat(amount)
    amount = round(float(amount), 2)
    #return "%s%s%s" % (intcomma(int(amount)).replace(',',' '), ",", ("%0.2f" % amount)[-2:])
    return "%s%s%s" % (intcomma(int(amount)).replace('.',' '), ",", ("%0.2f" % amount)[-2:])

@register.filter(name='monetary')
def monetary(amount):
    #return "%s" % (intcomma(amount).replace(',',' ').replace('.',','))
    amount = makeFloat(amount)
    amount = round(float(amount), 3) #Ajout de cette ligne pour arrondir à 3 rang après la virgule
    return "%s" % (intcomma(amount).replace('.',' '))

@register.filter(name='boolean')
def boolean(bool):
    try:
        if bool == True: return "Oui"
        elif bool == False: return "Non"
        else : return "N/A"
    except Exception as e:
        return "N/A"
    
@register.filter(name='input_float')
def input_float(number):
    num = "{}".format(str(number).replace(',','.'))
    print("Num: {}".format(num))
    return num

