from __future__ import unicode_literals
import unidecode
from ErpBackOffice.models import Model_Personne
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count


class dao_personne(object):
    id = 0
    prenom=""
    nom=""
    nom_complet = ""
    image   = ""
    email = ""
    phone = ""
    adresse = ""
    commune_quartier_id = None
    est_actif = True
    auteur_id = None
    est_particulier = False
    user_id = None


    @staticmethod
    def toCreateEmploye(prenom,nom, postnom, nom_complet, image,email, phone, adresse, commune_quartier_id, est_actif, compte_id = None, est_particulier = False,profilrh_id= None,unite_fonctionnelle_id = None,lieu_travail_id = None, categorie_employe_id = None,poste_id = None, classification_pro_id = None, diplome_id = None, modele_bulletin_id = None, statutrh_id = None, document_id = None):
        try:
            employe = dao_personne()
            employe.nom_complet = unidecode.unidecode(nom_complet)
            employe.prenom = prenom
            employe.nom = nom
            employe.image = image
            employe.email = email
            employe.phone = phone
            employe.adresse = adresse
            employe.commune_quartier_id = commune_quartier_id
            employe.est_actif = est_actif
            employe.est_particulier = True
            return employe
        except Exception as e:
            print("ERREUR LORS DE LA CREATION DE LA PERSONNE")
            print(e)
            return None

    @staticmethod
    def toSaveEmploye(auteur,objet_dao_personne):
        try:

            employe  = Model_Personne()
            if not objet_dao_personne.email or len(objet_dao_personne.email) < 10 or objet_dao_personne.email == None:
                objet_dao_personne.email = objet_dao_personne.nom_complet.lstrip().rstrip().replace(" ",".").lower() + "@etaxe-nsandax.com"
            # else:
            employe.email = objet_dao_personne.email

            user = User.objects.filter(username = objet_dao_personne.email)
            if not user:
                user = User.objects.create_user(
                    username = objet_dao_personne.email,
                    password = "employeDGTP2023@",
                    email = objet_dao_personne.email
                )

            # print('Email Pro Create', objet_dao_personne.email)
            employe.nom_complet = objet_dao_personne.nom_complet
            employe.prenom = objet_dao_personne.prenom
            employe.nom = objet_dao_personne.nom
            employe.image = objet_dao_personne.image
            employe.phone = objet_dao_personne.phone
            employe.adresse = objet_dao_personne.adresse
            employe.commune_quartier_id = objet_dao_personne.commune_quartier_id
            employe.est_actif = objet_dao_personne.est_actif
            employe.est_particulier = objet_dao_personne.est_particulier
            employe.user_id = user.id
            employe.auteur_id = auteur.id
            employe.save()
            return employe
        except Exception as e:
            print("ERREUR LORS DE L'ENREGISTREMENT EMPLOYE")
            print(e)
            return None

    @staticmethod
    def toUpdateEmploye(id, objet_dao_personne):
        try:
            employe  = dao_personne.toGetEmploye(id)
            if not objet_dao_personne.email or len(objet_dao_personne.email) < 10 or objet_dao_personne.email == None:
                objet_dao_personne.email = objet_dao_personne.nom_complet.lstrip().rstrip().replace(" ",".").lower() + "@etaxe-nsandax.com"
            # else:
                # employe.email = objet_dao_personne.email
            employe.email = objet_dao_personne.email
            # print('Email Pro update', objet_dao_personne.email)
            employe.nom_complet = objet_dao_personne.nom_complet
            employe.prenom = objet_dao_personne.prenom
            employe.nom = objet_dao_personne.nom
            employe.image = objet_dao_personne.image
            employe.phone = objet_dao_personne.phone
            employe.adresse = objet_dao_personne.adresse
            employe.commune_quartier_id = objet_dao_personne.commune_quartier_id
            employe.est_actif = objet_dao_personne.est_actif
            employe.est_particulier = objet_dao_personne.est_particulier

            employe.save()

            return employe
        except Exception as e:
            # print("ERREUR UPDATE EMPLOYE")
            # print(e)
            return None

    @staticmethod
    def toActiveEmploye(id, est_actif):
        try:
            employe = Model_Personne.objects.get(pk = id)
            employe.est_actif = est_actif
            employe.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetEmploye(id):
        try:
            return Model_Personne.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetEmployeFromUser(id):
        try:
            return Model_Personne.objects.filter(user_id = id).first()
        except Exception as e:
            return None

    @staticmethod
    def toGetEmployeByFullName(nom_complet):
        try:
            nom_complet = unidecode.unidecode(nom_complet)
            return Model_Personne.objects.filter(nom_complet = nom_complet).first()
        except Exception as e:
            print("err toGetEmployeByFullName", e)
            return None

    @staticmethod
    def toDeleteEmploye(id):
        try:
            employe = Model_Personne.objects.get(pk = id)
            employe.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListEmployes():
        try:
            return Model_Personne.objects.all().order_by('nom_complet')
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return None

    @staticmethod
    def toListEmployesActifs():
        try:
            return Model_Personne.objects.filter(est_actif = True)
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []

    @staticmethod
    def togetNombreEmployesActifs():
        try:
            return Model_Personne.objects.filter(est_actif = True).count()
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []


    @staticmethod
    def toListEmployesOfDepartement(departement_id):
        try:
            return Model_Personne.objects.filter(unite_fonctionnelle_id = departement_id)
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []
    @staticmethod
    def toListEmployesOfDepartementByCode(code_departement):
        try:
            return Model_Personne.objects.filter(unite_fonctionnelle__code = code_departement)
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []
    
    @staticmethod
    def toListEmployeOfClassificationByDepartementCode(code_departement, classification_pro_code):
        try:
            return Model_Personne.objects.filter(unite_fonctionnelle__code = code_departement, classification_pro__code = classification_pro_code )
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []

    @staticmethod
    def changeImag(image,id):
        #print('TOUCHE PROFIL',image)
        employe  = dao_personne.toGetEmploye(id)
        employe.image=image
        employe.save()
        #print('AFTER TOUCHE PROFIL',image)
    @staticmethod
    def getchangeImag(id):
        employe  = dao_personne.toGetEmploye(id)
        return employe.image


    @staticmethod
    def toListEmployes_years():
        try:
            list_=[]
            employes=Model_Personne.objects.all().order_by('nom_complet')
            for employe in employes:
                list_.append(employe.creation_date.year)
            return set(list_)
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []

    @staticmethod
    def toGetResponsableEmplye(employe):
        try:
            List=[]
            employe = Model_Personne.objects.get(pk = employe)
            profil = employe.GetprofilRH
            List.append(profil.responsable_id)
            print('***LIST RESPONSABLE', List)
            return List
        except Exception as e:
            return []


    @staticmethod
    def toListnombreEmployéParMoisAnneeEncours(today=timezone.now().year):
        try:

            # ListeExpression = Model_Expression.objects.annotate(month=TruncMonth('date_expression')).values('month').annotate(total=Count('demandeur'))
            ListSol = [0,0,0,0,0,0,0,0,0,0,0,0]
            ListeQuery =Model_Personne.objects.annotate(month=TruncMonth('creation_date')).values('month').annotate(total=Count('creation_date')).filter(creation_date__year = today)
            #print("Pour 2020 : {}".format(Model_Expression.objects.annotate(month=TruncMonth('date_expression')).values('month').annotate(total=Count('demandeur')).filter(date_expression__year = 2019)))
            for item in ListeQuery:

                if item["month"].month==1:

                    #ListSol.remove()
                    if item["total"] == 0:
                        ListSol[0] = 0
                    else:
                        ListSol[0] = item["total"]
                    continue
                elif item["month"].month==2:
                    if item["total"] == 0:
                        ListSol[1] = 0
                    else:
                        ListSol[1] = item["total"]
                    continue
                elif item["month"].month==3:
                    if item["total"] == 0:
                        ListSol[2] = 0
                    else:
                        ListSol[2] = item["total"]
                    continue
                elif item["month"].month==4:
                    if item["total"] == 0:
                        ListSol[3] = 0
                    else:
                        ListSol[3] = item["total"]
                    continue
                elif item["month"].month==5:
                    if item["total"] == 0:
                        ListSol[4] = 0
                    else:
                        ListSol[4] = item["total"]
                    continue
                elif item["month"].month==6:
                    if item["total"] == 0:
                        ListSol[5] = 0
                    else:
                        ListSol[5] = item["total"]
                    continue
                elif item["month"].month==7:
                    if item["total"] == 0:
                        ListSol[6] = 0
                    else:
                        ListSol[6] = item["total"]
                    continue
                elif item["month"].month==8:
                    if item["total"] == 0:
                        ListSol[7] = 0
                    else:
                        ListSol[7] = item["total"]
                    continue
                elif item["month"].month==9:
                    if item["total"] == 0:
                        ListSol[8] = 0
                    else:
                        ListSol[8] = item["total"]
                    continue
                elif item["month"].month==10:
                    if item["total"] == 0:
                        ListSol[9] = 0
                    else:
                        ListSol[9] = item["total"]
                    continue
                elif item["month"].month==11:
                    if item["total"] == 0:
                        ListSol[10] = 0
                    else:
                        ListSol[10] = item["total"]
                    continue
                elif item["month"].month==12:
                    if item["total"] == 0:
                        ListSol[11] = 0
                    else:
                        ListSol[11] = item["total"]
                    continue
                else:
                    pass

            #print('Liste des expression %s' %(ListSol))
            return ListSol
        except Exception as e:
            #print("ERRER LISTEEXPRESSION BY MONTH WITHOUT USER ID")
            #print(e)
            pass





