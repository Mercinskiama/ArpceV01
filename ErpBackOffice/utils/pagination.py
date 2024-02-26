from __future__ import unicode_literals
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur, Model_Personne
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class pagination(object):
    
    @staticmethod
    def toGet(request, model, lenght = 50):
        try:
            if request.method == 'POST':
                page = int(request.POST.get("page",1))			
                count = int(request.POST.get("count",lenght))
            else:
                page = int(request.GET.get("page",1))			
                count = int(request.GET.get("count",lenght))
        except Exception as e:
            count = 10
            page = 1 

        paginator = []
        paginator = Paginator(model, count)
        try:
            model = paginator.page(page)
        except PageNotAnInteger:
            model = paginator.page(1)
        except EmptyPage:
            model = paginator.page(paginator.num_pages)
        
        model.num_items = count
        return model

    @staticmethod
    def toGetData(model, page = 1, count = 50):
        paginator = []
        paginator = Paginator(model, count)
        try:
            model = paginator.page(page)
        except PageNotAnInteger:
            model = paginator.page(1)
        except EmptyPage:
            model = paginator.page(paginator.num_pages)
        
        model.num_items = count
        return model
    
    @staticmethod
    def toAddVarsToContext(model, context):
        try:
            try:
                model_has_other_pages = model.has_other_pages()
                print(f"model_has_other_pages: {model_has_other_pages}")
            except  Exception as e:
                model_has_other_pages = False
            
            try:
                model_has_previous = model.has_previous()
                print(f"model_has_previous: {model_has_previous}")
            except  Exception as e:
                model_has_previous = False
                
            try:
                model_previous_page_number = model.previous_page_number()
                print(f"model_previous_page_number: {model_previous_page_number}")
            except  Exception as e:
                model_previous_page_number = 0
                
            try:
                model_start_index = model.start_index()
                print(f"model_start_index: {model_start_index}")
            except  Exception as e:
                model_start_index = 0
                
            try:
                model_end_index = model.end_index()
                print(f"model_end_index: {model_end_index}")
            except  Exception as e:
                model_end_index = 0
                
            try:
                model_has_next = model.has_next()
                print(f"model_has_next: {model_has_next}")
            except  Exception as e:
                model_has_next = False
                        
            try:
                model_next_page_number = model.next_page_number()
                print(f"model_next_page_number: {model_next_page_number}")
            except  Exception as e:
                model_next_page_number = False
                
            try:
                model_paginator_page_range = []
                page_range = model.paginator.page_range
                for i in page_range:
                    model_paginator_page_range.append(i)
                print(f"model_paginator_page_range: {model_paginator_page_range}")
            except  Exception as e:
                model_paginator_page_range = []
            
            context["model_has_other_pages"] = model_has_other_pages
            context["model_has_previous"] = model_has_previous
            context["model_previous_page_number"] = model_previous_page_number
            context["model_start_index"] = model_start_index
            context["model_end_index"] = model_end_index
            context["model_has_next"] = model_has_next
            context["model_next_page_number"] = model_next_page_number
            context["model_paginator_count"] = model.paginator.count
            context["model_paginator_num_pages"] = model.paginator.num_pages
            context["model_number"] = model.number
            context["model_num_items"] = model.num_items
            context["model_paginator_page_range"] = model_paginator_page_range
            
            return context
        except  Exception as e:
            print(f"Erreur: {e}")
            return context