from ast import operator
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import connection
from datetime import time, timedelta, datetime, date
from django.conf import settings
#from .dao_query import dao_query

class dao_query_builder():

    def toListContentTypes():
        return ContentType.objects.filter(app_label = "ErpBackOffice")
    
    def toGetContentTypeByName(name):
        try:
            model_content_type = ContentType.objects.filter(model = name).first()
            return model_content_type       
        except Exception as e:
            return None
    
    def toListRelatedOfModel(model_id):
        #refaire
        result = []
        objet_modele = ContentType.objects.get(pk = model_id).model_class()
        for f in objet_modele._meta.get_fields():
            #print(f)
            modele = objet_modele._meta.get_field(f.name).related_model
            if f.model:
                try:
                    model_content_type = ContentType.objects.get_for_model(modele)
                    result.append(model_content_type)        
                except Exception as e:
                    pass
            
        return result

    def toListFieldOfModel(model_id):
        '''Fonction qui retourne les champs propres à un modèle. Cette fonction retourne un
        tuple comprenant le verbose name et le name du champ '''
        fields = []
        try:
            objet_modele = ContentType.objects.get(pk = model_id).model_class()
            #print(f"fields {objet_modele._meta.fields}")
            for f in objet_modele._meta.fields:
                #if not(isinstance(f,models.ForeignKey) or isinstance(f, models.ManyToManyField)):
                if f.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"):
                    choices = dao_query_builder.generate_list_choices(f.choices)
                    db_column = f.db_column
                    if db_column == None: 
                        db_column = f.name
                        if f.__class__.__name__ in ("ForeignKey", "OneToOneField"): db_column = f"{f.name}_id"
                    fields.append((f.name, db_column, f.verbose_name, f.__class__.__name__, choices))
            return fields
        except Exception as e:
            print(f"EX {e}")
            return fields 
        
    def toListFieldRelated(model_id, type = ""):
        '''Fonction qui retourne les champs propres à un modèle. Cette fonction retourne un
        tuple comprenant le verbose name et le name du champ '''
        fields = []
        try:
            objet_modele = ContentType.objects.get(pk = model_id).model_class()
            DB_ENGINE = "mssql"
            if "mysql" in settings.DATABASES["default"]["ENGINE"]: DB_ENGINE = "mysql" 
            DB_NAME = settings.DATABASES["default"]["NAME"]
            for f in objet_modele._meta.fields:
                model_table_name_rel = ""
                field_name_rel = ""
                fields_rel = []
                if f.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"):
                    if  f.__class__.__name__ in ('ForeignKey', 'OneToOneField') and f.related_model != None: 
                        related_model = f.related_model.__name__
                        model_content_ref_rel = ContentType.objects.filter(model = related_model.lower()).first()
                        model_class_rel = model_content_ref_rel.model_class()
                        model_table_name_rel = model_class_rel._meta.db_table
                        if DB_ENGINE == "mssql": model_table_name_rel = f"{DB_NAME}.dbo.{model_table_name_rel}"
                        #field_name_rel = model_class_rel._meta.fields[1].name
                        field_name_rel = model_class_rel._meta.fields[1].db_column
                        if field_name_rel == None: field_name_rel = model_class_rel._meta.fields[1].name
                        
                        fields_rel = []
                        #print(f"fields m {model_class_rel._meta.fields}")
                        for frel in model_class_rel._meta.fields:
                            if frel.__class__.__name__ not in ("ManyToOneRel", "ManyToManyRel"):
                                choices = dao_query_builder.generate_list_choices(frel.choices)
                                #fields_rel.append((frel.name, frel.verbose_name, frel.__class__.__name__, choices))
                                frel_name = frel.name
                                if frel.__class__.__name__ in ("ForeignKey", "OneToOneField"): frel_name = f"{frel.name}_id"
                             
                                f_name_rel = frel.db_column
                                if f_name_rel == None: f_name_rel = frel_name
                                if type == "wkf":
                                    f_name_rel = frel_name
                                                                    
                                fields_rel.append((f_name_rel, frel.verbose_name, frel.__class__.__name__, choices))
                    db_column = f.db_column
                    if db_column == None: db_column = f.name            
                    fields.append((f.name, db_column, f.__class__.__name__, model_table_name_rel, field_name_rel, fields_rel))
            return fields
        except Exception as e:
            print(f"EX {e}")
            return fields
        
    def toListFieldsNombre(model_id):
        '''Fonction qui retourne les champs propres à un modèle qui peuvent être mesurés. Cette fonction retourne un
        tuple comprenant le verbose name et le name du champ '''
        fields = []
        try:
            objet_modele = ContentType.objects.get(pk = model_id).model_class()
            for f in objet_modele._meta.fields:
                if f.__class__.__name__ in ("IntegerField", "FloatField"):
                    db_column = f.db_column
                    if db_column == None: db_column = f.name
                    fields.append((f.name, db_column, f.verbose_name))
            return fields
        except Exception as e:
            return fields 
        
    def toListFieldsTexte(model_id):
        '''Fonction qui retourne les champs propres à un modèle qui sont de type texte. Cette fonction retourne un
        tuple comprenant le verbose name et le name du champ '''
        fields = []
        try:
            objet_modele = ContentType.objects.get(pk = model_id).model_class()
            for f in objet_modele._meta.fields:
                if f.__class__.__name__ in ("CharField", "EmailField"):
                    db_column = f.db_column
                    if db_column == None: db_column = f.name
                    fields.append((f.name, db_column, f.verbose_name))
            return fields
        except Exception as e:
            return fields 

    def toListFieldsDate(model_id):
        '''Fonction qui retourne les champs propres à un modèle qui sont des dates. Cette fonction retourne un
        tuple comprenant le verbose name et le name du champ '''
        fields = []
        try:
            objet_modele = ContentType.objects.get(pk = model_id).model_class()
            for f in objet_modele._meta.fields:
                if f.__class__.__name__ in ("DateTimeField", "DateField"):
                    db_column = f.db_column
                    if db_column == None: db_column = f.name
                    fields.append((f.name, db_column, f.verbose_name))
            return fields
        except Exception as e:
            return fields
           
    def toPerformQueryForTable(auteur, model_id, champs_afficher, filter_logic, filter_item, \
                        filter_operateur, filter_valeur, regrouper_item =[], regroupe_elements = None, plage_item = [], plage_valeur = [], order_by = "", order_sens = "", limit = "" ):
        '''Fonction qui se charge de creer la requete en fonction des valeurs saisies et
        creer un objet Query qu'il enregistre dans la BD. 
        Il s'agit d'une création manuelle flexible d'un script SQL.        
        '''
        try:
            DB_ENGINE = "mssql"
            if "mysql" in settings.DATABASES["default"]["ENGINE"]: DB_ENGINE = "mysql" 
            DB_NAME = settings.DATABASES["default"]["NAME"]
            main_modele_id = model_id
            #recuperation du modele de l'objet à partir de l'identifiant du content type
            model_content_ref = ContentType.objects.get(pk = main_modele_id)          
            model_class = model_content_ref.model_class()
            nom_modele = model_content_ref.model.replace("model_","").capitalize()
            nom_modele_verbose = model_class._meta.verbose_name
            nom_modele_verbose_plural = model_class._meta.verbose_name_plural
            model_table_name = model_class._meta.db_table
            if DB_ENGINE == "mssql": model_table_name = f"{DB_NAME}.dbo.{model_table_name}"
            #model_table_name = f"{model_content_ref.app_label}_{model_content_ref.model}" 
            nom_modele_class = model_class.__name__
            
            query_sql = "SELECT "
            if DB_ENGINE == "mssql":
                if limit != "all": query_sql += f"TOP {limit} "
                limit = ""
            select = ""
            filter = ""
            group_by = ""
            plage = ""
            select_fields = []
            champs = dao_query_builder.toListFieldRelated(model_id)            

            #recuperation du modele reliés
            joints = ""
            #Pour gérer les tables doublons dans les jointures
            tables_joints = [] 
            letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
            i = 0
            for field in model_class._meta.fields: 
                if  field.__class__.__name__ in ('ForeignKey', 'OneToOneField') and field.related_model != None: 
                    i += 1
                    related_model = field.related_model.__name__
                    model_content_ref_rel = ContentType.objects.filter(model = related_model.lower()).first()
                    model_class_rel = model_content_ref_rel.model_class()
                    if DB_ENGINE == "mysql":
                        model_table_name_rel = model_class_rel._meta.db_table
                        joints += f" LEFT JOIN `{model_table_name_rel}` ON (`{model_table_name}`.`{field.db_column}` = `{model_table_name_rel}`.`id`)"
                    elif DB_ENGINE == "mssql": 
                        model_table_name_rel = f"{DB_NAME}.dbo.{model_class_rel._meta.db_table}"
                        if model_class_rel._meta.db_table not in tables_joints:  
                            joints += f" LEFT JOIN {model_table_name_rel} ON ({model_table_name}.{field.db_column} = {model_table_name_rel}.id)"
                            tables_joints.append(model_class_rel._meta.db_table)
                        else:
                            joints += f" LEFT JOIN {model_table_name_rel} AS {letter[i]} ON ({model_table_name}.{field.db_column} = {letter[i]}.id)"
                                    
            #SELECT, GROUPBY
            var_select_group_by = "" 
            if regroupe_elements != None: 
                regr_el = regroupe_elements.split(";;")
                regr_value = regr_el[1]
            if regrouper_item == [] or regroupe_elements != None:
                if champs_afficher:
                    for name, db_name, type, table, field_name, fields in champs:
                        nom_champs = db_name
                        #if db_name == None: nom_champs = "id"
                        if type in ('ForeignKey', 'OneToOneField'): name = name + "_id"
                        if name in champs_afficher:
                            if type in ('ForeignKey', 'OneToOneField'): 
                                select_fields.append(f"{table}.{field_name}")
                            else: select_fields.append(f"{model_table_name}.{nom_champs}")                
                    
                    for obj in select_fields:
                        select += f"{obj},"
                    select = select[:-1] #On enleve la dernière virgule
                else:
                    select = "* "
            if regrouper_item != []:
                regrouper = regrouper_item.split(";")   
                select_group_by = "" 
                group_by = ""
                for name, db_name, type, table, field_name, fields in champs:
                    if name == regrouper[0]:
                        nom_champs = db_name
                        #if db_name == None: nom_champs = "id"
                        if type in ('ForeignKey', 'OneToOneField'): 
                            name = name + "_id"
                            var_select_group_by = f"{table}.{field_name}"
                            select_group_by = f"{table}.{field_name}, COUNT(*)"
                            group_by = f" GROUP BY {table}.id"
                        elif len(regrouper) > 1: 
                            funct = regrouper[1].upper()
                            if funct == "DATE":
                                if DB_ENGINE == "mysql":
                                    var_select_group_by = f'DATE_FORMAT({model_table_name}.{nom_champs}, "%d/%m/%Y")'
                                    select_group_by = f'DATE_FORMAT({model_table_name}.{nom_champs}, "%d/%m/%Y"), COUNT(*)'
                                    group_by = f' GROUP BY DATE_FORMAT({model_table_name}.{nom_champs}, "%d/%m/%Y")'
                                elif DB_ENGINE == "mssql": 
                                    var_select_group_by = f"FORMAT({model_table_name}.{nom_champs}, 'dd/MM/yyyy')"
                                    select_group_by = f"FORMAT({model_table_name}.{nom_champs}, 'dd/MM/yyyy'), COUNT(*)"
                                    group_by = f" GROUP BY FORMAT({model_table_name}.{nom_champs}, 'dd/MM/yyyy')"                                   
                            elif funct == "MONTH":
                                if DB_ENGINE == "mysql":
                                    var_select_group_by = f'DATE_FORMAT({model_table_name}.{nom_champs}, "%M %Y")'
                                    select_group_by = f'DATE_FORMAT({model_table_name}.{nom_champs}, "%M %Y"), COUNT(*)'
                                    group_by = f" GROUP BY {funct}({model_table_name}.{nom_champs})"
                                elif DB_ENGINE == "mssql": 
                                    var_select_group_by = f"FORMAT({model_table_name}.{nom_champs}, 'MMMM yyyy', 'fr-FR')"
                                    select_group_by = f"FORMAT({model_table_name}.{nom_champs}, 'MMMM yyyy', 'fr-FR'), COUNT(*)"
                                    group_by = f" GROUP BY FORMAT({model_table_name}.{nom_champs}, 'MMMM yyyy', 'fr-FR')"                                    
                            else:
                                var_select_group_by = f"{funct}({model_table_name}.{nom_champs})"
                                select_group_by = f"{funct}({model_table_name}.{nom_champs}), COUNT(*)"
                                group_by = f" GROUP BY {funct}({model_table_name}.{nom_champs})"
                        else: 
                            var_select_group_by = f"{model_table_name}.{nom_champs}"
                            select_group_by = f"{model_table_name}.{nom_champs}, COUNT(*)"
                            group_by = f" GROUP BY {model_table_name}.{nom_champs}" 
                        break
                if regroupe_elements == None: select = select_group_by
                else: group_by = ""
                

            #PLAGE                                  
            if plage_item != []:
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if plage_valeur == "last_7days":
                    #Les 7 derniers jours
                    last_7days = today + timedelta(days=-7)
                    date_debut = last_7days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "last_30days":
                    #Les 30 derniers jours 
                    last_30days = today + timedelta(days=-30)
                    date_debut = last_30days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_365days":                    
                    #Dernier 365 jours
                    last_365days = today + timedelta(days=-365)
                    date_debut = last_365days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "today":
                    #Aujourd'hui
                    date = today.strftime('%d/%m/%Y')
                    if DB_ENGINE == "mysql":
                        plage = f"DATE_FORMAT({model_table_name}.{plage_item}, '%d/%m/%Y') = '{date}'"
                    elif DB_ENGINE == "mssql": 
                       plage = f"FORMAT({model_table_name}.{plage_item}, 'dd/MM/yyyy') = '{date}'" 
                elif plage_valeur == "this_week":
                    #Cette semaine 
                    day_of_week = int(today.strftime('%w'))
                    first_day_of_week = today + timedelta(days=-day_of_week+1)
                    end_week = first_day_of_week + timedelta(days=6)
                    date_debut = first_day_of_week.strftime('%Y/%m/%d')
                    date_fin = end_week.strftime('%Y/%m/%d')
                                        
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "this_month":
                    #Ce mois
                    this_month = int(today.strftime('%m'))
                    next_month = this_month + 1 
                    first_day_this_month = today.replace(day=1)                    
                    if next_month == 13:
                        next_year = int(today.strftime('%Y')) + 1
                        first_day_next_month = today.replace(day=1, month=1, year=next_year)
                    else: first_day_next_month = today.replace(day=1, month=next_month)
                    last_day_this_month = first_day_next_month - timedelta(days=1)
                    date_debut = first_day_this_month.strftime('%Y/%m/%d')
                    date_fin = last_day_this_month.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "this_quarter": 
                    #Ce trimestre
                    this_month = int(today.strftime('%m'))
                    if this_month >= 1 and this_month <= 3:
                        first_day_this_quarter = today.replace(day=1, month=1)
                        last_day_this_quarter = today.replace(day=31, month=3)
                    elif this_month >= 4 and this_month <= 6:
                        first_day_this_quarter = today.replace(day=1, month=4)
                        last_day_this_quarter = today.replace(day=30, month=6)
                    elif this_month >= 7 and this_month <= 9:
                        first_day_this_quarter = today.replace(day=1, month=7)
                        last_day_this_quarter = today.replace(day=30, month=9)
                    elif this_month >= 10 and this_month <= 12:
                        first_day_this_quarter = today.replace(day=1, month=10)
                        last_day_this_quarter = today.replace(day=31, month=12)
                    date_debut = first_day_this_quarter.strftime('%Y/%m/%d')
                    date_fin = last_day_this_quarter.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "this_year": 
                    #Cette année                    this_month = int(today.strftime('%m'))
                    first_day_this_year = today.replace(day=1, month=1)
                    last_day_this_year = today.replace(day=31, month=12)
                    date_debut = first_day_this_year.strftime('%Y/%m/%d')
                    date_fin = last_day_this_year.strftime('%Y/%m/%d')

                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "yesterday": 
                    #Hier
                    yesterday = today - timedelta(days=1)
                    date = yesterday.strftime('%d/%m/%Y')
                    if DB_ENGINE == "mysql":
                        plage = f"DATE_FORMAT({model_table_name}.{plage_item}, '%d/%m/%Y') = '{date}'"
                    elif DB_ENGINE == "mssql": 
                        plage = f"FORMAT({model_table_name}.{plage_item}, 'dd/MM/yyyy') = '{date}'"
                elif plage_valeur == "last_week": 
                    #La semaine dernière
                    day_of_week = int(today.strftime('%w'))
                    first_day_of_week = today + timedelta(days=-day_of_week+1)
                    first_day_of_last_week = first_day_of_week + timedelta(days=-7)
                    last_day_of_last_week = first_day_of_week + timedelta(days=-1)
                    date_debut = first_day_of_last_week.strftime('%Y/%m/%d')
                    date_fin = last_day_of_last_week.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "last_month": 
                    #Le mois dernier
                    first_day_this_month = today.replace(day=1)
                    last_day_last_month = first_day_this_month - timedelta(days=1)
                    first_day_last_month = last_day_last_month.replace(day=1)
                    date_debut = first_day_last_month.strftime('%Y/%m/%d')
                    date_fin = last_day_last_month.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_quarter": 
                    #dernier trimestre
                    this_month = int(today.strftime('%m'))
                    if this_month >= 1 and this_month <= 3:
                        this_quarter = "Q1"
                    elif this_month >= 4 and this_month <= 6:
                        this_quarter = "Q2"
                    elif this_month >= 7 and this_month <= 9:
                        this_quarter = "Q3"
                    elif this_month >= 10 and this_month <= 12:
                        this_quarter = "Q4"

                    if this_quarter == "Q1":
                        last_year = int(today.strftime('%Y')) - 1
                        first_day_last_quarter = today.replace(day=1, month=1, year=last_year)
                        last_day_last_quarter = today.replace(day=31, month=3, year=last_year)
                    elif this_quarter == "Q2":
                        first_day_last_quarter = today.replace(day=1, month=1)
                        last_day_last_quarter = today.replace(day=31, month=3)
                    elif this_quarter == "Q3":
                        first_day_last_quarter = today.replace(day=1, month=4)
                        last_day_last_quarter = today.replace(day=30, month=6)
                    elif this_quarter == "Q4":
                        first_day_last_quarter = today.replace(day=1, month=7)
                        last_day_last_quarter = today.replace(day=30, month=9)
                    date_debut = first_day_last_quarter.strftime('%Y/%m/%d')
                    date_fin = last_day_last_quarter.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_year": 
                    #L'année dernière
                    last_year = int(today.strftime('%Y')) - 1
                    first_day_last_year = today.replace(day=1, month=1, year=last_year)
                    last_day_last_year = today.replace(day=31, month=12, year=last_year)
                    date_debut = first_day_last_year.strftime('%Y/%m/%d')
                    date_fin = last_day_last_year.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                
            #FILTRE                                  
            if filter_item:
                filter += " WHERE "
                for i in range(len(filter_item)):
                    if filter_logic: #On sarrete pr l'instant à une ligne (on doit gerer après les AND OR xx)
                        if i > 0: #On saute la premiere iteration pour equilibrer les tailles 
                            filter += f' {filter_logic[i]} ' 
                    filter_comparison = f"{filter_operateur[i]} '{filter_valeur[i]}'"
                    if filter_operateur[i] == "contient":
                        filter_comparison = f"LIKE '%{filter_valeur[i]}%'"
                    elif filter_operateur[i] == "contient_pas": 
                        filter_comparison = f"NOT LIKE '%{filter_valeur[i]}%'" 
                    elif filter_operateur[i] == "defini": 
                        filter_comparison = f"IS NOT NULL"
                    elif filter_operateur[i] == "pas_defini": 
                        filter_comparison = f"IS NULL"
                    elif filter_operateur[i] == "vrai": 
                        filter_comparison = f"= True"
                    elif filter_operateur[i] == "faux": 
                        filter_comparison = f"= False" 
                    else: filter_comparison = f"{filter_operateur[i]} '{filter_valeur[i]}'"
                    
                    f_item = filter_item[i].split(";")
                    #Si champs non relationel    
                    if f_item[0].find(".") != -1:
                        filt = f"{f_item[0]}"
                    else: 
                        filt = f"{model_table_name}.{f_item[0]}"
                    
                    #Si type est une date    
                    if len(f_item) > 1:
                        funct = f_item[1].upper()
                        if funct == "DATE":
                            if DB_ENGINE == "mysql":
                                filter += f'DATE_FORMAT({filt}, "%d/%m/%Y") {filter_comparison}'
                            elif DB_ENGINE == "mssql": filter += f"FORMAT({filt}, 'dd/MM/yyyy') {filter_comparison}"
                        elif funct == "MONTH":
                            if DB_ENGINE == "mysql":
                                filter += f'DATE_FORMAT({filt}, "%m/%Y") {filter_comparison}'
                            elif DB_ENGINE == "mssql": filter += f"FORMAT({filt}, 'MM/yyyy') {filter_comparison}"
                        else:
                            filter += f'YEAR({filt}) {filter_comparison}'
                    else: 
                        filter += f"{filt} {filter_comparison}"
                #S'il ya des filter et une requete plage
                if plage_item != []:
                    filter += f" AND {plage}"        
                #S'il ya des filter et on a groupé
                if regroupe_elements != None: 
                    regr_el = regroupe_elements.split(";;")
                    regr_value = regr_el[1]
                    filter += f" AND {var_select_group_by} = '{regr_value}'"
            #S'il ya pas des filter et on a groupé        
            elif filter_item == [] and regroupe_elements != None: 
                if plage_item != []: plage = f"{plage} AND "
                filter += f" WHERE {plage}{var_select_group_by} = '{regr_value}'"  
            elif filter_item == [] and regroupe_elements == None and plage_item != []:
                filter += f" WHERE {plage}"                          

                                        
            query_sql += select                          
            if DB_ENGINE == "mysql": query_sql += f" FROM `{model_table_name}` " 
            elif DB_ENGINE == "mssql": query_sql += f" FROM {model_table_name} " 
            query_sql += joints           
            query_sql += filter
            query_sql += group_by
            
            if DB_ENGINE == "mysql": 
                if limit == "all": limit = ""
                else: limit = f"LIMIT {limit}"
            
            if regrouper_item != []: query_sql += f" {limit}" 
            else : query_sql += f" ORDER BY {model_table_name}.{order_by} {order_sens} {limit}"                                   
            print(query_sql)
            
            result_row = dao_query_builder.my_custom_sql(query_sql) if query_sql else [] #Si requete non vide, then run
            return result_row, query_sql
        except Exception as e:
            print("Error on toPerformQueryForTable", e) 
            return []  
        
    def toPerformQueryForChart(auteur, model_id, champs_afficher, measure_function = "", measure_attribute = "", dimension = "", filter_logic = [], filter_item = [], \
                        filter_operateur = [], filter_valeur = [], chart_type =0, plage_item = [], plage_valeur = [], order_by = "", order_sens = "", limit = "" ):
        '''Fonction qui se charge de creer la requete en fonction des valeurs saisies et
        creer un objet Query qu'il enregistre dans la BD. 
        Il s'agit d'une création manuelle flexible d'un script SQL.        
        '''
        try:
            DB_ENGINE = "mssql"
            if "mysql" in settings.DATABASES["default"]["ENGINE"]: DB_ENGINE = "mysql" 
            DB_NAME = settings.DATABASES["default"]["NAME"]
            main_modele_id = model_id
            #recuperation du modele de l'objet à partir de l'identifiant du content type
            model_content_ref = ContentType.objects.get(pk = main_modele_id)          
            model_class = model_content_ref.model_class()
            nom_modele = model_content_ref.model.replace("model_","").capitalize()
            nom_modele_verbose = model_class._meta.verbose_name
            nom_modele_verbose_plural = model_class._meta.verbose_name_plural
            model_table_name = model_class._meta.db_table
            if DB_ENGINE == "mssql": model_table_name = f"{DB_NAME}.dbo.{model_table_name}"
            nom_modele_class = model_class.__name__
            list_logique = "OR"

            query_graphic = "SELECT "
            if DB_ENGINE == "mssql":
                if limit != "all": query_graphic += f"TOP {limit} "
                limit = ""
            select = ""
            filter = ""
            group_by = ""
            plage = ""
            select_fields = []
            champs = dao_query_builder.toListFieldRelated(model_id)            

            #recuperation du modele reliés
            joints = ""
            #Pour gérer les tables doublons dans les jointures
            tables_joints = [] 
            letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
            i = 0
            for field in model_class._meta.fields: 
                if  field.__class__.__name__ in ('ForeignKey', 'OneToOneField') and field.related_model != None: 
                    i += 1
                    related_model = field.related_model.__name__
                    model_content_ref_rel = ContentType.objects.filter(model = related_model.lower()).first()
                    model_class_rel = model_content_ref_rel.model_class()
                    if DB_ENGINE == "mysql":
                        model_table_name_rel = model_class_rel._meta.db_table
                        joints += f" LEFT JOIN `{model_table_name_rel}` ON (`{model_table_name}`.`{field.db_column}` = `{model_table_name_rel}`.`id`)"
                    elif DB_ENGINE == "mssql": 
                        model_table_name_rel = f"{DB_NAME}.dbo.{model_class_rel._meta.db_table}"
                        if model_class_rel._meta.db_table not in tables_joints:  
                            joints += f" LEFT JOIN {model_table_name_rel} ON ({model_table_name}.{field.db_column} = {model_table_name_rel}.id)"
                            tables_joints.append(model_class_rel._meta.db_table)
                        else:
                            joints += f" LEFT JOIN {model_table_name_rel} AS {letter[i]} ON ({model_table_name}.{field.db_column} = {letter[i]}.id)"
            
            #SELECT, GROUPBY
            if chart_type == "1":
                if champs_afficher:
                    for name, db_name, type, table, field_name, fields in champs:
                        nom_champs = db_name
                        if db_name == None: nom_champs = "id"
                        if type in ('ForeignKey', 'OneToOneField'): name = name + "_id"
                        if name in champs_afficher:
                            if type in ('ForeignKey', 'OneToOneField'): 
                                select_fields.append(f"{table}.{field_name}")
                            else: select_fields.append(f"{model_table_name}.{nom_champs}")                
                    
                    for obj in select_fields:
                        select += f"{obj},"
                    select = select[:-1] #On enleve la dernière virgule
                else:
                    select = "* "
            else: 
                dimension_array = dimension.split(";") 
                group_by = ""
                for name, db_name, type, table, field_name, fields in champs:
                    if name == dimension_array[0]:
                        nom_champs = db_name
                        if db_name == None: nom_champs = "id"
                        if type in ('ForeignKey', 'OneToOneField'): 
                            name = name + "_id"
                            select = f"{table}.{field_name}, {measure_function}({model_table_name}.{measure_attribute})"
                            group_by = f" GROUP BY {table}.id"
                        elif len(dimension_array) > 1: 
                            funct = dimension_array[1].upper()
                            if funct == "DATE":
                                if DB_ENGINE == "mysql":
                                    select = f'DATE_FORMAT({model_table_name}.{nom_champs}, "%d/%m/%Y"), {measure_function}({model_table_name}.{measure_attribute})'
                                    group_by = f' GROUP BY DATE_FORMAT({model_table_name}.{nom_champs}, "%d/%m/%Y")' 
                                elif DB_ENGINE == "mssql": 
                                    select = f"FORMAT({model_table_name}.{nom_champs}, 'dd/MM/yyyy'), {measure_function}({model_table_name}.{measure_attribute})"
                                    group_by = f" GROUP BY FORMAT({model_table_name}.{nom_champs}, 'dd/MM/yyyy')" 
                            elif funct == "MONTH":
                                if DB_ENGINE == "mysql":
                                    select = f'DATE_FORMAT({model_table_name}.{nom_champs}, "%M %Y"), {measure_function}({model_table_name}.{measure_attribute})'
                                    group_by = f" GROUP BY {funct}({model_table_name}.{nom_champs})"
                                elif DB_ENGINE == "mssql": 
                                    select = f"FORMAT({model_table_name}.{nom_champs}, 'MMMM yyyy', 'fr-FR'), {measure_function}({model_table_name}.{measure_attribute})"
                                    group_by = f" GROUP BY FORMAT({model_table_name}.{nom_champs}, 'MMMM yyyy', 'fr-FR')"         
                            else:
                                select = f"{funct}({model_table_name}.{nom_champs}), {measure_function}({model_table_name}.{measure_attribute})"
                                group_by = f" GROUP BY {funct}({model_table_name}.{nom_champs})"
                        else: 
                            select = f"{model_table_name}.{nom_champs}, {measure_function}({model_table_name}.{measure_attribute})"
                            group_by = f" GROUP BY {model_table_name}.{nom_champs}" 
                        break
                
            #PLAGE                                  
            if plage_item != []:
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if plage_valeur == "last_7days":
                    #Les 7 derniers jours
                    last_7days = today + timedelta(days=-7)
                    date_debut = last_7days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "last_30days":
                    #Les 30 derniers jours 
                    last_30days = today + timedelta(days=-30)
                    date_debut = last_30days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_365days":                    
                    #Dernier 365 jours
                    last_365days = today + timedelta(days=-365)
                    date_debut = last_365days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "today":
                    #Aujourd'hui
                    date = today.strftime('%d/%m/%Y')
                    
                    if DB_ENGINE == "mysql":
                        plage = f"DATE_FORMAT({model_table_name}.{plage_item}, '%d/%m/%Y') = '{date}'"
                    elif DB_ENGINE == "mssql": 
                        plage = f"FORMAT({model_table_name}.{plage_item}, 'dd/MM/yyyy') = '{date}'"
                elif plage_valeur == "this_week":
                    #Cette semaine 
                    day_of_week = int(today.strftime('%w'))
                    first_day_of_week = today + timedelta(days=-day_of_week+1)
                    end_week = first_day_of_week + timedelta(days=6)
                    date_debut = first_day_of_week.strftime('%Y/%m/%d')
                    date_fin = end_week.strftime('%Y/%m/%d')
                                        
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "this_month":
                    #Ce mois
                    this_month = int(today.strftime('%m'))
                    next_month = this_month + 1 
                    first_day_this_month = today.replace(day=1)                    
                    if next_month == 13:
                        next_year = int(today.strftime('%Y')) + 1
                        first_day_next_month = today.replace(day=1, month=1, year=next_year)
                    else: first_day_next_month = today.replace(day=1, month=next_month)
                    last_day_this_month = first_day_next_month - timedelta(days=1)
                    date_debut = first_day_this_month.strftime('%Y/%m/%d')
                    date_fin = last_day_this_month.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "this_quarter": 
                    #Ce trimestre
                    this_month = int(today.strftime('%m'))
                    if this_month >= 1 and this_month <= 3:
                        first_day_this_quarter = today.replace(day=1, month=1)
                        last_day_this_quarter = today.replace(day=31, month=3)
                    elif this_month >= 4 and this_month <= 6:
                        first_day_this_quarter = today.replace(day=1, month=4)
                        last_day_this_quarter = today.replace(day=30, month=6)
                    elif this_month >= 7 and this_month <= 9:
                        first_day_this_quarter = today.replace(day=1, month=7)
                        last_day_this_quarter = today.replace(day=30, month=9)
                    elif this_month >= 10 and this_month <= 12:
                        first_day_this_quarter = today.replace(day=1, month=10)
                        last_day_this_quarter = today.replace(day=31, month=12)
                    date_debut = first_day_this_quarter.strftime('%Y/%m/%d')
                    date_fin = last_day_this_quarter.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "this_year": 
                    #Cette année                    this_month = int(today.strftime('%m'))
                    first_day_this_year = today.replace(day=1, month=1)
                    last_day_this_year = today.replace(day=31, month=12)
                    date_debut = first_day_this_year.strftime('%Y/%m/%d')
                    date_fin = last_day_this_year.strftime('%Y/%m/%d')

                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "yesterday": 
                    #Hier
                    yesterday = today - timedelta(days=1)
                    date = yesterday.strftime('%d/%m/%Y')
                    
                    if DB_ENGINE == "mysql":
                        plage = f"DATE_FORMAT({model_table_name}.{plage_item}, '%d/%m/%Y') = '{date}'"
                    elif DB_ENGINE == "mssql": 
                        plage = f"FORMAT({model_table_name}.{plage_item}, 'dd/MM/yyyy') = '{date}'"                    
                elif plage_valeur == "last_week": 
                    #La semaine dernière
                    day_of_week = int(today.strftime('%w'))
                    first_day_of_week = today + timedelta(days=-day_of_week+1)
                    first_day_of_last_week = first_day_of_week + timedelta(days=-7)
                    last_day_of_last_week = first_day_of_week + timedelta(days=-1)
                    date_debut = first_day_of_last_week.strftime('%Y/%m/%d')
                    date_fin = last_day_of_last_week.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "last_month": 
                    #Le mois dernier
                    first_day_this_month = today.replace(day=1)
                    last_day_last_month = first_day_this_month - timedelta(days=1)
                    first_day_last_month = last_day_last_month.replace(day=1)
                    date_debut = first_day_last_month.strftime('%Y/%m/%d')
                    date_fin = last_day_last_month.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_quarter": 
                    #dernier trimestre
                    this_month = int(today.strftime('%m'))
                    if this_month >= 1 and this_month <= 3:
                        this_quarter = "Q1"
                    elif this_month >= 4 and this_month <= 6:
                        this_quarter = "Q2"
                    elif this_month >= 7 and this_month <= 9:
                        this_quarter = "Q3"
                    elif this_month >= 10 and this_month <= 12:
                        this_quarter = "Q4"

                    if this_quarter == "Q1":
                        last_year = int(today.strftime('%Y')) - 1
                        first_day_last_quarter = today.replace(day=1, month=1, year=last_year)
                        last_day_last_quarter = today.replace(day=31, month=3, year=last_year)
                    elif this_quarter == "Q2":
                        first_day_last_quarter = today.replace(day=1, month=1)
                        last_day_last_quarter = today.replace(day=31, month=3)
                    elif this_quarter == "Q3":
                        first_day_last_quarter = today.replace(day=1, month=4)
                        last_day_last_quarter = today.replace(day=30, month=6)
                    elif this_quarter == "Q4":
                        first_day_last_quarter = today.replace(day=1, month=7)
                        last_day_last_quarter = today.replace(day=30, month=9)
                    date_debut = first_day_last_quarter.strftime('%Y/%m/%d')
                    date_fin = last_day_last_quarter.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_year": 
                    #L'année dernière
                    last_year = int(today.strftime('%Y')) - 1
                    first_day_last_year = today.replace(day=1, month=1, year=last_year)
                    last_day_last_year = today.replace(day=31, month=12, year=last_year)
                    date_debut = first_day_last_year.strftime('%Y/%m/%d')
                    date_fin = last_day_last_year.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                    
                                    
            #FILTRE                                  
            if filter_item:
                filter += " WHERE "
                for i in range(len(filter_item)):
                    if filter_logic: #On sarrete pr l'instant à une ligne (on doit gerer après les AND OR xx)
                        if i > 0: #On saute la premiere iteration pour equilibrer les tailles 
                            filter += f' {filter_logic[i]} ' 
                    filter_comparison = f"{filter_operateur[i]} '{filter_valeur[i]}'"
                    if filter_operateur[i] == "contient":
                        filter_comparison = f"LIKE '%{filter_valeur[i]}%'"
                    elif filter_operateur[i] == "contient_pas": 
                        filter_comparison = f"NOT LIKE '%{filter_valeur[i]}%'" 
                    elif filter_operateur[i] == "defini": 
                        filter_comparison = f"IS NOT NULL"
                    elif filter_operateur[i] == "pas_defini": 
                        filter_comparison = f"IS NULL"
                    elif filter_operateur[i] == "vrai": 
                        filter_comparison = f"= True"
                    elif filter_operateur[i] == "faux": 
                        filter_comparison = f"= False" 
                    else: filter_comparison = f"{filter_operateur[i]} '{filter_valeur[i]}'"
                    
                    f_item = filter_item[i].split(";")
                    #Si champs non relationel    
                    if f_item[0].find(".") != -1:
                        filt = f"{f_item[0]}"
                    else: 
                        filt = f"{model_table_name}.{f_item[0]}"
                    
                    #Si type est une date    
                    if len(f_item) > 1:
                        funct = f_item[1].upper()
                        if funct == "DATE":
                            if DB_ENGINE == "mysql":
                                filter += f'DATE_FORMAT({filt}, "%d/%m/%Y") {filter_comparison}'
                            elif DB_ENGINE == "mssql": filter += f"FORMAT({filt}, 'dd/MM/yyyy') {filter_comparison}"
                        elif funct == "MONTH":
                            if DB_ENGINE == "mysql":
                                filter += f'DATE_FORMAT({filt}, "%m/%Y") {filter_comparison}'
                            elif DB_ENGINE == "mssql": filter += f"FORMAT({filt}, 'dd/MM/yyyy') {filter_comparison}"
                        else:
                            filter += f'YEAR({filt}) {filter_comparison}'
                    else: 
                        filter += f"{filt} {filter_comparison}"
                #S'il ya des filter et une requete plage
                if plage_item != []:
                    filter += f" AND {plage}"        
            #S'il ya pas des filter et on a une requete plage        
            elif filter_item == [] and plage_item != []: 
                filter += f" WHERE {plage}" 
                                                        
            query_graphic += select  
            if DB_ENGINE == "mysql": query_graphic += f" FROM `{model_table_name}` " 
            elif DB_ENGINE == "mssql": query_graphic += f" FROM {model_table_name} "   
            query_graphic += joints           
            query_graphic += filter
            query_graphic += group_by

            if DB_ENGINE == "mysql":                 
                if limit == "all": limit = ""
                else: limit = f"LIMIT {limit}"

            query_graphic += f" {limit}"                                   
            print(query_graphic)
                        
            result_graphic = dao_query_builder.my_custom_sql(query_graphic) if query_graphic else [] #Si requete non vide, then run
            #Creating query Object

            #Traitement des données graphiques
            if chart_type == 0: result_graphic = dao_query_builder.processing_data_graphic(dimension, result_graphic)
            return result_graphic, query_graphic
        except Exception as e:
            print("Error on toPerformQueryForChart", e) 
            return [] 
        
    def toPerformQueryForCard(auteur, model_id, card_function = "", card_attribute = "", filter_logic = [], filter_item = [], \
                        filter_operateur = [], filter_valeur = [], regrouper_item =[], plage_item = [], plage_valeur = [], order_by = "", order_sens = "", limit = "" ):
        '''Fonction qui se charge de creer la requete en fonction des valeurs saisies et
        creer un objet Query qu'il enregistre dans la BD. 
        Il s'agit d'une création manuelle flexible d'un script SQL.        
        '''
        try:
            DB_ENGINE = "mssql"
            if "mysql" in settings.DATABASES["default"]["ENGINE"]: DB_ENGINE = "mysql" 
            DB_NAME = settings.DATABASES["default"]["NAME"]
            main_modele_id = model_id
            #recuperation du modele de l'objet à partir de l'identifiant du content type
            model_content_ref = ContentType.objects.get(pk = main_modele_id)          
            model_class = model_content_ref.model_class()
            nom_modele = model_content_ref.model.replace("model_","").capitalize()
            nom_modele_verbose = model_class._meta.verbose_name
            nom_modele_verbose_plural = model_class._meta.verbose_name_plural
            model_table_name = model_class._meta.db_table
            if DB_ENGINE == "mssql": model_table_name = f"{DB_NAME}.dbo.{model_table_name}"
            nom_modele_class = model_class.__name__
            list_logique = "OR"

            query_card = "SELECT "
            if DB_ENGINE == "mssql":
                if limit != "all": query_card += f"TOP {limit} "
                limit = ""
            select = ""
            filter = ""
            group_by = ""
            plage = ""
            select_fields = []
            champs = dao_query_builder.toListFieldRelated(model_id)            

            #recuperation du modele reliés
            joints = ""
            #Pour gérer les tables doublons dans les jointures
            tables_joints = [] 
            letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
            i = 0
            for field in model_class._meta.fields: 
                if  field.__class__.__name__ in ('ForeignKey', 'OneToOneField') and field.related_model != None: 
                    i += 1
                    related_model = field.related_model.__name__
                    model_content_ref_rel = ContentType.objects.filter(model = related_model.lower()).first()
                    model_class_rel = model_content_ref_rel.model_class()
                    if DB_ENGINE == "mysql":
                        model_table_name_rel = model_class_rel._meta.db_table
                        joints += f" LEFT JOIN `{model_table_name_rel}` ON (`{model_table_name}`.`{field.db_column}` = `{model_table_name_rel}`.`id`)"
                    elif DB_ENGINE == "mssql": 
                        model_table_name_rel = f"{DB_NAME}.dbo.{model_class_rel._meta.db_table}"
                        if model_class_rel._meta.db_table not in tables_joints:  
                            joints += f" LEFT JOIN {model_table_name_rel} ON ({model_table_name}.{field.db_column} = {model_table_name_rel}.id)"
                            tables_joints.append(model_class_rel._meta.db_table)
                        else:
                            joints += f" LEFT JOIN {model_table_name_rel} AS {letter[i]} ON ({model_table_name}.{field.db_column} = {letter[i]}.id)"

            #SELECT
            select = f"{card_function}({model_table_name}.{card_attribute}) "

            
            #PLAGE                                  
            if plage_item != []:
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if plage_valeur == "last_7days":
                    #Les 7 derniers jours
                    last_7days = today + timedelta(days=-7)
                    date_debut = last_7days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "last_30days":
                    #Les 30 derniers jours 
                    last_30days = today + timedelta(days=-30)
                    date_debut = last_30days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_365days":                    
                    #Dernier 365 jours
                    last_365days = today + timedelta(days=-365)
                    date_debut = last_365days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "today":
                    #Aujourd'hui
                    date = today.strftime('%d/%m/%Y')
                    
                    if DB_ENGINE == "mysql":
                        plage = f"DATE_FORMAT({model_table_name}.{plage_item}, '%d/%m/%Y') = '{date}'"
                    elif DB_ENGINE == "mssql": 
                        plage = f"FORMAT({model_table_name}.{plage_item}, 'dd/MM/yyyy') = '{date}'"
                elif plage_valeur == "this_week":
                    #Cette semaine 
                    day_of_week = int(today.strftime('%w'))
                    first_day_of_week = today + timedelta(days=-day_of_week+1)
                    end_week = first_day_of_week + timedelta(days=6)
                    date_debut = first_day_of_week.strftime('%Y/%m/%d')
                    date_fin = end_week.strftime('%Y/%m/%d')
                                        
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "this_month":
                    #Ce mois
                    this_month = int(today.strftime('%m'))
                    next_month = this_month + 1 
                    first_day_this_month = today.replace(day=1)                    
                    if next_month == 13:
                        next_year = int(today.strftime('%Y')) + 1
                        first_day_next_month = today.replace(day=1, month=1, year=next_year)
                    else: first_day_next_month = today.replace(day=1, month=next_month)
                    last_day_this_month = first_day_next_month - timedelta(days=1)
                    date_debut = first_day_this_month.strftime('%Y/%m/%d')
                    date_fin = last_day_this_month.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "this_quarter": 
                    #Ce trimestre
                    this_month = int(today.strftime('%m'))
                    if this_month >= 1 and this_month <= 3:
                        first_day_this_quarter = today.replace(day=1, month=1)
                        last_day_this_quarter = today.replace(day=31, month=3)
                    elif this_month >= 4 and this_month <= 6:
                        first_day_this_quarter = today.replace(day=1, month=4)
                        last_day_this_quarter = today.replace(day=30, month=6)
                    elif this_month >= 7 and this_month <= 9:
                        first_day_this_quarter = today.replace(day=1, month=7)
                        last_day_this_quarter = today.replace(day=30, month=9)
                    elif this_month >= 10 and this_month <= 12:
                        first_day_this_quarter = today.replace(day=1, month=10)
                        last_day_this_quarter = today.replace(day=31, month=12)
                    date_debut = first_day_this_quarter.strftime('%Y/%m/%d')
                    date_fin = last_day_this_quarter.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "this_year": 
                    #Cette année                    this_month = int(today.strftime('%m'))
                    first_day_this_year = today.replace(day=1, month=1)
                    last_day_this_year = today.replace(day=31, month=12)
                    date_debut = first_day_this_year.strftime('%Y/%m/%d')
                    date_fin = last_day_this_year.strftime('%Y/%m/%d')

                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "yesterday": 
                    #Hier
                    yesterday = today - timedelta(days=1)
                    date = yesterday.strftime('%d/%m/%Y')
                    
                    if DB_ENGINE == "mysql":
                        plage = f"DATE_FORMAT({model_table_name}.{plage_item}, '%d/%m/%Y') = '{date}'"
                    elif DB_ENGINE == "mssql": 
                        plage = f"FORMAT({model_table_name}.{plage_item}, 'dd/MM/yyyy') = '{date}'"
                elif plage_valeur == "last_week": 
                    #La semaine dernière
                    day_of_week = int(today.strftime('%w'))
                    first_day_of_week = today + timedelta(days=-day_of_week+1)
                    first_day_of_last_week = first_day_of_week + timedelta(days=-7)
                    last_day_of_last_week = first_day_of_week + timedelta(days=-1)
                    date_debut = first_day_of_last_week.strftime('%Y/%m/%d')
                    date_fin = last_day_of_last_week.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "last_month": 
                    #Le mois dernier
                    first_day_this_month = today.replace(day=1)
                    last_day_last_month = first_day_this_month - timedelta(days=1)
                    first_day_last_month = last_day_last_month.replace(day=1)
                    date_debut = first_day_last_month.strftime('%Y/%m/%d')
                    date_fin = last_day_last_month.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_quarter": 
                    #dernier trimestre
                    this_month = int(today.strftime('%m'))
                    if this_month >= 1 and this_month <= 3:
                        this_quarter = "Q1"
                    elif this_month >= 4 and this_month <= 6:
                        this_quarter = "Q2"
                    elif this_month >= 7 and this_month <= 9:
                        this_quarter = "Q3"
                    elif this_month >= 10 and this_month <= 12:
                        this_quarter = "Q4"

                    if this_quarter == "Q1":
                        last_year = int(today.strftime('%Y')) - 1
                        first_day_last_quarter = today.replace(day=1, month=1, year=last_year)
                        last_day_last_quarter = today.replace(day=31, month=3, year=last_year)
                    elif this_quarter == "Q2":
                        first_day_last_quarter = today.replace(day=1, month=1)
                        last_day_last_quarter = today.replace(day=31, month=3)
                    elif this_quarter == "Q3":
                        first_day_last_quarter = today.replace(day=1, month=4)
                        last_day_last_quarter = today.replace(day=30, month=6)
                    elif this_quarter == "Q4":
                        first_day_last_quarter = today.replace(day=1, month=7)
                        last_day_last_quarter = today.replace(day=30, month=9)
                    date_debut = first_day_last_quarter.strftime('%Y/%m/%d')
                    date_fin = last_day_last_quarter.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_year": 
                    #L'année dernière
                    last_year = int(today.strftime('%Y')) - 1
                    first_day_last_year = today.replace(day=1, month=1, year=last_year)
                    last_day_last_year = today.replace(day=31, month=12, year=last_year)
                    date_debut = first_day_last_year.strftime('%Y/%m/%d')
                    date_fin = last_day_last_year.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                    
                                    
            #FILTRE                                  
            if filter_item:
                filter += " WHERE "
                for i in range(len(filter_item)):
                    if filter_logic: #On sarrete pr l'instant à une ligne (on doit gerer après les AND OR xx)
                        if i > 0: #On saute la premiere iteration pour equilibrer les tailles 
                            filter += f' {filter_logic[i]} ' 
                    filter_comparison = f"{filter_operateur[i]} '{filter_valeur[i]}'"
                    if filter_operateur[i] == "contient":
                        filter_comparison = f"LIKE '%{filter_valeur[i]}%'"
                    elif filter_operateur[i] == "contient_pas": 
                        filter_comparison = f"NOT LIKE '%{filter_valeur[i]}%'" 
                    elif filter_operateur[i] == "defini": 
                        filter_comparison = f"IS NOT NULL"
                    elif filter_operateur[i] == "pas_defini": 
                        filter_comparison = f"IS NULL"
                    elif filter_operateur[i] == "vrai": 
                        filter_comparison = f"= True"
                    elif filter_operateur[i] == "faux": 
                        filter_comparison = f"= False" 
                    else: filter_comparison = f"{filter_operateur[i]} '{filter_valeur[i]}'"
                    
                    f_item = filter_item[i].split(";")
                    #Si champs non relationel    
                    if f_item[0].find(".") != -1:
                        filt = f"{f_item[0]}"
                    else: 
                        filt = f"{model_table_name}.{f_item[0]}"
                    
                    #Si type est une date    
                    if len(f_item) > 1:
                        funct = f_item[1].upper()
                        if funct == "DATE":
                            if DB_ENGINE == "mysql":
                                filter += f"DATE_FORMAT({filt}, '%d/%m/%Y') {filter_comparison}"
                            elif DB_ENGINE == "mssql": 
                                filter += f"FORMAT({filt}, 'dd/MM/yyyy') {filter_comparison}"
                        elif funct == "MONTH":                           
                            if DB_ENGINE == "mysql":
                                filter += f'DATE_FORMAT({filt}, "%m/%Y") {filter_comparison}'
                            elif DB_ENGINE == "mssql": 
                                filter += f"FORMAT({filt}, 'MM/yyyy') {filter_comparison}"
                        else:
                            filter += f'YEAR({filt}) {filter_comparison}'
                    else: 
                        filter += f"{filt} {filter_comparison}"
                #S'il ya des filter et une requete plage
                if plage_item != []:
                    filter += f" AND {plage}"        
            #S'il ya pas des filter et on a une requete plage        
            elif filter_item == [] and plage_item != []: 
                filter += f" WHERE {plage}" 
                                                         
            query_card += select            
            if DB_ENGINE == "mysql": query_card += f" FROM `{model_table_name}` " 
            elif DB_ENGINE == "mssql": query_card += f" FROM {model_table_name} "  
            query_card += joints           
            query_card += filter
            query_card += group_by

            if DB_ENGINE == "mysql": 
                if limit == "all": limit = ""
                else: limit = f"LIMIT {limit}"

            query_card += f" {limit}"                                  
            print(query_card)

            #Traitement des données card
            result_card = dao_query_builder.my_custom_sql(query_card) if query_card else []
            data = result_card[0][0]
            return data, query_card
        except Exception as e:
            print("Error on toPerformQueryForCard", e) 
            return [] 


    def toPerformQueryForPivot(auteur, model_id, champs_afficher, filter_logic = [], filter_item = [], \
                        filter_operateur = [], filter_valeur = [], chart_type =0, plage_item = [], plage_valeur = [], order_by = "", order_sens = "", limit = "" ):
        '''Fonction qui se charge de creer la requete en fonction des valeurs saisies et
        creer un objet Query qu'il enregistre dans la BD. 
        Il s'agit d'une création manuelle flexible d'un script SQL.        
        '''
        try:
            DB_ENGINE = "mssql"
            if "mysql" in settings.DATABASES["default"]["ENGINE"]: DB_ENGINE = "mysql" 
            DB_NAME = settings.DATABASES["default"]["NAME"]
            main_modele_id = model_id
            #recuperation du modele de l'objet à partir de l'identifiant du content type
            model_content_ref = ContentType.objects.get(pk = main_modele_id)          
            model_class = model_content_ref.model_class()
            nom_modele = model_content_ref.model.replace("model_","").capitalize()
            nom_modele_verbose = model_class._meta.verbose_name
            nom_modele_verbose_plural = model_class._meta.verbose_name_plural
            model_table_name = model_class._meta.db_table
            if DB_ENGINE == "mssql": model_table_name = f"{DB_NAME}.dbo.{model_table_name}"
            nom_modele_class = model_class.__name__
            list_logique = "OR"

            query_pivot = "SELECT "
            if DB_ENGINE == "mssql":
                if limit != "all": query_pivot += f"TOP {limit} "
                limit = ""
            select = ""
            filter = ""
            group_by = ""
            plage = ""
            select_fields = []
            champs = dao_query_builder.toListFieldRelated(model_id)            

            #recuperation du modele reliés
            joints = ""
            #Pour gérer les tables doublons dans les jointures
            tables_joints = [] 
            letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
            i = 0
            for field in model_class._meta.fields: 
                if  field.__class__.__name__ in ('ForeignKey', 'OneToOneField') and field.related_model != None: 
                    i += 1
                    related_model = field.related_model.__name__
                    model_content_ref_rel = ContentType.objects.filter(model = related_model.lower()).first()
                    model_class_rel = model_content_ref_rel.model_class()
                    if DB_ENGINE == "mysql":
                        model_table_name_rel = model_class_rel._meta.db_table
                        joints += f" LEFT JOIN `{model_table_name_rel}` ON (`{model_table_name}`.`{field.db_column}` = `{model_table_name_rel}`.`id`)"
                    elif DB_ENGINE == "mssql": 
                        model_table_name_rel = f"{DB_NAME}.dbo.{model_class_rel._meta.db_table}"
                        if model_class_rel._meta.db_table not in tables_joints:  
                            joints += f" LEFT JOIN {model_table_name_rel} ON ({model_table_name}.{field.db_column} = {model_table_name_rel}.id)"
                            tables_joints.append(model_class_rel._meta.db_table)
                        else:
                            joints += f" LEFT JOIN {model_table_name_rel} AS {letter[i]} ON ({model_table_name}.{field.db_column} = {letter[i]}.id)" 
             
            #SELECT
            if champs_afficher:
                for name, db_name, type, table, field_name, fields in champs:
                    nom_champs = db_name
                    if db_name == None: nom_champs = "id"
                    if type in ('ForeignKey', 'OneToOneField'): name = name + "_id"
                    if name in champs_afficher:
                        if type in ('ForeignKey', 'OneToOneField'): 
                            select_fields.append(f"{table}.{field_name}")
                        else: select_fields.append(f"{model_table_name}.{nom_champs}")                
                
                for obj in select_fields:
                    select += f"{obj},"
                select = select[:-1] #On enleve la dernière virgule
            else:
                select = "* "

                
            #PLAGE                                  
            if plage_item != []:
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if plage_valeur == "last_7days":
                    #Les 7 derniers jours
                    last_7days = today + timedelta(days=-7)
                    date_debut = last_7days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "last_30days":
                    #Les 30 derniers jours 
                    last_30days = today + timedelta(days=-30)
                    date_debut = last_30days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_365days":                    
                    #Dernier 365 jours
                    last_365days = today + timedelta(days=-365)
                    date_debut = last_365days.strftime('%Y/%m/%d')
                    date_fin = today.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "today":
                    #Aujourd'hui
                    date = today.strftime('%d/%m/%Y')
                    
                    if DB_ENGINE == "mysql":
                        plage = f"DATE_FORMAT({model_table_name}.{plage_item}, '%d/%m/%Y') = '{date}'"
                    elif DB_ENGINE == "mssql": 
                        plage = f"FORMAT({model_table_name}.{plage_item}, 'dd/MM/yyyy') = '{date}'"
                elif plage_valeur == "this_week":
                    #Cette semaine 
                    day_of_week = int(today.strftime('%w'))
                    first_day_of_week = today + timedelta(days=-day_of_week+1)
                    end_week = first_day_of_week + timedelta(days=6)
                    date_debut = first_day_of_week.strftime('%Y/%m/%d')
                    date_fin = end_week.strftime('%Y/%m/%d')
                                        
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "this_month":
                    #Ce mois
                    this_month = int(today.strftime('%m'))
                    next_month = this_month + 1 
                    first_day_this_month = today.replace(day=1)                    
                    if next_month == 13:
                        next_year = int(today.strftime('%Y')) + 1
                        first_day_next_month = today.replace(day=1, month=1, year=next_year)
                    else: first_day_next_month = today.replace(day=1, month=next_month)
                    last_day_this_month = first_day_next_month - timedelta(days=1)
                    date_debut = first_day_this_month.strftime('%Y/%m/%d')
                    date_fin = last_day_this_month.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "this_quarter": 
                    #Ce trimestre
                    this_month = int(today.strftime('%m'))
                    if this_month >= 1 and this_month <= 3:
                        first_day_this_quarter = today.replace(day=1, month=1)
                        last_day_this_quarter = today.replace(day=31, month=3)
                    elif this_month >= 4 and this_month <= 6:
                        first_day_this_quarter = today.replace(day=1, month=4)
                        last_day_this_quarter = today.replace(day=30, month=6)
                    elif this_month >= 7 and this_month <= 9:
                        first_day_this_quarter = today.replace(day=1, month=7)
                        last_day_this_quarter = today.replace(day=30, month=9)
                    elif this_month >= 10 and this_month <= 12:
                        first_day_this_quarter = today.replace(day=1, month=10)
                        last_day_this_quarter = today.replace(day=31, month=12)
                    date_debut = first_day_this_quarter.strftime('%Y/%m/%d')
                    date_fin = last_day_this_quarter.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "this_year": 
                    #Cette année                    this_month = int(today.strftime('%m'))
                    first_day_this_year = today.replace(day=1, month=1)
                    last_day_this_year = today.replace(day=31, month=12)
                    date_debut = first_day_this_year.strftime('%Y/%m/%d')
                    date_fin = last_day_this_year.strftime('%Y/%m/%d')

                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "yesterday": 
                    #Hier
                    yesterday = today - timedelta(days=1)
                    date = yesterday.strftime('%d/%m/%Y')
                    
                    if DB_ENGINE == "mysql":
                        plage = f"DATE_FORMAT({model_table_name}.{plage_item}, '%d/%m/%Y') = '{date}'"
                    elif DB_ENGINE == "mssql": 
                        plage = f"FORMAT({model_table_name}.{plage_item}, 'dd/MM/yyyy') = '{date}'"
                elif plage_valeur == "last_week": 
                    #La semaine dernière
                    day_of_week = int(today.strftime('%w'))
                    first_day_of_week = today + timedelta(days=-day_of_week+1)
                    first_day_of_last_week = first_day_of_week + timedelta(days=-7)
                    last_day_of_last_week = first_day_of_week + timedelta(days=-1)
                    date_debut = first_day_of_last_week.strftime('%Y/%m/%d')
                    date_fin = last_day_of_last_week.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'"
                elif plage_valeur == "last_month": 
                    #Le mois dernier
                    first_day_this_month = today.replace(day=1)
                    last_day_last_month = first_day_this_month - timedelta(days=1)
                    first_day_last_month = last_day_last_month.replace(day=1)
                    date_debut = first_day_last_month.strftime('%Y/%m/%d')
                    date_fin = last_day_last_month.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_quarter": 
                    #dernier trimestre
                    this_month = int(today.strftime('%m'))
                    if this_month >= 1 and this_month <= 3:
                        this_quarter = "Q1"
                    elif this_month >= 4 and this_month <= 6:
                        this_quarter = "Q2"
                    elif this_month >= 7 and this_month <= 9:
                        this_quarter = "Q3"
                    elif this_month >= 10 and this_month <= 12:
                        this_quarter = "Q4"

                    if this_quarter == "Q1":
                        last_year = int(today.strftime('%Y')) - 1
                        first_day_last_quarter = today.replace(day=1, month=1, year=last_year)
                        last_day_last_quarter = today.replace(day=31, month=3, year=last_year)
                    elif this_quarter == "Q2":
                        first_day_last_quarter = today.replace(day=1, month=1)
                        last_day_last_quarter = today.replace(day=31, month=3)
                    elif this_quarter == "Q3":
                        first_day_last_quarter = today.replace(day=1, month=4)
                        last_day_last_quarter = today.replace(day=30, month=6)
                    elif this_quarter == "Q4":
                        first_day_last_quarter = today.replace(day=1, month=7)
                        last_day_last_quarter = today.replace(day=30, month=9)
                    date_debut = first_day_last_quarter.strftime('%Y/%m/%d')
                    date_fin = last_day_last_quarter.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                elif plage_valeur == "last_year": 
                    #L'année dernière
                    last_year = int(today.strftime('%Y')) - 1
                    first_day_last_year = today.replace(day=1, month=1, year=last_year)
                    last_day_last_year = today.replace(day=31, month=12, year=last_year)
                    date_debut = first_day_last_year.strftime('%Y/%m/%d')
                    date_fin = last_day_last_year.strftime('%Y/%m/%d')
                    
                    plage = f"{model_table_name}.{plage_item} BETWEEN '{date_debut}' AND '{date_fin}'" 
                    
                                    
            #FILTRE                                  
            if filter_item:
                filter += " WHERE "
                for i in range(len(filter_item)):
                    if filter_logic: #On sarrete pr l'instant à une ligne (on doit gerer après les AND OR xx)
                        if i > 0: #On saute la premiere iteration pour equilibrer les tailles 
                            filter += f' {filter_logic[i]} ' 
                    filter_comparison = f"{filter_operateur[i]} '{filter_valeur[i]}'"
                    if filter_operateur[i] == "contient":
                        filter_comparison = f"LIKE '%{filter_valeur[i]}%'"
                    elif filter_operateur[i] == "contient_pas": 
                        filter_comparison = f"NOT LIKE '%{filter_valeur[i]}%'" 
                    elif filter_operateur[i] == "defini": 
                        filter_comparison = f"IS NOT NULL"
                    elif filter_operateur[i] == "pas_defini": 
                        filter_comparison = f"IS NULL"
                    elif filter_operateur[i] == "vrai": 
                        filter_comparison = f"= True"
                    elif filter_operateur[i] == "faux": 
                        filter_comparison = f"= False" 
                    else: filter_comparison = f"{filter_operateur[i]} '{filter_valeur[i]}'"
                    
                    f_item = filter_item[i].split(";")
                    #Si champs non relationel    
                    if f_item[0].find(".") != -1:
                        filt = f"{f_item[0]}"
                    else: 
                        filt = f"{model_table_name}.{f_item[0]}"
                    
                    #Si type est une date    
                    if len(f_item) > 1:
                        funct = f_item[1].upper()
                        if funct == "DATE":
                            if DB_ENGINE == "mysql":
                                filter += f"DATE_FORMAT({filt}, '%d/%m/%Y') {filter_comparison}"
                            elif DB_ENGINE == "mssql": 
                                filter += f"FORMAT({filt}, 'dd/MM/yyyy') {filter_comparison}"
                        elif funct == "MONTH":
                            if DB_ENGINE == "mysql":
                                filter += f"DATE_FORMAT({filt}, '%d/%m/%Y') {filter_comparison}"
                            elif DB_ENGINE == "mssql": 
                                filter += f"FORMAT({filt}, 'MM/yyyy') {filter_comparison}"
                        else:
                            filter += f'YEAR({filt}) {filter_comparison}'
                    else: 
                        filter += f"{filt} {filter_comparison}"
                #S'il ya des filter et une requete plage
                if plage_item != []:
                    filter += f" AND {plage}"        
            #S'il ya pas des filter et on a une requete plage        
            elif filter_item == [] and plage_item != []: 
                filter += f" WHERE {plage}" 
                 
                                        
            query_pivot += select            
            if DB_ENGINE == "mysql": query_pivot += f" FROM `{model_table_name}` "
            elif DB_ENGINE == "mssql": query_pivot += f" FROM {model_table_name} "     
            query_pivot += joints           
            query_pivot += filter
            query_pivot += group_by

            if DB_ENGINE == "mysql":                 
                if limit == "all": limit = ""
                else: limit = f"LIMIT {limit}"

            query_pivot += f" {limit}"                                  
            print(query_pivot)
                        
            result_pivot = dao_query_builder.my_custom_sql(query_pivot) if query_pivot else [] #Si requete non vide, then run
            return result_pivot, query_pivot
        except Exception as e:
            print("Error on toPerformQueryForPivot", e) 
            return [] 

    def my_custom_sql(query):
        "Fonction qui execute une requete sql et retour le resultat sous forme de liste de tuples"
        try: 
            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchall()
            return row
        except Exception as e:
            print("Error on my_custom_sql", e)
            return []
    
    def processing_data_graphic(dimension, result_graphic):
        try:
            category_list = []
            dataset_list = []
            for result in result_graphic:
                category_list.append(result[0])
                dataset_list.append(result[1])

            return {"categories":category_list, "datasets": dataset_list}
        except Exception as e:
            print("Error on processing_data_graphic", e)
            return None
        
    
    def testIfFieldIsFK(thefield, model_content_type):
        #refaire
        result = []
        objet_modele = model_content_type.model_class()
        for f in objet_modele._meta.get_fields():
            if f.name == thefield:
                if f.model:
                    try:
                        modele = objet_modele._meta.get_field(f.name).related_model                
                        model_content_ref = ContentType.objects.get_for_model(modele)
                        ref_model_name = f"{model_content_ref.app_label}_{model_content_ref.model}"

                        return ref_model_name      
                    except Exception as e:
                        return None
        return None
    
    def checkSelectFieldFK(list_select, model_content_type):
        list_join = []
        

    def generate_list_choices(dict_choices):
        list = []
        try:
            for key, value in dict_choices:
                item = {'id' : key,'designation' : value}
                list.append(item)
            return list
        except Exception as e:
            return list