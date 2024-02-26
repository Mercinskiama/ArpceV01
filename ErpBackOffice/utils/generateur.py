import math, unidecode, codecs, os, inspect
from django.contrib.contenttypes import models
from django.contrib.contenttypes.models import ContentType
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
from ErpBackOffice.models import *
from ErpBackOffice.dao.dao_sous_module import dao_sous_module
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
from ErpBackOffice.dao.dao_groupe_menu import dao_groupe_menu
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.dao.dao_regle import dao_regle
from ModuleConfiguration.dao.dao_permission import dao_permission
from ModuleConfiguration.dao.dao_actionutilisateur import dao_actionutilisateur
from ModuleConversation.dao.dao_notification import dao_notification
from ErpBackOffice.dao.dao_organisation import dao_organisation
from ModuleConfiguration.dao.dao_sousmodule import dao_sousmodule
from ModuleConfiguration.dao.dao_groupemenu import dao_groupemenu
from ErpBackOffice.utils.utils import utils

def genLayoutHtmlOfModule():
    texte_a_ajouter = u'''
{% extends "ErpProject/ErpBackOffice/shared/layout.html" %} {% block content %} {% load static %}
{% if not isPopup %}
<!-- Suite Menu Nav -->
<!-- Menu lateral -->
<div class="sidebar" role="navigation">
    <div class="contenair-profil only-on-large-screen" style="background-color: transparent;">
        {% if utilisateur.image != None and utilisateur.image != '' %}
        <img src="{% static utilisateur.image %}"  class="profil">
        {% else %}
            <img src="/static/ErpProject/image/icone_profile.png" class="profil">
        {% endif %}
        <label class="nom-admin">{{ utilisateur.nom_complet }}</label>
        <p class="fonction">{% if utilisateur.poste == None %} {{"Administrateur"}} {% else %}{{ utilisateur.poste.designation }}{% endif %}</p>
        <div class="divider" style="background-color: transparent;"></div>
    </div>
    <div class="sidebar-nav navbar-collapse" style="background-color: transparent;">
        <ul class=" nav" id="side-menu" style="background-color: transparent;">
            {% include 'ErpProject/ErpBackOffice/widget/menu.html' %}
        </ul>
    </div>
    <!-- /.sidebar-collapse -->
</div>
<!-- /.Menu lateral -->
</nav>
<!-- /.Menu Navbar -->

<!-- Corps de la page (A définir dans chaque fonction du module) -->
<div id="page-wrapper" style="background-color:#f9f9f9;">
{% else %}
<div id="page-wrapper"  style="background-color:#f9f9f9;margin:0!important">
{% endif %}
    {% block page %}{% endblock %}
</div>
<!-- Fin Corps de la page -->
{% endblock %}

'''
    return texte_a_ajouter

def genIndexTemplate(nomModule, nom_pattern="#"):
    if nom_pattern != "#": nom_pattern = f'{nom_pattern}_tableau_de_bord'
    texte_a_ajouter = u'''

{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}}{{% load static %}}{{% load account_filters %}}

<style type="text/css">
    @import url({{% static 'ErpProject/css/home_module.css' %}});
    .hh2{{
        color: #fff;
        font-size: 19px;
        font-family: Roboto bold;
        text-decoration: none;
        background-color: #0092CC;
        text-align: left;
    }}
    .btn:focus, .btn:active:focus, .btn.active:focus, .btn.focus, .btn:active.focus, .btn.active.focus {{
        outline: thin dotted; 
        outline: 1px solid #0092CC;
        outline-offset: 0px;
    }}
</style>

<div style="padding-top: 40px; ">
    <!-- Appel de la fonction message -->
    {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}
    <div class="row" style="align-items: center; justify-content: space-around;">
        <div class="col-md-3" style="justify-content: space-between;margin-top: 10px;">
            <div class="col-md-12"> <span style="font-size: 1.6em; font-weight: bold;">Notifications</span> </div>
            <div class="col-md-12" style="justify-content: space-between;">
                <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 180px; display: flex; flex-direction: column; justify-content: space-between;">  
                    <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly; position: relative;">
                        <div style="width: 45%; display: flex; align-items: center; justify-content: center; position: relative; margin: 0 10px;">
                            <img src="{{% static 'ErpProject/image/icones/alarm--v1.png' %}}" />
                        </div>
                        <div style="width: 45%;" class="text-center">
                            <span style="color: white; text-align: left; font-size: 1.3em; font-weight: 400;" >Non lues </span>
                        </div>
                        <span class="label label-danger" style="color: white; font-size: 35px; font-weight: 700; position: absolute; top: 11px; right: 15%; padding: 0 10px;">{{{{msg_no_open}}}}</span>
                    </div>
            
                    <a class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px; text-decoration: none;" href=""><span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Lire tout</span></a>
                </div>
                <br>
                <br>
                <div style="margin: 5px 0px;">
                    <span style="font-weight: 700; font-size: 18px; padding: 5px 0px;">Les dernières notifications</span>
                </div>
                <div style="overflow-y: scroll; scroll-behavior: smooth; display: grid;">
                    {{% if temp_notif_list|length > 0 %}}
                        {{% for item in temp_notif_list %}}
                            <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
                                <div class="panel panel-default">
                                <div class="panel-heading" role="tab" id="headingOne" style="background-color:#0092CC;color: #fff;">
                                    <h4 class="panel-title">
                                    <a class="hh2" style="text-decoration: none;" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse-{{{{forloop.counter0}}}}" aria-expanded="true" aria-controls="collapseOne">
                                    <span class="fa fa-bell"></span> Notification
                                    </a>
                                    </h4>
                                    <p style="margin-left: 1.5em;color:#A5A5A7;">{{{{item.notification.created_at}}}}</p>
                                </div>
                                <div id="collapse-{{{{forloop.counter0}}}}" class="panel-collapse collapse out" role="tabpanel" aria-labelledby="headingOne">
                                    <div class="panel-body" style="min-height: auto !important;">
                                        {{{{item.notification.text}}}}
                                    <br>
                                        <button class="btn rounded primary_color_{{{{module.name|lower}}}}"
                                        onclick="javascript:window.location.assign('{{% url item.lien_action item.source_identifiant %}}')">Vérifier
                                        </button>
                                    </div>
                                </div>
                                </div>
                            </div>
                        {{% endfor %}}
                    {{% else %}}
                           <p style="text-align:center;">Aucune Notification en cours</p>
                    {{% endif %}}
                </div>
            </div>

        </div>
        <div class="col-md-9" style="justify-content: space-between;margin-top: 10px;">
            <div class="row">
                <div class="col-md-12" style="justify-content: space-between;margin-top: 10px;"> <span style="font-size: 1.6em; font-weight: bold;">Gestion Quotidienne</span></div>
                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;">
                    
                    <div style="width: 100%; height: 180px; display: flex; flex-direction: row; align-items: center; justify-content: space-between;">
                        <div class="primary_color_{{{{module.name|lower}}}}" style="width: 48%; height: 180px;">
                            <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                                <a id="add-element" onclick="javascript:document.getElementById('btn-choose-element-modal').click()" href="#" class="leaf">
                                    <div style="width: 100%; display: flex; align-items: center; justify-content: center;">
                                        <img src="{{% static 'ErpProject/image/icones/paie.png' %}}"/>
                                    </div>
                                </a>
                            </div>
                            <div class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;">
                                <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Élément 1</span>
                            </div>
                        </div>
                        <div class="primary_color_{{{{module.name|lower}}}}" style="width: 48%; height: 180px;">
                            <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                                <a id="remove-user" href="#" class="leaf">
                                    <div style="width: 100%; display: flex; align-items: center; justify-content: center;">
                                        <img src="{{% static 'ErpProject/image/icones/bill_pay.png' %}}"/>
                                    </div>
                                </a>
                            </div>
                            <div class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;">
                                <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Élément 2</span>
                            </div>
                        </div>
                    </div>
                </div> 

                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;">
                    <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 180px;">
                        <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                            
                            <div id="search-user" style="width: 45%; display: flex; align-items: center; justify-content: center;">
                                <a href="#" class="leaf">
                                    <img src="{{% static 'ErpProject/image/icones/fss_setting.png' %}}"/>
                                </a>
                            </div>
                            
                            <div style="width: 45%;">
                                <span style="color: white; text-align: left; font-size: 1.3em; font-weight: 400;">Élément 3</span>
                            </div>
                        </div>
                        <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;">
                            <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Gestions Élément 3</span>
                        </div>
                    </div>
                </div> 

                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;">
                    <div style="width: 100%; height: 180px; background-color: rgb(0, 117, 94);">
                        <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                            <div id="reporting" style="width: 45%; display: flex; align-items: center; justify-content: center;">
                                <a href="#" class="leaf">
                                    <img src="{{% static 'ErpProject/image/icones/rapport.png' %}}"/>
                                </a>
                            </div>
                            <div style="width: 45%;">
                                <span style="color: white; text-align: left; font-size: 1.3em; font-weight: 400;">Rapports et Tableau de bord</span>
                            </div>
                        </div>
                        <div style="width: 100%; height: 40px; background-color: rgb(0, 107, 84); padding: 8px 10px;">
                            <a href="#" class="leaf" onclick="javascript:window.location.assign('{{% url '{1}' %}}')"> 
                                <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Reporting </span>
                            </a>
                        </div>
                    </div>
                </div> 
            </div>
            <div class="row">
                <div class="col-md-12" style="justify-content: space-between;margin-top: 10px;"> <span style="font-size: 1.6em; font-weight: bold;">Gestion Periodique</span></div>
                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;">                  
                    <div style="width: 100%; height: 180px; display: flex; flex-direction: row; align-items: center; justify-content: space-between;">
                        <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 48%; height: 180px;">
                            <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                                <a id="add-element" onclick="javascript:document.getElementById('btn-choose-element-modal').click()" href="#" class="leaf">
                                    <div style="width: 100%; display: flex; align-items: center; justify-content: center;">
                                        <img src="{{% static 'ErpProject/image/icones/expire_doc.png' %}}"/>
                                    </div>
                                </a>
                            </div>
                            <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;">
                                <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Expiration Document</span>
                            </div>
                        </div>
                        <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 48%; height: 180px;">
                            <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                                <a id="remove-user" href="#" class="leaf">
                                    <div style="width: 100%; display: flex; align-items: center; justify-content: center;">
                                        <img src="{{% static 'ErpProject/image/icones/remove-user-male.png' %}}"/>
                                    </div>
                                </a>
                            </div>
                            <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;">
                                <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Rapport</span>
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;" onclick="">
                    <div class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 180px;">
                        <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                            <div style="width: 45%; display: flex; align-items: center; justify-content: center;">
                                <img src="{{% static 'ErpProject/image/icones/send-file.png' %}}"/>
                            </div>
                            <div style="width: 45%;">
                                <span style="color: white; text-align: left; font-size: 1.3em; font-weight: 400;">DSN mensuelle</span>
                            </div>
                        </div>
                        <div class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;">
                            <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">DNS</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;" onclick="">
                    <div style="width: 100%; height: 180px; background-color: rgb(130, 103, 168);">
                        <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                            <div style="width: 45%; display: flex; align-items: center; justify-content: center;">
                                <img src="{{% static 'ErpProject/image/icones/clipboard.png' %}}"/>
                            </div>
                            <div style="width: 45%;">
                                <span style="color: white; text-align: left; font-size: 1.3em; font-weight: 400;">Charges à payer par caisse</span>
                            </div>
                        </div>
                        <div style="width: 100%; height: 40px; background-color: rgb(123, 93, 161); padding: 8px 10px;">
                            <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Charges à payer</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12" style="justify-content: space-between;margin-top: 10px;"> <span style="font-size: 1.6em; font-weight: bold;">Paramètrages</span></div>
                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;">
                    <div class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 180px;">
                        <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                            
                            <div id="search-user" style="width: 45%; display: flex; align-items: center; justify-content: center;">
                                <a href="#" class="leaf">
                                    <img src="{{% static 'ErpProject/image/icones/analyse_blanc.png' %}}"/>
                                </a>
                            </div>
                            
                            <div style="width: 45%;">
                                <span style="color: white; text-align: left; font-size: 1.3em; font-weight: 400;">Modèle de Calcul</span>
                            </div>
                        </div>
                        <div class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;">
                            <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Calcul</span>
                        </div>
                    </div>
                </div> 

                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;" onclick="">
                    <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 180px;">
                        <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                            <div id="reporting" style="width: 45%; display: flex; align-items: center; justify-content: center;">
                                <a href="#" class="leaf">
                                    <img src="{{% static 'ErpProject/image/icones/process.png' %}}"/>
                                </a>
                            </div>
                            <div style="width: 45%;">
                                <span style="color: white; text-align: left; font-size: 1.3em; font-weight: 400;">Procédures</span>
                            </div>
                        </div>
                        <div class="secondary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;">
                            <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">Workflow Module</span>
                        </div>
                    </div>
                </div> 
                <div class="col-md-4" style="justify-content: space-between;margin-top: 10px;" onclick="">
                    <div class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 180px;">
                        <div style="width: 100%; height: 140px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly;">
                            <div style="width: 45%; display: flex; align-items: center; justify-content: center;">
                                <img src="{{% static 'ErpProject/image/icones/update-file.png' %}}"/>
                            </div>
                            <div style="width: 45%;">
                                <span style="color: white; text-align: left; font-size: 1.3em; font-weight: 400;">Calcule du CICE</span>
                            </div>
                        </div>
                        <div class="primary_color_{{{{module.name|lower}}}}" style="width: 100%; height: 40px; padding: 8px 10px;; opacity:0.8!important;">
                            <span style="color: white; text-align: left; font-size: 0.9em; font-weight: 600;">CICE</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Trigger the modal with a button -->
<button style="display:none" id="btn-choose-element-modal" type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#chooseElementModal">Open Modal</button>
<!-- Modal -->
<div id="chooseElementModal" class="modal fade" role="dialog">
    <div class="modal-dialog">
        <!-- Modal content-->
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">Choisissez le type d'Élément</h4>
            </div>
            <div class="modal-body">
                <div class="row">
                    <div class="col-md-12">
                        <p style="border: 1px solid #34aadc; border-radius: 2px; color: #34aadc; text-align: center; padding: 7px; font-size: 16px; font-weight: 800;">
                            <a id="reporting" style="text-decoration: none;" href="#" class="leaf"> Type élément 1</a>
                        </p>
                        <p style="border: 1px solid #34aadc; border-radius: 2px; color: #34aadc; text-align: center; padding: 7px; font-size: 16px; font-weight: 800;">
                            <a id="reporting" style="text-decoration: none;" href="#" class="leaf"> Type élément 2</a>
                        </p>
                        <p style="border: 1px solid #34aadc; border-radius: 2px; color: #34aadc; text-align: center; padding: 7px; font-size: 16px; font-weight: 800;">
                            <a id="reporting" style="text-decoration: none;" href="#" class="leaf"> Type élément 3</a>
                        </p>
                        <p style="border: 1px solid #34aadc; border-radius: 2px; color: #34aadc; text-align: center; padding: 7px; font-size: 16px; font-weight: 800;">
                            <a id="reporting" style="text-decoration: none;" href="#" class="leaf"> Type élément 4</a>
                        </p>
                    </div> 
                </div>
            </div>
            <div class="modal-footer">
                <!-- /.Button dropdown -->
                <button type="button" class="theme-btn theme-btn-sm rounded chargement-au-click" data-dismiss="modal">Fermer</button>
            </div>
        </div>
    </div>
</div>
{{% endblock %}}

    '''.format(nomModule, nom_pattern)
    return texte_a_ajouter

def genDashBoardTemplate1(nomModule):
    texte_a_ajouter = u'''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}}{{% load static %}}{{% load account_filters %}}

<style type="text/css">
body {{background-color: grey!important;}}
.btSh{{border-radius: 0px;margin-right: 10px;margin-bottom: 0px;margin-bottom: 3%;}}
.f{{margin:2%;}}
.block_f{{margin-left: 0%;}}
.fond{{background-color: rgba(240, 240, 240, 0.3);border-radius: 50px;height: 50px;width: 50px;opacity:3.5;float: right;display: flex;justify-content: center;align-items: center;}}
</style>

<!-- Design Admin -->
<div id="vue_Admin" class="row" style="padding-top:30px;">
    <div class="col-lg-12">
    <h2>{{{{title}}}}</h2>
    <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
    <div class="separ" style="background-color: grey;opacity: 0.2"></div>
        <div class="panel panel-default" style="border: none;">
            <!-- Appel de la fonction message -->
            {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}

            <!--Notification-->
            <div class="panel" style="background-color:#f5f5f5;border: none;"></div>
            {{% if temp_notif_count > 0 %}}
            <div class="col-md-12" style="padding: 10px;">
                {{% for item in temp_notif_list %}}
                <div class="col-md-4" style="padding: 10px;">
                    <div style="">
                        <div class="mb-4 ">
                            <div class="card-body shadow" style="padding: 0px;background-color: white;">
                                <div style="width: 100%;background-color: white;/*padding: 10px;">
                                    <div style="padding: 10px;">
                                        <strong class="sub-header"
                                            style="margin: 10px;font-weight: 900;">Notification</strong>
                                        <small style="margin-right:50">{{{{item.notification.created_at}}}}</small>
                                        <button
                                            onclick="javascript:window.location.assign('{{% url 'back_office_notification' item.id %}}')"
                                            type="button" class="ml-2 mb-1 close" data-dismiss="toast"
                                            aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="separ"
                                        style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;">
                                    </div>

                                </div>
                                <div class="pt-4"
                                    style="padding: 15px;background-color: white;padding-top: 0px;padding-bottom: 0px;">
                                    <p>
                                        {{{{item.notification.text}}}}<br>
                                    </p>
                                </div>
                                <div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>

                                <div style="padding: 15px;padding-top: 0px;">
                                    {{% if item.type_action == "Link" %}}
                                    <button class="btn rounded primary_color_{{{{module.name|lower}}}}"
                                        onclick="javascript:window.location.assign('{{% url item.lien_action item.source_identifiant %}}')">Vérifier</button>
                                    {{% endif %}}
                                </div>
                                <div class="primary_color_{{{{module.name|lower}}}}" style="height: 5px;"></div>

                            </div>
                        </div>
                    </div>
                </div>
                {{% endfor %}}
            </div>
            {{% endif %}}
        </div>
        <!--END Notification-->
        <div class="Menu_Inventaire">
            <div class="row">
                <div class="col-md-3">
                    <div class="panel panel-success" style="border-radius: 0px;border-bottom: none;background-color:#FF6A22;">
                        <div class="panel-heading" style="background-color: transparent;color: white;">
                            <div class="row">
                                <div class="col-xs-7 text-left">
                                    <div class="header_vente_stat" style="">Élément 1</div>
                                    <p style="font-weight: 800;font-size: 22px;font-family: 'Poppins Bold'">15</p>
                                </div>
                                <div class="col-xs-3 text-right fond">
                                    <span class="mif-stack" style="float: left;font-size:25px"></span>
                                </div>
                                <div>
                                    <p style="float: left;font-size:80%;color:#fff;">Éléments nouvellement inscrits ou sympatisant</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="panel panel-success p2" style="border-radius: 0px;border-bottom: none;">
                        <div class="panel-heading" style="background-color: transparent;color: white;">
                            <div class="row">
                                <div class="col-md-7 text-left">
                                    <div class="header_vente_stat" style="">Élément 2</div>
                                    <p style="font-weight: 800;font-size: 22px;font-family: 'Poppins Bold'">8</p>
                                </div>
                                <div class="col-md-3 text-right fond">
                                    <span class="mif-calendar" style="float: left;font-size:25px"></span>
                                </div>
                                <div>
                                    <p style="float: left;font-size:80%;color:#fff;">Nombre de éléments actifs au sein du groupe</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="panel panel-success p3" style="border-radius: 0px;border-bottom: none;">
                        <div class="panel-heading" style="background-color: transparent;color: white;">
                            <div class="row">
                                <div class="col-xs-7 text-left">
                                    <div class="header_vente_stat" style="">Élément 3</div>
                                    <p style="font-weight: 800;font-size: 22px;font-family: 'Poppins Bold'">10</p>
                                </div>
                                <div class="col-xs-3 text-right fond">
                                    <span class="mif-exit" style="float: left;font-size:25px"></span>
                                </div>
                                <div>
                                    <p style="float: left;font-size:80%;color:#fff;">Nombre total d'Éléments officiels du groupe</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="panel panel-success p4" style="border-radius: 0px;border-bottom: none;">
                        <div class="panel-heading" style="background-color: transparent;color: white;">
                            <div class="row">
                                <div class="col-xs-7 text-left">
                                    <div class="header_vente_stat" style="">Élément 4</div>
                                    <p style="font-weight: 800;font-size: 22px;font-family: 'Poppins Bold'">5</p>
                                </div>
                                <div class="col-xs-3 text-right fond">
                                    <span class="mif-database" style="font-size:25px"></span>
                                </div>
                                <div>
                                    <p style="float: left;font-size:80%;color:#fff;">Le nombre total de cellules officielles du parti</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="mb-4">
                        <!-- Card Body -->
                        <div class="card-body" style="padding: 0;">
                        <div class="chart-area item-dash" style="padding: 15px;background-color: white;">
                            <center> <p>Evolution des éléments par province</p></center>
                            <canvas id="bar-chart" width="400" height="100"></canvas>
                        </div>
                        </div>
                    </div>
                </div>
            </div><br>

            <div class="row">
                <div class="col-md-4" style="padding: 10px;">
                    <div class="mb-4">
                        <div class="card-body shadow" style="padding: 0px;background-color: white;">
                            <div  style="width: 100%;background-color: white;/*padding: 10px;">
                                <div style="padding: 10px;"> 
                                    <strong class="sub-header" style="margin: 10px;font-weight: 900;">Indicateur 1</strong>
                                </div>
                                <div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>  
                            </div>
                            <div class="pt-4" style="padding: 15px;background-color: white;padding-top: 0px;padding-bottom: 0px;">
                                <h3 style="color: gray;font-weight: bold;">100 USD</h3>
                                <div class="" style="margin:2% 0 2% 0;font-style:normal;font-size:85%;">
                                    <span class="fg-red"><i class="fa fa-arrow-down"></i> <i>En diminution</i></span>
                                    <span class="fg-green" style="margin-left:20px"><i class="fa fa-arrow-up"></i> <i>En hausse</i></span>
                                </div>
                            </div>
                            <div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>                              
                            <div style="padding: 15px;padding-top: 0px;"     >
                                <button  onclick="javascript:window.location.assign('')" class="btn rounded primary_color_{{{{module.name|lower}}}}">Voir plus</button>
                                <button  onclick="javascript:window.location.assign('')" class="button rounded btn btn-default ">Annuler</button>
                            </div>
                            <div class="primary_color_{{{{module.name|lower}}}}" style="height: 5px;"></div>
                        </div>
                    </div>
                </div>

                <div class="col-md-4" style="padding: 10px;">
                    <div class="mb-4 ">
                        <div class="card-body shadow" style="padding: 0px;background-color: white;">
                            <div  style="width: 100%;background-color: white;/*padding: 10px;">
                                <div style="padding: 10px;"> 
                                    <strong class="sub-header" style="margin: 10px;font-weight: 900;">Indicateur 2</strong>
                                </div>
                                <div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>                                   
                            </div>
                            <div class="pt-4" style="padding: 15px;background-color: white;padding-top: 0px;padding-bottom: 0px;">
                                <h3 style="color: gray;font-weight: bold;">550 USD</h3>  
                                <div class="" style="margin:2% 0 2% 0;font-style:normal;font-size:85%;">
                                    <span class="fg-red"><i class="fa fa-arrow-down"></i> <i>En diminution</i></span>
                                    <span class="fg-green" style="margin-left:20px"><i class="fa fa-arrow-up"></i> <i>En hausse</i></span>
                                </div>
                            </div>
                            <div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>                              
                            <div style="padding: 15px;padding-top: 0px;"     >
                                <button  class="btn rounded primary_color_{{{{module.name|lower}}}}" onclick="javascript:window.location.assign('')">Voir plus</button>
                                <button  class="button rounded btn btn-default" onclick="javascript:window.location.assign('')">Annuler</button>
                            </div>
                            <div class="primary_color_{{{{module.name|lower}}}}" style="height: 5px;"></div>                                        
                        </div>
                    </div>
                </div>

                <div class="col-md-4" style="padding: 10px;">
                    <div class="mb-4 ">
                        <div class="card-body shadow" style="padding: 0px;background-color: white;">
                            <div  style="width: 100%;background-color: white;/*padding: 10px;">
                                <div style="padding: 10px;"> 
                                    <strong class="sub-header" style="margin: 10px;font-weight: 900;">Indicateur 3</strong>
                                </div>
                                <div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>             
                            </div>
                            <div class="pt-4" style="padding: 15px;background-color: white;padding-top: 0px;padding-bottom: 0px;">
                                <h3 style="color: gray;font-weight: bold;">200 USD</h3>   
                                <div class="" style="margin:2% 0 2% 0;font-style:normal;font-size:85%;">
                                    <span class="fg-red"><i class="fa fa-arrow-down"></i> <i>En diminution</i></span>
                                    <span class="fg-green" style="margin-left:20px"><i class="fa fa-arrow-up"></i> <i>En hausse</i></span>
                                </div>
                            </div>
                            <div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>                               
                            <div style="padding: 15px;padding-top: 0px;">
                                <button  onclick="javascript:window.location.assign('')" class="btn rounded primary_color_{{{{module.name|lower}}}}">Voir plus</button>
                                <button  onclick="javascript:window.location.assign('')" class="button rounded btn btn-default ">Annuler</button>
                            </div>
                            <div class="primary_color_{{{{module.name|lower}}}}" style="height: 5px;"></div>     
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- End Design Admin -->

<script src="{{% static 'ErpProject/js/Chart.min.js' %}}"></script>
<script>
    // Bar chart
    new Chart(document.getElementById("bar-chart"), {{
        type: 'bar',
        data: {{
        labels: ["Kinshasa", "Kongo Centrale", "Kwango", "Kwilu", "Lomami", "Lualaba", "Mai-Ndombe", "Maniema", "Mongala", "Nord-Kivu", "Nord-Ubangi", "Sankuru", "Sud-Kivu", "Sud-Ubangi", "Tanganyika", "Tshopo", "Tshuapa", "Kasaï oriental", "Kasaï central", "Kasaï", "Ituri", "Haut-Katanga", "Haut-Lomami", "Bas-Uele", "Haut-Uele", "Équateur"],
        datasets: [
            {{
            label: "Elément au niveau national",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
            data: [2478,5267,734,784,433,2478,5267,734,784,433,2478,5267,734,784,433,2478,5267,734,784,433,433,2478,5267,734,784,433]
            }}
        ]}},
        options: {{
            legend: {{ display: false }},
            title: {{
                display: true,
                text: "Courbe d'évolution de nouveaux éléments en 2021"
            }},
            font: {{
                family: 'Poppins'
            }}
        }}
    }});
</script>
{{% endblock %}}    
    '''.format(nomModule)
    return texte_a_ajouter

def genDashBoardTemplate2(nomModule):
    texte_a_ajouter = u'''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}}{{% load static %}}{{% load account_filters %}}

<style type="text/css">
    body {{background-color: grey!important;}}
</style>

<div class="row" style="padding-top: 30px;">
    <div class="col-lg-12">
        <h2>{{{{title}}}}</h2>
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>
        <div class="panel panel-default" style="border: none;">
            <!-- Appel de la fonction message -->
            {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}

            <!--Notification-->
            <div class="panel" style="background-color:#f5f5f5;border: none;"></div>
            {{% if temp_notif_count > 0 %}}
            <div class="col-md-12" style="padding: 10px;">
                {{% for item in temp_notif_list %}}
                <div class="col-md-4" style="padding: 10px;">
                    <div style="">
                        <div class="mb-4 ">
                            <div class="card-body shadow" style="padding: 0px;background-color: white;">
                                <div style="width: 100%;background-color: white;/*padding: 10px;">
                                    <div style="padding: 10px;">
                                        <strong class="sub-header"
                                            style="margin: 10px;font-weight: 900;">Notification</strong>
                                        <small style="margin-right:50">{{{{item.notification.created_at}}}}</small>
                                        <button
                                            onclick="javascript:window.location.assign('{{% url 'back_office_notification' item.id %}}')"
                                            type="button" class="ml-2 mb-1 close" data-dismiss="toast"
                                            aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="separ"
                                        style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;">
                                    </div>

                                </div>
                                <div class="pt-4"
                                    style="padding: 15px;background-color: white;padding-top: 0px;padding-bottom: 0px;">
                                    <p>
                                        {{{{item.notification.text}}}}<br>
                                    </p>
                                </div>
                                <div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>

                                <div style="padding: 15px;padding-top: 0px;">
                                    {{% if item.type_action == "Link" %}}
                                    <button class="btn rounded primary_color_{{{{module.name|lower}}}}"
                                        onclick="javascript:window.location.assign('{{% url item.lien_action item.source_identifiant %}}')">Vérifier</button>
                                    {{% endif %}}
                                </div>
                                <div class="primary_color_{{{{module.name|lower}}}}" style="height: 5px;"></div>

                            </div>
                        </div>
                    </div>
                </div>
                {{% endfor %}}
            </div>
            {{% endif %}}
        </div>
        <!--END Notification-->
        <div class="panel panel-default" style="border: none;">
            <div class="panel" style="background-color:#f5f5f5;border: none;">
                <div class="col-md-8" style="padding: 10px;">
                    <div>
                        <div class="mb-4">
                            <!-- Card Body -->
                            <div class="card-body">
                                <div class="chart-area item-dash" style="padding: 15px;background-color: white;">
                                    <canvas id="myAreaChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4" style="padding: 10px;">
                    <div style="">
                        <div class="mb-4 ">
                            <!-- Card Body -->
                            <div class="card-body">
                                <div class="chart-pie pt-4 item-dash" style="padding: 15px;background-color: white;">
                                    <canvas id="myPieChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="panel panel-success p1" style="border-radius: 10px;border-bottom: none;">
                    <div class="panel-heading" style="background-color: transparent;color: white;">
                        <div class="row">
                            <div class="col-xs-7 text-left">
                                <div style="font-weight: 500;">Documents</div>
                                <p style="font-size: 20px;font-family: gotham">260</p>
                            </div>
                            <div class="col-xs-5 text-right">
                                <i class="fa fa-bank fa-3x" style="float: left;opacity: 0.3"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="panel panel-success p2" style="border-radius: 10px;border-bottom: none;">
                    <div class="panel-heading" style="background-color: transparent;color: white;">
                        <div class="row">
                            <div class="col-xs-7 text-left">
                                <div style="font-weight: 500;">Dossiers</div>
                                <p style="font-size: 20px;font-family: gotham">260</p>
                            </div>
                            <div class="col-xs-5 text-right">
                                <i class="fa fa-bank fa-3x" style="float: left;opacity: 0.3"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="panel panel-success p3" style="border-radius: 10px;border-bottom: none;">
                    <div class="panel-heading" style="background-color: transparent;color: white;">
                        <div class="row">
                            <div class="col-xs-7 text-left">
                                <div style="font-weight: 500;">Documents</div>
                                <p style="font-size: 20px;font-family: gotham">260</p>
                            </div>
                            <div class="col-xs-5 text-right">
                                <i class="fa fa-bank fa-3x" style="float: left;opacity: 0.3"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="panel panel-success p4" style="border-radius: 10px;border-bottom: none;">
                    <div class="panel-heading" style="background-color: transparent;color: white;">
                        <div class="row">
                            <div class="col-xs-7 text-left">
                                <div style="font-weight: 500;">Dossiers</div>
                                <p style="font-size: 20px;font-family: gotham">260</p>
                            </div>
                            <div class="col-xs-5 text-right">
                                <i class="fa fa-bank fa-3x" style="float: left;opacity: 0.3"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4" style="padding: 10px;">
                <div class="item-dash col-md-12" style="background-color: white;height: 300px;padding: 20px;padding-top: 25px;">
                    <label style="font-weight: 900;">Documents Recents</label>

                    <ul style="width: 100%;padding: 10px;">
                        <li><strong style="font-weight: 600;">Bon d'achat BA001</strong>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>

                    </ul>
                </div>
            </div>
            <div class="col-md-4" style="padding: 10px;">
                <div class="item-dash col-md-12" style="background-color: white;height: 300px;padding: 20px;padding-top: 25px;">
                    <label style="font-weight: 900;">Documents Recents</label>

                    <ul style="width: 100%;padding: 10px;">
                        <li><strong style="font-weight: 600;">Bon d'achat BA001</strong>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>

                    </ul>
                </div>
            </div>
            <div class="col-md-4" style="padding: 10px;">
                <div class="item-dash col-md-12" style="background-color: white;height: 300px;padding: 20px;padding-top: 25px;">
                    <label style="font-weight: 900;">Documents Recents</label>

                    <ul style="width: 100%;padding: 10px;">
                        <li><strong style="font-weight: 600;">Bon d'achat BA001</strong>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>

                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>


<script src="{{% static 'ErpProject/js/Chart.min.js' %}}"></script>
<script src="{{% static 'ErpProject/js/chart-pie-demo.js' %}}"></script>
<script src="{{% static 'ErpProject/js/chart-area-demo.js' %}}"></script>

{{% endblock %}}
    '''.format(nomModule)
    return texte_a_ajouter

#TO DO: Completer design templates
def genDashBoardTemplate3(nomModule):
    texte_a_ajouter = u'''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}}{{% load static %}}{{% load account_filters %}}

<style type="text/css">
    @import url({{% static 'ErpProject/css/home_module.css' %}});
</style>

    '''.format(nomModule)
    return texte_a_ajouter
    
def genCssOrangeTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
    background: -moz-linear-gradient(top,rgba(92, 52, 33, 0.7) 0%,rgba(116, 72, 54, 0.79) 29%,rgba(155, 125, 90, 0.89) 62%,rgb(175, 146, 126) 100%);
    background: -webkit-linear-gradient(top,rgba(92, 52, 33, 0.7) 0%,rgba(116, 72, 54, 0.79) 29%,rgba(155, 125, 90, 0.89) 62%,rgb(175, 146, 126) 100%);
    background: linear-gradient(to bottom,rgba(92, 52, 33, 0.7) 0%,rgba(116, 72, 54, 0.79) 29%,rgba(155, 125, 90, 0.89) 62%,rgb(175, 146, 126) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#b3d64f0d', endColorstr='#e58f4e',GradientType=0 ); /* IE6-9 */
}}
.color_{1}s {{
    background: rgb(104, 53, 28);
    background: -moz-linear-gradient(left,rgba(104, 53, 28, 0.7) 0%,rgba(143, 83, 56, 0.79) 29%,rgba(153, 117, 77, 0.89) 62%,rgb(214, 163, 127) 100%);
    background: -webkit-linear-gradient(left,rgba(104, 53, 28, 0.7) 0%,rgba(143, 83, 56, 0.79) 29%,rgba(153, 117, 77, 0.89) 62%,rgb(214, 163, 127) 100%);
    background: linear-gradient(to right,rgba(104, 53, 28, 0.7) 0%,rgba(143, 83, 56, 0.79) 29%,rgba(153, 117, 77, 0.89) 62%,rgb(214, 163, 127) 100%);
    filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#ff6821', endColorstr='#fd9526', GradientType=1);
    border: none;
    color: white;
}}
/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
    background: #723c21 !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
    border-color: #8f4c2b #8f4c2b #8f4c2b transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #8f4c2b !important;
}}
.active_module_{1} {{
    border-bottom: 4px solid rgba(104, 53, 28, 0.7) !important;
}}
.active_module_{1} > a {{
    color: rgba(214, 79, 13, 1) !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
    background-color: rgba(214, 79, 13, 1) !important;
    color: white !important;
}}
.secondary_color_module_{1} {{
    background-color: rgba(214, 79, 13, 0.6) !important;
    color: white !important;
}}
.thirdy_color_module_{1} {{
    background-color: rgba(214, 79, 13, 0.2) !important;
    color: white !important;
}}
.primary_color_module_{1}:hover {{
    background-color: #d64f0d !important;
    color: white !important;
}}
.breadcrumbs2 .primary_color_module_{1} a {{
    background: #d64f0d !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
    border-color: #d64f0d #d64f0d #d64f0d transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #d64f0d !important;
}}
.module_{1} .head {{
    background-color: #d64f0d !important;
    padding: 10px!important;
    color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/   
        
    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower().replace(" ","_")))
    return texte_a_ajouter

def genCssVertTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
    background: -moz-linear-gradient(top,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    background: -webkit-linear-gradient(top,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    background: linear-gradient(to bottom,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc999900', endColorstr='#c1b507',Gradi0ntType=0 ); /* IE6-9 */
}}
.color_{1}s {{
    background: -moz-linear-gradient(top,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    background: -webkit-linear-gradient(top,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    background: linear-gradient(to bottom,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc999900', endColorstr='#c1b507',Gradi0ntType=0 ); /* IE6-9 */
}}
/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
    background: rgb(20, 102, 71) !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
    border-color: #991b58 #991b58 #991b58 transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #991b58 !important;
}}
.active_module_{1} {{
    border-bottom: 4px solid rgb(20, 102, 71) !important;
}}
.active_module_{1} > a {{
    color: rgb(20, 102, 71) !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
    background-color: rgba(27, 124, 79, 0.8) !important;
    color: white !important;
}}
.primary_color_module_{1}:hover {{
    background-color: #d5ab47 !important;
    color: white !important;
}}
.secondary_color_module_{1} {{
    background-color: rgba(31, 126, 82, 0.8) !important;
    color: white !important;
}}
.thirdy_color_module_{1} {{
    background-color: rgba(27, 124, 79, 0.2) !important;
    color: white !important;
}}
.primary_color_module_{1}:hover {{
    background-color: rgba(154, 194, 175, 0.2) !important;
    color: white !important;
}}
.module_{1} .head {{
    background-color: rgba(27, 124, 79, 0.8)!important;
    padding: 10px!important;
    color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/  
            
    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower().replace(" ","_")))
    return texte_a_ajouter

def genCssBleuTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
    background: -moz-linear-gradient(top,rgba(1, 79, 141, 0.7) 0%,rgba(11, 89, 151, 0.79) 30%,rgba(46, 160, 161, 0.89) 64%,rgba(66, 206, 161, 1) 100%);
    background: -webkit-linear-gradient(top,rgba(1, 79, 141, 0.7) 0%,rgba(11, 89, 151, 0.79) 30%,rgba(46, 160, 161, 0.89) 64%,rgba(66, 206, 161, 1) 100%);
    background: linear-gradient(to bottom,rgba(1, 79, 141, 0.7) 0%,rgba(11, 89, 151, 0.79) 30%,rgba(46, 160, 161, 0.89) 64%,rgba(66, 206, 161, 1) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#b3014f8d', endColorstr='#42cea1',GradientType=0 ); /* IE6-9 */
}}
.color_{1}s {{
    background: rgb(102, 114, 250);
    /* Old browsers */
    background: -moz-linear-gradient(left,rgba(102, 114, 250, 1) 0%,rgba(103, 132, 250, 1) 29%,rgba(104, 152, 252, 1) 52%,rgba(106, 200, 252, 1) 100%);
    background: -webkit-linear-gradient(left,rgba(102, 114, 250, 1) 0%,rgba(103, 132, 250, 1) 29%,rgba(104, 152, 252, 1) 52%,rgba(106, 200, 252, 1) 100%);
    background: linear-gradient(to right,rgba(102, 114, 250, 1) 0%,rgba(103, 132, 250, 1) 29%,rgba(104, 152, 252, 1) 52%,rgba(106, 200, 252, 1) 100%);
    filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#6672fa', endColorstr='#6ac8fc', GradientType=1);
    color: white;
}}
/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
    background: #216ca8 !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
    border-color: #216ca8 #216ca8 #216ca8 transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #216ca8!important;
}}
.active_module_{1} {{
    border-bottom: 4px solid #216ca8 !important;
}}
.active_module_{1} > a {{
    color: #216ca8 !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
    background-color: rgba(33, 108, 168, 1)!important;
    color: white!important;
}}
.secondary_color_module_{1} {{
    background-color: rgba(33, 108, 168, 0.6)!important;
    color: white!important;
}}
.thirdy_color_module_{1} {{
    background-color: rgba(33, 108, 168, 0.2)!important;
    color: white!important;
}}
.primary_color_module_{1}:hover {{
    background-color: #216ca8!important;
    color: white!important;
}}
.module_{1} .head {{
    background-color: rgba(33, 108, 168, 1)!important;
    padding: 10px!important;
    color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/    
        
    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower().replace(" ","_")))
    return texte_a_ajouter

def genCssBleuCielTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
    background: -moz-linear-gradient(top,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
    background: -webkit-linear-gradient(top,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
    background: linear-gradient(to bottom,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#b3d64f0d', endColorstr='#e58f4e',GradientType=0 ); /* IE6-9 */
}}
.color_{1}s {{
    background: rgb(117, 114, 220);
    background: -moz-linear-gradient(left,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
    background: -webkit-linear-gradient(left,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
    background: linear-gradient(to right,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
    filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#ff6821', endColorstr='#fd9526', GradientType=1);
    border: none;
    color: white;
}}
/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
    background: #6977E2 !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
    border-color: #7572DC #7572DC #7572DC transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #7572DC !important;
}}
.active_module_{1} {{
    border-bottom: 4px solid rgba(117, 114, 220, 0.7) !important;
}}
.active_module_{1} > a {{
    color: rgba(106, 121, 227, 1) !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
    background-color: rgba(106, 121, 227, 1) !important;
    color: white !important;
}}
.secondary_color_module_{1} {{
    background-color: rgba(106, 121, 227, 0.6) !important;
    color: white !important;
}}
.thirdy_color_module_{1} {{
    background-color: rgba(106, 121, 227, 0.2) !important;
    color: white !important;
}}
.primary_color_module_{1}:hover {{
    background-color: #6A79E3 !important;
    color: white !important;
}}
.breadcrumbs2 .primary_color_module_{1} a {{
    background: #6A79E3 !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
    border-color: #6A79E3 #6A79E3 #6A79E3 transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #6A79E3 !important;
}}
.module_{1} .head {{
    background-color: #6A79E3 !important;
    padding: 10px!important;
    color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/       
    
    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower().replace(" ","_")))
    return texte_a_ajouter

def genCssMagentaTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
    background: -moz-linear-gradient(top,rgba(89, 15, 92, 0.7) 0%,rgba(118, 39, 121, 0.7) 30%,rgba(162, 88, 163, 0.7) 64%,rgba(192, 157, 194, 0.7) 100%);
    background: -webkit-linear-gradient(top,rgba(89, 15, 92, 0.7) 0%,rgba(118, 39, 121, 0.7) 30%,rgba(162, 88, 163, 0.7) 64%,rgba(192, 157, 194, 0.7) 100%);
    background: linear-gradient(to bottom,rgba(89, 15, 92, 0.7) 0%,rgba(118, 39, 121, 0.7) 30%,rgba(162, 88, 163, 0.7) 64%,rgba(192, 157, 194, 0.7) 100%);
    filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#b361188d', endColorstr='#c21e65', GradientType=0);
}}
.color_{1}s {{
    background: rgba(89, 15, 92, 0.7);
    background: -moz-linear-gradient(left,rgba(89, 15, 92, 0.7) 0%,rgba(89, 15, 92, 0.7) 29%,rgba(89, 15, 92, 0.7) 52%,rgba(89, 15, 92, 0.7) 100%);
    background: -webkit-linear-gradient(left,rgba(89, 15, 92, 0.7) 0%,rgba(89, 15, 92, 0.7) 29%,rgba(89, 15, 92, 0.7) 52%,rgba(89, 15, 92, 0.7) 100%);
    background: linear-gradient(to right,rgba(89, 15, 92, 0.7) 0%,rgba(89, 15, 92, 0.7) 29%,rgba(89, 15, 92, 0.7) 52%,rgba(89, 15, 92, 0.7) 100%);
    filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#494949', endColorstr='#989898', GradientType=1);
}}
/** Liste Active item dans le navbar **/
.active_module_{1} {{
    border-bottom: 4px solid rgb(89, 15, 92) !important;
}}
.active_module_{1} > a {{
    color: rgb(89, 15, 92) !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
    background-color: rgba(89, 15, 92, 0.7) !important;
    color: white !important;
}}
.secondary_color_module_{1} {{
    background-color: rgba(162, 88, 163, 0.7) !important;
    color: white !important;
}}
.thirdy_color_module_{1} {{
    background-color: rgba(192, 157, 194, 0.2) !important;
    color: white !important;
}}
.primary_color_module_{1}:hover {{
    background-color: #8600a7 !important;
    color: white !important;
}}
.module_{1} .head {{
    background-color: rgba(89, 15, 92, 0.7) !important;
    padding: 10px!important;
    color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/       
    
    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower().replace(" ","_")))
    return texte_a_ajouter

def genCssPourpreTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
    background: rgb(169,3,41);
    background: -moz-linear-gradient(top,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
    background: -webkit-linear-gradient(top,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
    background: linear-gradient(to bottom,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#a90329', endColorstr='#6d0019',GradientType=0 );
    
}}
.color_{1}s {{
    background: rgb(169,3,41);
    background: -moz-linear-gradient(top,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
    background: -webkit-linear-gradient(top,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
    background: linear-gradient(to bottom,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#a90329', endColorstr='#6d0019',GradientType=0 );	
}}

/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
    background: #991b58 !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
border-color: #991b58 #991b58 #991b58 transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #991b58 !important;
}}
.active_module_{1} {{
    border-bottom: 4px solid #991b58 !important;
}}
.active_module_{1} > a {{
    color: #991b58 !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1}_new_color{{
    background:#BD6C93;
    color:#000;
}}
.primary_color_module_{1} {{
    background-color: rgba(153, 27, 88, 1) !important;
    color: white !important;
}}
.secondary_color_module_{1} {{
    background-color: rgba(153, 27, 88, 0.6) !important;
    color: white !important;
}}
.thirdy_color_module_{1} {{
    background-color: rgba(153, 27, 88, 0.2) !important;
    color: white !important;
}}
.primary_color_module_{1}:hover {{
    background-color: #991b58 !important;
    color: white !important;
}}
.secondary_color_module_{1} {{
    background-color: rgba(33, 108, 168, 0.6);
    color: white;
}}
.thirdy_color_module_{1} {{
    background-color: rgba(33, 108, 168, 0.2);
    color: white;
}}
.primary_color_module_{1}:hover {{
    background-color: #216ca8;
    color: white;
}}
.module_{1} .head {{
    background-color: rgba(153, 27, 88, 1) !important;
    padding: 10px!important;
    color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/              
    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower().replace(" ","_")))
    return texte_a_ajouter


def genDAOofModelContentType(content_type_id, module_id):    
    module = dao_module.toGetModule(module_id)
    nomModule = module.nom_application
    
    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()
    
    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__
    
    list_nom_champ = [] 
    list_type_champ = []
    list_champs = []
    list_champs_api = [] 
    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): list_nom_champ.append(field.name) 

    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): list_type_champ.append(field.__class__.__name__)         

    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): list_champs.append(field) 
        
    for field in model_class._meta.get_fields(): 
        if field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): list_champs_api.append(field) 
            
    #Creation dossier dao
    try:
        path = os.path.abspath(os.path.curdir)
        path = path + "\\{0}\\dao".format(nomModule)
        os.mkdir(utils.format_path(path))
    except Exception as e:
        pass

    print("Dossier Dao cree")
    nomdao="dao_{0}".format(nom_modele.lower())
    path = path + "\\{0}.py".format(nomdao)
    
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')
    
    # WRITE import lib  
    if nomModule == "ErpBackOffice": texte_a_ajouter_dao = "from __future__ import unicode_literals\nfrom {0}.models import *\nfrom django.utils import timezone\nfrom django.forms import model_to_dict".format(nomModule,nom_modele_class,nomdao)
    else : texte_a_ajouter_dao = "from __future__ import unicode_literals\nfrom {0}.models import *\nfrom ErpBackOffice.models import *\nfrom ModuleConfiguration.models import *\nfrom ErpBackOffice.utils.separateur import makeFloat, checkDateTimeFormat, checkDateFormat, makeStringFromFloatExcel, makeInt, makeIntId, makeString\nfrom django.utils import timezone\nfrom django.forms import model_to_dict\nimport traceback\nfrom ErpBackOffice.utils.utils import utils".format(nomModule,nom_modele_class,nomdao)

    # WRITE Class Dao and Properties
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\nclass {}(object):".format(nomdao)
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        try:
            nom_champ = list_nom_champ[i]
            nom_champ = nom_champ.lower()
        except Exception as e:
            pass
        try:
            texte_add = ""
            type_data = str(list_type_champ[i])            
            if type_data in ("CharField", "EmailField", "TextField") :
                texte_add = "\n\t{0} = ''".format(nom_champ)
            elif type_data == "IntegerField":
                texte_add = "\n\t{0} = 0".format(nom_champ)
            elif type_data == "DateTimeField":
                texte_add = "\n\t{0} = None".format(nom_champ)
            elif type_data == "DateField":
                texte_add = "\n\t{0} = None".format(nom_champ)
            elif type_data == "FloatField":
                texte_add = "\n\t{0} = 0.0".format(nom_champ)
            elif type_data == "BooleanField" :
                texte_add = "\n\t{0} = False".format(nom_champ)
            elif type_data == "ManyToManyField" :
                texte_add = "\n\t{0} = []".format(nom_champ)
            elif type_data in ("ForeignKey", "OneToOneField"):
                texte_add = "\n\t{0}_id = None".format(nom_champ)
            else:
                texte_add = "\n\t{0} = None".format(nom_champ)
        except Exception as e:
            pass
        texte_a_ajouter_dao = texte_a_ajouter_dao + texte_add

    # WRITE toList() Function
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t@staticmethod\n\tdef toList(query='', auteur=None):\n\t\ttry:\n\t\t\tif query == '':\n\t\t\t\tif auteur == None or auteur.societe_id == None: return {0}.objects.all().order_by('-creation_date')\n\t\t\t\treturn {0}.objects.filter(Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')).order_by('-creation_date').distinct()\n\t\t\telse:\n\t\t\t\tif auteur == None or auteur.societe_id == None: return {0}.objects.filter(".format(nom_modele_class)
    
    text_parenthese = ""
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        try:
            nom_champ = list_nom_champ[i].lower()
            type_data = str(list_type_champ[i])  
        except Exception as e:
            pass
        
        if type_data in ("IntegerField", "FloatField", "EmailField", "CharField", "TextField"):
            text_parenthese = text_parenthese + "| Q({0}__icontains = query) ".format(nom_champ)
        
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_parenthese
    texte_a_ajouter_dao = texte_a_ajouter_dao.replace("(| ", "(")    
    texte_a_ajouter_dao = texte_a_ajouter_dao + ").order_by('-creation_date').distinct()"
    texte_a_ajouter_dao = texte_a_ajouter_dao.replace(") )", "))") 
    
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\t\telse: return {0}.objects.filter((Q(societe_id = auteur.societe_id) | Q(societe__code = 'MD')) & (".format(nom_modele_class)
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_parenthese
    texte_a_ajouter_dao = texte_a_ajouter_dao.replace("(| ", "(")
    texte_a_ajouter_dao = texte_a_ajouter_dao + ")).order_by('-creation_date').distinct()"
    texte_a_ajouter_dao = texte_a_ajouter_dao.replace(") )", "))") 
       
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE LA SELECTION DE LA LISTE {1}')\n\t\t\t#print(e)\n\t\t\treturn []".format(nom_modele.lower(),nom_modele.upper())


    # WRITE toListAll() Function
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t@staticmethod\n\tdef toListAll(query=''):\n\t\ttry:\n\t\t\tif query == '':\n\t\t\t\treturn {0}.objects.all().order_by('-creation_date')\n\n\t\t\treturn {0}.objects.filter(".format(nom_modele_class)
    
    text_parenthese = ""
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        try:
            nom_champ = list_nom_champ[i].lower()
            type_data = str(list_type_champ[i])  
        except Exception as e:
            pass
        
        if type_data in ("IntegerField", "FloatField", "EmailField", "CharField", "TextField"):
            text_parenthese = text_parenthese + "| Q({0}__icontains = query) ".format(nom_champ)
        
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_parenthese
    texte_a_ajouter_dao = texte_a_ajouter_dao.replace("(| ", "(")    
    texte_a_ajouter_dao = texte_a_ajouter_dao + ").order_by('-creation_date').distinct()"
    texte_a_ajouter_dao = texte_a_ajouter_dao.replace(") )", "))") 
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE LA SELECTION DE LA LISTE {1}')\n\t\t\t#print(e)\n\t\t\treturn []".format(nom_modele.lower(),nom_modele.upper())

    # WRITE toListJson() Function
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t@staticmethod\n\tdef toListJson(model=[]):\n\t\ttry:\n\t\t\tlistes = []\n\t\t\tfor item in model: \n\t\t\t\telement = {"
    texte_boucle = ""
    for i in range(0, len(list_champs_api)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs_api[i].name.lower()
            type_data = str(list_champs_api[i].__class__.__name__)  
            default_value = list_champs_api[i].default
            is_null = list_champs_api[i].null
        except Exception as e:
            pass

        # Attribution des champs
        if type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : item.{0}.__str__() if item.{0} else '-',".format(nom_champ)
            elif type_data == "DateTimeField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "DateField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "FloatField" and list_champs_api[i].choices == None: 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : makeFloat(item.{0}),".format(nom_champ)
            elif type_data == "BooleanField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "EmailField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : str(item.{0}),".format(nom_champ)
            elif type_data == "CharField" and list_champs_api[i].choices == None: 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : str(item.{0}),".format(nom_champ)
            elif type_data == "TextField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : str(item.{0}),".format(nom_champ)
            elif type_data == "IntegerField" and list_champs_api[i].choices == None:
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : makeInt(item.{0}),".format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs_api[i].choices != None:
                if type_data == "CharField":
                    texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : str(item.value_{0}),".format(nom_champ)
                if type_data == "IntegerField":
                    texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : makeInt(item.value_{0}),".format(nom_champ)
                if type_data == "FloatField":
                    texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : makeFloat(item.value_{0}),".format(nom_champ)
            elif type_data in ("ImageField", "FileField"): 
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : item.{0}.url if item.{0} != None else None,".format(nom_champ)
            else:
                texte_boucle = texte_boucle + "\n\t\t\t\t\t'{0}' : item.{0},".format(nom_champ)

    texte_a_ajouter_dao = texte_a_ajouter_dao + texte_boucle
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\t\t}\n\t\t\t\tlistes.append(element)\n\t\t\treturn listes"
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE LA SELECTION DE LA LISTE {1}  EN JSON')\n\t\t\t#print(e)\n\t\t\treturn []".format(nom_modele.lower(),nom_modele.upper())    
        
    # WRITE toCreate() Function declaration
    text_parenthese = "\n\n\t@staticmethod\n\tdef toCreate("
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_nom_champ[i].lower()
            type_data = str(list_type_champ[i])  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        check_nullable = True          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False
        
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
            
        #if check_nullable: 
        if type_data == "ManyToManyField":
            text_parenthese = text_parenthese + "{0} = [], ".format(nom_champ)
        elif type_data in ("EmailField", "CharField", "TextField"):
            text_parenthese = text_parenthese + "{0} = '', ".format(nom_champ)
        elif type_data == "BooleanField":
            text_parenthese = text_parenthese + "{0} = False, ".format(nom_champ)
        elif type_data == "IntegerField":
            text_parenthese = text_parenthese + "{0} = 0, ".format(nom_champ)
        elif type_data in ("FloatField", "DecimalField"):
            text_parenthese = text_parenthese + "{0} = 0.0, ".format(nom_champ)
        else:
            text_parenthese = text_parenthese + "{0} = None, ".format(nom_champ)
        #else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
        
        
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + "):"
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_parenthese

    # WRITE toCreate() Function Body
    text_tocreate = "\n\t\ttry:\n\t\t\t{0} = {1}()".format(nom_modele.lower(),nomdao)
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        try:
            nom_champ = list_nom_champ[i]
            nom_champ = nom_champ.lower()
            type_data = str(list_type_champ[i])  
        except Exception as e:
            pass
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        text_tocreate = text_tocreate + "\n\t\t\t{0}.{1} = {1}".format(nom_modele.lower(),nom_champ)
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_tocreate
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\treturn {0}\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE LA CREATION DE LA {1}')\n\t\t\t#print(e)\n\t\t\treturn None".format(nom_modele.lower(),nom_modele.upper())

    # WRITE toSave() Function
    text_tosave = "\n\n\t@staticmethod\n\tdef toSave(auteur, objet_dao_{0}, request_post = []):\n\t\ttry:\n\t\t\t{0}  = {1}()".format(nom_modele.lower(),nom_modele_class)
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_nom_champ[i]
            type_data = str(list_type_champ[i])  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        check_nullable = True          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False
        
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if type_data != "ManyToManyField": 
            if type_data in ("ImageField", "FileField") or check_nullable: 
                text_tosave = text_tosave + "\n\t\t\tif objet_dao_{0}.{1} != None : {0}.{1} = objet_dao_{0}.{1}".format(nom_modele.lower(), nom_champ.lower())
            else: text_tosave = text_tosave + "\n\t\t\t{0}.{1} = objet_dao_{0}.{1}".format(nom_modele.lower(), nom_champ.lower())
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_tosave
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\tif auteur != None : {0}.auteur_id = auteur.id\n\n\t\t\t{0}.save()".format(nom_modele.lower())

    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel") and field.__class__.__name__ == 'ManyToManyField' and field.related_model != None: 
            texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\t#Ajout Champs (ManyToMany - Creation)\n\t\t\tfor i in range(0, len(objet_dao_{0}.{1})):\n\t\t\t\ttry:\n\t\t\t\t\tobjet = {2}.objects.get(pk = objet_dao_{0}.{1}[i])\n\t\t\t\t\t{0}.{1}.add(objet)\n\t\t\t\texcept Exception as e: pass".format(nom_modele.lower(),field.name, field.related_model.__name__)

    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\t#HISTORIQUE AJOUT\n\t\t\tif request_post != []:\n\t\t\t\tdata={{}}\n\t\t\t\tdata['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet\n\t\t\t\tdata['valeur_avant'] = ''\n\t\t\t\tdata['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)\n\t\t\t\tdata['modele'] = '{2} [{1}]'\n\t\t\t\tutils.history_in_database(data)".format(nom_modele.lower(), nom_modele_class, nom_modele_verbose)
            
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\treturn True, {0}, ''\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE L ENREGISTREMENT DE LA {1}')\n\t\t\t#print(e)\n\t\t\treturn False, None, e".format(nom_modele.lower(),nom_modele.upper())

    # WRITE toUpdate() Function
    text_toupdate = "\n\n\t@staticmethod\n\tdef toUpdate(id, objet_dao_{0}, auteur = None, request_post = []):\n\t\ttry:\n\t\t\t{0} = {2}.objects.get(pk = id)\n\t\t\t# ON RECUPERE L'ANCIENNE VALEUR DE OBJET\n\t\t\tbefore_{0} = model_to_dict({0})\n".format(nom_modele.lower(),nom_modele.upper(),nom_modele_class)
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        try:
            nom_champ = list_nom_champ[i]
            nom_champ = nom_champ.lower()
            type_data = str(list_type_champ[i])  
        except Exception as e:
            pass
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if type_data != "ManyToManyField": 
            if type_data in ("ImageField", "FileField"): 
                text_toupdate = text_toupdate + "\n\t\t\tif objet_dao_{0}.{1} != None : {0}.{1} = objet_dao_{0}.{1}".format(nom_modele.lower(), nom_champ.lower())
            else: text_toupdate = text_toupdate + "\n\t\t\t{0}.{1} = objet_dao_{0}.{1}".format(nom_modele.lower(), nom_champ.lower())
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_toupdate   
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\tif auteur != None : {0}.update_by_id = auteur.id".format(nom_modele.lower())
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\t{0}.save()".format(nom_modele.lower(),nom_modele.upper())

    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel") and field.__class__.__name__ == 'ManyToManyField' and field.related_model != None: 
            texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\t#Mise à jour Champs (ManyToMany - Creation)\n\t\t\t{1}_old = {0}.{1}.all()\n\t\t\t{1}_updated = []\n\t\t\tfor i in range(0, len(objet_dao_{0}.{1})):\n\t\t\t\ttry:\n\t\t\t\t\tobjet = {2}.objects.get(pk = objet_dao_{0}.{1}[i])\n\t\t\t\t\tif objet not in {1}_old: {0}.{1}.add(objet)\n\t\t\t\t\t{1}_updated.append(objet.id)\n\t\t\t\texcept Exception as e: pass\n\t\t\t# Suppression éléments qui n'existent plus\n\t\t\tfor item in {1}_old:\n\t\t\t\tif item.id not in {1}_updated: {0}.{1}.remove(item)".format(nom_modele.lower(),nom_champ.lower(), field.related_model.__name__)

    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\t#HISTORIQUE MISE A JOUR\n\t\t\tif request_post != []:\n\t\t\t\tdata={{}}\n\t\t\t\tdata['auteur'] =  'Unknown' if auteur == None else auteur.nom_complet\n\t\t\t\tdata['valeur_avant'] = json.dumps(before_{0}, indent=4, sort_keys=True, default=str)\n\t\t\t\tdata['valeur_apres']= json.dumps(request_post, indent=4, sort_keys=True, default=str)\n\t\t\t\tdata['modele'] = '{2} [{1}]'\n\t\t\t\tutils.history_in_database(data)".format(nom_modele.lower(), nom_modele_class, nom_modele_verbose)
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\treturn True, {0}, ''\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE LA MODIFICATION DE LA {1}')\n\t\t\t#print(e)\n\t\t\treturn False, None, e".format(nom_modele.lower(),nom_modele.upper())
    
    # WRITE toGet() Function
    text_toget = "\n\n\t@staticmethod\n\tdef toGet(id):\n\t\ttry:\n\t\t\treturn {2}.objects.get(pk = id)\n\t\texcept Exception as e:\n\t\t\treturn None".format(nom_modele.lower(),nom_modele.upper(),nom_modele_class)
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_toget
    
    # WRITE toListById() Function
    text_toget = "\n\n\t@staticmethod\n\tdef toListById(id):\n\t\ttry:\n\t\t\treturn {2}.objects.filter(pk = id)\n\t\texcept Exception as e:\n\t\t\treturn []".format(nom_modele.lower(),nom_modele.upper(),nom_modele_class)
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_toget
        
    # WRITE toDelete() Function
    text_todelete = "\n\n\t@staticmethod\n\tdef toDelete(id):\n\t\ttry:\n\t\t\t{0} = {2}.objects.get(pk = id)\n\t\t\t{0}.delete()\n\t\t\treturn True\n\t\texcept Exception as e:\n\t\t\treturn False".format(nom_modele.lower(),nom_modele.upper(),nom_modele_class)
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_todelete    
    
    fichier.write(texte_a_ajouter_dao)
    fichier.close()
    print("Fichier Dao cree")
    
    
def genTemplateOfContentType(content_type_id, module_id, relateds = []):
    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()
    module = dao_module.toGetModule(module_id)
    print("genTemplateOfContentType #1")
    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__
    nomdao = "dao_{0}".format(nom_modele.lower())
    nom_pattern = 'module_{0}'.format(unidecode.unidecode(module.nom_module.lower().replace(" ","_")))
    nomModule = module.nom_application
    print("genTemplateOfContentType #2")
    
    url_name_create = "{1}_add_{0}".format(nom_modele.lower(),nom_pattern)
    url_name_list = "{1}_list_{0}".format(nom_modele.lower(),nom_pattern)
    url_name_update = "{1}_update_{0}".format(nom_modele.lower(),nom_pattern)
    url_name_reporting = "{1}_get_generer_{0}".format(nom_modele.lower(),nom_pattern)
    
    print("genTemplateOfContentType #3")    
    list_champs = [] 
    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): list_champs.append(field) 
        
    # CREATION FONCTIONS CRUD DANS views.py
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\views.py".format(nomModule)
    fichier = codecs.open(utils.format_path(path),"a", encoding='utf-8')
    print("genTemplateOfContentType #4")
    # GET LISTER
    texte_a_ajouter_views_py = "\n\n# {2} CONTROLLERS\nfrom {4}.dao.{1} import {1}\n\ndef get_lister_{0}(request):\n\ttry:\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)\n\t\tif response != None: return response\n\n\t\tview, query, page, count = utils.get_list_request(request)\n\t\t#print(f'view {{view}} query {{query}} page {{page}} count {{count}}')\n\n\t\t#*******Filtre sur les règles **********#\n\t\tmodel = auth.toListWithRules({1}.toList(query,utilisateur), permission, groupe_permissions, utilisateur)\n\t\t#******* End Regle *******************#\n\n\t\tmodel = pagination.toGetData(model, page, count)\n\n\t\tif request.method == 'POST':\n\t\t\tcontext = {{\n\t\t\t\t'error' : False,\n\t\t\t\t'message' : 'Recupération effectuée avec succès',\n\t\t\t\t'model' : {1}.toListJson(model.object_list),\n\t\t\t\t'view' : view,\n\t\t\t\t'query' : query,\n\t\t\t\t'page' : page,\n\t\t\t\t'count' : count,\n\t\t\t}}\n\t\t\tcontext = pagination.toAddVarsToContext(model, context)\n\t\t\treturn JsonResponse(context, safe=False)\n\n\t\tisPopup = False\n\t\tif 'isPopup' in request.GET:\n\t\t\tisPopup = True\n\t\t\tview = 'list'\n\n\t\tcontext = {{\n\t\t\t'title' : \"Liste des {3}\",\n\t\t\t'model' : model,\n\t\t\t'view' : view,\n\t\t\t'query' : query,\n\t\t\t'page' : page,\n\t\t\t'count' : count,\n\t\t\t'isPopup' : isPopup,\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'user_actions': actions,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation()\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{4}/{0}/list.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\tif request.method == 'POST': return auth.toReturnApiFailed(request, e, traceback.format_exc())\n\t\telse: return auth.toReturnFailed(request, e, traceback.format_exc(), reverse('{5}_index'))".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose_plural.lower(),nomModule,nom_pattern)

    # GET CREER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef get_creer_{0}(request):\n\ttry:\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)\n\t\tif response != None: return response\n\n\t\tcontext = {{\n\t\t\t'title' : \"Formulaire d'enregistrement - {1}\",\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'user_actions': actions,\n\t\t\t'isPopup': True if 'isPopup' in request.GET else False,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation' : dao_organisation.toGetMainOrganisation(),\n\t\t\t'model' : {2}(),".format(nom_modele.lower(),nom_modele_verbose,nom_modele_class)
    related_models = []
    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel") and field.__class__.__name__ in ('ForeignKey', 'ManyToManyField', 'OneToOneField') and field.related_model != None and field.related_model.__name__  not in related_models: 
            related_model = field.related_model.__name__
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t'{0}s' : {1}.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],".format(related_model.replace("Model_", "").lower(), related_model)
            related_models.append(related_model)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{1}/{0}/add.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc(), reverse('{2}_list_{0}'))".format(nom_modele.lower(),nomModule, nom_pattern)
    print("genTemplateOfContentType #5")
    # POST CREER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n@transaction.atomic\ndef post_creer_{0}(request):\n\tsid = transaction.savepoint()\n\ttry:\n\t\tsame_perm_with = '{1}'\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)\n\t\tif response != None: return response\n".format(nom_modele.lower(), url_name_create)
    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        texte_check_nullable = "" 
        texte_check_format_date = "\n\t\tif is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date saisi', '', msg = 'La valeur saisi sur le champ \\'{1}\\' ne correspond pas au format jj/mm/aaaa')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))  
        texte_check_format_datetime = "\n\t\tif is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \\'{1}\\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'")) 
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\tif {0}_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))
            else : texte_check_nullable = "\n\t\tif {0} in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))

        # Attribution des champs
        if type_data in ("ForeignKey", "OneToOneField"): 
            texte_boucle = texte_boucle + "\n\n\t\t{0}_id = makeIntId(request.POST['{0}_id'])".format(nom_champ) + texte_check_nullable
        elif type_data == "ManyToManyField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.POST.getlist('{0}', None)".format(nom_champ)
        elif type_data == "DateTimeField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}']){1}\n\t\tis_formated, {0} = checkDateTimeFormat({0}){2}".format(nom_champ, texte_check_nullable, texte_check_format_datetime)
        elif type_data == "DateField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}']){1}\n\t\tis_formated, {0} = checkDateFormat({0}){2}".format(nom_champ, texte_check_nullable, texte_check_format_date)
        elif type_data == "FloatField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = makeFloat(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "BooleanField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = True if '{0}' in request.POST else False".format(nom_champ)
        elif type_data == "EmailField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "CharField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "TextField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "IntegerField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = makeInt(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data in ("ImageField", "FileField"): 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.FILES['{0}'] if '{0}' in request.FILES else None".format(nom_champ)
        else:
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.POST['{0}']".format(nom_champ)  + texte_check_nullable

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tauteur = identite.utilisateur(request)"
    
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t{0} = {1}.toCreate(".format(nom_modele.lower(),nomdao)
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        check_nullable = True          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False
            
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
        #if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
        #else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + text_parenthese    
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\tsaved, {0}, message = {1}.toSave(auteur, {0}, request.POST)\n\n\t\tif saved == False: raise Exception(message)".format(nom_modele.lower(),nomdao)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t#*******Filtre sur les règles **********#\n\t\tmodel = auth.toGetWithRules({1}.toListById({0}.id), permission, groupe_permissions, utilisateur)\n\t\t#******* End Regle *******************#\n\n\t\tif model == None: \n\t\t\ttransaction.savepoint_rollback(sid)\n\t\t\treturn auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la création', '', msg = 'Vous n\\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')".format(nom_modele.lower(),nomdao)
    for i in range(0, len(relateds)):
        if relateds[i] != "":
            list_relateds = relateds[i].split(",")
            content_id = list_relateds[0]
            field_name = list_relateds[1]
            field_type = list_relateds[2]
            model_related = ContentType.objects.get(pk = content_id)
            model_class_related = model_related.model_class()
            nom_model_class_related = model_related.model_class().__name__
            nom_model_related = nom_model_class_related.replace("Model_", "").lower()
            input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t#Ajout Champ (OneToMany - Creation)\n\t\t{1} = request.POST.getlist('{1}', [])\n\t\tfor i in range(0, len({1})):\n\t\t\ttry:\n\t\t\t\tobjet = {2}.objects.get(pk = {1}[i])\n\t\t\t\tobjet.{3} = {0}\n\t\t\t\tobjet.save()\n\t\t\texcept Exception as e: pass".format(nom_modele.lower(), input_name_related, nom_model_class_related, field_name)                
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t#Initialisation du workflow\n\t\twkf_task.initializeWorkflow(auteur, {0})\n\n\t\tisPopup = 0\n\t\tif 'isPopup' in request.POST: isPopup = 1\n\n\t\ttransaction.savepoint_commit(sid)\n\t\tcontext = {{\n\t\t\t'error' : False,\n\t\t\t'message' : 'Enregistrement effectué avec succès',\n\t\t\t'isPopup': isPopup,\n\t\t\t'id' : {0}.id,\n\t\t}}\n\t\treturn JsonResponse(context, safe=False)\n\texcept Exception as e:\n\t\ttransaction.savepoint_rollback(sid)\n\t\treturn auth.toReturnApiFailed(request, e, traceback.format_exc())".format(nom_modele.lower())
    print("genTemplateOfContentType #6")
    # GET SELECT
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef get_select_{0}(request,ref):\n\ttry:\n\t\tsame_perm_with = '{1}'\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)\n\t\tif response != None: return response".format(nom_modele.lower(), url_name_list)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t{0} = {1}.toGet(ref)\n\n\t\tif 'isPopup' in request.GET:\n\t\t\tpopup_response_data = json.dumps({{'value': str({0}.id),'obj': str({0})}})\n\t\t\treturn TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', {{ 'popup_response_data': popup_response_data }})\n\n\t\treturn HttpResponseRedirect(reverse('{4}_detail_{0}', args=({0}.id,)))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(), nomdao, nom_modele_class, nomModule, nom_pattern, nom_modele_verbose)
    print("genTemplateOfContentType #7")
    # GET DETAILS
    texte_a_ajouter_views_py= texte_a_ajouter_views_py + "\n\ndef get_details_{0}(request,ref):\n\ttry:\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)\n\t\tif response != None: return response".format(nom_modele.lower())
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tref = int(ref)\n\n\t\t#*******Filtre sur les règles **********#\n\t\t{0} = auth.toGetWithRules({1}.toListById(ref), permission, groupe_permissions, utilisateur)\n\t\t#******* End Regle *******************#\n\n\t\tif {0} == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))\n\n\t\thistorique, transitions_etapes_suivantes, content_type_id, documents = wkf_task.get_details(utilisateur, {0}) \n\n\t\tcontext = {{\n\t\t\t'title' : \"Détails - {5} : {{}}\".format({0}),\n\t\t\t'model' : {0},\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'user_actions': actions,\n\t\t\t'historique': historique,\n\t\t\t'etapes_suivantes' : transitions_etapes_suivantes,\n\t\t\t'content_type_id': content_type_id,\n\t\t\t'documents': documents,\n\t\t\t'roles': groupe_permissions,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation(),\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{3}/{0}/item.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc(), reverse('{4}_list_{0}'))".format(nom_modele.lower(), nomdao, nom_modele_class, nomModule, nom_pattern, nom_modele_verbose)
    print("genTemplateOfContentType #8")
    # GET MODIFIER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py +"\n\ndef get_modifier_{0}(request,ref):\n\ttry:\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)\n\t\tif response != None: return response\n\n\t\tref = int(ref)\n\t\tmodel = {1}.toGet(ref)\n\t\tcontext = {{\n\t\t\t'title' : \"Formulaire de mise à jour - {2}\",\n\t\t\t'model':model,\n\t\t\t'utilisateur': utilisateur,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation(),".format(nom_modele.lower(),nomdao,nom_modele_verbose,nomModule)
    related_models = []
    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel") and field.__class__.__name__ in ('ForeignKey', 'ManyToManyField', 'OneToOneField') and field.related_model != None and field.related_model.__name__  not in related_models: 
            related_model = field.related_model.__name__
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t'{0}s' : {1}.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],".format(related_model.replace("Model_", "").lower(), related_model)
            related_models.append(related_model)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py +"\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{1}/{0}/update.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomModule)
    print("genTemplateOfContentType #9")            
    #POST MODIFIER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n@transaction.atomic\ndef post_modifier_{0}(request):\n\tsid = transaction.savepoint()\n\tid = int(request.POST['ref'])\n\ttry:\n\t\tsame_perm_with = '{1}'\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)\n\t\tif response != None: return response\n".format(nom_modele.lower(), url_name_update)
    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        texte_check_nullable = ""   
        texte_check_format_date = "\n\t\tif is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date saisi', '', msg = 'La valeur saisi sur le champ \\'{1}\\' ne correspond pas au format jj/mm/aaaa')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))  
        texte_check_format_datetime = "\n\t\tif is_formated == False: return auth.toReturnApiFailed(request, 'Mauvais format Date et temps saisi', '', msg = 'La valeur saisi sur le champ \\'{1}\\' ne correspond pas au format jj/mm/aaaa HH:MM:SS')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'")) 
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\tif {0}_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))
            else : texte_check_nullable = "\n\t\tif {0} in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))

        # Attribution des champs
        if type_data in ("ForeignKey", "OneToOneField"): 
            texte_boucle = texte_boucle + "\n\n\t\t{0}_id = makeIntId(request.POST['{0}_id'])".format(nom_champ) + texte_check_nullable
        elif type_data == "ManyToManyField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.POST.getlist('{0}', None)".format(nom_champ)
        elif type_data == "DateTimeField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}']){1}\n\t\tis_formated, {0} = checkDateTimeFormat({0}){2}".format(nom_champ, texte_check_nullable, texte_check_format_datetime)
        elif type_data == "DateField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}']){1}\n\t\tis_formated, {0} = checkDateFormat({0}){2}".format(nom_champ, texte_check_nullable, texte_check_format_date)
        elif type_data == "FloatField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = makeFloat(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "BooleanField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = True if '{0}' in request.POST else False".format(nom_champ)
        elif type_data == "EmailField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "CharField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "TextField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "IntegerField": 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = makeInt(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data in ("ImageField", "FileField"): 
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.FILES['{0}'] if '{0}' in request.FILES else None".format(nom_champ)
        else:
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.POST['{0}']".format(nom_champ)  + texte_check_nullable
            
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\tauteur = identite.utilisateur(request)"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t{0} = {1}.toCreate(".format(nom_modele.lower(),nomdao)
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        check_nullable = True          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False
            
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
        #if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
        #else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + text_parenthese
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\tsaved, {0}, message = {1}.toUpdate(id, {0}, auteur, request.POST)\n\n\t\tif saved == False: raise Exception(message)".format(nom_modele.lower(), nomdao)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t#*******Filtre sur les règles **********#\n\t\tmodel = auth.toGetWithRules({1}.toListById({0}.id), permission, groupe_permissions, utilisateur)\n\t\t#******* End Regle *******************#\n\n\t\tif model == None: \n\t\t\ttransaction.savepoint_rollback(sid)\n\t\t\treturn auth.toReturnApiFailed(request, 'Erreur: Violation de règle sur la modification', '', msg = 'Vous n\\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')".format(nom_modele.lower(),nomdao)
    for i in range(0, len(relateds)):
        if relateds[i] != "":
            list_relateds = relateds[i].split(",")
            content_id = list_relateds[0]
            field_name = list_relateds[1]
            field_type = list_relateds[2]
            model_related = ContentType.objects.get(pk = content_id)
            model_class_related = model_related.model_class()
            nom_model_class_related = model_related.model_class().__name__
            nom_model_related = nom_model_class_related.replace("Model_", "").lower()
            input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
            print("input_name_related: {}".format(input_name_related))
            print("model_class_related: {}".format(model_class_related))
            related_query_name = ""
            if field_type == "ForeignKey":
                related_query_name = model_class_related._meta.get_field(field_name).related_query_name()
                if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name) 
            elif field_type == "ManyToManyRel":
                if field_name.startswith("model_") : related_query_name = "{}_set".format(field_name)
                else: related_query_name = field_name
            print("related_query_name: {}".format(related_query_name))
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t#MAJ Champ (OneToMany - Modification)\n\t\t{1} = request.POST.getlist('{1}', [])\n\t\t{0}.{4}.all().update({3} = None)\n\t\tfor i in range(0, len({1})):\n\t\t\ttry:\n\t\t\t\tobjet = {2}.objects.get(pk = {1}[i])\n\t\t\t\tobjet.{3} = {0}\n\t\t\t\tobjet.save()\n\t\t\texcept Exception as e: pass".format(nom_modele.lower(), input_name_related, nom_model_class_related, field_name, related_query_name)   
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tisPopup = 0\n\t\tif 'isPopup' in request.POST: isPopup = 1\n\n\t\ttransaction.savepoint_commit(sid)\n\t\tcontext = {{\n\t\t\t'error' : False,\n\t\t\t'message' : 'Mise à jour effectuée avec succès',\n\t\t\t'isPopup': isPopup,\n\t\t\t'id' : {0}.id,\n\t\t}}\n\t\treturn JsonResponse(context, safe=False)\n\texcept Exception as e:\n\t\ttransaction.savepoint_rollback(sid)\n\t\treturn auth.toReturnApiFailed(request, e, traceback.format_exc())".format(nom_modele.lower())

    # GET DUPLIQUER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py +"\n\ndef get_dupliquer_{0}(request,ref):\n\ttry:\n\t\tsame_perm_with = '{3}'\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)\n\t\tif response != None: return response\n\n\t\tref = int(ref)\n\t\tmodel = {1}.toGet(ref)\n\t\tcontext = {{\n\t\t\t'title' : \"Formulaire d'enregistrement\",\n\t\t\t'model':model,\n\t\t\t'utilisateur': utilisateur,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation(),".format(nom_modele.lower(), nomdao, nom_modele_verbose, url_name_create)
    related_models = []
    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel") and field.__class__.__name__ in ('ForeignKey', 'ManyToManyField', 'OneToOneField') and field.related_model != None and field.related_model.__name__  not in related_models: 
            related_model = field.related_model.__name__
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t'{0}s' : {1}.objects.filter(Q(societe_id = utilisateur.societe_id) | Q(societe__code = 'MD')).order_by('-id')[:10],".format(related_model.replace("Model_", "").lower(), related_model)
            related_models.append(related_model)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py +"\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{3}/{0}/duplicate.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomdao,nom_modele_verbose,nomModule)
    print("genTemplateOfContentType #10")    
    # GET IMPRIMER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef get_imprimer_{0}(request,ref):\n\ttry:\n\t\tsame_perm_with = '{1}'\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)\n\t\tif response != None: return response".format(nom_modele.lower(),url_name_list)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tref = int(ref)\n\n\t\t#*******Filtre sur les règles **********#\n\t\t{0} = auth.toGetWithRules({1}.toListById(ref), permission, groupe_permissions, utilisateur)\n\t\t#******* End Regle *******************#\n\n\t\tif {0} == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))\n\n\t\tcontext = {{\n\t\t\t'title' : \"Détails - {2} : {{}}\".format({0}),\n\t\t\t'model' : {0},\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'user_actions': actions,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation(),\n\t\t}}".format(nom_modele.lower(), nomdao, nom_modele_verbose)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\treturn weasy_print('ErpProject/{1}/reporting/print_{0}.html', 'print_{0}.pdf', context, request)\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(), nomModule)
    print("genTemplateOfContentType #11")
    # GET UPLOAD
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef get_upload_{0}(request):\n\ttry:\n\t\tsame_perm_with = '{3}'\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)\n\t\tif response != None: return response\n\n\t\tmodel_content_type = dao_query_builder.toGetContentTypeByName('{2}')\n\t\tchamps = dao_query_builder.toListFieldOfModel(model_content_type.id)\n\n\t\tcontext = {{\n\t\t\t'title' : \"Import de la liste des {1}\",\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'champs': champs,\n\t\t\t'user_actions': actions,\n\t\t\t'isPopup': True if 'isPopup' in request.GET else False,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation' : dao_organisation.toGetMainOrganisation(),".format(nom_modele.lower() ,nom_modele_verbose_plural.lower(), content_type.model, url_name_create)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{1}/{0}/upload.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomModule)
    print("genTemplateOfContentType #12")
    # POST UPLOAD
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n@transaction.atomic\ndef post_upload_{0}(request):\n\tsid = transaction.savepoint()\n\ttry:\n\t\tmedia_dir = settings.MEDIA_ROOT + '/excel/'\n\t\tfile_name = ''\n\t\trandomId = randint(111, 999)\n\t\tif 'file_upload' in request.FILES:\n\t\t\tfile = request.FILES['file_upload']\n\t\t\tsave_path = os.path.join(media_dir, str(randomId) + '.xlsx')\n\t\t\tif default_storage.exists(save_path):\n\t\t\t\tdefault_storage.delete(save_path)\n\t\t\tfile_name = default_storage.save(save_path, file)\n\t\telse: file_name = ''\n\t\tsheet = str(request.POST['sheet'])\n\n\t\tdf = pd.read_excel(io=save_path, sheet_name=sheet, engine='openpyxl')\n\t\tdf = df.fillna('') #Replace all nan value\n\n\t\tauteur = identite.utilisateur(request)".format(nom_modele.lower())

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n"
    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        texte_check_nullable = ""          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\tif header_{0}_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))
            else : texte_check_nullable = "\n\t\tif header_{0} in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))

        # Attribution des champs
        if type_data not in ("ImageField", "FileField", "ManyToManyField"):
            if type_data in ("ForeignKey", "OneToOneField"): 
                texte_boucle = texte_boucle + "\n\n\t\theader_{0}_id = makeString(request.POST['{0}_id'])".format(nom_champ) + texte_check_nullable
                texte_boucle = texte_boucle + "\n\t\t#print(f'header_{0}_id: {{header_{0}_id}}')".format(nom_champ)
            else:
                texte_boucle = texte_boucle + "\n\n\t\theader_{0} = makeString(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
                texte_boucle = texte_boucle + "\n\t\t#print(f'header_{0}_id: {{header_{0}_id}}')".format(nom_champ)

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tfor i in df.index:".format(nom_modele.lower())
    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        texte_check_nullable = ""          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\t\tif {0}_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))
            else : texte_check_nullable = "\n\t\t\tif {0} in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))

        # Attribution des champs
        if type_data not in ("ImageField", "FileField", "ManyToManyField"):
            if type_data in ("ForeignKey", "OneToOneField"): 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0}_id = None\n\t\t\tif header_{0}_id != '': {0}_id = makeIntId(str(df[header_{0}_id][i]))".format(nom_champ) + texte_check_nullable
            elif type_data == "DateTimeField": 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = None\n\t\t\tif header_{0} != '': {0} = df[header_{0}][i]{1}".format(nom_champ, texte_check_nullable)
            elif type_data == "DateField": 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = None\n\t\t\tif header_{0} != '': {0} = df[header_{0}][i]{1}".format(nom_champ, texte_check_nullable)
            elif type_data == "FloatField": 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = 0\n\t\t\tif header_{0} != '': {0} = makeFloat(df[header_{0}][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "BooleanField": 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = False\n\t\t\tif header_{0} != '': {0} = True if makeString(df[header_{0}][i]) == 'True' else False".format(nom_champ)
            elif type_data == "EmailField": 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = ''\n\t\t\tif header_{0} != '': {0} = makeString(df[header_{0}][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "CharField": 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = ''\n\t\t\tif header_{0} != '': {0} = makeString(df[header_{0}][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "TextField": 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = ''\n\t\t\tif header_{0} != '': {0} = makeString(df[header_{0}][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "IntegerField": 
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = 0\n\t\t\tif header_{0} != '': {0} = makeInt(df[header_{0}][i])".format(nom_champ)  + texte_check_nullable
            else:
                texte_boucle = texte_boucle + "\n\n\t\t\t{0} = ''\n\t\t\tif header_{0} != '': {0} = makeString(df[header_{0}][i])".format(nom_champ)  + texte_check_nullable

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t\t{0} = {1}.toCreate(".format(nom_modele.lower(),nomdao)
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        check_nullable = True          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False
        
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if type_data not in ("ImageField", "FileField", "ManyToManyField"): 
            text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)   
            #if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
            #else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + text_parenthese
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\tsaved, {0}, message = {1}.toSave(auteur, {0})\n\n\t\t\tif saved == False: raise Exception(message)\n\n\t\ttransaction.savepoint_commit(sid)\n\t\tmessages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')".format(nom_modele.lower(),nomdao)
    texte_a_ajouter_views_py= texte_a_ajouter_views_py + "\n\t\treturn HttpResponseRedirect(reverse('{1}_list_{0}'))\n\texcept Exception as e:\n\t\ttransaction.savepoint_rollback(sid)\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nom_pattern,nom_modele.upper())

    fichier.write(texte_a_ajouter_views_py)
    fichier.close()
    
    # SCRIPT IMPORT DATA
    path = os.path.abspath(os.path.curdir)
    path = path + "\\scripts"
    try:
        os.mkdir(utils.format_path(path))
    except Exception as e:
        pass
    path = path + "\\import_{0}.py".format(nom_modele.lower())
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')
    
    texte_a_ajouter_script_import_py = "" 
    texte_a_ajouter_script_import_py = texte_a_ajouter_script_import_py + "from django.conf import settings\nfrom django.core.files.storage import FileSystemStorage\nfrom django.core.files.base import ContentFile\nfrom django.core.files.storage import default_storage\nimport os\nfrom datetime import time, timedelta, datetime, date\nfrom django.utils import timezone\nimport json, random\nfrom django.db import transaction\nimport pandas as pd\nfrom ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId, makeString\nfrom ErpBackOffice.models import Model_Personne"
    texte_a_ajouter_script_import_py = texte_a_ajouter_script_import_py + "\n\nfrom {2}.models import Model_Compte\nfrom {2}.dao.{1} import {1}\n\n\ndef run():\n\tprint('--- Execution script importation des {0}s ---')\n\timport_{0}('liste_{0}s')".format(nom_modele.lower(), nomdao, nomModule)
    texte_a_ajouter_script_import_py = texte_a_ajouter_script_import_py + "\n\n@transaction.atomic\ndef import_{0}(file_name):\n\tprint('import_{0}() ...')\n\tsid = transaction.savepoint()\n\ttry:\n\t\timport_dir = settings.MEDIA_ROOT\n\t\timport_dir = import_dir + '/excel/'\n\t\tfile_path = os.path.join(import_dir, str(file_name) + '.xlsx')\n\t\tif default_storage.exists(file_path):\n\t\t\tfilename = default_storage.generate_filename(file_path)\n\t\t\tsheet = 'Sheet1'\n\t\t\tprint('Sheet : {{}} file: {{}}'.format(sheet, filename))\n\t\t\tdf = pd.read_excel(io=filename, sheet_name=sheet, engine='openpyxl')\n\t\t\tdf = df.fillna('') #Replace all nan value\n\n\t\t\tauteur = Model_Personne.objects.get(pk = 7)\n\n\t\t\tfor i in df.index:".format(nom_modele.lower())
    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        texte_check_nullable = ""          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\t\t\tif {0}_id in (None, '') : raise Exception('Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))
            else : texte_check_nullable = "\n\t\t\t\tif {0} in (None, '') : raise Exception('Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))

        # Attribution des champs
        if type_data not in ("ImageField", "FileField", "ManyToManyField"):
            if type_data in ("ForeignKey", "OneToOneField"): 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0}_id = makeIntId(str(df['{0}_id'][i]))".format(nom_champ) + texte_check_nullable
            elif type_data == "DateTimeField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = makeString(df['{0}'][i]){1}\n\t\t\t{0} = timezone.datetime(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]), int({0}[11:13]), int({0}[14:16]))".format(nom_champ, texte_check_nullable)
            elif type_data == "DateField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = makeString(df['{0}'][i]){1}\n\t\t\t{0} = date(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]))".format(nom_champ, texte_check_nullable)
            elif type_data == "FloatField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = makeFloat(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "BooleanField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = True if str(df['{0}'][i]) == 'True' else False".format(nom_champ)
            elif type_data == "EmailField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = makeString(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "CharField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = makeString(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "TextField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = makeString(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "IntegerField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = makeInt(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            else:
                texte_boucle = texte_boucle + "\n\t\t\t\t{0} = makeString(df['{0}'][i])".format(nom_champ)  + texte_check_nullable

    texte_a_ajouter_script_import_py = texte_a_ajouter_script_import_py + texte_boucle
    
    texte_a_ajouter_script_import_py = texte_a_ajouter_script_import_py + "\n\n\t\t\t\t{0} = {1}.toCreate(".format(nom_modele.lower(),nomdao)
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        check_nullable = True          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False
        
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if type_data not in ("ImageField", "FileField", "ManyToManyField"): 
            text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)   
            #if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
            #else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_script_import_py = texte_a_ajouter_script_import_py + text_parenthese
    texte_a_ajouter_script_import_py = texte_a_ajouter_script_import_py + "\n\t\t\t\tsaved, {0}, message = {1}.toSave(auteur, {0})\n\n\t\t\t\tif saved == False: raise Exception(message)\n\n\t\t\t\tprint('{2} ID {{}} cree '.format({0}.id))".format(nom_modele.lower(),nomdao,nom_modele.upper())
    texte_a_ajouter_script_import_py= texte_a_ajouter_script_import_py + "\n\t\t\ttransaction.savepoint_commit(sid)\n\t\telse: print('Fichier Excel non trouvé')\n\texcept Exception as e:\n\t\tprint('ERREUR IMPORT {1}')\n\t\tprint(e)\n\t\ttransaction.savepoint_rollback(sid)".format(nom_modele.lower(),nom_modele.upper())

    fichier.write(texte_a_ajouter_script_import_py)
    fichier.close()
    
    print("genTemplateOfContentType #13")
    
    # CREATION DES TEMPLATES CRUD ET UPLOAD DU MODELE
    
    # TEMPLATE LIST
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    try:
        os.mkdir(utils.format_path(path))
    except Exception as e:
        pass
    path = path + "\\list.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')

    texteTemplate = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
{{% if not isPopup %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="leaf chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>
{{% endif %}}

<div class="row"  style="padding-top: 10px;">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>        
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>
        <div class="panel panel-default" style="border: none;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">  
                {{% if not isPopup %}}         
                <div class="row">
                    {{% if user_actions.can_create is True %}} 
                    <div class="col-md-3 col-xs-12">
                        <button onclick="javascript:window.location.assign('{{% url '{2}_add_{3}' %}}')" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}" style="width: 100%;">
                            Créer 
                        </button>
                    </div>
                    {{% endif %}}
                    <div class="col-md-3 col-xs-12">
                        <div id="btn-view" data-role="group" data-group-type="one-state">
                            <button id="btn-tree" class="button btn-typeview btn-secondary {{% if view == "list" %}}{{{{ "active" }}}}{{% endif %}}"><span class="mif-list"></span></button>
                            <button id="btn-kanban" class="button btn-typeview btn-secondary {{% if view == "kanban" %}}{{{{ "active" }}}}{{% endif %}}"><span class="mif-apps"></span></button>
                        </div>
                    </div>
                </div><br> 
                            
                <hr class="hr-ligne">
                {{% endif %}}
                <!-- Appel de la fonction message -->           
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>

                <div id="datalist" class="row" style="">
                    <!-- Vue de type list -->
                    <div id="list-view" class="row" style="margin-top: 10px;overflow: auto; position: relative; display: inline-block;">        
                        <table id="data_table" class="display nowrap border bordered striped" cellspacing="0" style="width:100%">
                            <thead>
                                <tr>
                                    <th style="width: 20px; background-color:#2e416a; white"></th>'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize())
    textebcl=""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            textebcl = textebcl + '''
                                    <th>{0}</th>'''.format(nom_champ_verbose)
    textebcl = textebcl + '''
                                    <th>Date de création</th>
                                    <th>Créé par</th>'''
    texteTemplate = texteTemplate + textebcl

    texteTemplate= texteTemplate + '''
                                </tr>
                            </thead>
                            <tbody id="tbody">
                                {{% for item in model %}}
                                <tr>
                                    <td>
                                        <label class="small-check">
                                            <input type="checkbox"><span class="check"></span>
                                        </label>
                                    </td>
                                    <td>
                                        <a class="lien chargement-au-click" href="{{% url '{0}_select_{1}' item.id %}}{{% if isPopup %}}?isPopup=1{{% endif %}}">{{{{ item.{2} }}}}</a>
                                    </td>'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)

    textebcl = ""
    for i in range(1,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            if type_data == "FloatField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                                    <td>{{{{item.{0}|monetary}}}}</td>'''.format(nom_champ)
            elif type_data == "CharField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                                    <td>{{{{item.{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
            elif type_data == "IntegerField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                                    <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)
            elif type_data == "BooleanField":
                textebcl = textebcl + '''
                                    <td>{{{{item.{0}|boolean}}}}</td>'''.format(nom_champ)
            elif type_data == "DateTimeField":
                textebcl = textebcl + '''
                                    <td>{{{{item.{0}|date:"d/m/Y H:i"}}}}</td>'''.format(nom_champ)
            elif type_data == "DateField":
                textebcl = textebcl + '''
                                    <td>{{{{item.{0}|date:"d/m/Y"}}}}</td>'''.format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
                if type_data == "CharField":
                    textebcl = textebcl + '''
                                    <td>{{{{item.value_{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
                elif type_data == "IntegerField":
                    textebcl = textebcl + '''
                                    <td>{{{{item.value_{0}}}}}</td>'''.format(nom_champ)
                elif type_data == "FloatField":
                    textebcl = textebcl + '''
                                    <td>{{{{item.value_{0}|monetary}}}}</td>'''.format(nom_champ)
            else :
                textebcl = textebcl + '''
                                    <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)

    texteTemplate = texteTemplate + textebcl

    texteTemplate = texteTemplate + '''
                                    <td>{{{{item.creation_date|date:'d/m/Y'}}}}</td>
                                    <td>{{{{item.auteur.nom_complet}}}}</td>
                                </tr>
                                {{% endfor %}}
                            </tbody>
                        </table>
                    </div>

                    <!-- Vue de type card -->
                    <div id="kanban-view" class="row" style="margin-top: 10px; display: none;">
                        <div id="card-list" class="row" style="">
                            {{% for item in model %}}
                            <div class="col-md-4">
                                <div class="card-item" style="margin-top: 10px; margin-bottom: 15px">
                                    <div class="card-item-content">
                                        <div class="thumb">
                                        </div>
                                        <div class="texts">
                                            <a class="link chargement-au-click" href="{{% url '{0}_select_{1}' item.id %}}{{% if isPopup %}}?isPopup=1{{% endif %}}">{{{{ item.{2} }}}}</a><br>
                                            <div class="mt-2"></div>
                                            <span class="inner-text">Créé par : {{{{ item.auteur.nom_complet }}}}</span><br>
                                            <span class="inner-text">Créé le : {{{{ item.creation_date|date:'d/m/Y' }}}}</span><br>
                                            <a href="{{% url '{0}_select_{1}' item.id %}}{{% if isPopup %}}?isPopup=1{{% endif %}}" class="mt-3 btn btn-block btn-wide rounded chargement-au-click">voir detail</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            {{% endfor %}}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
<script>
    url_item = "{{% url '{0}_select_{1}' '100' %}}";
    url_list = "{{% url '{0}_list_{1}' %}}";

    function formatTableRow(url, item) {{
        td = 
        `<td>
            <label class="small-check">
                <input type="checkbox"><span class="check"></span>
            </label>
        </td>
        <td>
            <a class="lien chargement-au-click" href="${{url}}">${{ item.{2} }}</a>
        </td>'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)
        
    textebcl = ""
    for i in range(1,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            if type_data == "FloatField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
        <td>${{formatFloat(item.{0})}}</td>'''.format(nom_champ)
            elif type_data == "CharField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
        <td>${{formatChar(item.{0})}}</td>'''.format(nom_champ)
            elif type_data == "IntegerField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
        <td>${{formatInt(item.{0})}}</td>'''.format(nom_champ)
            elif type_data == "BooleanField":
                textebcl = textebcl + '''
        <td>${{formatBool(item.{0})}}</td>'''.format(nom_champ)
            elif type_data == "DateTimeField":
                textebcl = textebcl + '''
        <td>${{formatDateTime(item.{0})}}</td>'''.format(nom_champ)
            elif type_data == "DateField":
                textebcl = textebcl + '''
        <td>${{formatDate(item.{0})}}</td>'''.format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
                if type_data == "CharField":
                    textebcl = textebcl + '''
        <td>${{formatChar( item.{0})}}</td>'''.format(nom_champ)
                elif type_data == "IntegerField":
                    textebcl = textebcl + '''
        <td>${{formatInt( item.{0})}}</td>'''.format(nom_champ)
                elif type_data == "FloatField":
                    textebcl = textebcl + '''
        <td>${{formatFloat( item.{0})}}</td>'''.format(nom_champ)
            else :
                textebcl = textebcl + '''
        <td>${{formatChar(item.{0})}}</td>'''.format(nom_champ)

    texteTemplate = texteTemplate + textebcl

    texteTemplate = texteTemplate + '''        
        <td>${{formatDateTime(item.creation_date)}}</td>
        <td>${{formatChar(item.auteur)}}</td>
        
        `;
        return td;
    }}

    function formatKanbanRow(url, item) {{
        card = 
        `
        <div class="col-md-4">
            <div class="card-item" style="margin-top: 10px; margin-bottom: 15px">
                <div class="card-item-content">
                    <div class="thumb">
                    </div>
                    <div class="texts">
                        <a class="link chargement-au-click" href="${{url}}">${{ formatChar(item.{2})}}</a><br>
                        <div class="mt-2"></div>
                        <span class="inner-text">Créé par : ${{formatChar(item.auteur)}}</span><br>
                        <span class="inner-text">Créé le : ${{formatDateTime(item.creation_date)}}</span><br>
                        <a href="${{url}}" class="mt-3 btn btn-block btn-wide rounded chargement-au-click">voir detail</a>
                    </div>
                </div>
            </div>
        </div>
        `;
        return card;
    }}
</script>
{{% include 'ErpProject/ErpBackOffice/widget/list_view.html' %}}
{{% endblock %}}
'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)
    fichier.write(texteTemplate)
    fichier.close()
    print("genTemplateOfContentType #14")
    # TEMPLATE ADD
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule, nom_modele.lower())
    path = path + "\\add.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')
    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
{{% if not isPopup %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_list_{3}' %}}">Liste des {5}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>
{{% endif %}}

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>
        
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <button onclick="javascript:document.getElementById('submit').click()" class="validate-btn theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
                    {{% if not isPopup %}}
                    <button onclick="javascript:window.location.assign('{{% url '{2}_get_upload_{3}' %}}')" class="theme-btn theme-btn-sm rounded chargement-au-click">Importer les données à partir excel</button>
                    <button onclick="javascript:window.location.assign('{{% url '{2}_list_{3}' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                    {{% endif %}}
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>
                
                <form id="form" method="POST" action="{{% url '{2}_post_add_{3}' %}}"  enctype="multipart/form-data" data-role="validator" data-show-required-state="false" data-hint-mode="line" data-hint-background="bg-red" data-hint-color="fg-white" data-hide-error="5000"
                    novalidate="novalidate" data-on-error-input="notifyOnErrorInput" data-show-error-hint="false">
                    {{% csrf_token %}}
                    <input id="submit" type="submit" style="display: none">
                    {{% if isPopup %}}<input id="isPopup" name="isPopup" value="1" type="text" style="display: none">{{% endif %}}
                    <div class="row">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural)

    print("111111111111111111111111111") 
    textebcl = ""
    print(f"{len(list_champs)} -------- ")
    for i in range(0,len(list_champs)):
        print("Debut")
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        is_required = False         
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": is_required = True
        print("Debut 4")
        if type_data == "FloatField" and list_champs[i].choices == None:
            print("FloatField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input name="{0}" id="{0}" type="number" step="0.01" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "CharField" and list_champs[i].choices == None:
            print("CharField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"

            if list_champs[i].max_length != None and list_champs[i].max_length >= 500:
                textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <textarea name="{0}" id="{0}" '''.format(nom_champ)   
                if is_required == True :                                 
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + "></textarea>"  
            else:
                textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input name="{0}" id="{0}" type="text" '''.format(nom_champ)
                if is_required == True :                                 
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "EmailField":
            print("EmailField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control email full-size" data-role="input">
                                <input name="{0}" id="{0}" type="email" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, email" data-validate-hint="Saisissez une adresse email valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "TextField":
            print("TextField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <textarea name="{0}" id="{0}" '''.format(nom_champ)   
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + "></textarea>"   
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "IntegerField" and list_champs[i].choices == None:
            print("IntegerField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input name="{0}" id="{0}" type="number" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "ImageField":
            print("ImageField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                            <div class="tile-container">  
                                <input class="image_upload" name="{1}" id="{1}" type="file" accept="image/*" style="display:none;">                              
                                <a id="trigger-input-file" href="#" class="trigger-input-file tile-wide fg-white shadow" style="height: 100px!important; width: 100px!important;" data-role="tile"> 
                                    <div class="tile-content slide-up">
                                        <div class="slide">
                                            <img class="image_preview" src="{{% static 'ErpProject/image/upload/articles/default.png' %}}" style="height: 100px; width: 100px;">
                                        </div>
                                        <div class="slide-over op-dark padding10" style="text-align: center!important; opacity: 60%!important;">
                                            <span class="icon mif-pencil" style="text-align: center!important; font-size: 40px!important;"></span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "FileField":
            print("FileField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                            <div class="input-control file full-size" data-role="input">
                                <input name="{1}" id="{1}" type="file"><button class="button"><span class="mif-folder"></span></button>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "ForeignKey":
            print("ForeignKey")
            related_model = list_champs[i].related_model.__name__ 
            related_model_url_vers = getUrlVersOfRelatedModel(related_model)               
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select name="{0}_id" id="{0}_id" class="selectpicker form-control" title="Sélectionner une option">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    <option class="search_option" value='-200' data-url="/{1}/{2}/list?isPopup=1">Voir plus ...</option>
                                    {{% for item in {2}s %}}<option value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model_url_vers, related_model.replace("Model_", "").lower())
        elif type_data == "OneToOneField":
            print("OneToMany")
            related_model = list_champs[i].related_model.__name__
            related_model_url_vers = getUrlVersOfRelatedModel(related_model) 
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select name="{0}_id" id="{0}_id" class="selectpicker form-control" title="Sélectionner une option">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau ...</option>
                                    <option class="search_option" value='-200' data-url="/{1}/{2}/list?isPopup=1">Voir plus ...</option>
                                    {{% for item in {2}s %}}<option value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model_url_vers, related_model.replace("Model_", "").lower())
        elif type_data == "ManyToManyField":
            print("ManyToMany") 
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="text full-size">
                                <select multiple="multiple" class="multi-select multi_select2" name="{0}" id="{0}">
                                    {{% for item in {1}s %}}<option value="{{{{ item.id }}}}">{{{{item}}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model.replace("Model_", "").lower())
        elif type_data == "BooleanField":
            print("BooleanField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label class="input-control checkbox small-check full-size">
                                <input name="{1}" id="{1}" type="checkbox">
                                <span class="check"></span><span class="caption">{0}</span>'''.format(nom_champ_verbose, nom_champ)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            </label>
                        </div>'''
        elif type_data == "DateTimeField":
            print("DateTimeField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size datetimepicker">
                                <input type="text" name="{1}" id="{1}" placeholder="jj/mm/aaaa hh:mm">
                                <div class="button"><span class="glyphicon glyphicon-screenshot far fa-calendar" style="margin-right:3px;"></span><span class="glyphicon glyphicon-screenshot far fa-clock"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "DateField":
            print("DateField")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                                <input type="text" name="{1}" id="{1}" placeholder="jj/mm/aaaa">
                                <div class="button"><span class="mif-calendar"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
            print("Choice")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select name="{0}" id="{0}" class="selectpicker form-control" title="Sélectionner une option">
                                    <option value="">Sélectionnez une option</option>
                                    {{% for item in model.list_{0} %}}<option value="{{{{ item.id }}}}">{{{{ item.designation }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ)
        else :
            print("Else")
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input name="{0}" id="{0}" type="text" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
            
    texteTemplateLayout = texteTemplateLayout + textebcl
    texteTemplateLayout = texteTemplateLayout + '''
                    </div>'''               
    if len(relateds) > 0: 
        texteTemplateLayout = texteTemplateLayout + '''     
                    <br><br>
                    <div class="row">
                        <ul class="nav nav-tabs navtab-bg"> 
                            <li class="active"><a href="#frame_autres" data-toggle="tab" aria-expanded="false"><span>Autres informations</span></a></li>
                        </ul>
                        <div class="tab-content"> 
                            <div class="tab-pane active" id="frame_autres">
                                <div class="row margin20 no-margin-left no-margin-right">'''

        for i in range(0, len(relateds)):
            if relateds[i] != "":
                list_relateds = relateds[i].split(",")
                content_id = list_relateds[0]
                field_name = list_relateds[1]
                field_type = list_relateds[2]
                model_related = ContentType.objects.get(pk = content_id)
                model_class_related = model_related.model_class()
                nom_model_class_related = model_related.model_class().__name__
                related_model_url_vers = getUrlVersOfRelatedModel(nom_model_class_related)
                nom_model_related = nom_model_class_related.replace("Model_", "").lower()
                input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
                related_query_name = ""
                if field_type == "ForeignKey":
                    related_query_name = model_class_related._meta.get_field(field_name).related_query_name() 
                    if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name)
                elif field_type == "ManyToManyRel":
                    if field_name.startswith("model_") : related_query_name = "{}_set".format(field_name)
                    else: related_query_name = field_name
                print("related_query_name: {}".format(related_query_name))    
                
                texteTemplateLayout = texteTemplateLayout + '''                                
                                <div class="col-md-6">
                                    <div class="section-otm" data-compteur="1">
                                        <table class="table bordered no-margin" style="width:100%;">
                                            <thead>	
                                                <tr>
                                                    <th width="90%">{0}</th>
                                                    <th width="10%"></th>
                                                </tr>
                                            </thead>                
                                            <tbody class="tbl_posts_body">
                                                <tr>
                                                    <td>
                                                        <div class="input-control text full-size">                                
                                                            <select class="selectpicker form-control" title="sélectionner une option" name="{3}" id="{3}-1">
                                                                <option value="">Sélectionnez une nouvelle option {0}</option>
                                                                <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                            </select>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div class="pagination no-border">
                                                            <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                        </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table> 
                                        <br><button type="button" class="button rounded add-record">Ajouter</button>
                                        <table class="sample_table" style="display:none;">       
                                            <tr>
                                                <td>
                                                    <div class="input-control text full-size">                                
                                                        <select class="form-control" title="Sélectionner une option" name="{3}" id="">
                                                            <option value="">Sélectionnez une nouvelle option {0}</option>
                                                            <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                        </select>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="pagination no-border">
                                                        <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>
                                </div>'''.format(model_class_related._meta.verbose_name, related_model_url_vers, nom_model_related, input_name_related)  
        texteTemplateLayout = texteTemplateLayout + '''                                                                
                            </div>
                        </div>
                    </div>'''                    
    print("44444444444444444444444444")                 
    texteTemplateLayout = texteTemplateLayout + '''
                </form>
            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
<script>
    url_item = "{{% url '{0}_select_{1}' '100' %}}";    
</script>
{{% include 'ErpProject/ErpBackOffice/widget/create_view.html' %}}
{{% endblock %}}'''.format(nom_pattern, nom_modele.lower())
    fichier.write(texteTemplateLayout)
    fichier.close()
    print("genTemplateOfContentType #15")

    # TEMPLATE ITEM
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    path = path + "\\item.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')
    
    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
<style type="text/css">
    .kanban_image {{
        width: 70px;
        height: 70px;
        display: inline-block;
        position: relative;
        text-align: center;
        background-size: contain;
    }}
    .kanban_image[data-mimetype='application/pdf'] {{
        background-image: url({{% static 'ErpProject/image/mimetypes/pdf.svg' %}});
    }}
</style>
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_list_{3}' %}}">Liste des {5}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>
        
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>
        
        <!-- GESTION DU WORKFLOW -->
        {{% include 'ErpProject/ErpBackOffice/widget/workflow.html' with utilisateur=utilisateur model=model content_type_id=content_type_id historique=historique roles=roles etapes_suivantes=etapes_suivantes url_add="{2}_add_{3}" url_detail="{2}_detail_{3}" csrf_token=csrf_token module=module type_doc="{6}" only %}}
        <!--FIN GESTION DU WORKFLOW--> 

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    {{% if user_actions.can_update is True %}}<button onclick="javascript:window.location.assign('{{% url '{2}_update_{3}' model.id %}}')" class="validate-btn theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Modifier</button>{{% endif %}}
                    {{% if user_actions.can_create is True %}}<button onclick="javascript:window.location.assign('{{% url '{2}_duplicate_{3}' model.id %}}')" class="validate-btn theme-btn theme-btn-sm rounded chargement-au-click">Dupliquer</button>{{% endif %}}
                    <button onclick="javascript:window.location.assign('{{% url '{2}_print_{3}' model.id %}}')" class="validate-btn theme-btn theme-btn-sm rounded success chargement-au-click">Imprimer</button>
                    {{% if user_actions.can_delete is True %}}<button id="supprimer" class="validate-btn theme-btn theme-btn-sm rounded danger chargement-au-click">Supprimer</button>{{% endif %}}
                    <button onclick="javascript:window.location.assign('{{% url '{2}_list_{3}' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>
                
                <div class="row">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural, nom_modele_verbose)

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        
        if type_data == "FloatField" and list_champs[i].choices == None:
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{model.{0}|monetary}}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "BooleanField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <label class="input-control checkbox small-check full-size">
                            <input name="{0}" id="{0}"  {{% if model.{0} is True %}}{{{{ "checked" }}}}{{% endif %}} type="checkbox" disabled="disabled">
                            <span class="check"></span>
                            <span class="caption">{1}</span>
                        </label>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data in ("ForeignKey", "OneToOneField"):
            related_model = list_champs[i].related_model.__name__
            related_nom_pattern = getUrlOfRelatedModel(related_model)
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            {{% if model.{0} is None %}}
                            <span class="sub-alt-header"> - </span>
                            {{% else %}}
                            <span class="sub-alt-header"><a class="link chargement-au-click" href="{{% url '{2}_detail_{3}' model.{0}_id %}}">{{{{ model.{0} }}}}</a></span>
                            {{% endif %}}
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose, related_nom_pattern, related_model.replace("Model_", "").lower())
        elif type_data == "ImageField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            {{% if model.{0} %}}
                            <a data-magnify="gallery" href="{{% static model.{0}.url %}}">
                                <img class="" src="{{% static model.{0}.url %}}" style="height: 100px; width: 100px;">
                            </a>                           
                            {{% else %}}
                            <img src="{{% static 'ErpProject/image/upload/articles/default.png' %}}" style="height: 100px; width: 100px;">
                            {{% endif %}}
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "FileField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            {{% if model.{0} %}}
                            <a href="{{% static model.{0}.url %}}"><img src="{{% static 'ErpProject/image/document.png' %}}" style="height: 70px; width: 70px;"></a>
                            <br><span style=" color: #000; font-size: 9px;">{{{{model.{0}.name|truncatechars:25}}}}</span>                          
                            {{% else %}}<span class="sub-alt-header">Aucun document attaché</span>{{% endif %}}
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "ManyToManyField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p class="fg-gray">
                            <label>{1} :</label><br>
                            {{% for item in model.{0}.all %}}
                                <span class="sub-alt-header badge badge-light"> {{{{ item }}}} </span><br>
                            {{% endfor %}}                     
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "DateTimeField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{model.{0}|date:"d/m/Y H:i"}}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "DateField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{model.{0}|date:"d/m/Y"}}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{ model.value_{0} }}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        else :
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{ model.{0} }}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
            
    texteTemplateLayout = texteTemplateLayout + textebcl 
    texteTemplateLayout = texteTemplateLayout + '''
                </div>'''

                    
    if len(relateds) > 0: 
        texteTemplateLayout = texteTemplateLayout + '''     
                <br><br>
                <div class="row">
                    <ul class="nav nav-tabs navtab-bg"> 
                        <li class="active"><a href="#frame_autres" data-toggle="tab" aria-expanded="false"><span>Autres informations</span></a></li>
                        <li class=""><a href="#frame_documents" data-toggle="tab" aria-expanded="false"><span>Documents associés</span></a></li>
                    </ul>
                    <div class="tab-content"> 
                        <div class="tab-pane active" id="frame_autres">
                            <div class="row margin20 no-margin-left no-margin-right">'''
        for i in range(0, len(relateds)):
            if relateds[i] != "":
                list_relateds = relateds[i].split(",")
                content_id = list_relateds[0]
                field_name = list_relateds[1]
                field_type = list_relateds[2]
                model_related = ContentType.objects.get(pk = content_id)
                model_class_related = model_related.model_class()
                nom_model_class_related = model_related.model_class().__name__
                nom_model_related = nom_model_class_related.replace("Model_", "").lower()
                input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
                related_query_name = ""
                if field_type == "ForeignKey":
                    related_query_name = model_class_related._meta.get_field(field_name).related_query_name() 
                    if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name)
                elif field_type == "ManyToManyRel":
                    if field_name.startswith("model_") : related_query_name = "{}_set".format(field_name)
                    else: related_query_name = field_name
                print("related_query_name: {}".format(related_query_name)) 
                
                texteTemplateLayout = texteTemplateLayout + '''                                
                                <div class="col-md-6">
                                    <table class="table bordered no-margin" style="width:100%;">
                                        <thead><tr><th>{0}</th></tr></thead>                
                                        <tbody class="tbl_posts_body">
                                            {{% for item in model.{1}.all %}}
                                                <tr><td><span class="sub-alt-header">{{{{ item }}}}</span></td></tr>
                                            {{% endfor %}}  
                                        </tbody>
                                    </table>
                                </div>'''.format(model_class_related._meta.verbose_name_plural, related_query_name) 
                
    texteTemplateLayout = texteTemplateLayout + '''
                            </div>
                        </div>
                        <div class="tab-pane" id="frame_documents">
                            <div class="row margin20 no-margin-left no-margin-right">
                                {{% for item in documents %}}
                                <div class="col-md-4">
                                    <div class="card-item" style="margin-top: 10px; margin-bottom: 15px">
                                        <div class="card-item-content" style="margin: 10px">
                                            <div class="thumb kanban_image" data-mimetype="application/pdf">
                                            </div>
                                            <div class="texts">
                                                <div class="texts-record_selector">
                                                    <a class="link chargement-au-click" href="{{% if item.fichier %}}{{% static item.fichier.url %}}{{% else %}}{{% url 'module_archivage_detail_document' item.id %}}{{% endif %}}" style="float: left;">{{{{ item.designation }}}}</a>
                                                </div>
                                                <br>
                                                <div class="mt-2"></div>
                                                <span class="inner-text">{{{{ item.dossier.designation }}}}</span><br>
                                                <div class="texts-favorite">
                                                    <span class="inner-text" style="float: left;">{{{{ item.creation_date|date:'d/m/Y' }}}}</span>
                                                </div>
                                                <br>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                {{% endfor %}}                    
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<script>
    //-------  Deux variables pour la suppression  ---------------
    var modele = "{0}"
    var the_url = "{1}"
</script>
{{% include 'ErpProject/ErpBackOffice/widget/item_view.html' %}}
{{% endblock %}}'''.format(nom_modele_class, url_name_list)
    fichier.write(texteTemplateLayout)
    fichier.close()

    print("genTemplateOfContentType #16")
    #TEMPLATE UPDATE
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    path = path + "\\update.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')

    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_list_{3}' %}}">Liste des {5}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_detail_{3}' model.id %}}">{{{{ model }}}}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>
        
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <button onclick="javascript:document.getElementById('submit').click()" class="validate-btn theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
                    <button onclick="javascript:window.location.assign('{{% url '{2}_detail_{3}' model.id %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>
                
                <form id="form" method="POST" action="{{% url '{2}_post_update_{3}' %}}"  enctype="multipart/form-data" data-role="validator" data-show-required-state="false" data-hint-mode="line" data-hint-background="bg-red" data-hint-color="fg-white" data-hide-error="5000"
                    novalidate="novalidate" data-on-error-input="notifyOnErrorInput" data-show-error-hint="false">
                    {{% csrf_token %}}
                    <input id="submit" type="submit" style="display: none">
                    <input type="text"  id="ref" name="ref" value ="{{{{ model.id }}}}" style="display: none">
                    {{% if isPopup %}}<input id="isPopup" name="isPopup" value="1" type="text" style="display: none">{{% endif %}}
                    <div class="row">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural)

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        is_required = False         
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": is_required = True
        
        if type_data == "FloatField" and list_champs[i].choices == None:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input value="{{{{ model.{0}|input_float }}}}" name="{0}" id="{0}" type="number" step="0.01" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "CharField" and list_champs[i].choices == None:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            if list_champs[i].max_length != None and list_champs[i].max_length >= 500 :
                textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <textarea name="{0}" id="{0}" '''.format(nom_champ)   
                if is_required == True :                                 
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + ">{{{{ model.{0} }}}}</textarea>".format(nom_champ)  
            else:
                textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="text" '''.format(nom_champ)
                if is_required == True :                                 
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "EmailField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control email full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="email" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, email" data-validate-hint="Saisissez une adresse email valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "TextField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <textarea name="{0}" id="{0}" '''.format(nom_champ)   
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">{{{{ model.{0} }}}}</textarea>".format(nom_champ)  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "IntegerField" and list_champs[i].choices == None:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="number" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "ImageField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                            <div class="tile-container">  
                                <input class="image_upload" name="{1}" id="{1}" type="file" accept="image/*" style="display:none;">                              
                                <a id="trigger-input-file" href="#" class="trigger-input-file tile-wide fg-white shadow" style="height: 100px!important; width: 100px!important;" data-role="tile"> 
                                    <div class="tile-content slide-up">
                                        <div class="slide">
                                            {{% if model.{1} %}}<img class="image_preview" src="{{% static model.{1}.url %}}" style="height: 100px; width: 100px;"> {{% else %}}
                                            <img class="image_preview" src="{{% static 'ErpProject/image/upload/articles/default.png' %}}" style="height: 100px; width: 100px;">{{% endif %}}
                                        </div>
                                        <div class="slide-over op-dark padding10" style="text-align: center!important; opacity: 60%!important;">
                                            <span class="icon mif-pencil" style="text-align: center!important; font-size: 40px!important;"></span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "FileField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                                {{% if model.document %}}                         
                                <span style=" color: #000; font-size: 10px;">Actuellement: <a href="{{% static model.document.url %}}">{{{{model.document.name|truncatechars:45}}}}</a></span>                         
                                {{% else %}}<span style=" color: #000; font-size: 10px;">Actuellement: Aucun document attaché</span>{{% endif %}}
                            <div class="input-control file full-size" data-role="input">
                                <input name="{1}" id="{1}" type="file"><button class="button"><span class="mif-folder"></span></button>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "ForeignKey":
            related_model = list_champs[i].related_model.__name__
            related_model_url_vers = getUrlVersOfRelatedModel(related_model)
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select class="selectpicker form-control" title="Sélectionner une option" name="{0}_id" id="{0}_id">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    <option class="search_option" value='-200' data-url="/{1}/{2}/list?isPopup=1">Voir plus ...</option>
                                    {{% for item in {2}s %}}<option {{% if model.{0}_id == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model_url_vers, related_model.replace("Model_", "").lower())
        elif type_data == "OneToOneField":
            related_model = list_champs[i].related_model.__name__
            related_model_url_vers = getUrlVersOfRelatedModel(related_model)
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select class="selectpicker form-control" title="Sélectionner une option" name="{0}_id" id="{0}_id">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    <option class="search_option" value='-200' data-url="/{1}/{2}/list?isPopup=1">Voir plus ...</option>
                                    {{% for item in {2}s %}}<option {{% if model.{0}_id == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model_url_vers, related_model.replace("Model_", "").lower())
        elif type_data == "ManyToManyField":
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="text full-size">
                                <select multiple="multiple" class="multi-select multi_select2" name="{0}" id="{0}">
                                    {{% for item in {1}s %}}<option {{% for object in model.{0}.all %}} {{% if object.id == item.id %}}{{{{ "selected" }}}}{{% endif %}}{{% endfor %}} value="{{{{ item.id }}}}">{{{{item}}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model.replace("Model_", "").lower())
        elif type_data == "BooleanField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label class="input-control checkbox small-check full-size">
                                <input name="{1}" id="{1}" {{% if model.{1} == True %}} {{{{ "checked" }}}} {{% endif %}} type="checkbox">
                                <span class="check"></span><span class="caption">{0}</span>'''.format(nom_champ_verbose, nom_champ)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            </label>
                        </div>'''
        elif type_data == "DateTimeField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size datetimepicker">
                                <input type="text" name="{1}" id="{1}" placeholder="jj/mm/aaaa hh:mm" value="{{{{ model.{1}|date:"d/m/Y H:i" }}}}">
                                <div class="button"><span class="glyphicon glyphicon-screenshot far fa-calendar" style="margin-right:3px;"></span><span class="glyphicon glyphicon-screenshot far fa-clock"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "DateField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                                <input type="text" name="{1}" id="{1}" placeholder="jj/mm/aaaa" value="{{{{ model.{1}|date:"d/m/Y" }}}}">
                                <div class="button"><span class="mif-calendar"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select class="selectpicker form-control" title="sélectionner une option" name="{0}" id="{0}">
                                    <option value="">Sélectionnez une option</option>
                                    {{% for item in model.list_{0} %}}<option {{% if model.{0} == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item.designation }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ)
        else :
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="text" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
            
    texteTemplateLayout = texteTemplateLayout + textebcl
    texteTemplateLayout = texteTemplateLayout + '''
                    </div>'''
                    
    if len(relateds) > 0: 
        texteTemplateLayout = texteTemplateLayout + '''     
                    <br><br>
                    <div class="row">
                        <ul class="nav nav-tabs navtab-bg"> 
                            <li class="active"><a href="#frame_autres" data-toggle="tab" aria-expanded="false"><span>Autres informations</span></a></li>
                        </ul>
                        <div class="tab-content"> 
                            <div class="tab-pane active" id="frame_autres">
                                <div class="row margin20 no-margin-left no-margin-right">'''
        for i in range(0, len(relateds)):
            if relateds[i] != "":
                list_relateds = relateds[i].split(",")
                content_id = list_relateds[0]
                field_name = list_relateds[1]
                field_type = list_relateds[2]
                model_related = ContentType.objects.get(pk = content_id)
                model_class_related = model_related.model_class()
                nom_model_class_related = model_related.model_class().__name__
                related_model_url_vers = getUrlVersOfRelatedModel(nom_model_class_related)
                nom_model_related = nom_model_class_related.replace("Model_", "").lower()
                input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
                related_query_name = ""
                if field_type == "ForeignKey":
                    related_query_name = model_class_related._meta.get_field(field_name).related_query_name() 
                    if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name)
                elif field_type == "ManyToManyRel":
                    if field_name.startswith("model_") : related_query_name = "{}_set".format(field_name)
                    else: related_query_name = field_name
                print("related_query_name: {}".format(related_query_name))   
                
                texteTemplateLayout = texteTemplateLayout + '''                                
                                <div class="col-md-6">
                                    <div class="section-otm" data-compteur="1">
                                        <table class="table bordered no-margin" style="width:100%;">
                                            <thead>	
                                                <tr>
                                                    <th width="90%">{0}</th>
                                                    <th width="10%"></th>
                                                </tr>
                                            </thead>                
                                            <tbody class="tbl_posts_body">
                                                {{% for item in model.{4}.all %}}
                                                <tr>
                                                    <td>
                                                        <div class="input-control text full-size">                                
                                                            <select class="selectpicker form-control" title="sélectionner une option" name="{3}" id="{3}-1">
                                                                <option value="">Sélectionnez une nouvelle option {0}</option>
                                                                <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                                <option {{{{ "selected" }}}} value="{{{{ item.id }}}}"> {{{{ item }}}} </option>
                                                            </select>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div class="pagination no-border">
                                                            <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                        </div>
                                                    </td>
                                                </tr>
                                                {{% endfor %}}
                                            </tbody>
                                        </table> 
                                        <br><button type="button" class="button rounded add-record">Ajouter</button>
                                        <table class="sample_table" style="display:none;">       
                                            <tr>
                                                <td>
                                                    <div class="input-control text full-size">                                
                                                        <select class="form-control" title="Sélectionner une option" name="{3}" id="">
                                                            <option value="">Sélectionnez une nouvelle option {0}</option>
                                                            <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                        </select>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="pagination no-border">
                                                        <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>'''.format(model_class_related._meta.verbose_name, related_model_url_vers, nom_model_related, input_name_related, related_query_name)  
        texteTemplateLayout = texteTemplateLayout + '''                                
                                </div>
                            </div>
                        </div>
                    </div>'''                    
                    
    texteTemplateLayout = texteTemplateLayout + '''
                </form>
            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
<script>
    url_item = "{{% url '{0}_select_{1}' '100' %}}";    
</script>
{{% include 'ErpProject/ErpBackOffice/widget/update_view.html' %}}
{{% endblock %}}'''.format(nom_pattern, nom_modele.lower())
    fichier.write(texteTemplateLayout)
    fichier.close()
    
    print("genTemplateOfContentType #17")    
    #TEMPLATE DUPLICATE
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    path = path + "\\duplicate.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')

    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_list_{3}' %}}">Liste des {5}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_detail_{3}' model.id %}}">{{{{ model }}}}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>
        
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <button onclick="javascript:document.getElementById('submit').click()" class="validate-btn theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
                    <button onclick="javascript:window.location.assign('{{% url '{2}_detail_{3}' model.id %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>
                
                <form id="form" method="POST" action="{{% url '{2}_post_add_{3}' %}}"  enctype="multipart/form-data" data-role="validator" data-show-required-state="false" data-hint-mode="line" data-hint-background="bg-red" data-hint-color="fg-white" data-hide-error="5000"
                    novalidate="novalidate" data-on-error-input="notifyOnErrorInput" data-show-error-hint="false">
                    {{% csrf_token %}}
                    <input id="submit" type="submit" style="display: none">
                    <input type="text"  id="ref" name="ref" value ="{{{{ model.id }}}}" style="display: none">
                    {{% if isPopup %}}<input id="isPopup" name="isPopup" value="1" type="text" style="display: none">{{% endif %}}
                    <div class="row">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural)

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        is_required = False         
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": is_required = True
        
        if type_data == "FloatField" and list_champs[i].choices == None:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input value="{{{{ model.{0}|input_float }}}}" name="{0}" id="{0}" type="number" step="0.01" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "CharField" and list_champs[i].choices == None:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            if list_champs[i].max_length != None and list_champs[i].max_length >= 500 :
                textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <textarea name="{0}" id="{0}" '''.format(nom_champ)   
                if is_required == True :                                 
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + ">{{{{ model.{0} }}}}</textarea>".format(nom_champ)  
            else:
                textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="text" '''.format(nom_champ)
                if is_required == True :                                 
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "EmailField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control email full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="email" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, email" data-validate-hint="Saisissez une adresse email valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "TextField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <textarea name="{0}" id="{0}" '''.format(nom_champ)   
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">{{{{ model.{0} }}}}</textarea>".format(nom_champ)  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "IntegerField" and list_champs[i].choices == None:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="number" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "ImageField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                            <div class="tile-container">  
                                <input class="image_upload" name="{1}" id="{1}" type="file" accept="image/*" style="display:none;">                              
                                <a id="trigger-input-file" href="#" class="trigger-input-file tile-wide fg-white shadow" style="height: 100px!important; width: 100px!important;" data-role="tile"> 
                                    <div class="tile-content slide-up">
                                        <div class="slide">
                                            {{% if model.{1} %}}<img class="image_preview" src="{{% static model.{1}.url %}}" style="height: 100px; width: 100px;"> {{% else %}}
                                            <img class="image_preview" src="{{% static 'ErpProject/image/upload/articles/default.png' %}}" style="height: 100px; width: 100px;">{{% endif %}}
                                        </div>
                                        <div class="slide-over op-dark padding10" style="text-align: center!important; opacity: 60%!important;">
                                            <span class="icon mif-pencil" style="text-align: center!important; font-size: 40px!important;"></span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "FileField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                                {{% if model.document %}}                         
                                <span style=" color: #000; font-size: 10px;">Actuellement: <a href="{{% static model.document.url %}}">{{{{model.document.name|truncatechars:45}}}}</a></span>                         
                                {{% else %}}<span style=" color: #000; font-size: 10px;">Actuellement: Aucun document attaché</span>{{% endif %}}
                            <div class="input-control file full-size" data-role="input">
                                <input name="{1}" id="{1}" type="file"><button class="button"><span class="mif-folder"></span></button>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "ForeignKey":
            related_model = list_champs[i].related_model.__name__
            related_model_url_vers = getUrlVersOfRelatedModel(related_model)
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select class="selectpicker form-control" title="Sélectionner une option" name="{0}_id" id="{0}_id">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    <option class="search_option" value='-200' data-url="/{1}/{2}/list?isPopup=1">Voir plus ...</option>
                                    {{% for item in {2}s %}}<option {{% if model.{0}_id == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model_url_vers, related_model.replace("Model_", "").lower())
        elif type_data == "OneToOneField":
            related_model = list_champs[i].related_model.__name__
            related_model_url_vers = getUrlVersOfRelatedModel(related_model)
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select class="selectpicker form-control" title="Sélectionner une option" name="{0}_id" id="{0}_id">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    <option class="search_option" value='-200' data-url="/{1}/{2}/list?isPopup=1">Voir plus ...</option>
                                    {{% for item in {2}s %}}<option {{% if model.{0}_id == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model_url_vers, related_model.replace("Model_", "").lower())
        elif type_data == "ManyToManyField":
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="text full-size">
                                <select multiple="multiple" class="multi-select multi_select2" name="{0}" id="{0}">
                                    {{% for item in {1}s %}}<option {{% for object in model.{0}.all %}} {{% if object.id == item.id %}}{{{{ "selected" }}}}{{% endif %}}{{% endfor %}} value="{{{{ item.id }}}}">{{{{item}}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model.replace("Model_", "").lower())
        elif type_data == "BooleanField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label class="input-control checkbox small-check full-size">
                                <input name="{1}" id="{1}" {{% if model.{1} == True %}} {{{{ "checked" }}}} {{% endif %}} type="checkbox">
                                <span class="check"></span><span class="caption">{0}</span>'''.format(nom_champ_verbose, nom_champ)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            </label>
                        </div>'''
        elif type_data == "DateTimeField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size datetimepicker">
                                <input type="text" name="{1}" id="{1}" value="{{{{ model.{1}|date:"d/m/Y H:i" }}}}">
                                <div class="button"><span class="glyphicon glyphicon-screenshot far fa-calendar" style="margin-right:3px;"></span><span class="glyphicon glyphicon-screenshot far fa-clock"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "DateField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                                <input type="text" name="{1}" id="{1}" value="{{{{ model.{1}|date:"d/m/Y" }}}}">
                                <div class="button"><span class="mif-calendar"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">                                
                                <select name="{0}" id="{0}">
                                    <option value="">Sélectionnez une option</option>
                                    {{% for item in model.list_{0} %}}<option {{% if model.{0} == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item.designation }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ)
        else :
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True : 
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="text" '''.format(nom_champ)
            if is_required == True :                                 
                textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"  
            textebcl = textebcl + '''
                            </div>
                        </div>'''
            
    texteTemplateLayout = texteTemplateLayout + textebcl
    texteTemplateLayout = texteTemplateLayout + '''
                    </div>'''
                    
    if len(relateds) > 0: 
        texteTemplateLayout = texteTemplateLayout + '''     
                    <br><br>
                    <div class="row">
                        <ul class="nav nav-tabs navtab-bg"> 
                            <li class="active"><a href="#frame_autres" data-toggle="tab" aria-expanded="false"><span>Autres informations</span></a></li>
                        </ul>
                        <div class="tab-content"> 
                            <div class="tab-pane active" id="frame_autres">
                                <div class="row margin20 no-margin-left no-margin-right">'''
        for i in range(0, len(relateds)):
            if relateds[i] != "":
                list_relateds = relateds[i].split(",")
                content_id = list_relateds[0]
                field_name = list_relateds[1]
                field_type = list_relateds[2]
                model_related = ContentType.objects.get(pk = content_id)
                model_class_related = model_related.model_class()
                nom_model_class_related = model_related.model_class().__name__
                related_model_url_vers = getUrlVersOfRelatedModel(nom_model_class_related)
                nom_model_related = nom_model_class_related.replace("Model_", "").lower()
                input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
                related_query_name = ""
                if field_type == "ForeignKey":
                    related_query_name = model_class_related._meta.get_field(field_name).related_query_name() 
                    if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name)
                elif field_type == "ManyToManyRel":
                    if field_name.startswith("model_") : related_query_name = "{}_set".format(field_name)
                    else: related_query_name = field_name
                print("related_query_name: {}".format(related_query_name))     
                
                texteTemplateLayout = texteTemplateLayout + '''                                
                                <div class="col-md-6">
                                    <div class="section-otm" data-compteur="1">
                                        <table class="table bordered no-margin" style="width:100%;">
                                            <thead>	
                                                <tr>
                                                    <th width="90%">{0}</th>
                                                    <th width="10%"></th>
                                                </tr>
                                            </thead>                
                                            <tbody class="tbl_posts_body">
                                                {{% for item in model.{4}.all %}}
                                                <tr>
                                                    <td>
                                                        <div class="input-control text full-size">                                
                                                            <select class="selectpicker form-control" title="sélectionner une option" name="{3}" id="{3}-1">
                                                                <option value="">Sélectionnez une nouvelle option {0}</option>
                                                                <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                                <option {{{{ "selected" }}}} value="{{{{ item.id }}}}"> {{{{ item }}}} </option>
                                                            </select>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div class="pagination no-border">
                                                            <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                        </div>
                                                    </td>
                                                </tr>
                                                {{% endfor %}}
                                            </tbody>
                                        </table> 
                                        <br><button type="button" class="button rounded add-record">Ajouter</button>
                                        <table class="sample_table" style="display:none;">       
                                            <tr>
                                                <td>
                                                    <div class="input-control text full-size">                                
                                                        <select class="form-control" title="Sélectionner une option" name="{3}" id="">
                                                            <option value="">Sélectionnez une nouvelle option {0}</option>
                                                            <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                        </select>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="pagination no-border">
                                                        <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>'''.format(model_class_related._meta.verbose_name, related_model_url_vers, nom_model_related, input_name_related, related_query_name)  
        texteTemplateLayout = texteTemplateLayout + '''                                
                                </div>
                            </div>
                        </div>
                    </div>'''                    
                    
    texteTemplateLayout = texteTemplateLayout + '''
                </form>
            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
<script>
    url_item = "{{% url '{0}_select_{1}' '100' %}}";    
</script>
{{% include 'ErpProject/ErpBackOffice/widget/create_view.html' %}}
{{% endblock %}}'''.format(nom_pattern, nom_modele.lower())
    fichier.write(texteTemplateLayout)
    fichier.close()    
    print("genTemplateOfContentType #18")    
    # TEMPLATE IMPRIMER OBJECT
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\reporting".format(nomModule, nom_modele.lower())
    try:
        os.mkdir(utils.format_path(path))
    except Exception as e:
        pass
    path = path + "\\print_{1}.html".format(nomModule, nom_modele.lower())
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')
    
    texteTemplate = '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{{{ title }}}}</title>
        <meta name="description" content="{{{{ title }}}}">
        <meta name="author" content="MelodyERP">
    </head>
    {{% load static %}}{{% load account_filters %}}{{% load humanize %}}

    <body>       
        <div id="report">
            <h2 class="align-center header">{{{{ title }}}}</h2>
            <span class="date-text">Le {{% now " d/m/Y" %}}</span>
            <div class="row">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize())

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        
        if type_data == "FloatField" and list_champs[i].choices == None:
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p>{1} :<br>
                        <span class="sub-alt-header">{{{{model.{0}|monetary}}}}</span>
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "BooleanField":
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <label class="input-control checkbox small-check full-size">
                        <input name="{0}" id="{0}"  {{% if model.{0} is True %}}{{{{ "checked" }}}}{{% endif %}} type="checkbox" disabled="disabled">
                        <span class="check"></span>
                        <span class="caption">{1}</span>
                    </label>
                </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data in ("ForeignKey", "OneToOneField"):
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p>{1} :<br>
                        {{% if model.{0} is None %}}
                        <span class="sub-alt-header"> - </span>
                        {{% else %}}
                        <span class="sub-alt-header">{{{{ model.{0} }}}}</span>
                        {{% endif %}}
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose, nom_pattern, related_model.replace("Model_", "").lower())
        elif type_data == "ImageField":
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p>{1} :<br>
                        {{% if model.{0} %}}
                        <img class="" src="{{% static model.{0}.url %}}" style="height: 100px; width: 100px;">
                        {{% else %}}
                        <img src="{{% static 'ErpProject/image/upload/articles/default.png' %}}" style="height: 100px; width: 100px;">
                        {{% endif %}}
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "FileField":
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p>{1} :<br>
                        {{% if model.{0} %}}
                        <a href="{{% static model.{0}.url %}}"><img src="{{% static 'ErpProject/image/document.png' %}}" style="height: 70px; width: 70px;"></a>
                        <br><span style=" color: #000; font-size: 9px;">{{{{model.{0}.name|truncatechars:25}}}}</span>                          
                        {{% else %}}<span class="sub-alt-header">Aucun document attaché</span>{{% endif %}}
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "ManyToManyField":
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p class="fg-gray">
                        <label>{1} :</label><br>
                        {{% for item in model.{0}.all %}}
                            <span class="sub-alt-header badge badge-light"> {{{{ item }}}} </span><br>
                        {{% endfor %}}                     
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "DateTimeField":
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p>{1} :<br>
                        <span class="sub-alt-header">{{{{model.{0}|date:"d/m/Y H:i"}}}}</span>
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "DateField":
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p>{1} :<br>
                        <span class="sub-alt-header">{{{{model.{0}|date:"d/m/Y"}}}}</span>
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p>{1} :<br>
                        <span class="sub-alt-header">{{{{ model.value_{0} }}}}</span>
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose)
        else :
            textebcl = textebcl + '''
                <div class="col-md-6">
                    <p>{1} :<br>
                        <span class="sub-alt-header">{{{{ model.{0} }}}}</span>
                    </p>
                </div>'''.format(nom_champ, nom_champ_verbose)            
    texteTemplate = texteTemplate + textebcl 
    texteTemplate = texteTemplate + '''
            </div>'''

    texteTemplate = texteTemplate + '''
        </div>
    </body>
</html>
'''
    fichier.write(texteTemplate)
    fichier.close()
    print("genTemplateOfContentType #19")

    # TEMPLATE UPLOAD
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule, nom_modele.lower())
    path = path + "\\upload.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')
    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_add_{3}' %}}">Création nouvel objet {5}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>
        
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <button onclick="selectFile()" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}} chargement-au-click">Choisir un fichier</button> 
                    <button id="btn-register" style="display:none;" onclick="enregistrer()" class="validate-btn theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
                    <button onclick="javascript:window.location.assign('{{% url '{2}_add_{3}' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>
                
                <div id="error_format_file" class="alert alert-danger col-md-12" style="display:none;">
                    <a class="close" data-dismiss="alert">×</a>
                    Charger un fichier Excel SVP !
                </div>
                
                <form id="form" method="POST" action="{{% url '{2}_post_upload_{3}' %}}"  enctype="multipart/form-data" data-role="validator" data-show-required-state="false" data-hint-mode="line" data-hint-background="bg-red" data-hint-color="fg-white" data-hide-error="5000"
                novalidate="novalidate" data-on-error-input="notifyOnErrorInput" data-show-error-hint="false">
                {{% csrf_token %}}
                <input id="submit" type="submit" style="display: none">
                <input type="file" id="input-excel" name="file_upload" style="display:none;"/>
                <input type="text" id="sheet" name="sheet" style="display:none;"/>
                    
                <div id="match_wrapper" class="row">
                    <ul class="nav nav-tabs navtab-bg"> 
                        <li class="active"><a href="#frame_matchs" data-toggle="tab" aria-expanded="false"><span>Correspondance entêtes Excel et champs de l'objet</span></a></li>
                    </ul>
                    <div class="tab-content"> 
                        <div class="tab-pane active" id="frame_matchs">
                            <div class="row margin20 no-margin-left no-margin-right">                  
'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose)

    textebcl = ""
    print(f"{len(list_champs)} -------- ")
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        is_required = False         
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": is_required = True
        if type_data not in ("ImageField", "FileField", "ManyToManyField"):
            if type_data in ("ForeignKey", "OneToOneField"):
                related_model = list_champs[i].related_model.__name__ 
                related_model_url_vers = getUrlVersOfRelatedModel(related_model)               
                textebcl = textebcl + '''
                                <div class="col-md-3 col-sm-6 col-xs-12">
                                    <label>{}</label>'''.format(nom_champ_verbose)
                texte_is_required = ""
                if is_required == True : 
                    texte_is_required = 'data-validate-func="required" data-validate-hint="Sélectionnez une valeur dans le champ {} SVP !"'.format(nom_champ_verbose)
                    textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
                textebcl = textebcl + '''               
                                    <div class="input-control text full-size">
                                        <select name="{0}_id" id="{0}_id" class="champ_filtrage" {1}>
                                            <option value="">Sélectionnez un champ</option>
                                        </select>
                                    </div> 
                                </div>'''.format(nom_champ, texte_is_required)

            else:
                textebcl = textebcl + '''
                                <div class="col-md-3 col-sm-6 col-xs-12">
                                    <label>{}</label>'''.format(nom_champ_verbose)
                texte_is_required = ""
                if is_required == True : 
                    texte_is_required = 'data-validate-func="required" data-validate-hint="Sélectionnez une valeur dans le champ {} SVP !'.format(nom_champ_verbose)
                    textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"

                textebcl = textebcl + '''               
                                    <div class="input-control text full-size">
                                        <select name="{0}" id="{0}" class="champ_filtrage" {1}>
                                            <option value="">Sélectionnez un champ</option>
                                        </select>
                                    </div> 
                                </div>'''.format(nom_champ, texte_is_required)
             
    texteTemplateLayout = texteTemplateLayout + textebcl

    texteTemplateLayout =  texteTemplateLayout + '''                  
                            </div>
                        </div>
                    </div>
                </div>
                </form>

                <div id="upload_wrapper">                              
                </div>
                
                <div id="bg" class="row no-margin-left no-margin-right" style="padding-top:300px;">
                    <div class="col-md-3 xs-hidden"></div>
                    <div class="col-md-6 col-xs-12">
                        <h3>Choisissez un fichier CSV ou Excel à importer.</h3>  
                        <span class="fg-gray" style="text-align:center;">Les fichiers Excel sont recommandés pour le formatage des champs.<br>
                    </div>
                    <div class="col-md-3 xs-hidden"></div>
                </div>

            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose)
            
    texteTemplateLayout = texteTemplateLayout + '''
<script type="text/javascript" src="{% static 'ErpProject/js/FileSaver.min.js' %}"></script>
<script type="text/javascript" src="{% static 'ErpProject/js/xlsx.full.min.js' %}"></script> 
<script>
    function enregistrer(){
        document.getElementById('submit').click();
    }
    
    function selectFile() {
        $('input[id=input-excel]').click();
    }

    function extractHeader(ws) {
        const header = []
        const columnCount = XLSX.utils.decode_range(ws['!ref']).e.c + 1
        for (let i = 0; i < columnCount; ++i) {
            header[i] = ws[`${XLSX.utils.encode_col(i)}1`].v
        }
        return header
    }

    function setOptionsHeaders(headers) {
        $('.champ_filtrage').children().remove(); 

        var ligne = "<option value=''>Aucune</option>";
        for(var i = 0; i < headers.length; i++){
            var header = headers[i];
            ligne += `<option value='${header}'> ${header} </option>`;
        }

        $('.champ_filtrage').append(ligne);
    }

    
    //Import excel
    $('#input-excel').change(function(e){
        const input = document.getElementById("input-excel")
        const file = input.files[0]


        $('#error_format_file').css('display', 'none');
        if (file.type !== 'application/vnd.ms-excel' && file.type !== "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") {
            $('#error_format_file').css('display', 'inline');
        }else{
            var reader = new FileReader();
            reader.readAsArrayBuffer(e.target.files[0]);
            reader.onload = function(e) {
                var data = new Uint8Array(reader.result);
                var wb = XLSX.read(data,{type:'array'});
                var ws_name = wb.SheetNames[0];
                console.log(ws_name);
                $("#sheet").val(ws_name);
                $("#upload_wrapper").children().remove();
                var sheet = wb.Sheets[ws_name];
                var htmlstr = XLSX.write(wb,{sheet: ws_name, type:'binary',bookType:'html'});
                htmlstr = decodeURIComponent(escape(htmlstr));
                $('#upload_wrapper')[0].innerHTML += htmlstr;
                $('#upload_wrapper table').addClass("display nowrap border bordered striped table-overflow");
                $('#upload_wrapper table').css('overflow', 'auto');
                $('#upload_wrapper table').css('position', 'relative');
                $('#upload_wrapper table').css('display', 'inline-block');
                $('#upload_wrapper table').css('width', '100%');
                
                $('#bg').css('display', 'none');
                $('#btn-register').css('display', 'inline');

                const headers = extractHeader(sheet)
                console.log("header");
                console.log(headers);
                setOptionsHeaders(headers);
            }
        }


    });
</script>
{% endblock %}
'''
    fichier.write(texteTemplateLayout)
    fichier.close()

    # CRUD AND URLS URLS
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\urls.py".format(nomModule)
    fichier = codecs.open(utils.format_path(path),"a", encoding='utf-8')

    texte_a_ajouter_urls_py_dossier_ap="\n#{2} URLS\n#=====================================\n#{2} CRUD URLS\nurlpatterns.append(url(r'^{0}/list', views.get_lister_{0}, name = '{1}_list_{0}'))".format(nom_modele.lower(),nom_pattern, nom_modele.upper())
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/add', views.get_creer_{0}, name = '{1}_add_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/post_add', views.post_creer_{0}, name = '{1}_post_add_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/select/(?P<ref>[0-9]+)/$', views.get_select_{0}, name = '{1}_select_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/item/(?P<ref>[0-9]+)/$', views.get_details_{0}, name = '{1}_detail_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/item/(?P<ref>[0-9]+)/update$', views.get_modifier_{0}, name = '{1}_update_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/item/post_update/$', views.post_modifier_{0}, name = '{1}_post_update_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_{0}, name = '{1}_duplicate_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_{0}, name = '{1}_print_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\n#{2} UPLOAD URLS\nurlpatterns.append(url(r'^{0}/upload/add', views.get_upload_{0}, name = '{1}_get_upload_{0}'))".format(nom_modele.lower(),nom_pattern, nom_modele.upper())
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/upload/post_add', views.post_upload_{0}, name = '{1}_post_upload_{0}'))\n".format(nom_modele.lower(),nom_pattern)
    fichier.write(texte_a_ajouter_urls_py_dossier_ap)
    fichier.close()
    print("genTemplateOfContentType #20")
    return nom_modele
    
    
def genReportingOfContentType(content_type_id, module_id):
    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()
    module = dao_module.toGetModule(module_id)
    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__
    nomdao = "dao_{0}".format(nom_modele.lower())
    nom_pattern = 'module_{0}'.format(unidecode.unidecode(module.nom_module.lower().replace(" ","_")))
    nomModule = module.nom_application
    
    url_name_reporting = "{1}_get_generer_{0}".format(nom_modele.lower(),nom_pattern)
    
    list_champs = [] 
    list_champs_excel = []
    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): 
            list_champs.append(field) 
            list_champs_excel.append(field) 
        #Pour le reporting excel on rajoute aussi l'auteur et la date de création
        if field.name in ("auteur", "creation_date"): list_champs_excel.append(field)
        
    # CREATION FONCTIONS RAPPORT DANS views.py
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\views.py".format(nomModule)
    fichier = codecs.open(utils.format_path(path), "a", encoding='utf-8')

    # GET GENERER RAPPORT
    texte_a_ajouter_views_py = "\n\n# {2} REPORTING CONTROLLERS\ndef get_generer_{0}(request):\n\ttry:\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)\n\t\tif response != None: return response\n\n\t\tcontext = {{\n\t\t\t'title' : \"Rapport {3}\",\n\t\t\t'devises' : dao_devise.toListDevisesActives(),\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'user_actions': actions,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation()\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{4}/{0}/generate.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)

    # POST TRAITER RAPPORT
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef post_traiter_{0}(request, utilisateur = None, modules = [], sous_modules = [], enum_module = vars_module):\n\t#On recupère et format les inputs reçus\n\tdate_debut = str(request.POST['date_debut'])\n\ttry:\n\t\tdate_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))\n\texcept Exception as e: date_debut = None\n\n\tdate_fin = str(request.POST['date_fin'])\n\ttry:\n\t\tdate_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)\n\texcept Exception as e: date_fin = None\n\n\t#On récupère les données suivant le filtre défini\n\tmodel = {2}.objects.filter(creation_date__range = [date_debut, date_fin]).order_by('-creation_date')\n\n\tcontext = {{\n\t\t'title' : \"Rapport {1}\",\n\t\t'model' : model,\n\t\t'date_debut' : request.POST['date_debut'],\n\t\t'date_fin' : request.POST['date_fin'],\n\t\t'utilisateur' : utilisateur,\n\t\t'modules' : modules,\n\t\t'sous_modules': sous_modules,\n\t\t'module' : enum_module,\n\t\t'organisation' : dao_organisation.toGetMainOrganisation(),\n\t}}\n\treturn context".format(nom_modele.lower(),nom_modele_verbose,nom_modele_class)

    # POST GENERER RAPPORT
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef post_generer_{0}(request):\n\ttry:\n\t\tsame_perm_with = '{5}'\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)\n\t\tif response != None: return response\n\n\t\tcontext = post_traiter_{0}(request, utilisateur, modules, sous_modules)\n\t\tmode_edition = makeString(request.POST['mode_edition'])\n\t\tif mode_edition == '': mode_edition = 'ecran'\n\t\tif mode_edition == 'pdf':\n\t\t\treturn weasy_print('ErpProject/{4}/reporting/rapport_{0}.html', 'rapport_{0}.pdf', context, request)\n\t\telse:\n\t\t\ttemplate = loader.get_template('ErpProject/{4}/{0}/generated.html')\n\t\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule,url_name_reporting)
   
    # POST EXPORT RAPPORT EXCEL
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef post_excel_rapport_{0}(request):\n\ttry:\n\t\t#On recupère et format les inputs reçus\n\t\tdate_debut = str(request.POST['date_debut'])\n\t\ttry:\n\t\t\tdate_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))\n\t\texcept Exception as e: date_debut = None\n\n\t\tdate_fin = str(request.POST['date_fin'])\n\t\ttry:\n\t\t\tdate_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)\n\t\texcept Exception as e: date_fin = None\n\n\t\t#On récupère les données suivant le filtre défini\n\t\tmodel = {2}.objects.filter(creation_date__range = [date_debut, date_fin]).order_by('-creation_date')\n\n\t\t#On génère le fichier excel file_name =  \"Rapport {1}.xlsx\"\n\t\twb = Workbook()\n\t\tws = wb.active\n\t\tws.sheet_view.showGridLines = False\n\t\tws.merge_cells('A1:D1')\n\t\tws.merge_cells('A2:I2')\n\t\tws.merge_cells('A3:D3')\n\n\t\tws['A1'] = 'Page: 1/ 1'\n\t\tdt_debut = request.POST['date_debut']\n\t\tdt_fin = request.POST['date_fin']\n\t\tws['A2'] = f\"Rapport {1}s enregistrés du {{dt_debut}} au {{dt_fin}}\"\n\t\ttoday = datetime.now().strftime('%d/%m/%Y')\n\t\tws['A3'] = f'Kinshasa, le: {{today}}'\n\n\t\tpageStyle = styles.NamedStyle(name = 'page_style')\n\t\tpageStyle.font = styles.Font(name = 'Calibri', size = 10, color = 'FF000000')\n\t\t#pageStyle.fill = styles.PatternFill(patternType = 'solid', fgColor = 'FFFF55')\n\t\tpageStyle.alignment = styles.Alignment(horizontal='right',vertical='top')\n\t\tborderStyle = styles.Side(style = 'dashDot', color = 'FF00FF')\n\t\tpageStyle.border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)\n\n\t\ttitleStyle = styles.NamedStyle(name = 'title_style')\n\t\ttitleStyle.font = styles.Font(name = 'Calibri', size = 14, color = 'FF000000', bold=True)\n\t\t#titleStyle.fill = styles.PatternFill(patternType = 'solid', fgColor = 'FFFF55')\n\t\ttitleStyle.alignment = styles.Alignment(horizontal='center', vertical='top',wrap_text=True)\n\n\t\tdateStyle = styles.NamedStyle(name = 'date_style')\n\t\tdateStyle.font = styles.Font(name = 'Calibri', size = 9, color = 'FF000000')\n\t\t#dateStyle.fill = styles.PatternFill(patternType = 'solid', fgColor = 'FFFF55')\n\t\tdateStyle.alignment = styles.Alignment(horizontal='right', vertical='top')\n\n\t\tfieldnameStyle = styles.NamedStyle(name = 'fieldname_style')\n\t\tfieldnameStyle.font = styles.Font(name = 'Calibri', size = 10, color = 'FF000000', bold=True)\n\t\t#fieldnameStyle.fill = styles.PatternFill(patternType = 'solid', fgColor = 'FFFF55')\n\t\tfieldnameStyle.alignment = styles.Alignment(horizontal='left', vertical='top',wrap_text=True)\n\t\tborderStyle = styles.Side(style = 'thin', color = 'FF000000')\n\t\tfieldnameStyle.border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)\n\n\t\tfieldvalueStyle = styles.NamedStyle(name = 'fieldvalue_style')\n\t\tfieldvalueStyle.font = styles.Font(name = 'Cambria', size = 8, color = 'FF000000')\n\t\t#fieldvalueStyle.fill = styles.PatternFill(patternType = 'solid', fgColor = 'FFFF55')\n\t\tfieldvalueStyle.alignment = styles.Alignment(horizontal='left', vertical='top',wrap_text=True)\n\t\tborderStyle = styles.Side(style = 'thin', color = 'FF000000')\n\t\tfieldvalueStyle.border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)\n\n\t\tws['A1'].style = pageStyle\n\t\tws['A2'].style = titleStyle\n\t\tws['A3'].style = dateStyle".format(nom_modele.lower(),nom_modele_verbose,nom_modele_class)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t#On crée les entêtes du tableau"  
    textebcl=""
    lettre = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ","BA","BB","BC","BD","BE","BF","BG","BH","BI","BJ","BK","BL","BM","BN","BO","BP","BQ","BR","BS","BT","BU","BV","BW","BX","BY","BZ"]
    index_lettre = 0
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField"):
            textebcl = textebcl + "\n\t\tws['{0}5'] = '{1}'\n\t\tws['{0}5'].style = fieldnameStyle".format(lettre[index_lettre], nom_champ_verbose)
            index_lettre = index_lettre+1
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + textebcl
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\trow = 6\n\n\t\tfor item in model:" 
    
    column=1 
    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField"):
            if type_data == "FloatField" and list_champs[i].choices == None:
                textebcl = textebcl + "\n\t\t\t{0} = ws.cell(row=row,column={1})\n\t\t\t{0}.value = item.{0}\n\t\t\t{0}.style = fieldvalueStyle\n\t\t\t{0}.data_type = 'n'\n\t\t\t{0}.number_format = '0.00'".format(nom_champ, column)
                column = column+1
            elif type_data == "CharField" and list_champs[i].choices == None:
                textebcl = textebcl + "\n\t\t\t{0} = ws.cell(row=row,column={1})\n\t\t\t{0}.value = item.{0}\n\t\t\t{0}.style = fieldvalueStyle".format(nom_champ, column)
                column = column+1
            elif type_data == "BooleanField":
                textebcl = textebcl + "\n\t\t\t{0} = ws.cell(row=row,column={1})\n\t\t\t{0}.value = item.{0}\n\t\t\t{0}.style = fieldvalueStyle".format(nom_champ, column)
                column = column+1
            elif type_data == "DateTimeField":
                textebcl = textebcl + "\n\t\t\t{0} = ws.cell(row=row,column={1})\n\t\t\t{0}.value = item.{0} if item.{0} else ''\n\t\t\t{0}.style = fieldvalueStyle\n\t\t\tif item.{0}:\n\t\t\t\t{0}.data_type = 'd'\n\t\t\t\t{0}.number_format = 'm/d/yy h:mm'".format(nom_champ, column)
                column = column+1
            elif type_data == "DateField":
                textebcl = textebcl + "\n\t\t\t{0} = ws.cell(row=row,column={1})\n\t\t\t{0}.value = item.{0} if item.{0} else ''\n\t\t\t{0}.style = fieldvalueStyle\n\t\t\tif item.{0}:\n\t\t\t\t{0}.data_type = 'd'\n\t\t\t\t{0}.number_format = 'mm-dd-yy'".format(nom_champ, column)
                column = column+1
            elif type_data in ("ForeignKey", "OneToOneField"):
                textebcl = textebcl + "\n\t\t\t{0} = ws.cell(row=row,column={1})\n\t\t\t{0}.value = item.{0}.__str__() if item.{0} else ''\n\t\t\t{0}.style = fieldvalueStyle".format(nom_champ, column)
                column = column+1
            elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
                textebcl = textebcl + "\n\t\t\t{0} = ws.cell(row=row,column={1})\n\t\t\t{0}.value = item.value_{0}\n\t\t\t{0}.style = fieldvalueStyle".format(nom_champ, column)
                column = column+1
            else :
                textebcl = textebcl + "\n\t\t\t{0} = ws.cell(row=row,column={1})\n\t\t\t{0}.value = item.{0}\n\t\t\t{0}.style = fieldvalueStyle".format(nom_champ, column)
                column = column+1
    #textebcl = textebcl + "\n\t\t\tcreation_date = ws.cell(row=row,column={0})\n\t\t\tcreation_date.value = item.creation_date\n\t\t\tcreation_date.style = fieldvalueStyle\n\t\t\tcreation_date.data_type = 'd'\n\t\t\tcreation_date.number_format = 'mm-dd-yy'".format(column)
    #column = column+1
    #textebcl = textebcl + "\n\t\t\tauteur = ws.cell(row=row,column={0})\n\t\t\tauteur.value = item.auteur.nom_complet if item.auteur else ''\n\t\t\tauteur.style = fieldvalueStyle".format(column)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + textebcl
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t\trow = row+1\n\n\t\tbuffer = BytesIO()\n\t\twb.save(buffer)\n\t\texcell_file = buffer.getvalue()\n\t\tbuffer.close()\n\t\tresponse = HttpResponse(excell_file, content_type='application/xlsx')\n\t\tresponse['Content-Disposition'] = 'inline;filename=Rapport_{0}.xlsx'\n\t\treturn response\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc(), reverse('{1}_get_generer_{0}'))".format(nom_modele.lower(), nom_pattern, nomModule) 
      
    fichier.write(texte_a_ajouter_views_py)
    fichier.close()

    # CREATION DES TEMPLATES REPORTING DU MODELE

    # TEMPLATE GENERATE
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule, nom_modele.lower())
    path = path + "\\generate.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')
    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <h2 class="text-light no-margin-left">{{{{ title }}}}</h2>
</div>

<div class="row">
    <button onclick="javascript:document.getElementById('submit').click()" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
    <button onclick="javascript:window.location.assign('{{% url '{2}_index' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
</div>

<hr class="hr-ligne">
<!-- Appel de la fonction message -->
{{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>

<div class="row item-content" style="margin-top: 10px">
    <form id="form" method="POST" action="{{% url '{2}_post_generer_{3}' %}}"
        data-role="validator" 
        data-show-required-state="false"
        data-hint-mode="line"
        data-hint-background="bg-red"
        data-hint-color="fg-white"
        data-hide-error="5000"
        novalidate="novalidate"
        data-on-error-input="notifyOnErrorInput"
        data-show-error-hint="false">
        {{% csrf_token %}}
        <input id="submit" type="submit" style="display: none">
        
        <div class="row">
            <div class="col-md-12">
                <div class="row">
                    <div class="col-md-6">
                        <label>Date de début :</label>
                        <div id="input-date-debut" class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                            <input type="text" placeholder="jj/mm/aaaa" name="date_debut" id="date_debut"
                                data-validate-func="required" 
                                data-validate-hint="Précisez la date de début svp.">
                            <div class="button"><span class="mif-calendar"></span></div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <label>Date de fin :</label>
                        <div id="input-date-fin" class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                            <input type="text" placeholder="jj/mm/aaaa" name="date_fin" id="date_fin"
                                data-validate-func="required" 
                                data-validate-hint="Précisez la date de fin svp.">
                            <div class="button"><span class="mif-calendar"></span></div>
                        </div>
                    </div>
                </div>
                <br/>
                <div class="row">
                    <div class="col-md-6">
                        <input type="hidden" id="mode_edition" value="ecran">
                        <label>Mode d'édition</label>
                        <div class="ui fluid search selection dropdown">
                            <input type="hidden" id="select_mode_edition" name="mode_edition" 
                            data-validate-func="required" 
                            data-validate-hint="Précisez le mode d'édition.">
                            <i class="dropdown icon"></i>
                            <div class="default text">Sélectionnez un mode</div>
                            <div class="menu">
                                <div class="item" data-value="ecran"><i class="fas fa-desktop" style="font-size: 25px;color:#424892;margin-right: 5px;"></i>Affichage à l'écran</div>
                                <div class="item" data-value="excel"><i class="far fa-file-excel" style="font-size: 30px;color:#236e43;margin-right: 5px;"></i>Export Excel</div>
                                <div class="item" data-value="pdf"><i class="far fa-file-pdf" style="font-size: 30px;color:#f44336;margin-right: 5px;"></i>Export PDF</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>       
</div>
{{% include 'ErpProject/ErpBackOffice/widget/include_view.html' %}}
<script>
    $("#valider").on("click", function(e) {{
        mode_edition = $("#mode_edition").val();       
        if (mode_edition == "excel"){{
            url_link = "{{% url '{2}_post_excel_rapport_{3}' %}}";
        }}else{{
            url_link = "{{% url '{2}_post_generer_{3}' %}}";
        }}   
        $("form").attr('action', url_link);    
        document.getElementById('submit').click()
    }}); 
    $("#select_mode_edition").on("change", function(e) {{
        mode_edition = $("#select_mode_edition").val();
        $("#mode_edition").val(mode_edition);
    }}); 
</script>
{{% endblock %}}'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural)

    fichier.write(texteTemplateLayout)
    fichier.close()

    
    # TEMPLATE GENERATED
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    path = path + "\\generated.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')

    texteTemplate = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <button id="export_pdf" class="theme-btn theme-btn-sm rounded"><span style="font-weight: bold"><i class="far fa-file-pdf" style="font-size:1rem;color:#f44336;margin-right:5px;"></i> Exporter en pdf</span></button>
    <button id="export_excel" class="theme-btn theme-btn-sm rounded chargement-au-click"><span style="font-weight: bold"><i class="far fa-file-excel" style="font-size:1rem;color:#236e43;margin-right:5px;"></i> Exporter en Excel</span></button>
    <button onclick="javascript:window.location.assign('{{% url '{2}_get_generer_{3}' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
</div>
<form id="form" method="POST" action="{{% url '{2}_post_generer_{3}' %}}">
    {{% csrf_token %}}
    <input id="submit" type="submit" style="display: none">
    <input type="text" placeholder="jj/mm/aaaa" name="date_debut" value="{{{{ date_debut }}}}" style="display: none">
    <input type="text" placeholder="jj/mm/aaaa" name="date_fin" value="{{{{ date_fin }}}}" style="display: none">
    <input type="text" name="mode_edition" value="pdf" style="display: none">
</form> 
<hr class="hr-ligne">
<div id="divToPrint" class="row item-content" style="margin-top: 20px" style="padding-top: 30px">
    <p class="align-center header">{{{{ title }}}}</p>
    <div class="row">
        <p>
            Période :<br>
            <span class="sub-header">Du {{{{ date_debut }}}} au {{{{ date_fin }}}} </span>
            <br>
            <br>
        </p>
    </div>
    <br>
    <br>
    <div id="list-view" class="row" style="margin-top: 10px;overflow: auto; position: relative; display: inline-block;"> 
        <table id="rapport" class="table bordered no-margin" style="width: 950px">
            <tr style="background-color:#f1f1f1">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize())

    textebcl=""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            textebcl = textebcl + '''
                <th>{0}</th>'''.format(nom_champ_verbose)
    textebcl = textebcl + '''
                <th>Date de création</th>
                <th>Créé par</th>'''
    texteTemplate = texteTemplate + textebcl

    texteTemplate= texteTemplate + '''
            </tr>
            {% for item in model %}
            <tr>'''

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            if type_data == "FloatField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                <td>{{{{item.{0}|monetary}}}}</td>'''.format(nom_champ)
            elif type_data == "CharField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                <td>{{{{item.{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
            elif type_data == "BooleanField":
                textebcl = textebcl + '''
                <td>{{{{item.{0}|boolean}}}}</td>'''.format(nom_champ)
            elif type_data == "DateTimeField":
                textebcl = textebcl + '''
                <td>{{{{item.{0}|date:"d/m/Y H:i"}}}}</td>'''.format(nom_champ)
            elif type_data == "DateField":
                textebcl = textebcl + '''
                <td>{{{{item.{0}|date:"d/m/Y"}}}}</td>'''.format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
                textebcl = textebcl + '''
                <td>{{{{ item.value_{0} }}}}</td>'''.format(nom_champ)
            else :
                textebcl = textebcl + '''
                <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)

    texteTemplate = texteTemplate + textebcl

    texteTemplate = texteTemplate + '''
                <td>{{{{item.creation_date|date:'d/m/Y'}}}}</td>
                <td>{{{{item.auteur.nom_complet}}}}</td>
            </tr>
            {{% endfor %}}
        </table>
    </div>
</div>
<script>
    $("#export_excel").on("click", function(e) {{
        url_link = "{{% url '{2}_post_excel_rapport_{3}' %}}";
        $("form").attr('action', url_link);      
        document.getElementById('submit').click()
    }}); 

    $("#export_pdf").on("click", function(e) {{
        url_link = "{{% url '{2}_post_generer_{3}' %}}";
        $("form").attr('action', url_link);     
        document.getElementById('submit').click()
    }}); 
</script>
{{% include 'ErpProject/ErpBackOffice/widget/export_excel.html' with btn_id="btn_export" table_id="rapport" filename="rapport_{1}" only %}}
{{% endblock %}}
'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)
    fichier.write(texteTemplate)
    fichier.close()


    # TEMPLATE RAPPORT
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\reporting".format(nomModule, nom_modele.lower())
    try:
        os.mkdir(utils.format_path(path))
    except Exception as e:
        pass
    path = path + "\\rapport_{1}.html".format(nomModule, nom_modele.lower())
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')
    
    texteTemplate = '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{{{ title }}}}</title>
        <meta name="description" content="{{{{ title }}}}">
        <meta name="author" content="MelodyERP">
    </head>
    {{% load static %}}{{% load account_filters %}}{{% load humanize %}}

    <body>       
        <div id="report">
            <h2 class="align-center header">{{{{ title }}}}</h2>
            <span class="date-text">Le {{% now " d/m/Y" %}}</span>
            <div class="row">
                <p>
                    Période :<br>
                    <span class="sub-header">Du {{{{ date_debut }}}} au {{{{ date_fin }}}} </span>
                    <br>
                    <br>
                </p>
            </div>
            <br>
            <table id="rapport" class="table bordered no-margin" style="width: 100%">
                <tr style="background-color:#f1f1f1">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize())

    textebcl=""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            textebcl = textebcl + '''
                    <th>{0}</th>'''.format(nom_champ_verbose)
    textebcl = textebcl + '''
                    <th>Date de création</th>
                    <th>Créé par</th>'''
    texteTemplate = texteTemplate + textebcl

    texteTemplate= texteTemplate + '''
                </tr>
                {% for item in model %}
                <tr>'''

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            if type_data == "FloatField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|monetary}}}}</td>'''.format(nom_champ)
            elif type_data == "CharField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
            elif type_data == "BooleanField":
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|boolean}}}}</td>'''.format(nom_champ)
            elif type_data == "DateTimeField":
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|date:"d/m/Y H:i"}}}}</td>'''.format(nom_champ)
            elif type_data == "DateField":
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|date:"d/m/Y"}}}}</td>'''.format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
                textebcl = textebcl + '''
                    <td>{{{{ item.value_{0} }}}}</td>'''.format(nom_champ)
            else :
                textebcl = textebcl + '''
                    <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)

    texteTemplate = texteTemplate + textebcl

    texteTemplate = texteTemplate + '''
                    <td>{{item.creation_date|date:'d/m/Y'}}</td>
                    <td>{{item.auteur.nom_complet}}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
</html>
'''
    fichier.write(texteTemplate)
    fichier.close()


    # CRUD AND URLS URLS
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\urls.py".format(nomModule)
    fichier = codecs.open(utils.format_path(path),"a", encoding='utf-8')

    texte_a_ajouter_urls_py_dossier_ap= "\n#{2} REPORTING URLS\nurlpatterns.append(url(r'^{0}/generate', views.get_generer_{0}, name = '{1}_get_generer_{0}'))".format(nom_modele.lower(),nom_pattern, nom_modele.upper())
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/post_generate', views.post_generer_{0}, name = '{1}_post_generer_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/excel_generate', views.post_excel_rapport_{0}, name = '{1}_post_excel_rapport_{0}'))\n".format(nom_modele.lower(),nom_pattern)
    fichier.write(texte_a_ajouter_urls_py_dossier_ap)
    fichier.close()
    return url_name_reporting   

def genBIOfContentType(content_type_id, module_id):
    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()
    module = dao_module.toGetModule(module_id)
    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__
    nomdao = "dao_{0}".format(nom_modele.lower())
    nom_pattern = 'module_{0}'.format(unidecode.unidecode(module.nom_module.lower().replace(" ","_")))
    nomModule = module.nom_application
    
    url_name_bi = "{1}_bi_{0}".format(nom_modele.lower(),nom_pattern)
    url_name_reporting = "{1}_get_generer_{0}".format(nom_modele.lower(),nom_pattern)
        
    list_champs = [] 
    for field in model_class._meta.get_fields(): 
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): list_champs.append(field) 
        
    # CREATION FONCTIONS BI DANS views.py
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\views.py".format(nomModule)
    fichier = codecs.open(utils.format_path(path), "a", encoding='utf-8')

    # GET BI
    texte_a_ajouter_views_py = "\n\n# {2} BI CONTROLLERS\ndef get_bi_{0}(request):\n\ttry:\n\t\tsame_perm_with = '{5}'\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)\n\t\tif response != None: return response\n\n\t\ttry:\n\t\t\tview = str(request.GET.get('view','table'))\n\t\texcept Exception as e:\n\t\t\tview = 'table'\n\n\t\t#*******Filtre sur les règles **********#\n\t\tmodel = auth.toListWithRules({1}.toList(), permission, groupe_permissions, utilisateur)\n\t\t#******* End Regle *******************#\n\n\t\tmodel = pagination.toGet(request, model, 100)\n\n\t\tmodel_content_type = dao_query_builder.toGetContentTypeByName('{6}')\n\t\tchamps = dao_query_builder.toListFieldOfModel(model_content_type.id)\n\t\tchamps_nombre = dao_query_builder.toListFieldsNombre(model_content_type.id)\n\t\tchamps_texte = dao_query_builder.toListFieldsTexte(model_content_type.id)\n\t\tchamps_date = dao_query_builder.toListFieldsDate(model_content_type.id)\n\n\t\tcontext = {{\n\t\t\t'title' : \"Analyse des {3}\",\n\t\t\t'model' : model,\n\t\t\t'model_id' : model_content_type.id,\n\t\t\t'modele' : {7}(),\n\t\t\t'champs' : champs,\n\t\t\t'champs_nombre' : champs_nombre,\n\t\t\t'champs_date' : champs_date,\n\t\t\t'champs_dimension' : champs_texte,\n\t\t\t'view' : view,\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'user_actions': actions,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation()\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{4}/{0}/bi.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose_plural.lower(),nomModule,url_name_reporting,nom_modele_class.lower(),nom_modele_class)
        
    fichier.write(texte_a_ajouter_views_py)
    fichier.close()

    # CREATION DES TEMPLATES BI DU MODELE
    # TEMPLATE BI
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    try:
        os.mkdir(utils.format_path(path))
    except Exception as e:
        pass
    path = path + "\\bi.html"
    fichier = codecs.open(utils.format_path(path),"w", encoding='utf-8')

    texteTemplate = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{% load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="leaf chargement-au-click" href="{{% url '{2}_index' %}}">Module {4}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>
<!-- Appel de la fonction message -->           
{{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>
<div class="panel panel-default" style="border: none;">
    <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;"> 

        {{% include 'ErpProject/ErpBackOffice/widget/bi_header_view.html' %}}

        <br><hr class="hr-ligne">
        
        <div class="row">
            <div class="col-md-9 col-xs-12">
                <!-- Button dropdown Filtre -->
                <button class="theme-btn-dropdown dropdown theme-btn theme-btn-sm rounded chargement-au-click" >
                    <a class="dropdown-toggle" style="text-decoration: none!important;" data-toggle="dropdown" href="#">
                        <i class="fa fa-filter"></i> Filtres <i class="fa fa-caret-down"></i>
                    </a>
                    <ul id="dropdown-filtre" class="dropdown-menu dropdown-user o_dropdown_menu">
                        <li><a href="#" data-id="filter_own" class="dropdown-item" data-selected="false" data-type="value" data-logic="OR" data-item="auteur_id" data-operateur="=" data-value="{{{{utilisateur.id}}}}"> Mes {7} </a></li>
                        <li class="divider"></li>
                        <li id="li-filtre-perso"><a href="#" id="toggle-filtre-perso" class="dropdown-item li-toggle" data-selected="false" data-show="false">Personnaliser <i class="fa fa-caret-right" style="margin-left: 3px;"></i></a></li>
                        <div id="filtre-perso" class="div-toggle">
                        </div>
                    </ul>
                </button>
                {{% if view == "table" %}}
                <!-- Button dropdown Grouper -->
                <button class="theme-btn-dropdown dropdown theme-btn theme-btn-sm rounded chargement-au-click" >
                    <a class="dropdown-toggle" style="text-decoration: none!important;" data-toggle="dropdown" href="#">
                        <i class="fa fa-bars"></i> Regrouper par <i class="fa fa-caret-down"></i>
                    </a>
                    <ul id="dropdown-regrouper" class="dropdown-menu dropdown-user o_dropdown_menu">
                        <li><a href="#" id="regroupe_{5}" class="dropdown-item" data-selected="false" data-value="{5}" data-function="false"> {6} </a></li>
                        <li class="divider"></li>
                        <li id="li-regrouper-perso"><a href="#" id="toggle-regrouper-perso" class="dropdown-item li-toggle" data-selected="false" data-show="false">Personnaliser <i class="fa fa-caret-right" style="margin-left: 3px;"></i></a></li>
                        <div id="regrouper-perso" class="div-toggle">
                        </div>
                    </ul>
                </button>
                {{% endif %}}
                <!-- Buttons dropdown Temps and Favoris -->
                {{% include 'ErpProject/ErpBackOffice/widget/bi_temps_favoris_view.html' %}}
            </div>
            <div class="col-md-3 col-xs-12">
                <div id="btn-view" data-role="group" data-group-type="one-state">
                    <button id="btn-table" onclick="javascript:window.location.assign('{{% url '{2}_bi_{3}' %}}?view=table')" class="button btn-typeview btn-secondary {{% if view == "table" %}}{{{{ "active" }}}}{{% endif %}}"><span class="mif-list"></span></button>
                    <button id="btn-chart" onclick="javascript:window.location.assign('{{% url '{2}_bi_{3}' %}}?view=chart')" class="button btn-typeview btn-secondary {{% if view == "chart" %}}{{{{ "active" }}}}{{% endif %}}"><span class="mif-chart-dots"></span></button>
                    <button id="btn-card" onclick="javascript:window.location.assign('{{% url '{2}_bi_{3}' %}}?view=card')" class="button btn-typeview btn-secondary {{% if view == "card" %}}{{{{ "active" }}}}{{% endif %}}"><span class="mif-apps"></span></button>
                    <button id="btn-pivot" onclick="javascript:window.location.assign('{{% url '{2}_bi_{3}' %}}?view=pivot')" class="button btn-typeview btn-secondary {{% if view == "pivot" %}}{{{{ "active" }}}}{{% endif %}}"><span class="mif-table"></span></button>
                </div>
            </div>
        </div>
        <hr class="hr-ligne">
        <div id="divToPrint" class="row item-content" style="margin-top: 20px" style="padding-top: 30px">
            <div class="col-lg-12">
                <p class="align-center header">{{{{ title }}}}</p>
                {{% if view == "table" %}}
                <div id="list-view" class="row" style="margin-top: 10px;overflow: auto; position: relative; display: inline-block;">        
                    <table id="default-table" class="table nowrap border bordered striped" cellspacing="0" style="width:100%">
                        <thead>
                            <tr>'''.format(nomModule, unidecode.unidecode(module.nom_module.lower().replace(" ","_")), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), list_champs[0].name, list_champs[0].verbose_name, nom_modele_verbose_plural)
    textebcl=""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            textebcl = textebcl + '''
                                <th class="head">{0}</th>'''.format(nom_champ_verbose)
    textebcl = textebcl + '''
                                <th class="head">Date de création</th>
                                <th class="head">Créé par</th>'''
    texteTemplate = texteTemplate + textebcl

    texteTemplate= texteTemplate + '''
                            </tr>
                        </thead>
                        <tbody>
                            {{% for item in model %}}
                            <tr>
                                <td>
                                    <a class="lien chargement-au-click" href="{{% url '{0}_detail_{1}' item.id %}}{{% if isPopup %}}?isPopup=1{{% endif %}}">{{{{ item.{2} }}}}</a>
                                </td>'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)

    textebcl = ""
    for i in range(1,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__) 
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField", "TextField"):
            if type_data == "FloatField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|monetary}}}}</td>'''.format(nom_champ)
            elif type_data == "CharField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
            elif type_data == "IntegerField" and list_champs[i].choices == None:
                textebcl = textebcl + '''
                                <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)
            elif type_data == "BooleanField":
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|boolean}}}}</td>'''.format(nom_champ)
            elif type_data == "DateTimeField":
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|date:"d/m/Y H:i"}}}}</td>'''.format(nom_champ)
            elif type_data == "DateField":
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|date:"d/m/Y"}}}}</td>'''.format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and list_champs[i].choices != None:
                if type_data == "CharField":
                    textebcl = textebcl + '''
                                <td>{{{{item.value_{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
                elif type_data == "IntegerField":
                    textebcl = textebcl + '''
                                <td>{{{{item.value_{0}}}}}</td>'''.format(nom_champ)
                elif type_data == "FloatField":
                    textebcl = textebcl + '''
                                <td>{{{{item.value_{0}|monetary}}}}</td>'''.format(nom_champ)
            else :
                textebcl = textebcl + '''
                                <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)

    texteTemplate = texteTemplate + textebcl

    texteTemplate = texteTemplate + '''
                                <td>{{{{item.creation_date|date:'d/m/Y'}}}}</td>
                                <td>{{{{item.auteur.nom_complet}}}}</td>
                            </tr>
                            {{% endfor %}}
                        </tbody>
                    </table>
                </div>
                
                {{% elif view == "chart" %}}
                <div id="chart-view" style="margin-top: 10px;">
                    <div class="row">
                        <div class="col-md-6" style="padding-top: 15px!important;" id="show-pie-chart">
                            <div class="card-item" style="background-color: white;padding: 0!important;margin-bottom: 2%;">
                                <div class="" style="height: 5px;background-color:#ACE5FE;"></div>
                                <div class="row">
                                    <!-- Show Pie Chart -->
                                    <div class="col-md-12">
                                        <div style="width: 600px;height: 500px;text-align:center;margin: auto;"> 
                                            <p id="title-chart"></p>
                                            <canvas id="pie-chart" height="400"></canvas>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-6" style="padding-top: 15px!important;" id="show-line-chart">
                            <div class="card-item" style="background-color: white;padding: 0!important;margin-bottom: 2%;">
                                <div class="" style="height: 5px;background-color:#ACE5FE;"></div>
                                <div class="row">
                                    <!-- Show Line Chart -->
                                    <div class="col-md-12">
                                        <div style="width: 750px;height: 400px;text-align:center;margin: auto;"> 
                                            <p id="title-chart"></p>
                                            <canvas id="line-chart" height="400"></canvas>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-12 show-bar-chart" style="padding-top: 15px!important;">
                            <div class="card-item" style="background-color: white;padding: 0!important;margin-bottom: 2%;">
                                <div class="" style="height: 5px;background-color:#ACE5FE;"></div>
                                <div class="row">
                                    <!-- Show Bar Chart -->
                                    <div class="col-md-12">
                                        <div style="width: 700px;height: 400px;text-align:center;margin: auto;"> 
                                            <p id="title-chart"></p>
                                            <canvas id="bar-chart"></canvas>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12 show-bar-chart" style="padding-top: 15px!important;">
                            <div class="card-item" style="background-color: white;padding: 0!important;margin-bottom: 2%;">
                                <div class="" style="height: 5px;background-color:#ACE5FE;"></div>
                                <div class="row">
                                    <!-- Show Dough Chart -->
                                    <div class="col-md-12">
                                        <div style="width: 700px;height: 400px;text-align:center;margin: auto;"> 
                                            <p id="title-chart"></p>
                                            <canvas id="horizontalbar-chart"></canvas>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="show-more-chart" class="row" style="margin-top: 10px;overflow: auto; position: relative; display: inline-block;"> 
                    <!-- More Chart -->
                    <div id="more-chart"></div>
                </div>
                {{% elif view == "card" %}}
                <div id="card-view" class="row" style="margin-top: 10px;overflow: auto; position: relative; display: inline-block;">
                    <!-- Show Card -->
                    <div class="row" id="show-card">
                        <div class="col-md-4">
                        </div>
                        <div class="col-md-4">
                            <div class="panel panel-success p3" style="border-radius: 0px;border-bottom: none;">
                                <div class="panel-heading" style="background-color: transparent;color: white;">
                                    <div class="row">
                                        <div class="col-xs-7 text-left">
                                            <div id="title_card" class="" style=""></div>
                                            <p id="value_card" style="font-weight: 800;font-size: 25px;font-family: 'Poppins Bold'"></p>
                                        </div>
                                        <div class="col-xs-3 text-right fond">
                                            <span class="mif-stack" style="float: left;font-size:25px"></span>
                                        </div>
                                        <br><br>
                                        <div>
                                            <p style="float: left;font-size:80%;color:#fff;"></p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                        </div>
                    </div>
                </div>
                {{% elif view == "pivot" %}}           
                <div id="pivot-view" class="row" style="margin-top: 10px;overflow: auto; position: relative; display: inline-block;"> 
                    <!-- Show Pivot -->
                    <div id="pivot_output" style="margin: 30px;"></div>
                </div>
                {{% endif %}}
            </div>
        </div>
    </div>
</div>

{{% include 'ErpProject/ErpBackOffice/widget/bi_view.html' %}}
{{% endblock %}}
'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)
    fichier.write(texteTemplate)
    fichier.close()

    # CRUD AND URLS URLS
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\urls.py".format(nomModule)
    fichier = codecs.open(utils.format_path(path),"a", encoding='utf-8')

    texte_a_ajouter_urls_py_dossier_ap= "\n#{2} BI URLS\nurlpatterns.append(url(r'^{0}/bi', views.get_bi_{0}, name = '{1}_bi_{0}'))\n".format(nom_modele.lower(),nom_pattern, nom_modele.upper())
    fichier.write(texte_a_ajouter_urls_py_dossier_ap)
    fichier.close()
    return url_name_bi  

def genAPIOfContentType(content_type_id, module_id):
    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()
    module = dao_module.toGetModule(module_id)
    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__
    nomdao = "dao_{0}".format(nom_modele.lower())
    nom_pattern = 'module_{0}'.format(unidecode.unidecode(module.nom_module.lower().replace(" ","_")))
    nomModule = module.nom_application
    
    list_champs = [] 
    for field in model_class._meta.get_fields(): 
        #if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by") and field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): list_champs.append(field) 
        if field.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"): list_champs.append(field) 
        
    # CREATION FONCTIONS API DANS views.py
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\views.py".format(nomModule)
    fichier = codecs.open(utils.format_path(path),"a", encoding='utf-8')

    # API GET LIST
    texte_a_ajouter_views_py = "\n\n# {2} API CONTROLLERS\ndef get_list_{0}(request):\n\ttry:\n\t\tcontext = {{}}\n\t\t#token = request.META.get('HTTP_TOKEN')\n\t\t#if not token: raise Exception('Erreur, Token manquant')\n\n\t\tfiltered = False\n\t\tif 'filtered' in request.GET : filtered = str(request.GET['filtered'])\n\t\tdate_from = None\n\t\tif 'date_from' in request.GET : date_from = request.GET['date_from']\n\t\tdate_to = None\n\t\tif 'date_to' in request.GET : date_to = request.GET['date_to']\n\t\tquery = ''\n\t\tif 'query' in request.GET : query = str(request.GET['query'])\n\n\t\tlistes = []\n\t\tmodel = dao_{0}.toList()\n\t\t#model = pagination.toGet(request, model)\n\n\t\tfor item in model:\n\t\t\telement = {{".format(nom_modele.lower(), nomdao, nom_modele.upper(), nom_modele_verbose.lower(),nomModule)

    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Attribution des champs
        if type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}_id' : makeIntId(item.{0}_id),".format(nom_champ)
            elif type_data == "DateTimeField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "DateField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "FloatField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : makeFloat(item.{0}),".format(nom_champ)
            elif type_data == "BooleanField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "EmailField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(item.{0}),".format(nom_champ)
            elif type_data == "CharField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(item.{0}),".format(nom_champ)
            elif type_data == "TextField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(item.{0}),".format(nom_champ)
            elif type_data == "IntegerField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : makeInt(item.{0}),".format(nom_champ)
            elif type_data in ("ImageField", "FileField"): 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0}.url if item.{0} != None else None,".format(nom_champ)
            else:
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0},".format(nom_champ)

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t}\n\t\t\tlistes.append(element)"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tcontext = {{\n\t\t\t'error' : False,\n\t\t\t'message' : 'Liste récupérée',\n\t\t\t'datas' : listes\n\t\t}}\n\t\treturn JsonResponse(context, safe=False)\n\texcept Exception as e:\n\t\treturn auth.toReturnApiFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)

    # API GET ITEM
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef get_item_{0}(request):\n\ttry:\n\t\tcontext = {{}}\n\t\t#token = request.META.get('HTTP_TOKEN')\n\t\t#if not token: raise Exception('Erreur, Token manquant')\n\n\t\tid = 0\n\t\tif 'id' in request.GET : id = int(request.GET['id'])\n\n\t\titem = {{}}\n\t\tmodel = dao_{0}.toGet(id)\n\t\tif model != None :\n\t\t\titem = {{".format(nom_modele.lower(), nomdao, nom_modele.upper(), nom_modele_verbose.lower(),nomModule)

    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Attribution des champs
        if type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}_id' : makeIntId(model.{0}_id),".format(nom_champ)
            elif type_data == "DateTimeField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0},".format(nom_champ)
            elif type_data == "DateField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0},".format(nom_champ)
            elif type_data == "FloatField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : makeFloat(model.{0}),".format(nom_champ)
            elif type_data == "BooleanField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0},".format(nom_champ)
            elif type_data == "EmailField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(model.{0}),".format(nom_champ)
            elif type_data == "CharField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(model.{0}),".format(nom_champ)
            elif type_data == "TextField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(model.{0}),".format(nom_champ)
            elif type_data == "IntegerField": 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : makeInt(model.{0}),".format(nom_champ)
            elif type_data in ("ImageField", "FileField"): 
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0}.url if model.{0} != None else None,".format(nom_champ)
            else:
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0},".format(nom_champ)

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t}"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tcontext = {{\n\t\t\t'error' : False,\n\t\t\t'message' : 'Objet récupéré',\n\t\t\t'item' : item\n\t\t}}\n\t\treturn JsonResponse(context, safe=False)\n\texcept Exception as e:\n\t\treturn auth.toReturnApiFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)


    # API POST CREATE
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n@api_view(['POST'])\n@transaction.atomic\ndef post_create_{0}(request):\n\tsid = transaction.savepoint()\n\ttry:\n\t\tcontext = {{}}\n\t\t#token = request.META.get('HTTP_TOKEN')\n\t\t#if not token: raise Exception('Erreur, Token manquant')\n".format(nom_modele.lower(), nomdao, nom_modele.upper(), nom_modele_verbose.lower(), nomModule)

    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        if nom_champ not in ("id", "statut", "etat", "creation_date", "update_date", "update_by"):         
            # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
            texte_check_nullable = ""          
            if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
                if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\tif {0}_id in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))
                else : texte_check_nullable = "\n\t\tif {0} in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', '', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name.replace("'", "\\'"))

            # Attribution des champs
            
            if type_data in ("ForeignKey", "OneToOneField"): 
                texte_boucle = texte_boucle + "\n\n\t\t{0}_id = None\n\t\tif '{0}' in request.POST : {0}_id = makeIntId(request.POST['{0}_id'])".format(nom_champ) + texte_check_nullable
            elif type_data == "ManyToManyField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = []".format(nom_champ)
            elif type_data == "DateTimeField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}']){1}\n\t\t{0} = timezone.datetime(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]), int({0}[11:13]), int({0}[14:16]))".format(nom_champ, texte_check_nullable)
            elif type_data == "DateField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}']){1}\n\t\t{0} = date(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]))".format(nom_champ, texte_check_nullable)
            elif type_data == "FloatField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = 0.0\n\t\tif '{0}' in request.POST : {0} = makeFloat(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data == "BooleanField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = True if '{0}' in request.POST else False".format(nom_champ)
            elif type_data == "EmailField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data == "CharField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data == "TextField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data == "IntegerField": 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = 0\n\t\tif '{0}' in request.POST : {0} = makeInt(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data in ("ImageField", "FileField"): 
                texte_boucle = texte_boucle + "\n\n\t\t{0} = request.FILES['{0}'] if '{0}' in request.FILES else None".format(nom_champ)
            else:
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = request.POST['{0}']".format(nom_champ)  + texte_check_nullable
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tauteur = dao_utilisateur.toGetUtilisateur(auteur_id)\n\n\t\t{0} = {1}.toCreate(".format(nom_modele.lower(), nomdao)
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis  
        check_nullable = True          
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False
                
        if nom_champ not in ("id", "statut", "etat", "creation_date", "update_date", "auteur", "update_by"): 
            if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
            text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
            #if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
            #else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
            
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + text_parenthese

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\tsaved, {0}, message = dao_{0}.toSave(auteur, {0})\n\n\t\tif saved == False: raise Exception(message)\n\n\t\tobjet = {{".format(nom_modele.lower())    

    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)  
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        # Attribution des champs
        if type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}_id' : makeIntId({1}.{0}_id),".format(nom_champ, nom_modele.lower())
            elif type_data == "DateTimeField": 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0},".format(nom_champ, nom_modele.lower())
            elif type_data == "DateField": 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0},".format(nom_champ, nom_modele.lower())
            elif type_data == "FloatField": 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : makeFloat({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data == "BooleanField": 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0},".format(nom_champ, nom_modele.lower())
            elif type_data == "EmailField": 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : str({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data == "CharField": 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : str({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data == "TextField": 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : str({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data == "IntegerField": 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : makeInt({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data in ("ImageField", "FileField"): 
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0}.url if {1}.{0} != None else None,".format(nom_champ, nom_modele.lower())
            else:
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0},".format(nom_champ, nom_modele.lower())
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t}\n\t\ttransaction.savepoint_commit(sid)"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tcontext = {{\n\t\t\t'error' : False,\n\t\t\t'message' : 'Enregistrement éffectué avec succès',\n\t\t\t'item' : objet\n\t\t}}\n\t\treturn JsonResponse(context, safe=False)\n\texcept Exception as e:\n\t\ttransaction.savepoint_rollback(sid)\n\t\treturn auth.toReturnApiFailed(request, e, traceback.format_exc())".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)
        
    fichier.write(texte_a_ajouter_views_py)
    fichier.close()


    # CRUD AND URLS URLS
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\urls.py".format(nomModule)
    fichier = codecs.open(utils.format_path(path),"a", encoding='utf-8')

    texte_a_ajouter_urls_py_dossier_ap= "\n#{2} API URLS\nurlpatterns.append(url(r'^api/{0}/list', views.get_list_{0}, name = '{1}_api_list_{0}'))".format(nom_modele.lower(), nom_pattern, nom_modele.upper())
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^api/{0}/item', views.get_item_{0}, name = '{1}_api_item_{0}'))".format(nom_modele.lower(), nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^api/{0}/create', views.post_create_{0}, name = '{1}_api_create_{0}'))\n".format(nom_modele.lower(), nom_pattern)
    fichier.write(texte_a_ajouter_urls_py_dossier_ap)
    fichier.close()
  
def getUrlVersOfRelatedModel(related_model):
    url_vers = ""
    try:
        related_model_ctype = ContentType.objects.get(model = related_model.lower())
        related_module = dao_module.toGetModuleByAppName(related_model_ctype.app_label) 
        if related_module != None:
            url_vers = related_module.url_vers.replace("/", "")
        elif related_model.lower() in ("model_devise","model_taux"): 
            url_vers = "comptabilite"
        elif related_model.lower() in ("model_civilite"): 
            url_vers = "vente"
        elif related_model.lower() in ("model_employe"): 
            url_vers = "ressourceshumaines"
        else: 
            url_vers = "configuration"
        return url_vers
    except Exception as e:
        return url_vers
    
def getUrlOfRelatedModel(related_model):
    nom_pattern = ""
    try:
        related_model_ctype = ContentType.objects.get(model = related_model.lower()) 
        related_module = dao_module.toGetModuleByAppName(related_model_ctype.app_label) 
        if related_module != None:
            nom_pattern = 'module_{0}'.format(unidecode.unidecode(related_module.nom_module.lower().replace(" ","_")))  
        elif related_model.lower() in ("model_devise","model_taux"): 
            nom_pattern = "module_comptabilite"
        elif related_model.lower() in ("model_civilite"): 
            nom_pattern = "module_vente"
        elif related_model.lower() in ("model_employe"): 
            nom_pattern = "module_ressources_humaines"
        else: 
            nom_pattern = "module_configuration"
        return nom_pattern
    except Exception as e:
        return nom_pattern