import math
from datetime import time, timedelta, datetime, date
from django.utils import timezone

def AfficheEntier(n, sep=" "):
    """
        #print(n)
        s = str(n)
        #print(s)
        l = len(s)
        nc = 0
        res = ""
        for i in range(l-1, -1, -1):
            res = s[i] + res
            nc += 1
            if nc == 3:
                res = sep + res
                nc = 0
        if res.startswith(sep):
            res = res[1:]

        if n < 0 and res[1] == sep:
            res = list(res)
            del res[1]
            res = "".join(res)
        return res
    """
    s = 0
    if n % 1 == 0:
            s = str(int(n))
    else:
            s = str(n)

    #print(s)

    l = len(s)
    nc = 0
    res = ""
    for i in range(l-1, -1, -1):
        res = s[i] + res
        nc += 1
        if nc == 3:
            res = sep + res
            nc = 0
    if res.startswith(sep):
        res = res[1:]
    if n < 0 and res[1] == sep:
        res = list(res)
        del res[1]
        res = "".join(res)
    return res



def makeFloat(nombre):
    try:
        if isinstance(nombre,str):
            nombre = nombre.replace(" ","")
            nombre = nombre.replace(",",".")
            if nombre == "": nombre = "0.0"
            #print("nombre str {}".format(nombre))
            nombre = float(nombre)
            if math.isnan(nombre): nombre = 0.0
            return nombre
        elif isinstance(nombre, int):
            nombre = str(nombre)
            if nombre == "": nombre = "0.0"
            #print("nombre int {}".format(nombre))
            nombre = float(nombre)
            if math.isnan(nombre): nombre = 0.0
            return nombre
        elif isinstance(nombre, float):
            #print("nombre float {}".format(nombre))
            if math.isnan(nombre): nombre = 0.0
            return nombre
        elif nombre is None:
            #print("nombre float {}".format(nombre))
            nombre = 0.0
            return nombre
        else:
            #print("nombre others {}".format(nombre))
            nombre = float(nombre)
            if math.isnan(nombre): nombre = 0.0
            return nombre
    except Exception as e: return 0.0

def makeStringFromFloatExcel(character):
    try:
        if isinstance(character, float):
            return str(int(character))
        elif character is None:
            return ""
        else:
            character = str(character)
            return character
    except Exception as e: return ""
    
def makeString(character):
    try:
        if isinstance(character, float):
            return str(character)
        elif character is None:
            return ""
        else:
            character = str(character)
            return character
    except Exception as e: return ""


def makeInt(nombre):
    try:
        if isinstance(nombre,str):
            if nombre == "": nombre = "0"
            #print("nombre str {}".format(nombre))
            nombre = int(nombre)
            if math.isnan(nombre): nombre = 0
            return nombre
        elif isinstance(nombre, float):
            nombre = str(nombre)
            if nombre == "": nombre = "0"
            #print("nombre float {}".format(nombre))
            nombre = int(nombre)
            if math.isnan(nombre): nombre = 0
            return nombre
        elif isinstance(nombre, int):
            #print("nombre int {}".format(nombre))
            if math.isnan(nombre): nombre = 0
            return nombre
        elif nombre is None:
            #print("nombre int {}".format(nombre))
            nombre = 0
            return nombre
        else:
            #print("nombre others {}".format(nombre))
            nombre = int(nombre)
            if math.isnan(nombre): nombre = 0
            return nombre
    except Exception as e:
        print("Ex ", e) 
        return 0
    
def makeIntId(nombre):
    nombre = makeInt(nombre)
    if nombre == 0: nombre = None
    return nombre

def checkDateFormat(character):
    try:
        #Si le champs est vide et n'est pas obligatoire, on l'affecte None
        if character == "": return True, None
        #Si le champs n'est pas vide et on verifie si c'est le bon format
        is_formated = datetime.strptime(character,"%d/%m/%Y")
        #Si c'est le bon format, on converti la chaine en format date
        date_format = date(int(character[6:10]), int(character[3:5]), int(character[0:2]))
        return True, date_format
    except ValueError as err: 
        return False, err
    
def checkDateTimeFormat(character):
    try:
        #Si le champs est vide et n'est pas obligatoire, on l'affecte None
        if character == "": return True, None
        #Si le champs n'est pas vide et on verifie si c'est le bon format
        is_formated = datetime.strptime(character,"%d/%m/%Y %H:%M:%S")
        #Si c'est le bon format, on converti la chaine en format date
        date_format = timezone.datetime(int(character[6:10]), int(character[3:5]), int(character[0:2]), int(character[11:13]), int(character[14:16]))
        return True, date_format
    except ValueError as err: 
        return False, err
    
def checkTimeFormat(character):
    """
    Cette fonction vérifie si une chaîne donnée est au format "HH:MM:SS" et renvoie un booléen indiquant
    si c'est le cas, ainsi que l'objet de temps converti, le cas échéant.
    
    :param character: La chaîne d'entrée qui représente une heure au format "HH:MM:SS"
    :return: un tuple à deux valeurs. La première valeur est un booléen indiquant si le caractère
    d'entrée est au format d'heure correct (HH:MM:SS). La deuxième valeur est soit None (si le caractère
    d'entrée est vide), soit un objet datetime.time représentant l'heure dans le caractère d'entrée. Si
    le caractère d'entrée n'est pas au format correct, la fonction renvoie False et un message d'erreur.
    """
    try:
        #Si le champs est vide et n'est pas obligatoire, on l'affecte None
        if character == "": return True, None
        #Si le champs n'est pas vide et on verifie si c'est le bon format
        is_formated = datetime.strptime(character,"%H:%M:%S")
        #Si c'est le bon format, on converti la chaine en format date
        date_format = time(int(character[0:2]), int(character[3:5]), int(character[6:8]))
        return True, date_format
    except ValueError as err: 
        return False, err
    
def checkDateFormatExcel(character):
    """
    Cette fonction vérifie si une chaîne donnée est dans le format de "Yyyy-mm-dd" et renvoie un booléen
    indiquant si c'est le cas, avec la date convertie si elle est valide.
    
    * character character : la chaîne d'entrée qui doit être vérifiée pour un format de date spécifique
    * return: un tuple avec deux valeurs: un booléen indiquant si le format de date est correct ou non,
    et aucun ou un objet de date si le format est correct.
    """
    try:
        #Si le champs est vide et n'est pas obligatoire, on l'affecte None
        if character == "": return True, None
        #Si le champs n'est pas vide et on verifie si c'est le bon format
        is_formated = datetime.strptime(character,"%Y-%m-%d")
        #Si c'est le bon format, on converti la chaine en format date
        date_format = date(int(character[0:4]), int(character[5:7]), int(character[8:10]))
        return True, date_format
    except ValueError as err: 
        return False, err
    
from django.contrib.humanize.templatetags.humanize import intcomma
def get_monetary_rounded(amount):
    amount = makeFloat(amount)
    amount = round(float(amount), 2)
    #return "%s%s%s" % (intcomma(int(amount)).replace(',',' '), ",", ("%0.2f" % amount)[-2:])
    return "%s%s%s" % (intcomma(int(amount)).replace('.',' '), ",", ("%0.2f" % amount)[-2:])

def get_monetary(amount):
    #return "%s" % (intcomma(amount).replace(',',' ').replace('.',','))
    amount = makeFloat(amount)
    amount = round(float(amount), 3) #Ajout de cette ligne pour arrondir à 3 rang après la virgule
    return "%s" % (intcomma(amount).replace('.',' '))





