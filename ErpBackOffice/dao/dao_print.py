from __future__ import unicode_literals
from django.utils import timezone
import ErpBackOffice
from ErpBackOffice.models import Model_Place, PlaceType


#### Structure de base du model à retourner
model = {
        'title':'', #Titre à donner au rapport
        'reference':'', #Sous-titre ou Référence
        'date_creation':'', #Date de création de l'objet
        'date_now':timezone.now(), #Date d'impression,
        'etat': '',
        'details':[], #Tableau contenant une liste des dictionnaires Champs - Valeurs, gérant l'affichage dans le fichier print.html
        #Dans le cas où le rapport contient des lignes de tableau relatif à l'objet 
        'tabEntete':[], #Tableau des entêtes souhaitées dans le tableau
        'tabLignes':[], #Tableau contenant les lignes relatifs aux données en fontion des entêtes prealablement défini
}
#### Fin de la structure

#********** Code Outils aidant à l'éxécution ************#


#creation d'une fonction qui renvoit "" dans le cas où la valeur recherchée par jointure est inexistante 
def get_value_of_attribute(attribut, objet):
    try:
        attribut = my_exec_objet(attribut, objet)
        return attribut
    except Exception as e:
        #print("errerur her",e)
        return ""

def my_exec_objet(code, objet):
    exec('global i; i = %s' % code)
    global i
    return i
#********** Fin Code Outils aidant à l'éxécution ************#