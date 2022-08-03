# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
import pandas as pd
from .models import data

@login_required(login_url="/login/")
def index(request):
    
    d=data.objects.values()

    return render(request,'home/index.html',{'data':d})


@login_required(login_url="/login/")
def uploads(request):

    if request.method=='POST':
        
        for f in request.FILES.getlist('files'):
            print(f)
            df=pd.read_excel(f,engine='openpyxl')
            df.columns = [c.strip().replace('  ',' ').replace('.','').replace('1st','First') for c in df.columns.values.tolist()]
            print(df)
            print(df['Genre'])
            for i in df.index:
                ob=data()
                ob.Rank=int(df.loc[i,'Rank'])
                ob.FILM=df.loc[i,'FILM']
                ob.Genre=df.loc[i,'Genre']
                ob.Sub_Genre_1=df.loc[i,'Sub Genre 1']
                ob.Sub_Genre_2=df.loc[i,'Sub Genre 2']
                ob.Rating=df.loc[i,'Rating']
                ob.Year_of_Release =df.loc[i,'Year of Release']
                ob.Country =df.loc[i,'Country']
                ob.Run_Time=df.loc[i,'Run Time']
                ob.Franchise=df.loc[i,'Franchise']
                ob.Synopsis =df.loc[i,'Synopsis']
                ob.Keywords_1=df.loc[i,'Keywords 1']
                ob.Keywords_2=df.loc[i,'Keywords 2']
                ob.Keywords_3=df.loc[i,'Keywords 3']
                ob.Keywords_4=df.loc[i,'Keywords 4']
                ob.Production_Method =df.loc[i,'Production Method']
                ob.Creative_Type =df.loc[i,'Creative Type']
                ob.Production_Companies=df.loc[i,'# Production Companies']
                ob.Production_Company_1=df.loc[i,'Production Company 1']
                ob.Production_Company_2=df.loc[i,'Production Company 2']
                ob.Production_Company_3=df.loc[i,'Production Company 3']
                ob.Production_Company_4=df.loc[i,'Production Company 4']
                ob.Director=df.loc[i,'Director']
                ob.Lead_Actor_1_Name =df.loc[i,'Lead Actor 1 Name']
                ob.Lead_Actor_1_Gender=df.loc[i,'Lead Actor 1 Gender']
                ob.Lead_Actor_1_Age =df.loc[i,'Lead Actor 1 Age']
                ob.Lead_Actor_1_Nationality=df.loc[i,'Lead Actor 1 Nationality']
                ob.Lead_Actor_2_Name =df.loc[i,'Lead Actor 2 Name']
                ob.Lead_Actor_2_Gender=df.loc[i,'Lead Actor 2 Gender']
                ob.Lead_Actor_2_Age =df.loc[i,'Lead Actor 2 Age']
                ob.Lead_Actor_2_Nationality=df.loc[i,'Lead Actor 2 Nationality']
                ob.Target_Audience =df.loc[i,'Target Audience']
                ob.Streamer =df.loc[i,'Streamer']
                ob.Awards_1  =df.loc[i,'Awards 1']
                ob.Awards_2  =df.loc[i,'Awards 2']
                ob.Awards_3  =df.loc[i,'Awards 3']
                ob.Type_of_Deal =df.loc[i,'Type of Deal']
                ob.RELEASE_DATE  =df.loc[i,'RELEASE DATE']
                ob.DIST  =df.loc[i,'DIST']
                ob.NO_Screens  =df.loc[i,'NO Screens']
                ob.Opening_Day_Amd  =df.loc[i,'Opening Day Amd']
                ob.First_Weekend_BO  =df.loc[i,'First Weekend BO']
                ob.First_Weekend_Amd  =df.loc[i,'First Weekend ADM']
                ob.First_Week_BO  =df.loc[i,'First Week BO']
                ob.First_Week_ADM  =df.loc[i,'First Week ADM']
                ob.CUM_BO  =df.loc[i,'CUM BO']
                ob.CUM_ADM  =df.loc[i,'CUM ADM']
                ob.CUM_GBO_USD  =df.loc[i,'CUM GBO USD']                
                ob.save()

            return render(request,'home/index.html')

    return render(request,'home/file_uploads.html')

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


