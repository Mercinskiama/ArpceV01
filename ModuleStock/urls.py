from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.get_index, name='module_stock_index'),
    url(r'^tableau', views.get_dashboard, name='module_stock_tableau_de_bord'),
]
    
#ARTICLE URLS
#=====================================
#ARTICLE CRUD URLS
urlpatterns.append(url(r'^article/list', views.get_lister_article, name = 'module_stock_list_article'))
urlpatterns.append(url(r'^article/add', views.get_creer_article, name = 'module_stock_add_article'))
urlpatterns.append(url(r'^article/post_add', views.post_creer_article, name = 'module_stock_post_add_article'))
urlpatterns.append(url(r'^article/select/(?P<ref>[0-9]+)/$', views.get_select_article, name = 'module_stock_select_article'))
urlpatterns.append(url(r'^article/item/(?P<ref>[0-9]+)/$', views.get_details_article, name = 'module_stock_detail_article'))
urlpatterns.append(url(r'^article/item/(?P<ref>[0-9]+)/update$', views.get_modifier_article, name = 'module_stock_update_article'))
urlpatterns.append(url(r'^article/item/post_update/$', views.post_modifier_article, name = 'module_stock_post_update_article'))
urlpatterns.append(url(r'^article/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_article, name = 'module_stock_duplicate_article'))
urlpatterns.append(url(r'^article/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_article, name = 'module_stock_print_article'))
#ARTICLE UPLOAD URLS
urlpatterns.append(url(r'^article/upload/add', views.get_upload_article, name = 'module_stock_get_upload_article'))
urlpatterns.append(url(r'^article/upload/post_add', views.post_upload_article, name = 'module_stock_post_upload_article'))

#ARTICLE BI URLS
urlpatterns.append(url(r'^article/bi', views.get_bi_article, name = 'module_stock_bi_article'))

#ARTICLE API URLS
urlpatterns.append(url(r'^api/article/list', views.get_list_article, name = 'module_stock_api_list_article'))
urlpatterns.append(url(r'^api/article/item', views.get_item_article, name = 'module_stock_api_item_article'))
urlpatterns.append(url(r'^api/article/create', views.post_create_article, name = 'module_stock_api_create_article'))

urlpatterns.append(url(r'^article/reporting', views.get_creer_rapport_article, name = 'module_stock_creer_rapport'))
urlpatterns.append(url(r'^rapport/post_article_stock/$', views.get_detail_article_stock, name='module_stock_post_rapport_article_in_stock'))

#STOCKAGE URLS
#=====================================
#STOCKAGE CRUD URLS
urlpatterns.append(url(r'^stockage/list', views.get_lister_stockage, name = 'module_stock_list_stockage'))
urlpatterns.append(url(r'^stockage/add', views.get_creer_stockage, name = 'module_stock_add_stockage'))
urlpatterns.append(url(r'^stockage/post_add', views.post_creer_stockage, name = 'module_stock_post_add_stockage'))
urlpatterns.append(url(r'^stockage/select/(?P<ref>[0-9]+)/$', views.get_select_stockage, name = 'module_stock_select_stockage'))
urlpatterns.append(url(r'^stockage/item/(?P<ref>[0-9]+)/$', views.get_details_stockage, name = 'module_stock_detail_stockage'))
urlpatterns.append(url(r'^stockage/item/(?P<ref>[0-9]+)/update$', views.get_modifier_stockage, name = 'module_stock_update_stockage'))
urlpatterns.append(url(r'^stockage/item/post_update/$', views.post_modifier_stockage, name = 'module_stock_post_update_stockage'))
urlpatterns.append(url(r'^stockage/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_stockage, name = 'module_stock_duplicate_stockage'))
urlpatterns.append(url(r'^stockage/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_stockage, name = 'module_stock_print_stockage'))
#STOCKAGE UPLOAD URLS
urlpatterns.append(url(r'^stockage/upload/add', views.get_upload_stockage, name = 'module_stock_get_upload_stockage'))
urlpatterns.append(url(r'^stockage/upload/post_add', views.post_upload_stockage, name = 'module_stock_post_upload_stockage'))

#STOCKAGE API URLS
urlpatterns.append(url(r'^api/stockage/list', views.get_list_stockage, name = 'module_stock_api_list_stockage'))
urlpatterns.append(url(r'^api/stockage/item', views.get_item_stockage, name = 'module_stock_api_item_stockage'))
urlpatterns.append(url(r'^api/stockage/create', views.post_create_stockage, name = 'module_stock_api_create_stockage'))

urlpatterns.append(url(r'^stockage/detail_item/(?P<ref>[0-9]+)/$', views.get_list_stock_from_empl, name = 'module_stock_get_list_stock_from_empl'))

#TYPE_ARTICLE URLS
#=====================================
#TYPE_ARTICLE CRUD URLS
urlpatterns.append(url(r'^type_article/list', views.get_lister_type_article, name = 'module_stock_list_type_article'))
urlpatterns.append(url(r'^type_article/add', views.get_creer_type_article, name = 'module_stock_add_type_article'))
urlpatterns.append(url(r'^type_article/post_add', views.post_creer_type_article, name = 'module_stock_post_add_type_article'))
urlpatterns.append(url(r'^type_article/select/(?P<ref>[0-9]+)/$', views.get_select_type_article, name = 'module_stock_select_type_article'))
urlpatterns.append(url(r'^type_article/item/(?P<ref>[0-9]+)/$', views.get_details_type_article, name = 'module_stock_detail_type_article'))
urlpatterns.append(url(r'^type_article/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_article, name = 'module_stock_update_type_article'))
urlpatterns.append(url(r'^type_article/item/post_update/$', views.post_modifier_type_article, name = 'module_stock_post_update_type_article'))
urlpatterns.append(url(r'^type_article/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_type_article, name = 'module_stock_duplicate_type_article'))
urlpatterns.append(url(r'^type_article/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_type_article, name = 'module_stock_print_type_article'))
#TYPE_ARTICLE UPLOAD URLS
urlpatterns.append(url(r'^type_article/upload/add', views.get_upload_type_article, name = 'module_stock_get_upload_type_article'))
urlpatterns.append(url(r'^type_article/upload/post_add', views.post_upload_type_article, name = 'module_stock_post_upload_type_article'))

#TYPE_ARTICLE API URLS
urlpatterns.append(url(r'^api/type_article/list', views.get_list_type_article, name = 'module_stock_api_list_type_article'))
urlpatterns.append(url(r'^api/type_article/item', views.get_item_type_article, name = 'module_stock_api_item_type_article'))
urlpatterns.append(url(r'^api/type_article/create', views.post_create_type_article, name = 'module_stock_api_create_type_article'))

#TYPE_EMPLACEMENT URLS
#=====================================
#TYPE_EMPLACEMENT CRUD URLS
urlpatterns.append(url(r'^type_emplacement/list', views.get_lister_type_emplacement, name = 'module_stock_list_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/add', views.get_creer_type_emplacement, name = 'module_stock_add_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/post_add', views.post_creer_type_emplacement, name = 'module_stock_post_add_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/select/(?P<ref>[0-9]+)/$', views.get_select_type_emplacement, name = 'module_stock_select_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/item/(?P<ref>[0-9]+)/$', views.get_details_type_emplacement, name = 'module_stock_detail_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_emplacement, name = 'module_stock_update_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/item/post_update/$', views.post_modifier_type_emplacement, name = 'module_stock_post_update_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_type_emplacement, name = 'module_stock_duplicate_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_type_emplacement, name = 'module_stock_print_type_emplacement'))
#TYPE_EMPLACEMENT UPLOAD URLS
urlpatterns.append(url(r'^type_emplacement/upload/add', views.get_upload_type_emplacement, name = 'module_stock_get_upload_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/upload/post_add', views.post_upload_type_emplacement, name = 'module_stock_post_upload_type_emplacement'))

#TYPE_EMPLACEMENT API URLS
urlpatterns.append(url(r'^api/type_emplacement/list', views.get_list_type_emplacement, name = 'module_stock_api_list_type_emplacement'))
urlpatterns.append(url(r'^api/type_emplacement/item', views.get_item_type_emplacement, name = 'module_stock_api_item_type_emplacement'))
urlpatterns.append(url(r'^api/type_emplacement/create', views.post_create_type_emplacement, name = 'module_stock_api_create_type_emplacement'))

#TYPE_MVT_STOCK URLS
#=====================================
#TYPE_MVT_STOCK CRUD URLS
urlpatterns.append(url(r'^type_mvt_stock/list', views.get_lister_type_mvt_stock, name = 'module_stock_list_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/add', views.get_creer_type_mvt_stock, name = 'module_stock_add_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/post_add', views.post_creer_type_mvt_stock, name = 'module_stock_post_add_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/select/(?P<ref>[0-9]+)/$', views.get_select_type_mvt_stock, name = 'module_stock_select_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/item/(?P<ref>[0-9]+)/$', views.get_details_type_mvt_stock, name = 'module_stock_detail_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_mvt_stock, name = 'module_stock_update_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/item/post_update/$', views.post_modifier_type_mvt_stock, name = 'module_stock_post_update_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_type_mvt_stock, name = 'module_stock_duplicate_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_type_mvt_stock, name = 'module_stock_print_type_mvt_stock'))
#TYPE_MVT_STOCK UPLOAD URLS
urlpatterns.append(url(r'^type_mvt_stock/upload/add', views.get_upload_type_mvt_stock, name = 'module_stock_get_upload_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/upload/post_add', views.post_upload_type_mvt_stock, name = 'module_stock_post_upload_type_mvt_stock'))

#TYPE_MVT_STOCK API URLS
urlpatterns.append(url(r'^api/type_mvt_stock/list', views.get_list_type_mvt_stock, name = 'module_stock_api_list_type_mvt_stock'))
urlpatterns.append(url(r'^api/type_mvt_stock/item', views.get_item_type_mvt_stock, name = 'module_stock_api_item_type_mvt_stock'))
urlpatterns.append(url(r'^api/type_mvt_stock/create', views.post_create_type_mvt_stock, name = 'module_stock_api_create_type_mvt_stock'))

#UNITE_MESURE URLS
#=====================================
#UNITE_MESURE CRUD URLS
urlpatterns.append(url(r'^unite_mesure/list', views.get_lister_unite_mesure, name = 'module_stock_list_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/add', views.get_creer_unite_mesure, name = 'module_stock_add_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/post_add', views.post_creer_unite_mesure, name = 'module_stock_post_add_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/select/(?P<ref>[0-9]+)/$', views.get_select_unite_mesure, name = 'module_stock_select_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/item/(?P<ref>[0-9]+)/$', views.get_details_unite_mesure, name = 'module_stock_detail_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/item/(?P<ref>[0-9]+)/update$', views.get_modifier_unite_mesure, name = 'module_stock_update_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/item/post_update/$', views.post_modifier_unite_mesure, name = 'module_stock_post_update_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_unite_mesure, name = 'module_stock_duplicate_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_unite_mesure, name = 'module_stock_print_unite_mesure'))
#UNITE_MESURE UPLOAD URLS
urlpatterns.append(url(r'^unite_mesure/upload/add', views.get_upload_unite_mesure, name = 'module_stock_get_upload_unite_mesure'))
urlpatterns.append(url(r'^unite_mesure/upload/post_add', views.post_upload_unite_mesure, name = 'module_stock_post_upload_unite_mesure'))

#UNITE_MESURE API URLS
urlpatterns.append(url(r'^api/unite_mesure/list', views.get_list_unite_mesure, name = 'module_stock_api_list_unite_mesure'))
urlpatterns.append(url(r'^api/unite_mesure/item', views.get_item_unite_mesure, name = 'module_stock_api_item_unite_mesure'))
urlpatterns.append(url(r'^api/unite_mesure/create', views.post_create_unite_mesure, name = 'module_stock_api_create_unite_mesure'))

#STATUT_OPERATION_STOCK URLS
#=====================================
#STATUT_OPERATION_STOCK CRUD URLS
urlpatterns.append(url(r'^statut_operation_stock/list', views.get_lister_statut_operation_stock, name = 'module_stock_list_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/add', views.get_creer_statut_operation_stock, name = 'module_stock_add_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/post_add', views.post_creer_statut_operation_stock, name = 'module_stock_post_add_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/select/(?P<ref>[0-9]+)/$', views.get_select_statut_operation_stock, name = 'module_stock_select_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/item/(?P<ref>[0-9]+)/$', views.get_details_statut_operation_stock, name = 'module_stock_detail_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_statut_operation_stock, name = 'module_stock_update_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/item/post_update/$', views.post_modifier_statut_operation_stock, name = 'module_stock_post_update_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_statut_operation_stock, name = 'module_stock_duplicate_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_statut_operation_stock, name = 'module_stock_print_statut_operation_stock'))
#STATUT_OPERATION_STOCK UPLOAD URLS
urlpatterns.append(url(r'^statut_operation_stock/upload/add', views.get_upload_statut_operation_stock, name = 'module_stock_get_upload_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/upload/post_add', views.post_upload_statut_operation_stock, name = 'module_stock_post_upload_statut_operation_stock'))

#STATUT_OPERATION_STOCK API URLS
urlpatterns.append(url(r'^api/statut_operation_stock/list', views.get_list_statut_operation_stock, name = 'module_stock_api_list_statut_operation_stock'))
urlpatterns.append(url(r'^api/statut_operation_stock/item', views.get_item_statut_operation_stock, name = 'module_stock_api_item_statut_operation_stock'))
urlpatterns.append(url(r'^api/statut_operation_stock/create', views.post_create_statut_operation_stock, name = 'module_stock_api_create_statut_operation_stock'))

#STATUT_AJUSTEMENT URLS
#=====================================
#STATUT_AJUSTEMENT CRUD URLS
urlpatterns.append(url(r'^statut_ajustement/list', views.get_lister_statut_ajustement, name = 'module_stock_list_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/add', views.get_creer_statut_ajustement, name = 'module_stock_add_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/post_add', views.post_creer_statut_ajustement, name = 'module_stock_post_add_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/select/(?P<ref>[0-9]+)/$', views.get_select_statut_ajustement, name = 'module_stock_select_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/item/(?P<ref>[0-9]+)/$', views.get_details_statut_ajustement, name = 'module_stock_detail_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_statut_ajustement, name = 'module_stock_update_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/item/post_update/$', views.post_modifier_statut_ajustement, name = 'module_stock_post_update_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_statut_ajustement, name = 'module_stock_duplicate_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_statut_ajustement, name = 'module_stock_print_statut_ajustement'))
#STATUT_AJUSTEMENT UPLOAD URLS
urlpatterns.append(url(r'^statut_ajustement/upload/add', views.get_upload_statut_ajustement, name = 'module_stock_get_upload_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/upload/post_add', views.post_upload_statut_ajustement, name = 'module_stock_post_upload_statut_ajustement'))

#STATUT_AJUSTEMENT API URLS
urlpatterns.append(url(r'^api/statut_ajustement/list', views.get_list_statut_ajustement, name = 'module_stock_api_list_statut_ajustement'))
urlpatterns.append(url(r'^api/statut_ajustement/item', views.get_item_statut_ajustement, name = 'module_stock_api_item_statut_ajustement'))
urlpatterns.append(url(r'^api/statut_ajustement/create', views.post_create_statut_ajustement, name = 'module_stock_api_create_statut_ajustement'))

#REBUT URLS
#=====================================
#REBUT CRUD URLS
urlpatterns.append(url(r'^rebut/list', views.get_lister_rebut, name = 'module_stock_list_rebut'))
urlpatterns.append(url(r'^rebut/add', views.get_creer_rebut, name = 'module_stock_add_rebut'))
urlpatterns.append(url(r'^rebut/post_add', views.post_creer_rebut, name = 'module_stock_post_add_rebut'))
urlpatterns.append(url(r'^rebut/select/(?P<ref>[0-9]+)/$', views.get_select_rebut, name = 'module_stock_select_rebut'))
urlpatterns.append(url(r'^rebut/item/(?P<ref>[0-9]+)/$', views.get_details_rebut, name = 'module_stock_detail_rebut'))
urlpatterns.append(url(r'^rebut/item/(?P<ref>[0-9]+)/update$', views.get_modifier_rebut, name = 'module_stock_update_rebut'))
urlpatterns.append(url(r'^rebut/item/post_update/$', views.post_modifier_rebut, name = 'module_stock_post_update_rebut'))
urlpatterns.append(url(r'^rebut/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_rebut, name = 'module_stock_duplicate_rebut'))
urlpatterns.append(url(r'^rebut/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_rebut, name = 'module_stock_print_rebut'))
#REBUT UPLOAD URLS
urlpatterns.append(url(r'^rebut/upload/add', views.get_upload_rebut, name = 'module_stock_get_upload_rebut'))
urlpatterns.append(url(r'^rebut/upload/post_add', views.post_upload_rebut, name = 'module_stock_post_upload_rebut'))

#REBUT BI URLS
urlpatterns.append(url(r'^rebut/bi', views.get_bi_rebut, name = 'module_stock_bi_rebut'))

#REBUT API URLS
urlpatterns.append(url(r'^api/rebut/list', views.get_list_rebut, name = 'module_stock_api_list_rebut'))
urlpatterns.append(url(r'^api/rebut/item', views.get_item_rebut, name = 'module_stock_api_item_rebut'))
urlpatterns.append(url(r'^api/rebut/create', views.post_create_rebut, name = 'module_stock_api_create_rebut'))

#OPERATION_STOCK URLS
#=====================================
#OPERATION_STOCK CRUD URLS
urlpatterns.append(url(r'^operation_stock/list', views.get_lister_operation_stock, name = 'module_stock_list_operation_stock'))
urlpatterns.append(url(r'^operation_stock/add', views.get_creer_operation_stock, name = 'module_stock_add_operation_stock'))
urlpatterns.append(url(r'^operation_stock/post_add', views.post_creer_operation_stock, name = 'module_stock_post_add_operation_stock'))
urlpatterns.append(url(r'^operation_stock/select/(?P<ref>[0-9]+)/$', views.get_select_operation_stock, name = 'module_stock_select_operation_stock'))
urlpatterns.append(url(r'^operation_stock/item/(?P<ref>[0-9]+)/$', views.get_details_operation_stock, name = 'module_stock_detail_operation_stock'))
urlpatterns.append(url(r'^operation_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_operation_stock, name = 'module_stock_update_operation_stock'))
urlpatterns.append(url(r'^operation_stock/item/post_update/$', views.post_modifier_operation_stock, name = 'module_stock_post_update_operation_stock'))
urlpatterns.append(url(r'^operation_stock/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_operation_stock, name = 'module_stock_duplicate_operation_stock'))
urlpatterns.append(url(r'^operation_stock/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_operation_stock, name = 'module_stock_print_operation_stock'))
#OPERATION_STOCK UPLOAD URLS
urlpatterns.append(url(r'^operation_stock/upload/add', views.get_upload_operation_stock, name = 'module_stock_get_upload_operation_stock'))
urlpatterns.append(url(r'^operation_stock/upload/post_add', views.post_upload_operation_stock, name = 'module_stock_post_upload_operation_stock'))

#OPERATION_STOCK API URLS
urlpatterns.append(url(r'^api/operation_stock/list', views.get_list_operation_stock, name = 'module_stock_api_list_operation_stock'))
urlpatterns.append(url(r'^api/operation_stock/item', views.get_item_operation_stock, name = 'module_stock_api_item_operation_stock'))
urlpatterns.append(url(r'^api/operation_stock/create', views.post_create_operation_stock, name = 'module_stock_api_create_operation_stock'))

#MVT_STOCK URLS
#=====================================
#MVT_STOCK CRUD URLS
urlpatterns.append(url(r'^mvt_stock/list', views.get_lister_mvt_stock, name = 'module_stock_list_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/add', views.get_creer_mvt_stock, name = 'module_stock_add_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/post_add', views.post_creer_mvt_stock, name = 'module_stock_post_add_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/select/(?P<ref>[0-9]+)/$', views.get_select_mvt_stock, name = 'module_stock_select_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/item/(?P<ref>[0-9]+)/$', views.get_details_mvt_stock, name = 'module_stock_detail_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_mvt_stock, name = 'module_stock_update_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/item/post_update/$', views.post_modifier_mvt_stock, name = 'module_stock_post_update_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_mvt_stock, name = 'module_stock_duplicate_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_mvt_stock, name = 'module_stock_print_mvt_stock'))
#MVT_STOCK UPLOAD URLS
urlpatterns.append(url(r'^mvt_stock/upload/add', views.get_upload_mvt_stock, name = 'module_stock_get_upload_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/upload/post_add', views.post_upload_mvt_stock, name = 'module_stock_post_upload_mvt_stock'))

#MVT_STOCK BI URLS
urlpatterns.append(url(r'^mvt_stock/bi', views.get_bi_mvt_stock, name = 'module_stock_bi_mvt_stock'))

#MVT_STOCK API URLS
urlpatterns.append(url(r'^api/mvt_stock/list', views.get_list_mvt_stock, name = 'module_stock_api_list_mvt_stock'))
urlpatterns.append(url(r'^api/mvt_stock/item', views.get_item_mvt_stock, name = 'module_stock_api_item_mvt_stock'))
urlpatterns.append(url(r'^api/mvt_stock/create', views.post_create_mvt_stock, name = 'module_stock_api_create_mvt_stock'))

#LIGNE_RECEPTION URLS
#=====================================
#LIGNE_RECEPTION CRUD URLS
urlpatterns.append(url(r'^ligne_reception/list', views.get_lister_ligne_reception, name = 'module_stock_list_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/add', views.get_creer_ligne_reception, name = 'module_stock_add_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/post_add', views.post_creer_ligne_reception, name = 'module_stock_post_add_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/select/(?P<ref>[0-9]+)/$', views.get_select_ligne_reception, name = 'module_stock_select_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_reception, name = 'module_stock_detail_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ligne_reception, name = 'module_stock_update_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/item/post_update/$', views.post_modifier_ligne_reception, name = 'module_stock_post_update_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_ligne_reception, name = 'module_stock_duplicate_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_ligne_reception, name = 'module_stock_print_ligne_reception'))
#LIGNE_RECEPTION UPLOAD URLS
urlpatterns.append(url(r'^ligne_reception/upload/add', views.get_upload_ligne_reception, name = 'module_stock_get_upload_ligne_reception'))
urlpatterns.append(url(r'^ligne_reception/upload/post_add', views.post_upload_ligne_reception, name = 'module_stock_post_upload_ligne_reception'))

#LIGNE_RECEPTION API URLS
urlpatterns.append(url(r'^api/ligne_reception/list', views.get_list_ligne_reception, name = 'module_stock_api_list_ligne_reception'))
urlpatterns.append(url(r'^api/ligne_reception/item', views.get_item_ligne_reception, name = 'module_stock_api_item_ligne_reception'))
urlpatterns.append(url(r'^api/ligne_reception/create', views.post_create_ligne_reception, name = 'module_stock_api_create_ligne_reception'))

#LIGNE_BON_TRANSFERT URLS
#=====================================
#LIGNE_BON_TRANSFERT CRUD URLS
urlpatterns.append(url(r'^ligne_bon_transfert/list', views.get_lister_ligne_bon_transfert, name = 'module_stock_list_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/add', views.get_creer_ligne_bon_transfert, name = 'module_stock_add_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/post_add', views.post_creer_ligne_bon_transfert, name = 'module_stock_post_add_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/select/(?P<ref>[0-9]+)/$', views.get_select_ligne_bon_transfert, name = 'module_stock_select_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_bon_transfert, name = 'module_stock_detail_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ligne_bon_transfert, name = 'module_stock_update_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/item/post_update/$', views.post_modifier_ligne_bon_transfert, name = 'module_stock_post_update_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_ligne_bon_transfert, name = 'module_stock_duplicate_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_ligne_bon_transfert, name = 'module_stock_print_ligne_bon_transfert'))
#LIGNE_BON_TRANSFERT UPLOAD URLS
urlpatterns.append(url(r'^ligne_bon_transfert/upload/add', views.get_upload_ligne_bon_transfert, name = 'module_stock_get_upload_ligne_bon_transfert'))
urlpatterns.append(url(r'^ligne_bon_transfert/upload/post_add', views.post_upload_ligne_bon_transfert, name = 'module_stock_post_upload_ligne_bon_transfert'))

#LIGNE_BON_TRANSFERT API URLS
urlpatterns.append(url(r'^api/ligne_bon_transfert/list', views.get_list_ligne_bon_transfert, name = 'module_stock_api_list_ligne_bon_transfert'))
urlpatterns.append(url(r'^api/ligne_bon_transfert/item', views.get_item_ligne_bon_transfert, name = 'module_stock_api_item_ligne_bon_transfert'))
urlpatterns.append(url(r'^api/ligne_bon_transfert/create', views.post_create_ligne_bon_transfert, name = 'module_stock_api_create_ligne_bon_transfert'))

#LIGNE_BON_SORTIE URLS
#=====================================
#LIGNE_BON_SORTIE CRUD URLS
urlpatterns.append(url(r'^ligne_bon_sortie/list', views.get_lister_ligne_bon_sortie, name = 'module_stock_list_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/add', views.get_creer_ligne_bon_sortie, name = 'module_stock_add_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/post_add', views.post_creer_ligne_bon_sortie, name = 'module_stock_post_add_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/select/(?P<ref>[0-9]+)/$', views.get_select_ligne_bon_sortie, name = 'module_stock_select_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_bon_sortie, name = 'module_stock_detail_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ligne_bon_sortie, name = 'module_stock_update_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/item/post_update/$', views.post_modifier_ligne_bon_sortie, name = 'module_stock_post_update_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_ligne_bon_sortie, name = 'module_stock_duplicate_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_ligne_bon_sortie, name = 'module_stock_print_ligne_bon_sortie'))
#LIGNE_BON_SORTIE UPLOAD URLS
urlpatterns.append(url(r'^ligne_bon_sortie/upload/add', views.get_upload_ligne_bon_sortie, name = 'module_stock_get_upload_ligne_bon_sortie'))
urlpatterns.append(url(r'^ligne_bon_sortie/upload/post_add', views.post_upload_ligne_bon_sortie, name = 'module_stock_post_upload_ligne_bon_sortie'))

#LIGNE_BON_SORTIE API URLS
urlpatterns.append(url(r'^api/ligne_bon_sortie/list', views.get_list_ligne_bon_sortie, name = 'module_stock_api_list_ligne_bon_sortie'))
urlpatterns.append(url(r'^api/ligne_bon_sortie/item', views.get_item_ligne_bon_sortie, name = 'module_stock_api_item_ligne_bon_sortie'))
urlpatterns.append(url(r'^api/ligne_bon_sortie/create', views.post_create_ligne_bon_sortie, name = 'module_stock_api_create_ligne_bon_sortie'))

#LIGNE_AJUSTEMENT URLS
#=====================================
#LIGNE_AJUSTEMENT CRUD URLS
urlpatterns.append(url(r'^ligne_ajustement/list', views.get_lister_ligne_ajustement, name = 'module_stock_list_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/add', views.get_creer_ligne_ajustement, name = 'module_stock_add_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/post_add', views.post_creer_ligne_ajustement, name = 'module_stock_post_add_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/select/(?P<ref>[0-9]+)/$', views.get_select_ligne_ajustement, name = 'module_stock_select_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_ajustement, name = 'module_stock_detail_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ligne_ajustement, name = 'module_stock_update_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/item/post_update/$', views.post_modifier_ligne_ajustement, name = 'module_stock_post_update_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_ligne_ajustement, name = 'module_stock_duplicate_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_ligne_ajustement, name = 'module_stock_print_ligne_ajustement'))
#LIGNE_AJUSTEMENT UPLOAD URLS
urlpatterns.append(url(r'^ligne_ajustement/upload/add', views.get_upload_ligne_ajustement, name = 'module_stock_get_upload_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/upload/post_add', views.post_upload_ligne_ajustement, name = 'module_stock_post_upload_ligne_ajustement'))

#LIGNE_AJUSTEMENT API URLS
urlpatterns.append(url(r'^api/ligne_ajustement/list', views.get_list_ligne_ajustement, name = 'module_stock_api_list_ligne_ajustement'))
urlpatterns.append(url(r'^api/ligne_ajustement/item', views.get_item_ligne_ajustement, name = 'module_stock_api_item_ligne_ajustement'))
urlpatterns.append(url(r'^api/ligne_ajustement/create', views.post_create_ligne_ajustement, name = 'module_stock_api_create_ligne_ajustement'))

#EMPLACEMENT URLS
#=====================================
#EMPLACEMENT CRUD URLS
urlpatterns.append(url(r'^emplacement/list', views.get_lister_emplacement, name = 'module_stock_list_emplacement'))
urlpatterns.append(url(r'^emplacement/add', views.get_creer_emplacement, name = 'module_stock_add_emplacement'))
urlpatterns.append(url(r'^emplacement/post_add', views.post_creer_emplacement, name = 'module_stock_post_add_emplacement'))
urlpatterns.append(url(r'^emplacement/select/(?P<ref>[0-9]+)/$', views.get_select_emplacement, name = 'module_stock_select_emplacement'))
urlpatterns.append(url(r'^emplacement/item/(?P<ref>[0-9]+)/$', views.get_details_emplacement, name = 'module_stock_detail_emplacement'))
urlpatterns.append(url(r'^emplacement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_emplacement, name = 'module_stock_update_emplacement'))
urlpatterns.append(url(r'^emplacement/item/post_update/$', views.post_modifier_emplacement, name = 'module_stock_post_update_emplacement'))
urlpatterns.append(url(r'^emplacement/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_emplacement, name = 'module_stock_duplicate_emplacement'))
urlpatterns.append(url(r'^emplacement/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_emplacement, name = 'module_stock_print_emplacement'))
#EMPLACEMENT UPLOAD URLS
urlpatterns.append(url(r'^emplacement/upload/add', views.get_upload_emplacement, name = 'module_stock_get_upload_emplacement'))
urlpatterns.append(url(r'^emplacement/upload/post_add', views.post_upload_emplacement, name = 'module_stock_post_upload_emplacement'))

#EMPLACEMENT BI URLS
urlpatterns.append(url(r'^emplacement/bi', views.get_bi_emplacement, name = 'module_stock_bi_emplacement'))

#EMPLACEMENT API URLS
urlpatterns.append(url(r'^api/emplacement/list', views.get_list_emplacement, name = 'module_stock_api_list_emplacement'))
urlpatterns.append(url(r'^api/emplacement/item', views.get_item_emplacement, name = 'module_stock_api_item_emplacement'))
urlpatterns.append(url(r'^api/emplacement/create', views.post_create_emplacement, name = 'module_stock_api_create_emplacement'))

#CATEGORIE URLS
#=====================================
#CATEGORIE CRUD URLS
urlpatterns.append(url(r'^categorie/list', views.get_lister_categorie, name = 'module_stock_list_categorie'))
urlpatterns.append(url(r'^categorie/add', views.get_creer_categorie, name = 'module_stock_add_categorie'))
urlpatterns.append(url(r'^categorie/post_add', views.post_creer_categorie, name = 'module_stock_post_add_categorie'))
urlpatterns.append(url(r'^categorie/select/(?P<ref>[0-9]+)/$', views.get_select_categorie, name = 'module_stock_select_categorie'))
urlpatterns.append(url(r'^categorie/item/(?P<ref>[0-9]+)/$', views.get_details_categorie, name = 'module_stock_detail_categorie'))
urlpatterns.append(url(r'^categorie/item/(?P<ref>[0-9]+)/update$', views.get_modifier_categorie, name = 'module_stock_update_categorie'))
urlpatterns.append(url(r'^categorie/item/post_update/$', views.post_modifier_categorie, name = 'module_stock_post_update_categorie'))
urlpatterns.append(url(r'^categorie/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_categorie, name = 'module_stock_duplicate_categorie'))
urlpatterns.append(url(r'^categorie/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_categorie, name = 'module_stock_print_categorie'))
#CATEGORIE UPLOAD URLS
urlpatterns.append(url(r'^categorie/upload/add', views.get_upload_categorie, name = 'module_stock_get_upload_categorie'))
urlpatterns.append(url(r'^categorie/upload/post_add', views.post_upload_categorie, name = 'module_stock_post_upload_categorie'))

#CATEGORIE API URLS
urlpatterns.append(url(r'^api/categorie/list', views.get_list_categorie, name = 'module_stock_api_list_categorie'))
urlpatterns.append(url(r'^api/categorie/item', views.get_item_categorie, name = 'module_stock_api_item_categorie'))
urlpatterns.append(url(r'^api/categorie/create', views.post_create_categorie, name = 'module_stock_api_create_categorie'))

#BON_TRANSFERT URLS
#=====================================
#BON_TRANSFERT CRUD URLS
urlpatterns.append(url(r'^bon_transfert/list', views.get_lister_bon_transfert, name = 'module_stock_list_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/add', views.get_creer_bon_transfert, name = 'module_stock_add_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/post_add', views.post_creer_bon_transfert, name = 'module_stock_post_add_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/select/(?P<ref>[0-9]+)/$', views.get_select_bon_transfert, name = 'module_stock_select_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/(?P<ref>[0-9]+)/$', views.get_details_bon_transfert, name = 'module_stock_detail_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/(?P<ref>[0-9]+)/update$', views.get_modifier_bon_transfert, name = 'module_stock_update_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/post_update/$', views.post_modifier_bon_transfert, name = 'module_stock_post_update_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_bon_transfert, name = 'module_stock_duplicate_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_bon_transfert, name = 'module_stock_print_bon_transfert'))
#BON_TRANSFERT UPLOAD URLS
urlpatterns.append(url(r'^bon_transfert/upload/add', views.get_upload_bon_transfert, name = 'module_stock_get_upload_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/upload/post_add', views.post_upload_bon_transfert, name = 'module_stock_post_upload_bon_transfert'))

#BON_TRANSFERT API URLS
urlpatterns.append(url(r'^api/bon_transfert/list', views.get_list_bon_transfert, name = 'module_stock_api_list_bon_transfert'))
urlpatterns.append(url(r'^api/bon_transfert/item', views.get_item_bon_transfert, name = 'module_stock_api_item_bon_transfert'))
urlpatterns.append(url(r'^api/bon_transfert/create', views.post_create_bon_transfert, name = 'module_stock_api_create_bon_transfert'))

#BON_SORTIE URLS
#=====================================
#BON_SORTIE CRUD URLS
urlpatterns.append(url(r'^bon_sortie/list', views.get_lister_bon_sortie, name = 'module_stock_list_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/add', views.get_creer_bon_sortie, name = 'module_stock_add_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/post_add', views.post_creer_bon_sortie, name = 'module_stock_post_add_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/select/(?P<ref>[0-9]+)/$', views.get_select_bon_sortie, name = 'module_stock_select_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/item/(?P<ref>[0-9]+)/$', views.get_details_bon_sortie, name = 'module_stock_detail_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/item/(?P<ref>[0-9]+)/update$', views.get_modifier_bon_sortie, name = 'module_stock_update_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/item/post_update/$', views.post_modifier_bon_sortie, name = 'module_stock_post_update_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_bon_sortie, name = 'module_stock_duplicate_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_bon_sortie, name = 'module_stock_print_bon_sortie'))
#BON_SORTIE UPLOAD URLS
urlpatterns.append(url(r'^bon_sortie/upload/add', views.get_upload_bon_sortie, name = 'module_stock_get_upload_bon_sortie'))
urlpatterns.append(url(r'^bon_sortie/upload/post_add', views.post_upload_bon_sortie, name = 'module_stock_post_upload_bon_sortie'))

#BON_SORTIE BI URLS
urlpatterns.append(url(r'^bon_sortie/bi', views.get_bi_bon_sortie, name = 'module_stock_bi_bon_sortie'))

#BON_SORTIE API URLS
urlpatterns.append(url(r'^api/bon_sortie/list', views.get_list_bon_sortie, name = 'module_stock_api_list_bon_sortie'))
urlpatterns.append(url(r'^api/bon_sortie/item', views.get_item_bon_sortie, name = 'module_stock_api_item_bon_sortie'))
urlpatterns.append(url(r'^api/bon_sortie/create', views.post_create_bon_sortie, name = 'module_stock_api_create_bon_sortie'))

#BON_RECEPTION URLS
#=====================================
#BON_RECEPTION CRUD URLS
urlpatterns.append(url(r'^bon_reception/list', views.get_lister_bon_reception, name = 'module_stock_list_bon_reception'))
urlpatterns.append(url(r'^bon_reception/add', views.get_creer_bon_reception, name = 'module_stock_add_bon_reception'))
urlpatterns.append(url(r'^bon_reception/post_add', views.post_creer_bon_reception, name = 'module_stock_post_add_bon_reception'))
urlpatterns.append(url(r'^bon_reception/select/(?P<ref>[0-9]+)/$', views.get_select_bon_reception, name = 'module_stock_select_bon_reception'))
urlpatterns.append(url(r'^bon_reception/item/(?P<ref>[0-9]+)/$', views.get_details_bon_reception, name = 'module_stock_detail_bon_reception'))
urlpatterns.append(url(r'^bon_reception/item/(?P<ref>[0-9]+)/update$', views.get_modifier_bon_reception, name = 'module_stock_update_bon_reception'))
urlpatterns.append(url(r'^bon_reception/item/post_update/$', views.post_modifier_bon_reception, name = 'module_stock_post_update_bon_reception'))
urlpatterns.append(url(r'^bon_reception/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_bon_reception, name = 'module_stock_duplicate_bon_reception'))
urlpatterns.append(url(r'^bon_reception/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_bon_reception, name = 'module_stock_print_bon_reception'))
#BON_RECEPTION UPLOAD URLS
urlpatterns.append(url(r'^bon_reception/upload/add', views.get_upload_bon_reception, name = 'module_stock_get_upload_bon_reception'))
urlpatterns.append(url(r'^bon_reception/upload/post_add', views.post_upload_bon_reception, name = 'module_stock_post_upload_bon_reception'))

#BON_RECEPTION BI URLS
urlpatterns.append(url(r'^bon_reception/bi', views.get_bi_bon_reception, name = 'module_stock_bi_bon_reception'))

#BON_RECEPTION API URLS
urlpatterns.append(url(r'^api/bon_reception/list', views.get_list_bon_reception, name = 'module_stock_api_list_bon_reception'))
urlpatterns.append(url(r'^api/bon_reception/item', views.get_item_bon_reception, name = 'module_stock_api_item_bon_reception'))
urlpatterns.append(url(r'^api/bon_reception/create', views.post_create_bon_reception, name = 'module_stock_api_create_bon_reception'))

#AJUSTEMENT URLS
#=====================================
#AJUSTEMENT CRUD URLS
urlpatterns.append(url(r'^ajustement/list', views.get_lister_ajustement, name = 'module_stock_list_ajustement'))
urlpatterns.append(url(r'^ajustement/add', views.get_creer_ajustement, name = 'module_stock_add_ajustement'))
urlpatterns.append(url(r'^ajustement/post_add', views.post_creer_ajustement, name = 'module_stock_post_add_ajustement'))
urlpatterns.append(url(r'^ajustement/select/(?P<ref>[0-9]+)/$', views.get_select_ajustement, name = 'module_stock_select_ajustement'))
urlpatterns.append(url(r'^ajustement/item/(?P<ref>[0-9]+)/$', views.get_details_ajustement, name = 'module_stock_detail_ajustement'))
urlpatterns.append(url(r'^ajustement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ajustement, name = 'module_stock_update_ajustement'))
urlpatterns.append(url(r'^ajustement/item/post_update/$', views.post_modifier_ajustement, name = 'module_stock_post_update_ajustement'))
urlpatterns.append(url(r'^ajustement/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_ajustement, name = 'module_stock_duplicate_ajustement'))
urlpatterns.append(url(r'^ajustement/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_ajustement, name = 'module_stock_print_ajustement'))
#AJUSTEMENT UPLOAD URLS
urlpatterns.append(url(r'^ajustement/upload/add', views.get_upload_ajustement, name = 'module_stock_get_upload_ajustement'))
urlpatterns.append(url(r'^ajustement/upload/post_add', views.post_upload_ajustement, name = 'module_stock_post_upload_ajustement'))

#AJUSTEMENT BI URLS
urlpatterns.append(url(r'^ajustement/bi', views.get_bi_ajustement, name = 'module_stock_bi_ajustement'))

#AJUSTEMENT API URLS
urlpatterns.append(url(r'^api/ajustement/list', views.get_list_ajustement, name = 'module_stock_api_list_ajustement'))
urlpatterns.append(url(r'^api/ajustement/item', views.get_item_ajustement, name = 'module_stock_api_item_ajustement'))
urlpatterns.append(url(r'^api/ajustement/create', views.post_create_ajustement, name = 'module_stock_api_create_ajustement'))

urlpatterns.append(url(r'^ajustement/cloturer_ajustement/post_add', views.post_cloturer_ajustement, name = 'module_stock_post_cloturer_ajustement'))

#ACTIF URLS
#=====================================
#ACTIF CRUD URLS
urlpatterns.append(url(r'^actif/list', views.get_lister_actif, name = 'module_stock_list_actif'))
urlpatterns.append(url(r'^actif/add', views.get_creer_actif, name = 'module_stock_add_actif'))
urlpatterns.append(url(r'^actif/post_add', views.post_creer_actif, name = 'module_stock_post_add_actif'))
urlpatterns.append(url(r'^actif/select/(?P<ref>[0-9]+)/$', views.get_select_actif, name = 'module_stock_select_actif'))
urlpatterns.append(url(r'^actif/item/(?P<ref>[0-9]+)/$', views.get_details_actif, name = 'module_stock_detail_actif'))
urlpatterns.append(url(r'^actif/item/(?P<ref>[0-9]+)/update$', views.get_modifier_actif, name = 'module_stock_update_actif'))
urlpatterns.append(url(r'^actif/item/post_update/$', views.post_modifier_actif, name = 'module_stock_post_update_actif'))
urlpatterns.append(url(r'^actif/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_actif, name = 'module_stock_duplicate_actif'))
urlpatterns.append(url(r'^actif/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_actif, name = 'module_stock_print_actif'))
#ACTIF UPLOAD URLS
urlpatterns.append(url(r'^actif/upload/add', views.get_upload_actif, name = 'module_stock_get_upload_actif'))
urlpatterns.append(url(r'^actif/upload/post_add', views.post_upload_actif, name = 'module_stock_post_upload_actif'))

#ACTIF BI URLS
urlpatterns.append(url(r'^actif/bi', views.get_bi_actif, name = 'module_stock_bi_actif'))

#ACTIF API URLS
urlpatterns.append(url(r'^api/actif/list', views.get_list_actif, name = 'module_stock_api_list_actif'))
urlpatterns.append(url(r'^api/actif/item', views.get_item_actif, name = 'module_stock_api_item_actif'))
urlpatterns.append(url(r'^api/actif/create', views.post_create_actif, name = 'module_stock_api_create_actif'))
