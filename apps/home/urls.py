# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
path('Dash/<str:file_name>', views.index, name='home'),
 path('upload/', views.uploads, name='upload'),
 path('tables/<str:table_name>', views.tables, name='tables'),
 path('dashboard/', views.dashboard_with_pivot, name='dashboard_with_pivot'),
 path('data/', views.pivot_data, name='pivot_data'),
 path('ALLSEARCH', views.ALLSEARCH, name='ALLSEARCH'),
 path('delete/<str:model_name>/<int:id>', views.delete_row, name='delete'),
 path('filter/<str:model_name>/<str:f>/<str:order>', views.filter, name='filter'),
 path('RangeFilters/<str:model_name>/<str:f>/<str:qrange>', views.RangeFilterss, name='RangeFilters'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
   

]
