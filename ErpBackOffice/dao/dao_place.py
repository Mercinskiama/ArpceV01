from __future__ import unicode_literals
from ErpBackOffice.models import Model_Place, PlaceType

class dao_place(object):
    designation	= ""
    code_telephone = ""
    place_type = 0
    code_pays = ""
    parent_id = 0

    @staticmethod
    def toCreatePlace(place_type, designation, code_telephone, parent_id=0, code_pays=None):
        place = dao_place()
        place.place_type = place_type
        place.designation = designation
        place.code_telephone = code_telephone
        if parent_id != 0 : place.parent_id = parent_id
        if code_pays != None : place.code_pays = code_pays
        return place
    
    @staticmethod
    def toSavePlace(object_dao_place):
        try:
            place = Model_Place()
            place.code_pays = object_dao_place.code_pays
            place.code_telephone = object_dao_place.code_telephone
            place.designation = object_dao_place.designation
            place.parent_id = object_dao_place.parent_id
            place.place_type = object_dao_place.place_type
            place.save()
            return place
        except Exception as e:
            #print("ERREUR !")
            #print(e)
            return None

    @staticmethod
    def toUpdatePlace(id, object_dao_place):
        try:
            place = Model_Place.objects.get(pk = id)
            place.code_pays = object_dao_place.code_pays
            place.code_telephone = object_dao_place.code_telephone
            place.designation = object_dao_place.designation
            place.parent_id = object_dao_place.parent_id
            place.place_type = object_dao_place.place_type
            place.save()
            return True
        except expression as identifier:
            #print("ERREUR !")
            #print(e)
            return False

    @staticmethod
    def toGetPlace(id):
        try:
            place = Model_Place.objects.get(pk = id)
            return place
        except Exception as e:
            return None

    @staticmethod
    def toListPlaces():
        return Model_Place.objects.all().order_by("designation")

    @staticmethod
    def toListPlacesOfType(place_type):
        return Model_Place.objects.filter(place_type = place_type).order_by("designation")

    @staticmethod
    def toListPlacesFilles(parent_id):
        return Model_Place.objects.filter(parent_id = parent_id).order_by("designation")
        