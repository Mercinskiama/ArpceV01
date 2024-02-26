from __future__ import unicode_literals
from ErpBackOffice.models import PlaceType

class dao_place_type(object):
    @staticmethod
    def toListTypesPlace():
        list = []
        for key, value in PlaceType:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypePlace(id):
        list = dao_place_type.toListTypesPlace()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetTypePays():
        return dao_place_type.toGetTypePlace(1)

    @staticmethod
    def toGetTypeEtatProvince():
        return dao_place_type.toGetTypePlace(2)

    @staticmethod
    def toGetTypeVille():
        return dao_place_type.toGetTypePlace(3)

    @staticmethod
    def toGetTypeCommune():
        return dao_place_type.toGetTypePlace(4)

    @staticmethod
    def toGetTypeQuartier():
        return dao_place_type.toGetTypePlace(5)