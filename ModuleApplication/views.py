# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.utils.auth import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.template import loader
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
from ErpBackOffice.dao.dao_place_type import dao_place_type
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
import datetime
import json
import array
from pprint import pprint
from ModuleConversation.dao.dao_notification import dao_notification
from ErpBackOffice.dao.dao_organisation import dao_organisation
from ErpBackOffice.utils.wkf_task import wkf_task

var_module_id = 6 #ID du Module en cours
vars_module = {"name" : "MODULE_APPLICATION", "value" : 98 }



def get_lister_applications(request):
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)

    if response != None:
        return response

    model = dao_module.toListModules()
    print ("NOTIFIIII %s" % identite.utilisateur(request).id)

    context = {
		'title' : 'Liste des applications',
        'model' : model,
        "utilisateur" : utilisateur,
        "modules" : modules,
        "module" : ErpModule.MODULE_APPLICATION,
        'organisation': dao_organisation.toGetMainOrganisation(),
        'degrade': 'module_application'
	}
    template = loader.get_template("ErpProject/ModuleApplication/application/list.html")
    return HttpResponse(template.render(context, request))

def get_details_application(request, ref):
    modules, utilisateur,response = auth.toGetAuth(request)

    if response != None:
        return response

    try:
        ref = int(ref)
        application = dao_module.toGetModule(ref)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,None)
        context = {
            'title' : application.nom_module,
            'model' : application,
            "utilisateur" : utilisateur,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": [],
            'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules,
            "module" : ErpModule.MODULE_APPLICATION,
        }
        template = loader.get_template("ErpProject/ModuleApplication/application/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        #print("ERREUR")
        #print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse("module_application_list_applications"))

def get_installer_application(request, ref):
    modules, utilisateur,response = auth.toGetAuth(request)

    if response != None:
        return response

    try:
        ref = int(ref)
        dao_module.toInstallModule(ref, True)
        return HttpResponseRedirect(reverse("module_application_details_application", args=(ref,)))
    except Exception as e:
        #print("ERREUR")
        #print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse("module_application_list_applications"))

def get_desinstaller_application(request, ref):
    modules, utilisateur,response = auth.toGetAuth(request)

    if response != None:
        return response

    try:
        ref = int(ref)
        dao_module.toInstallModule(ref, False)
        return HttpResponseRedirect(reverse("module_application_details_application", args=(ref,)))
    except Exception as e:
        #print("ERREUR")
        #print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse("module_application_list_applications"))
