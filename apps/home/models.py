# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class data(models.Model):
    Rank=models.IntegerField(default=0)
    FILM=models.CharField(default='',null=True,max_length=100)
    Genre=models.CharField(default='',null=True,max_length=100)
    Sub_Genre_1=models.CharField(default='',null=True,max_length=100)
    Sub_Genre_2=models.CharField(default='',null=True,max_length=100)
    Rating=models.CharField(default='',null=True,max_length=100)
    Year_of_Release =models.CharField(default='',null=True,max_length=100)
    Country =models.CharField(default='',null=True,max_length=100)
    Run_Time=models.CharField(default='',null=True,max_length=100)
    Franchise=models.CharField(default='',null=True,max_length=100)
    Synopsis =models.CharField(default='',null=True,max_length=100)
    Keywords_1=models.CharField(default='',null=True,max_length=100)
    Keywords_2=models.CharField(default='',null=True,max_length=100)
    Keywords_3=models.CharField(default='',null=True,max_length=100)
    Keywords_4=models.CharField(default='',null=True,max_length=100)
    Production_Method =models.CharField(default='',null=True,max_length=100)
    Creative_Type =models.CharField(default='',null=True,max_length=100)
    Production_Companies=models.CharField(default='',null=True,max_length=100)
    Production_Company_1=models.CharField(default='',null=True,max_length=100)
    Production_Company_2=models.CharField(default='',null=True,max_length=100)
    Production_Company_3=models.CharField(default='',null=True,max_length=100)
    Production_Company_4=models.CharField(default='',null=True,max_length=100)
    Director=models.CharField(default='',null=True,max_length=100)
    Lead_Actor_1_Name =models.CharField(default='',null=True,max_length=100)
    Lead_Actor_1_Gender=models.CharField(default='',null=True,max_length=100)
    Lead_Actor_1_Age =models.CharField(default='',null=True,max_length=100)
    Lead_Actor_1_Nationality=models.CharField(default='',null=True,max_length=100)
    Lead_Actor_2_Name =models.CharField(default='',null=True,max_length=100)
    Lead_Actor_2_Gender=models.CharField(default='',null=True,max_length=100)
    Lead_Actor_2_Age =models.CharField(default='',null=True,max_length=100)
    Lead_Actor_2_Nationality=models.CharField(default='',null=True,max_length=100)
    Target_Audience =models.CharField(default='',null=True,max_length=100)
    Streamer =models.CharField(default='',null=True,max_length=100)
    Awards_1  =models.CharField(default='',null=True,max_length=100)
    Awards_2  =models.CharField(default='',null=True,max_length=100)
    Awards_3  =models.CharField(default='',null=True,max_length=100)
    Type_of_Deal =models.CharField(default='',null=True,max_length=100)
    RELEASE_DATE  =models.CharField(default='',null=True,max_length=100)
    DIST  =models.CharField(default='',null=True,max_length=100)
    NO_Screens  =models.CharField(default='',null=True,max_length=100)
    Opening_Day_Amd  =models.CharField(default='',null=True,max_length=100)
    First_Weekend_BO  =models.CharField(default='',null=True,max_length=100)
    First_Weekend_Amd  =models.CharField(default='',null=True,max_length=100)
    First_Week_BO  =models.CharField(default='',null=True,max_length=100)
    First_Week_ADM  =models.CharField(default='',null=True,max_length=100)
    CUM_BO  =models.CharField(default='',null=True,max_length=100)
    CUM_ADM  =models.CharField(default='',null=True,max_length=100)
    CUM_GBO_USD  =models.CharField(default='',null=True,max_length=100)