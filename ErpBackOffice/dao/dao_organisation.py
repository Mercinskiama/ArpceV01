# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Organisation

class dao_organisation(object):
    id = 0
    image	= ""
    image_cover	= ""
    nom = ""
    slogan = ""
    nom_application = ""
    type_organisation_id = 0		
    devise_id = 0		
    commune_quartier_id = 0
    adresse = ""
    email = ""	
    phone = ""
    site_web = ""	
    fax	= ""		
    numero_fiscal = ""		


    @staticmethod
    def toListOrganisations():
        return Model_Organisation.objects.all()

    @staticmethod
    def toListOrganisationsDuType(type_organisation_id):
        return Model_Organisation.objects.filter(type_organisation_id = type_organisation_id)
		
    @staticmethod
    def toCreateOrganisation(image, image_cover, nom, slogan, nom_application, type_organisation_id = 0, devise_id = 0, commune_quartier_id = 0, adresse="",email="",phone="",site_web="",fax="",numero_fiscal=""):        
        try:
            organisation = dao_organisation()
            organisation.nom = nom
            if image != None:
                organisation.image = image
            if image_cover != None:
                organisation.image_cover = image_cover
            if slogan != None:
                organisation.slogan = slogan
            if nom_application != None:
                organisation.nom_application = nom_application
            if type_organisation_id != 0 :
                organisation.type_organisation_id = type_organisation_id
            if devise_id != 0 :
                organisation.devise_id = devise_id
            if commune_quartier_id != 0 :
                organisation.commune_quartier_id = commune_quartier_id
            organisation.adresse = adresse
            organisation.email = email
            organisation.phone = phone
            organisation.site_web = site_web			
            organisation.fax = fax
            organisation.numero_fiscal = numero_fiscal
            return organisation
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'organisation")
            #print(e)
            return None

    @staticmethod
    def toSaveOrganisation(auteur, object_dao_organisation):
        try:
            organisation = Model_Organisation()
            organisation.nom = object_dao_organisation.nom
            organisation.image = object_dao_organisation.image
            organisation.image_cover = object_dao_organisation.image_cover
            organisation.slogan = object_dao_organisation.slogan
            organisation.nom_application = object_dao_organisation.nom_application
            organisation.type_organisation_id = object_dao_organisation.type_organisation_id
            organisation.devise_id = object_dao_organisation.devise_id
            organisation.commune_quartier_id = object_dao_organisation.commune_quartier_id
            organisation.adresse = object_dao_organisation.adresse
            organisation.email = object_dao_organisation.email
            organisation.site_web = object_dao_organisation.site_web
            organisation.fax = object_dao_organisation.fax
            organisation.numero_fiscal = object_dao_organisation.numero_fiscal
            organisation.auteur_id = auteur.id
            organisation.save()
            return organisation
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE ORGANISATION")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateOrganisation(id, object_dao_organisation):
        try:
            organisation = Model_Organisation.objects.get(pk = id)
            organisation.nom = object_dao_organisation.nom
            organisation.image = object_dao_organisation.image
            organisation.image_cover = object_dao_organisation.image_cover
            organisation.slogan = object_dao_organisation.slogan
            organisation.nom_application = object_dao_organisation.nom_application
            organisation.type_organisation_id = object_dao_organisation.type_organisation_id
            organisation.devise_id = object_dao_organisation.devise_id
            organisation.commune_quartier_id = object_dao_organisation.commune_quartier_id
            organisation.adresse = object_dao_organisation.adresse
            organisation.email = object_dao_organisation.email
            organisation.site_web = object_dao_organisation.site_web
            organisation.fax = object_dao_organisation.fax
            organisation.numero_fiscal = object_dao_organisation.numero_fiscal
            organisation.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR ORGANISATION")
            #print(e)
            return False
  
    @staticmethod
    def toGetOrganisation(id):
        try:
            return Model_Organisation.objects.get(pk = id)
        except Exception as e:
            return None        

    @staticmethod
    def toGetMainOrganisation():
        try:
            return Model_Organisation.objects.filter(est_active = True)[0]
        except Exception as e:
            return None
        
    @staticmethod
    def toSetMainOrganisation(id):
        try:
            Model_Organisation.objects.all().update(est_active = False)
            organisation = Model_Organisation.objects.get(pk=id)
            organisation.est_active = True
            organisation.save()
        except Exception as e:
            return None

    @staticmethod
    def toDeleteOrganisation(id):
        try:
            organisation = Model_Organisation.objects.get(pk = id)
            organisation.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION ORGANISATION")
            #print(e)
            return False
        					
            