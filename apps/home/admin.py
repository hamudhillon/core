# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import data,global_box, ksa_tv, prod_companies, series
# Register your models here.



admin.site.register(data)
admin.site.register(global_box)
admin.site.register(series)
admin.site.register(ksa_tv)
admin.site.register(prod_companies)