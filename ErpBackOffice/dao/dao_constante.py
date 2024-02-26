# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import *
from django.utils import timezone

class dao_constante(object):
    id = 0
    designation             =    ""
    reference               =    ""
    description             =    ""
    code                    =    ""
    auteur_id               =    None
    type_constant           =    1
    base_test               =    0.0
    base_test_is_const      =    False
    base_test_const_id      =    None
    rubrique_id             =    None
    valeur                  =    0.0
    valeur_is_const         =    False
    valeur_const_id         =    None
    devise_id               =    None
    
    @staticmethod
    def toListTypeConstante():
        list = []
        for key, value in TypeConstante:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeOperationCalcul():
        list = []
        for key, value in TypeOperationCalcul:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeOperationTest():
        list = []
        for key, value in TypeOperationTest:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeConditionTest():
        list = []
        for key, value in TypeConditionTest:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
