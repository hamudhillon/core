# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from operator import or_
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
import pandas as pd
from .models import data,global_box, ksa_tv, netflix_Movies, netflix_series, prod_companies, series
from django.db.models import Max,Count
from django.db.utils import IntegrityError

from functools import reduce

from django.db.models import Q

from .filters import MovieFilter, Netflix_movies_filter, Netflix_series_filter, globalFilter, ksatvFilter, prodcompFilter, seriesFilter
from django.core import serializers

def genre_month_filter(months,genre):
    
    movies_months_genre=data.objects.filter(Genre__contains=genre).values('RELEASE_DATE')
    genree=[]
    
    for i in movies_months_genre:
        # print(i)
        print(i['RELEASE_DATE'])
        # print(i['Genre'])
        if i['RELEASE_DATE']:
            genree.append(i['RELEASE_DATE'].strftime('%b'))

    count = pd.Series(genree).value_counts(sort=True,ascending=True)
    # print(count.to_dict())
    from collections import OrderedDict
    od=OrderedDict(sorted(count.to_dict().items(),key =lambda x:months.index(x[0])))
    # print(od.keys())
    movies_month_label_release_genre=list(od.keys())
    # print(movies_month_label_release)
    movies_month_genre_count_release_genre=list(od.values())

    return [
        {f'movies_month_label_release':movies_month_label_release_genre},
        {f'movies_month_genre_count_release':movies_month_genre_count_release_genre}
        ]
    


@login_required(login_url="/login/")
def index(request,file_name):
    print(file_name)
    context = {}

    if file_name=='KSA':
        context = {'Dash':'KSA'}

        main_data=pd.DataFrame(data.objects.values())
        # print(main_data)

        # ----------------------------------------------
        # | MOVIES PER MONTH BY GENRE (TOP 5-6 GENRES) |
        # ----------------------------------------------

        top_6_Genre_list=[]
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] 
        TOP_GENRES=data.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))
        TOP_GENRES=pd.DataFrame(TOP_GENRES)
        top_6_genre=TOP_GENRES.sort_values(by='genre_count',ascending=False)[:6]
        
        context.update({'top_6_genre':top_6_genre['Genre']})
        for i in top_6_genre['Genre']:
            top_6_Genre_list.append(genre_month_filter(months,str(i).title()))

        context.update({'top_6_Genre_list':top_6_Genre_list})
        # print(context)
        print('---'*50)
        # genre_month_filter(months,'Action',context)
        # genre_month_filter(months,'Comedy',context)
        # genre_month_filter(months,'Horror',context)
        # genre_month_filter(months,'Drama',context)


        # ----------------------------------------------
        # | Total Movies                               |
        # ----------------------------------------------

        # ----------------------------------------------
        # | Highest CIM BO USD                         |
        # ----------------------------------------------
        CUM_GBO_USD___max=data.objects.aggregate(Max('CUM_GBO_USD'))
        
        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            }
            )




        # ----------------------------------------------
        # | MOST MOVIES FROM COUNTRY                   |
        # ----------------------------------------------
        Country___max=data.objects.aggregate(Max('Country'))


        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            'Country___max':Country___max,
            }
            )



        # ----------------------------------------------
        # | MOVIES PER MONTH                           |
        # ----------------------------------------------


        m=[]
        movies_months=data.objects.values('RELEASE_DATE')    
        for i in movies_months:
            # print(i['RELEASE_DATE'])
            if i['RELEASE_DATE']:
                m.append(i['RELEASE_DATE'].strftime('%b'))
            
        # m.sort()
        
        count = pd.Series(m).value_counts(sort=True,ascending=True)
        # print(count.to_dict())
        from collections import OrderedDict
        od=OrderedDict(sorted(count.to_dict().items(),key =lambda x:months.index(x[0])))
        # print(od.keys())
        movies_month_label_release=list(od.keys())
        # print(movies_month_label_release)
        movies_month_count_release=list(od.values())
        # print(movies_month_count_release)
        context.update({'movies_month_label_release':movies_month_label_release})
        # print(movies_month_label_release)
        context.update({'movies_month_count_release':movies_month_count_release})



        # ----------------------------------------------
        # | MOVIES/COUNTRY                             |
        # ----------------------------------------------

        countries=data.objects.values('Country').annotate(Country_count=Count('Country'))  
        
        df=pd.DataFrame(countries)
        print(df)
        import re
        for i in df.index:
            df.loc[i,'Country']=re.sub('[^\w\s_]+','',str(df.loc[i,'Country'])).capitalize().strip().replace('\n','')
            print(df.loc[i,'Country'])
            if 'United states' == df.loc[i,'Country'] :
                df.loc[i,'Country']='USA'
            if 'United states ' == df.loc[i,'Country']:
                df.loc[i,'Country']='USA'
        df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Country'].values()))
        context.update({'Country_label':list(df[:].to_dict()['Country'].values())})
        context.update({'Country_label_count':list(df[:].to_dict()['Country_count'].values())})



        # ----------------------------------------------
        # | MOVIES/GENRE                             |
        # ----------------------------------------------



        d=data.objects.exclude(Rating__in="nan").values_list('Rating','FILM','CUM_GBO_USD').order_by('-CUM_GBO_USD')
        cum_bo=data.objects.exclude(FILM__in='-').exclude(Rating__in="nan").values_list('Rating','FILM','CUM_BO').order_by('-CUM_BO')
        cum_adm=data.objects.exclude(FILM__in='-').exclude(Rating__in="nan").values_list('Rating','FILM','CUM_ADM').order_by('-CUM_ADM')
        lead_actor1_cum_bo=data.objects.exclude(Lead_Actor_1_Name__in='-').exclude(FILM__in='-').exclude(Rating__in="nan").values_list('Lead_Actor_1_Name','FILM','CUM_BO').order_by('-CUM_BO')
        lead_actor2_cum_bo=data.objects.exclude(Lead_Actor_2_Name__in='-').exclude(FILM__in='-').exclude(Rating__in="nan").values_list('Lead_Actor_2_Name','FILM','CUM_BO').order_by('-CUM_BO')
        prod_comp_cum_bo=data.objects.exclude(Production_Company_1__in='-').exclude(FILM__in='-').exclude(Rating__in="nan").values_list('Production_Company_1','FILM','CUM_BO').order_by('-CUM_BO')
        distrubute_cum_bo=data.objects.exclude(DIST__in='-').exclude(FILM__in='-').exclude(Rating__in="nan").values_list('DIST','FILM','CUM_BO').order_by('-CUM_BO')

        # print(cum_adm)
        context.update({
            'cum_bo':cum_bo,
            'cum_adm':cum_adm,
            'lead_actor1_cum_bo':lead_actor1_cum_bo,
            'lead_actor2_cum_bo':lead_actor2_cum_bo,
            'prod_comp_cum_bo':prod_comp_cum_bo,
            'distrubute_cum_bo':distrubute_cum_bo,

        })

        Movies_rating=data.objects.exclude(FILM__in='-').values_list('Rating','FILM','CUM_GBO_USD').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_Amazon=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Amazon').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        # print(pd.DataFrame(Movies_rating_Amazon))

        Series_rating=series.objects.values_list('Rating','Series_Name','Streamer').order_by('-Rating')
        prod_companies_num_mov=prod_companies.objects.values_list('Production_Companies','No_of_Movies').order_by('-No_of_Movies')
        prod_companies_WBO=prod_companies.objects.values_list('Production_Companies','Total_Worldwide_Box_Office').order_by('-Total_Worldwide_Box_Office')

        context.update({
            'Movies_rating_Amazon':Movies_rating_Amazon,
            'Movies_rating_netflix':Movies_rating_netflix,
            'Series_rating':Series_rating,
            'prod_companies_num_mov':prod_companies_num_mov,
            'prod_companies_WBO':prod_companies_WBO,
            'series':series.objects.all(),
            'ksatv':ksa_tv.objects.all(),
        })

        # COLORS- #3358f4 #00d0df
        
        # print(countries)

        # -----------------------
        # | Movie v/s STREAMER  |
        # -----------------------



        Movies_streamer=data.objects.values('Streamer')
        Movies_Netflix=0
        Movies_Amazone=0
        Movies_iTunes=0
        Movies_hulu=0
        Movies_Disney=0
        for i in Movies_streamer:
            # print(i['Streamer'])
            if 'netflix' in i['Streamer'].lower():
                Movies_Netflix+=1
            if 'amazon' in i['Streamer'].lower():
                Movies_Amazone+=1

            if 'itunes' in i['Streamer'].lower():
                Movies_iTunes+=1

            if 'hulu' in i['Streamer'].lower():
                Movies_hulu+=1
            if 'disney' in i['Streamer'].lower():
                Movies_Disney+=1
        Most_movies_on=pd.DataFrame([['Netflix','Amazon','iTunes','hulu','Disney'],[Movies_Netflix,
            Movies_Amazone,
            Movies_iTunes,
            Movies_hulu,
            Movies_Disney]],
            ).transpose().sort_values(by=1,ascending=False)[:1]
        # print()
        context.update({
            'Movies_Netflix':Movies_Netflix,
            'Movies_Amazone':Movies_Amazone,
            'Movies_iTunes':Movies_iTunes,
            'Movies_hulu':Movies_hulu,
            'Movies_Disney':Movies_Disney,
            'Most_movies_on':Most_movies_on.to_dict()[0][1],
            })


        




        # -----------------------
        # | Moives v/s Genre |
        # -----------------------



        movie_genre=data.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))  

        sgdf=pd.DataFrame(movie_genre)
        for i in sgdf.index:
            sgdf.loc[i,'Genre']=str(sgdf.loc[i,'Genre']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='genre_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_genre_label':list(sgdf[:].to_dict()['Genre'].values())})
        context.update({'movie_genre_label_count':list(sgdf[:].to_dict()['genre_count'].values())})
        # print(context)
       

        # -----------------------
        # | Moives v/s sub_Genre1|
        # -----------------------


    
        movie_Sub_Genre_1=data.objects.exclude(Sub_Genre_1__in='-').values('Sub_Genre_1').annotate(Sub_Genre_1_count=Count('Sub_Genre_1'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_1)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_1']=str(sgdf.loc[i,'Sub_Genre_1']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_1_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_1_label':list(sgdf[:].to_dict()['Sub_Genre_1'].values())})
        context.update({'movie_Sub_Genre_1_label_count':list(sgdf[:].to_dict()['Sub_Genre_1_count'].values())})
        # print(context)
       
        # -------------------------
        # | Moives v/s sub_Genre2 |
        # -------------------------


    
        movie_Sub_Genre_2=data.objects.exclude(Sub_Genre_2__in='-').values('Sub_Genre_2').annotate(Sub_Genre_2_count=Count('Sub_Genre_2'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_2)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_2']=str(sgdf.loc[i,'Sub_Genre_2']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_2_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_2_label':list(sgdf[:].to_dict()['Sub_Genre_2'].values())})
        context.update({'movie_Sub_Genre_2_label_count':list(sgdf[:].to_dict()['Sub_Genre_2_count'].values())})
        # print(context)
        print('---'*50)
        print(Movies_rating)
        context.update(
            {'data':d,
            'segment':'index',
            'Movies_rating':Movies_rating
            }
            )

    if file_name=='KSATV':
        context={'Dash':'KSATV'}
        # -----------------------
        # | SERIES v/s STREAMER |
        # -----------------------
        series_streamer=series.objects.values('Streamer')
        series_Netflix=0
        series_shahid=0
        series_viu=0
        series_Weyyak=0
        series_OSN=0
        for i in series_streamer:
            # print(i['Streamer'])
            if 'netflix' in i['Streamer'].lower():
                series_Netflix+=1
            if 'shahid' in i['Streamer'].lower():
                series_shahid+=1

            if 'viu' in i['Streamer'].lower():
                series_viu+=1

            if 'weyyak' in i['Streamer'].lower():
                series_Weyyak+=1
            if 'OSN+' in i['Streamer'].lower():
                series_OSN+=1
        Most_series_on=pd.DataFrame([['Netflix','shahid','viu','Weyyak','OSN'],[series_Netflix,
            series_shahid,
            series_viu,
            series_Weyyak,
            series_OSN]],
            ).transpose().sort_values(by=1,ascending=False)[:1]
        # print()
        context.update({
            'series_Netflix':series_Netflix,
            'series_shahid':series_shahid,
            'series_viu':series_viu,
            'series_Weyyak':series_Weyyak,
            'series_OSN':series_OSN,
            'Most_series_on':Most_series_on.to_dict()[0][1],
            })


        # ----------------------------
        # | SERIES v/s Program Types |
        # ----------------------------


        progType=ksa_tv.objects.values('Prog_Type').annotate(Prog_Type_count=Count('Prog_Type'))
        print(progType)
        progTypeDF=pd.DataFrame(progType)
        progTypeDF.sort_values(by='Prog_Type_count',ascending=False,inplace=True,ignore_index=True)
        # print(progTypeDF.to_dict())
        print(list(progTypeDF[:].to_dict()['Prog_Type'].values()))

        context.update({'Prog_Type_label':list(progTypeDF[:].to_dict()['Prog_Type'].values())})
        context.update({'Prog_Type_label_count':list(progTypeDF[:].to_dict()['Prog_Type_count'].values())})


        # ----------------------------
        # | SERIES v/s Program Sub Types |
        # ----------------------------


        progSubType=ksa_tv.objects.values('Prog_Sub_Type').annotate(Prog_Sub_Type_count=Count('Prog_Sub_Type'))
        print(progSubType)
        progSubTypeDF=pd.DataFrame(progSubType)
        progSubTypeDF.sort_values(by='Prog_Sub_Type_count',ascending=False,inplace=True,ignore_index=True)
        # print(progSubTypeDF.to_dict())
        print(list(progSubTypeDF[:].to_dict()['Prog_Sub_Type'].values()))

        context.update({'Prog_Sub_Type_label':list(progSubTypeDF[:].to_dict()['Prog_Sub_Type'].values())})
        context.update({'Prog_Sub_Type_label_count':list(progSubTypeDF[:].to_dict()['Prog_Sub_Type_count'].values())})



        # -----------------------------
        # | SERIES v/s Program Domain |
        # -----------------------------


        progDomain=ksa_tv.objects.values('Prog_Domain').annotate(Prog_Domain_count=Count('Prog_Domain'))
        print(progDomain)
        progDomainDF=pd.DataFrame(progDomain)
        progDomainDF.sort_values(by='Prog_Domain_count',ascending=False,inplace=True,ignore_index=True)
        # print(progDomainDF.to_dict())
        print(list(progDomainDF[:].to_dict()['Prog_Domain'].values()))

        context.update({'Prog_Domain_label':list(progDomainDF[:].to_dict()['Prog_Domain'].values())})
        context.update({'Prog_Domain_label_count':list(progDomainDF[:].to_dict()['Prog_Domain_count'].values())})


        # -----------------------
        # | SERIES v/s Genre    |
        # -----------------------


        series_Genre=series.objects.values('Genre')
        series_action=0
        series_drama=0
        series_thriller=0
        series_comedy=0
        series_Supernatural=0
        for i in series_Genre:
            # print(i['Streamer'])
            if 'action' in i['Genre'].lower():
                series_action+=1
            if 'drama' in i['Genre'].lower():
                series_drama+=1

            if 'thriller' in i['Genre'].lower():
                series_thriller+=1

            if 'comedy' in i['Genre'].lower():
                series_comedy+=1
            if 'supernatural' in i['Genre'].lower():
                series_Supernatural+=1
        Most_series_on=pd.DataFrame([['Netflix','drama','thriller','comedy','Supernatural'],[series_action,
            series_drama,
            series_thriller,
            series_comedy,
            series_Supernatural]],
            ).transpose().sort_values(by=1,ascending=False)[:1]
        # print()
        context.update({
            'series_action':series_action,
            'series_drama':series_drama,
            'series_thriller':series_thriller,
            'series_comedy':series_comedy,
            'series_Supernatural':series_Supernatural,
            'Most_genre_on':Most_series_on.to_dict()[0][1],
            })
        

        # -----------------------
        # | SERIES v/s AVG_AUD  |
        # -----------------------

        
        
        topProgAud=ksa_tv.objects.exclude(Prog_Name__in='-').values_list('Prog_Name','Avg_Aud_ALL').order_by('-Avg_Aud_ALL')
        
        context.update(
            {'topProgAud':topProgAud}
        )

    if file_name=='GLOBAL':
        context={'Dash':'GLOBAL'}
        main_data=pd.DataFrame(data.objects.values())
        # print(main_data)

        # ----------------------------------------------
        # | MOVIES PER MONTH BY GENRE (TOP 5-6 GENRES) |
        # ----------------------------------------------

        top_6_Genre_list=[]
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] 
        TOP_GENRES=data.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))
        TOP_GENRES=pd.DataFrame(TOP_GENRES)
        top_6_genre=TOP_GENRES.sort_values(by='genre_count',ascending=False)[:6]
        
        context.update({'top_6_genre':top_6_genre['Genre']})
        for i in top_6_genre['Genre']:
            top_6_Genre_list.append(genre_month_filter(months,str(i).title()))

        context.update({'top_6_Genre_list':top_6_Genre_list})
        print(context)
        print('---'*50)
        # genre_month_filter(months,'Action',context)
        # genre_month_filter(months,'Comedy',context)
        # genre_month_filter(months,'Horror',context)
        # genre_month_filter(months,'Drama',context)


        # ----------------------------------------------
        # | Total Movies                               |
        # ----------------------------------------------

        # ----------------------------------------------
        # | Highest CIM BO USD                         |
        # ----------------------------------------------
        CUM_GBO_USD___max=data.objects.aggregate(Max('CUM_GBO_USD'))
        
        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            }
            )




        # ----------------------------------------------
        # | MOST MOVIES FROM COUNTRY                   |
        # ----------------------------------------------
        Country___max=data.objects.aggregate(Max('Country'))


        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            'Country___max':Country___max,
            }
            )



        # ----------------------------------------------
        # | MOVIES PER MONTH                           |
        # ----------------------------------------------


        m=[]
        movies_months=data.objects.values('RELEASE_DATE')    
        for i in movies_months:
            # print(i['RELEASE_DATE'])
            if i['RELEASE_DATE']:
                m.append(i['RELEASE_DATE'].strftime('%b'))
            
        # m.sort()
        
        count = pd.Series(m).value_counts(sort=True,ascending=True)
        # print(count.to_dict())
        from collections import OrderedDict
        od=OrderedDict(sorted(count.to_dict().items(),key =lambda x:months.index(x[0])))
        # print(od.keys())
        movies_month_label_release=list(od.keys())
        # print(movies_month_label_release)
        movies_month_count_release=list(od.values())
        # print(movies_month_count_release)
        context.update({'movies_month_label_release':movies_month_label_release})
        # print(movies_month_label_release)
        context.update({'movies_month_count_release':movies_month_count_release})



        # ----------------------------------------------
        # | MOVIES/COUNTRY                             |
        # ----------------------------------------------

        Production_Country_1=global_box.objects.values('Production_Country_1').annotate(Country_count=Count('Production_Country_1'))  
        
        df=pd.DataFrame(Production_Country_1)
        print(df)
        import re
        for i in df.index:
            df.loc[i,'Production_Country_1']=re.sub('[^\w\s_]+','',str(df.loc[i,'Production_Country_1'])).capitalize().strip().replace('\n','')
            print(df.loc[i,'Production_Country_1'])
            if 'United states' == df.loc[i,'Production_Country_1'] :
                df.loc[i,'Production_Country_1']='USA'
            if 'United states ' == df.loc[i,'Production_Country_1']:
                df.loc[i,'Production_Country_1']='USA'
        df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Production_Country_1'].values()))
        context.update({'Production_Country_1_label':list(df[:].to_dict()['Production_Country_1'].values())})
        context.update({'Production_Country_1_label_count':list(df[:].to_dict()['Country_count'].values())})



        # ----------------------------------------------
        # | MOVIES/GENRE                             |
        # ----------------------------------------------



        d=global_box.objects.exclude(Movie__in="-").values_list('Rating','Movie','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        cum_bo=global_box.objects.exclude(Movie__in="-").values_list('Movie','Production_Budget').order_by('-Production_Budget')
        cum_bol=global_box.objects.exclude(Movie__in="-").values_list('Movie','Production_Budget').order_by('Production_Budget')
        cum_adm=global_box.objects.exclude(Movie__in="-").values_list('Movie','Other_Costs').order_by('-Other_Costs')
        cum_admlo=global_box.objects.exclude(Other_Costs__in="0").exclude(Movie__in="-").values_list('Movie','Other_Costs').order_by('Other_Costs')
        profit=global_box.objects.exclude(Movie__in="-").values_list('Movie','Profit').order_by('-Profit')
        profitlo=global_box.objects.exclude(Movie__in="-").values_list('Movie','Profit').order_by('Profit')
        Profitability=global_box.objects.exclude(Movie__in="-").values_list('Movie','Profitability').order_by('-Profitability')
        Profitabilitylo=global_box.objects.exclude(Movie__in="-").values_list('Movie','Profitability').order_by('Profitability')
        DBO=global_box.objects.exclude(Movie__in="-").values_list('Movie','Domestic_Box_office').order_by('-Domestic_Box_office')
        IBO=global_box.objects.exclude(Movie__in="-").values_list('Movie','International_Box_Office').order_by('-International_Box_Office')
        World_Wide_Box_Office=global_box.objects.exclude(Movie__in="-").values_list('Movie','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        Production_Country_1_World_Wide_Box_Office=global_box.objects.exclude(Prod_Company_1__in="-").values_list('Prod_Company_1','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        Production_Country_2_World_Wide_Box_Office=global_box.objects.exclude(Prod_Company_2__in="-").values_list('Prod_Company_2','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        Production_Country_3_World_Wide_Box_Office=global_box.objects.exclude(Prod_Company_3__in="-").values_list('Prod_Company_3','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        
        # lead_actor1_cum_bo=global_box.objects.exclude(Lead_Actor_1_Name__in='-').exclude(Movie__in="-").values_list('Lead_Actor_1_Name','FILM','CUM_BO').order_by('-CUM_BO')
        # lead_actor2_cum_bo=global_box.objects.exclude(Lead_Actor_2_Name__in='-').exclude(Movie__in="-").values_list('Lead_Actor_2_Name','FILM','CUM_BO').order_by('-CUM_BO')
        # prod_comp_cum_bo=global_box.objects.exclude(Production_Company_1__in='-').exclude(Movie__in="-").values_list('Production_Company_1','FILM','CUM_BO').order_by('-CUM_BO')
        # distrubute_cum_bo=global_box.objects.exclude(DIST__in='-').exclude(Movie__in="-").values_list('DIST','FILM','CUM_BO').order_by('-CUM_BO')

        # print(cum_adm)
        context.update({
            'cum_bo':cum_bo,
            'cum_bol':cum_bol,
            'cum_adm':cum_adm,
            'cum_admlo':cum_admlo,
            'profit':profit,
            'profitlo':profitlo,
            'Profitability':Profitability,
            'Profitabilitylo':Profitabilitylo,
            'DBO':DBO,

            'IBO':IBO,
            'World_Wide_Box_Office':World_Wide_Box_Office,
            'Production_Country_1_World_Wide_Box_Office':Production_Country_1_World_Wide_Box_Office,
            'Production_Country_2_World_Wide_Box_Office':Production_Country_2_World_Wide_Box_Office,
            'Production_Country_3_World_Wide_Box_Office':Production_Country_3_World_Wide_Box_Office,

            # 'lead_actor1_cum_bo':lead_actor1_cum_bo,
            # 'lead_actor2_cum_bo':lead_actor2_cum_bo,
            # 'prod_comp_cum_bo':prod_comp_cum_bo,
            # 'distrubute_cum_bo':distrubute_cum_bo,

        })

        Movies_rating=data.objects.exclude(FILM__in='-').values_list('Rating','FILM','CUM_GBO_USD').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_Amazon=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Amazon').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        # print(pd.DataFrame(Movies_rating_Amazon))

        Series_rating=series.objects.values_list('Rating','Series_Name','Streamer').order_by('-Rating')
        prod_companies_num_mov=prod_companies.objects.values_list('Production_Companies','No_of_Movies').order_by('-No_of_Movies')
        prod_companies_WBO=prod_companies.objects.values_list('Production_Companies','Total_Worldwide_Box_Office').order_by('-Total_Worldwide_Box_Office')

        context.update({
            'Movies_rating_Amazon':Movies_rating_Amazon,
            'Movies_rating_netflix':Movies_rating_netflix,
            'Series_rating':Series_rating,
            'prod_companies_num_mov':prod_companies_num_mov,
            'prod_companies_WBO':prod_companies_WBO,
            'series':series.objects.all(),
            'ksatv':ksa_tv.objects.all(),
        })

        # COLORS- #3358f4 #00d0df
        
        # print(countries)

        # -----------------------
        # | Movie v/s STREAMER  |
        # -----------------------



        Movies_streamer=data.objects.values('Streamer')
        Movies_Netflix=0
        Movies_Amazone=0
        Movies_iTunes=0
        Movies_hulu=0
        Movies_Disney=0
        for i in Movies_streamer:
            # print(i['Streamer'])
            if 'netflix' in i['Streamer'].lower():
                Movies_Netflix+=1
            if 'amazon' in i['Streamer'].lower():
                Movies_Amazone+=1

            if 'itunes' in i['Streamer'].lower():
                Movies_iTunes+=1

            if 'hulu' in i['Streamer'].lower():
                Movies_hulu+=1
            if 'disney' in i['Streamer'].lower():
                Movies_Disney+=1
        Most_movies_on=pd.DataFrame([['Netflix','Amazon','iTunes','hulu','Disney'],[Movies_Netflix,
            Movies_Amazone,
            Movies_iTunes,
            Movies_hulu,
            Movies_Disney]],
            ).transpose().sort_values(by=1,ascending=False)[:1]
        # print()
        context.update({
            'Movies_Netflix':Movies_Netflix,
            'Movies_Amazone':Movies_Amazone,
            'Movies_iTunes':Movies_iTunes,
            'Movies_hulu':Movies_hulu,
            'Movies_Disney':Movies_Disney,
            'Most_movies_on':Most_movies_on.to_dict()[0][1],
            })


        




        # -----------------------
        # | Moives v/s Genre |
        # -----------------------



        movie_genre=global_box.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))  

        sgdf=pd.DataFrame(movie_genre)
        for i in sgdf.index:
            sgdf.loc[i,'Genre']=str(sgdf.loc[i,'Genre']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='genre_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_genre_label':list(sgdf[:].to_dict()['Genre'].values())})
        context.update({'movie_genre_label_count':list(sgdf[:].to_dict()['genre_count'].values())})
        # print(context)
       

        # -----------------------
        # | Moives v/s sub_Genre1|
        # -----------------------

         # ----------------------------------------------
        # | MOVIES/Year                             |
        # ----------------------------------------------

        Release_Year_m=global_box.objects.exclude(Release_Year__in='None').exclude(Release_Year__in='-').values('Release_Year').annotate(Country_count=Count('Release_Year'))  
        print(Release_Year_m)
        df=pd.DataFrame(Release_Year_m)
        print(df)
        import re
        
        # df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Release_Year'].values()))
        context.update({'Release_Year_label':list(df[:].to_dict()['Release_Year'].values())})
        context.update({'Release_Year_label_count':list(df[:].to_dict()['Country_count'].values())})

    
        movie_Sub_Genre_1=global_box.objects.exclude(Sub_Genera_1__in='-').values('Sub_Genera_1').annotate(Sub_Genera_1_count=Count('Sub_Genera_1'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_1)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genera_1']=str(sgdf.loc[i,'Sub_Genera_1']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genera_1_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_1_label':list(sgdf[:].to_dict()['Sub_Genera_1'].values())})
        context.update({'movie_Sub_Genre_1_label_count':list(sgdf[:].to_dict()['Sub_Genera_1_count'].values())})
        # print(context)
       
        # -------------------------
        # | Moives v/s sub_Genre2 |
        # -------------------------


    
        movie_Sub_Genera_2=global_box.objects.exclude(Sub_Genera_2__in='-').values('Sub_Genera_2').annotate(Sub_Genera_2_count=Count('Sub_Genera_2'))  

        sgdf=pd.DataFrame(movie_Sub_Genera_2)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genera_2']=str(sgdf.loc[i,'Sub_Genera_2']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genera_2_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_2_label':list(sgdf[:].to_dict()['Sub_Genera_2'].values())})
        context.update({'movie_Sub_Genre_2_label_count':list(sgdf[:].to_dict()['Sub_Genera_2_count'].values())})
        # print(context)


        context.update(
            {'data':d,
            'segment':'index',
            'Movies_rating':Movies_rating
            }
            )
    
    if file_name=='Prod-House':
        context={'Dash':'PROD'}
        main_data=pd.DataFrame(data.objects.values())
        # print(main_data)

        # ----------------------------------------------
        # | MOVIES PER MONTH BY GENRE (TOP 5-6 GENRES) |
        # ----------------------------------------------


        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] 
        


        # ----------------------------------------------
        # | Total Movies                               |
        # ----------------------------------------------

        # ----------------------------------------------
        # | Highest CIM BO USD                         |
        # ----------------------------------------------
        CUM_GBO_USD___max=data.objects.aggregate(Max('CUM_GBO_USD'))
        
        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            }
            )




        # ----------------------------------------------
        # | MOST MOVIES FROM COUNTRY                   |
        # ----------------------------------------------
        Country___max=data.objects.aggregate(Max('Country'))


        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            'Country___max':Country___max,
            }
            )



        # ----------------------------------------------
        # | MOVIES PER MONTH                           |
        # ----------------------------------------------


        m=[]
        movies_months=data.objects.values('RELEASE_DATE')    
        for i in movies_months:
            # print(i['RELEASE_DATE'])
            if i['RELEASE_DATE']:
                m.append(i['RELEASE_DATE'].strftime('%b'))
            
        # m.sort()
        
        count = pd.Series(m).value_counts(sort=True,ascending=True)
        # print(count.to_dict())
        from collections import OrderedDict
        od=OrderedDict(sorted(count.to_dict().items(),key =lambda x:months.index(x[0])))
        # print(od.keys())
        movies_month_label_release=list(od.keys())
        # print(movies_month_label_release)
        movies_month_count_release=list(od.values())
        # print(movies_month_count_release)
        context.update({'movies_month_label_release':movies_month_label_release})
        # print(movies_month_label_release)
        context.update({'movies_month_count_release':movies_month_count_release})



        # ----------------------------------------------
        # | MOVIES/COUNTRY                             |
        # ----------------------------------------------

        countries=data.objects.values('Country').annotate(Country_count=Count('Country'))  
        
        df=pd.DataFrame(countries)
        print(df)
        import re
        for i in df.index:
            df.loc[i,'Country']=re.sub('[^\w\s_]+','',str(df.loc[i,'Country'])).capitalize().strip().replace('\n','')
            print(df.loc[i,'Country'])
            if 'United states' == df.loc[i,'Country'] :
                df.loc[i,'Country']='USA'
            if 'United states ' == df.loc[i,'Country']:
                df.loc[i,'Country']='USA'
        df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Country'].values()))
        context.update({'Country_label':list(df[:].to_dict()['Country'].values())})
        context.update({'Country_label_count':list(df[:].to_dict()['Country_count'].values())})



       


        # ----------------------------------------------
        # | MOVIES/GENRE                             |
        # ----------------------------------------------



        d=prod_companies.objects.all()
        prod_comp_worldBO=prod_companies.objects.exclude(Production_Companies__in='-').values_list('Production_Companies','Total_Worldwide_Box_Office').order_by('-Total_Worldwide_Box_Office')
        prod_compDomesticBO=prod_companies.objects.exclude(Production_Companies__in='-').values_list('Production_Companies','Total_Domestic_Box_Office').order_by('-Total_Domestic_Box_Office')
        prod_compBynoOfMovies=prod_companies.objects.exclude(Production_Companies__in='-').values_list('Production_Companies','No_of_Movies').order_by('-No_of_Movies')
        # lead_actor1_cum_bo=data.objects.exclude(Lead_Actor_1_Name__in='-').exclude(Production_Companies__in='-').values_list('Lead_Actor_1_Name','Production_Companies','CUM_BO').order_by('-CUM_BO')
        # lead_actor2_cum_bo=data.objects.exclude(Lead_Actor_2_Name__in='-').exclude(FILM__in='-').values_list('Lead_Actor_2_Name','FILM','CUM_BO').order_by('-CUM_BO')
        # prod_comp_cum_bo=data.objects.exclude(Production_Company_1__in='-').exclude(FILM__in='-').exclude(Rating__in="nan").values_list('Production_Company_1','FILM','CUM_BO').order_by('-CUM_BO')
        # distrubute_cum_bo=data.objects.exclude(DIST__in='-').exclude(FILM__in='-').exclude(Rating__in="nan").values_list('DIST','FILM','CUM_BO').order_by('-CUM_BO')

        # print(Total_Domestic_Box_Office)
        context.update({
            'prod_comp_worldBO':prod_comp_worldBO,
            'prod_compDomesticBO':prod_compDomesticBO,
            'prod_compBynoOfMovies':prod_compBynoOfMovies,
            # 'lead_actor1_cum_bo':lead_actor1_cum_bo,
            # 'lead_actor2_cum_bo':lead_actor2_cum_bo,
            # 'prod_comp_cum_bo':prod_comp_cum_bo,
            # 'distrubute_cum_bo':distrubute_cum_bo,

        })

        Movies_rating=data.objects.exclude(FILM__in='-').values_list('Rating','FILM','CUM_GBO_USD').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_Amazon=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Amazon').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        # print(pd.DataFrame(Movies_rating_Amazon))

        Series_rating=series.objects.values_list('Rating','Series_Name','Streamer').order_by('-Rating')
        prod_companies_num_mov=prod_companies.objects.values_list('Production_Companies','No_of_Movies').order_by('-No_of_Movies')
        prod_companies_WBO=prod_companies.objects.values_list('Production_Companies','Total_Worldwide_Box_Office').order_by('-Total_Worldwide_Box_Office')

        context.update({
            'Movies_rating_Amazon':Movies_rating_Amazon,
            'Movies_rating_netflix':Movies_rating_netflix,
            'Series_rating':Series_rating,
            'prod_companies_num_mov':prod_companies_num_mov,
            'prod_companies_WBO':prod_companies_WBO,
            'series':series.objects.all(),
            'ksatv':ksa_tv.objects.all(),
        })

        # COLORS- #3358f4 #00d0df
        
        # print(countries)

        # -----------------------
        # | Movie v/s STREAMER  |
        # -----------------------



        Movies_streamer=data.objects.values('Streamer')
        Movies_Netflix=0
        Movies_Amazone=0
        Movies_iTunes=0
        Movies_hulu=0
        Movies_Disney=0
        for i in Movies_streamer:
            # print(i['Streamer'])
            if 'netflix' in i['Streamer'].lower():
                Movies_Netflix+=1
            if 'amazon' in i['Streamer'].lower():
                Movies_Amazone+=1

            if 'itunes' in i['Streamer'].lower():
                Movies_iTunes+=1

            if 'hulu' in i['Streamer'].lower():
                Movies_hulu+=1
            if 'disney' in i['Streamer'].lower():
                Movies_Disney+=1
        Most_movies_on=pd.DataFrame([['Netflix','Amazon','iTunes','hulu','Disney'],[Movies_Netflix,
            Movies_Amazone,
            Movies_iTunes,
            Movies_hulu,
            Movies_Disney]],
            ).transpose().sort_values(by=1,ascending=False)[:1]
        # print()
        context.update({
            'Movies_Netflix':Movies_Netflix,
            'Movies_Amazone':Movies_Amazone,
            'Movies_iTunes':Movies_iTunes,
            'Movies_hulu':Movies_hulu,
            'Movies_Disney':Movies_Disney,
            'Most_movies_on':Most_movies_on.to_dict()[0][1],
            })


        




        # -----------------------
        # | Moives v/s Genre |
        # -----------------------



        movie_genre=data.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))  

        sgdf=pd.DataFrame(movie_genre)
        for i in sgdf.index:
            sgdf.loc[i,'Genre']=str(sgdf.loc[i,'Genre']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='genre_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_genre_label':list(sgdf[:].to_dict()['Genre'].values())})
        context.update({'movie_genre_label_count':list(sgdf[:].to_dict()['genre_count'].values())})
        # print(context)
       
        # -----------------------
        # | Moives v/s Genre |
        # -----------------------



        movie_Production_Company_1=data.objects.exclude(Production_Company_1__in='-').values('Production_Company_1').annotate(Production_Company_1_count=Count('Production_Company_1'))  

        sgdf=pd.DataFrame(movie_Production_Company_1)
        for i in sgdf.index:
            sgdf.loc[i,'Production_Company_1']=str(sgdf.loc[i,'Production_Company_1']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Production_Company_1_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Production_Company_1_label':list(sgdf[:].to_dict()['Production_Company_1'].values())})
        context.update({'movie_Production_Company_1_label_count':list(sgdf[:].to_dict()['Production_Company_1_count'].values())})
        # print(context)
       
        # -----------------------
        # | Moives v/s sub_Production_Company_11|
        # -----------------------


    
        movie_Sub_Genre_1=data.objects.exclude(Sub_Genre_1__in='-').values('Sub_Genre_1').annotate(Sub_Genre_1_count=Count('Sub_Genre_1'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_1)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_1']=str(sgdf.loc[i,'Sub_Genre_1']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_1_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_1_label':list(sgdf[:].to_dict()['Sub_Genre_1'].values())})
        context.update({'movie_Sub_Genre_1_label_count':list(sgdf[:].to_dict()['Sub_Genre_1_count'].values())})
        # print(context)
       
        # -------------------------
        # | Moives v/s sub_Genre2 |
        # -------------------------


    
        movie_Sub_Genre_2=data.objects.exclude(Sub_Genre_2__in='-').values('Sub_Genre_2').annotate(Sub_Genre_2_count=Count('Sub_Genre_2'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_2)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_2']=str(sgdf.loc[i,'Sub_Genre_2']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_2_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_2_label':list(sgdf[:].to_dict()['Sub_Genre_2'].values())})
        context.update({'movie_Sub_Genre_2_label_count':list(sgdf[:].to_dict()['Sub_Genre_2_count'].values())})
        # print(context)


        context.update(
            {'data':d,
            'segment':'index',
            'Movies_rating':Movies_rating
            }
            )

    if file_name=='Netflix-Series':
        context={'Dash':'NSERIES'}
        main_data=pd.DataFrame(data.objects.values())
        # print(main_data)

        # ----------------------------------------------
        # | MOVIES PER MONTH BY GENRE (TOP 5-6 GENRES) |
        # ----------------------------------------------

        top_6_Genre_list=[]
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] 
        TOP_GENRES=data.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))
        TOP_GENRES=pd.DataFrame(TOP_GENRES)
        top_6_genre=TOP_GENRES.sort_values(by='genre_count',ascending=False)[:6]
        
        context.update({'top_6_genre':top_6_genre['Genre']})
        for i in top_6_genre['Genre']:
            top_6_Genre_list.append(genre_month_filter(months,str(i).title()))

        context.update({'top_6_Genre_list':top_6_Genre_list})
        print(context)
        print('---'*50)
        # genre_month_filter(months,'Action',context)
        # genre_month_filter(months,'Comedy',context)
        # genre_month_filter(months,'Horror',context)
        # genre_month_filter(months,'Drama',context)


        # ----------------------------------------------
        # | Total Movies                               |
        # ----------------------------------------------

        # ----------------------------------------------
        # | Highest CIM BO USD                         |
        # ----------------------------------------------
        CUM_GBO_USD___max=data.objects.aggregate(Max('CUM_GBO_USD'))
        
        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            }
            )




        # ----------------------------------------------
        # | MOST MOVIES FROM COUNTRY                   |
        # ----------------------------------------------
        Country___max=netflix_series.objects.aggregate(Max('Country'))
        # Streamer___max=netflix_series.objects.aggregate(Max('Country'))


        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            'Country___max':Country___max,
            }
            )



        # ----------------------------------------------
        # | MOVIES PER MONTH                           |
        # ----------------------------------------------


        m=[]
        movies_months=data.objects.values('RELEASE_DATE')    
        for i in movies_months:
            # print(i['RELEASE_DATE'])
            if i['RELEASE_DATE']:
                m.append(i['RELEASE_DATE'].strftime('%b'))
            
        # m.sort()
        
        count = pd.Series(m).value_counts(sort=True,ascending=True)
        # print(count.to_dict())
        from collections import OrderedDict
        od=OrderedDict(sorted(count.to_dict().items(),key =lambda x:months.index(x[0])))
        # print(od.keys())
        movies_month_label_release=list(od.keys())
        # print(movies_month_label_release)
        movies_month_count_release=list(od.values())
        # print(movies_month_count_release)
        context.update({'movies_month_label_release':movies_month_label_release})
        # print(movies_month_label_release)
        context.update({'movies_month_count_release':movies_month_count_release})



        # ----------------------------------------------
        # | MOVIES/COUNTRY                             |
        # ----------------------------------------------

        Country=netflix_series.objects.values('Country').annotate(Country_count=Count('Country'))  
        
        df=pd.DataFrame(Country)
        print(df)
        import re
        for i in df.index:
            df.loc[i,'Country']=re.sub('[^\w\s_]+','',str(df.loc[i,'Country'])).capitalize().strip().replace('\n','')
            print(df.loc[i,'Country'])
            if 'United states' == df.loc[i,'Country'] :
                df.loc[i,'Country']='USA'
            if 'United states ' == df.loc[i,'Country']:
                df.loc[i,'Country']='USA'
        df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Country'].values()))
        context.update({'Production_Country_1_label':list(df[:].to_dict()['Country'].values())})
        context.update({'Production_Country_1_label_count':list(df[:].to_dict()['Country_count'].values())})



        # ----------------------------------------------
        # | MOVIES/GENRE                             |
        # ----------------------------------------------



        d=netflix_series.objects.exclude(Name__in="-").values_list('Rating','Name','Points').order_by('-Points')
        cum_bo=netflix_series.objects.exclude(Name__in="-").values_list('Name','Rating').order_by('-Rating')
        cum_bol=netflix_series.objects.exclude(Name__in="-").values_list('Name','Points').order_by('-Points')
        cum_adm=netflix_series.objects.exclude(Name__in="-").exclude(Genre__in="-").values_list('Genre','Points').order_by('-Points')
        cum_admlo=netflix_series.objects.exclude(Lead_Actor_1_Name__in="-").exclude(Name__in="-").values_list('Lead_Actor_1_Name','Points').order_by('-Points')
        profit=netflix_series.objects.exclude(Lead_Actor_2_Name__in="-").values_list('Lead_Actor_2_Name','Points').order_by('-Points')
        profitlo=netflix_series.objects.exclude(Production_Company_1__in="-").values_list('Production_Company_1','Points').order_by('-Points')
        Profitability=netflix_series.objects.exclude(Production_Company_1__in="-").values_list('Production_Company_1','Points').order_by('-Points')
        Profitabilitylo=netflix_series.objects.exclude(Production_Company_1__in="-").values_list('Production_Company_1','Points').order_by('-Points')
        # DBO=global_box.objects.exclude(Name__in="-").values_list('Name','Domestic_Box_office').order_by('-Domestic_Box_office')
        # IBO=global_box.objects.exclude(Name__in="-").values_list('Name','International_Box_Office').order_by('-International_Box_Office')
        # World_Wide_Box_Office=global_box.objects.exclude(Name__in="-").values_list('Name','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        # Production_Country_1_World_Wide_Box_Office=global_box.objects.exclude(Production_Country_1__in="-").values_list('Production_Country_1','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        # Production_Country_2_World_Wide_Box_Office=global_box.objects.exclude(Production_Country_2__in="-").values_list('Production_Country_2','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        # Production_Country_3_World_Wide_Box_Office=global_box.objects.exclude(Production_Country_3__in="-").values_list('Production_Country_3','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        
        # lead_actor1_cum_bo=global_box.objects.exclude(Lead_Actor_1_Name__in='-').exclude(Movie__in="-").values_list('Lead_Actor_1_Name','FILM','CUM_BO').order_by('-CUM_BO')
        # lead_actor2_cum_bo=global_box.objects.exclude(Lead_Actor_2_Name__in='-').exclude(Movie__in="-").values_list('Lead_Actor_2_Name','FILM','CUM_BO').order_by('-CUM_BO')
        # prod_comp_cum_bo=global_box.objects.exclude(Production_Company_1__in='-').exclude(Movie__in="-").values_list('Production_Company_1','FILM','CUM_BO').order_by('-CUM_BO')
        # distrubute_cum_bo=global_box.objects.exclude(DIST__in='-').exclude(Movie__in="-").values_list('DIST','FILM','CUM_BO').order_by('-CUM_BO')

        # print(cum_adm)
        context.update({
            'cum_bo':cum_bo,
            'cum_bol':cum_bol,
            'cum_adm':cum_adm,
            'cum_admlo':cum_admlo,
            'profit':profit,
            'profitlo':profitlo,
            'Profitability':Profitability,
            'Profitabilitylo':Profitabilitylo,
            # 'DBO':DBO,

            # 'IBO':IBO,
            # 'World_Wide_Box_Office':World_Wide_Box_Office,
            # 'Production_Country_1_World_Wide_Box_Office':Production_Country_1_World_Wide_Box_Office,
            # 'Production_Country_2_World_Wide_Box_Office':Production_Country_2_World_Wide_Box_Office,
            # 'Production_Country_3_World_Wide_Box_Office':Production_Country_3_World_Wide_Box_Office,

            # 'lead_actor1_cum_bo':lead_actor1_cum_bo,
            # 'lead_actor2_cum_bo':lead_actor2_cum_bo,
            # 'prod_comp_cum_bo':prod_comp_cum_bo,
            # 'distrubute_cum_bo':distrubute_cum_bo,

        })

        Movies_rating=data.objects.exclude(FILM__in='-').values_list('Rating','FILM','CUM_GBO_USD').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_Amazon=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Amazon').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        # print(pd.DataFrame(Movies_rating_Amazon))

        Series_rating=series.objects.values_list('Rating','Series_Name','Streamer').order_by('-Rating')
        prod_companies_num_mov=prod_companies.objects.values_list('Production_Companies','No_of_Movies').order_by('-No_of_Movies')
        prod_companies_WBO=prod_companies.objects.values_list('Production_Companies','Total_Worldwide_Box_Office').order_by('-Total_Worldwide_Box_Office')

        context.update({
            'Movies_rating_Amazon':Movies_rating_Amazon,
            'Movies_rating_netflix':Movies_rating_netflix,
            'Series_rating':Series_rating,
            'prod_companies_num_mov':prod_companies_num_mov,
            'prod_companies_WBO':prod_companies_WBO,
            'series':series.objects.all(),
            'ksatv':ksa_tv.objects.all(),
        })

        # COLORS- #3358f4 #00d0df
        
        # print(countries)

        # -----------------------
        # | Movie v/s STREAMER  |
        # -----------------------



        Movies_streamer=data.objects.values('Streamer')
        Movies_Netflix=0
        Movies_Amazone=0
        Movies_iTunes=0
        Movies_hulu=0
        Movies_Disney=0
        for i in Movies_streamer:
            # print(i['Streamer'])
            if 'netflix' in i['Streamer'].lower():
                Movies_Netflix+=1
            if 'amazon' in i['Streamer'].lower():
                Movies_Amazone+=1

            if 'itunes' in i['Streamer'].lower():
                Movies_iTunes+=1

            if 'hulu' in i['Streamer'].lower():
                Movies_hulu+=1
            if 'disney' in i['Streamer'].lower():
                Movies_Disney+=1
        Most_movies_on=pd.DataFrame([['Netflix','Amazon','iTunes','hulu','Disney'],[Movies_Netflix,
            Movies_Amazone,
            Movies_iTunes,
            Movies_hulu,
            Movies_Disney]],
            ).transpose().sort_values(by=1,ascending=False)[:1]
        # print()
        context.update({
            'Movies_Netflix':Movies_Netflix,
            'Movies_Amazone':Movies_Amazone,
            'Movies_iTunes':Movies_iTunes,
            'Movies_hulu':Movies_hulu,
            'Movies_Disney':Movies_Disney,
            'Most_movies_on':Most_movies_on.to_dict()[0][1],
            })


        




        # -----------------------
        # | Moives v/s Genre |
        # -----------------------



        movie_genre=netflix_series.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))  

        sgdf=pd.DataFrame(movie_genre)
        for i in sgdf.index:
            sgdf.loc[i,'Genre']=str(sgdf.loc[i,'Genre']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='genre_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_genre_label':list(sgdf[:].to_dict()['Genre'].values())})
        context.update({'movie_genre_label_count':list(sgdf[:].to_dict()['genre_count'].values())})
        # print(context)
       

        # -----------------------
        # | Moives v/s sub_Genre1|
        # -----------------------

         # ----------------------------------------------
        # | MOVIES/Year                             |
        # ----------------------------------------------

        Release_Year_m=global_box.objects.exclude(Release_Year__in='None').exclude(Release_Year__in='-').values('Release_Year').annotate(Country_count=Count('Release_Year'))  
        print(Release_Year_m)
        df=pd.DataFrame(Release_Year_m)
        print(df)
        import re
        
        # df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Release_Year'].values()))
        context.update({'Release_Year_label':list(df[:].to_dict()['Release_Year'].values())})
        context.update({'Release_Year_label_count':list(df[:].to_dict()['Country_count'].values())})

    
        movie_Sub_Genre_1=netflix_series.objects.exclude(Sub_Genre_1__in='-').values('Sub_Genre_1').annotate(Sub_Genre_1_count=Count('Sub_Genre_1'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_1)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_1']=str(sgdf.loc[i,'Sub_Genre_1']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_1_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_1_label':list(sgdf[:].to_dict()['Sub_Genre_1'].values())})
        context.update({'movie_Sub_Genre_1_label_count':list(sgdf[:].to_dict()['Sub_Genre_1_count'].values())})
        # print(context)
       
        # -------------------------
        # | Moives v/s sub_Genre2 |
        # -------------------------


    
        movie_Sub_Genre_2=netflix_series.objects.exclude(Sub_Genre_2__in='-').values('Sub_Genre_2').annotate(Sub_Genre_2_count=Count('Sub_Genre_2'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_2)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_2']=str(sgdf.loc[i,'Sub_Genre_2']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_2_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_2_label':list(sgdf[:].to_dict()['Sub_Genre_2'].values())})
        context.update({'movie_Sub_Genre_2_label_count':list(sgdf[:].to_dict()['Sub_Genre_2_count'].values())})
        # print(context)


        context.update(
            {'data':d,
            'segment':'index',
            'Movies_rating':Movies_rating
            }
            )
    
    if file_name=='NIG-movies':
        context={'Dash':'NIG'}
    
        main_data=pd.DataFrame(data.objects.values())
        # print(main_data)

        # ----------------------------------------------
        # | MOVIES PER MONTH BY GENRE (TOP 5-6 GENRES) |
        # ----------------------------------------------

        top_6_Genre_list=[]
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] 
        TOP_GENRES=data.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))
        TOP_GENRES=pd.DataFrame(TOP_GENRES)
        top_6_genre=TOP_GENRES.sort_values(by='genre_count',ascending=False)[:6]
        
        context.update({'top_6_genre':top_6_genre['Genre']})
        for i in top_6_genre['Genre']:
            top_6_Genre_list.append(genre_month_filter(months,str(i).title()))

        context.update({'top_6_Genre_list':top_6_Genre_list})
        print(context)
        print('---'*50)
        # genre_month_filter(months,'Action',context)
        # genre_month_filter(months,'Comedy',context)
        # genre_month_filter(months,'Horror',context)
        # genre_month_filter(months,'Drama',context)


        # ----------------------------------------------
        # | Total Movies                               |
        # ----------------------------------------------

        # ----------------------------------------------
        # | Highest CIM BO USD                         |
        # ----------------------------------------------
        CUM_GBO_USD___max=data.objects.aggregate(Max('CUM_GBO_USD'))
        
        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            }
            )




        # ----------------------------------------------
        # | MOST MOVIES FROM COUNTRY                   |
        # ----------------------------------------------
        Country___max=netflix_Movies.objects.aggregate(Max('Country'))
        # Streamer___max=netflix_Movies.objects.aggregate(Max('Country'))


        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            'Country___max':Country___max,
            }
            )



        # ----------------------------------------------
        # | MOVIES PER MONTH                           |
        # ----------------------------------------------


        m=[]
        movies_months=data.objects.values('RELEASE_DATE')    
        for i in movies_months:
            # print(i['RELEASE_DATE'])
            if i['RELEASE_DATE']:
                m.append(i['RELEASE_DATE'].strftime('%b'))
            
        # m.sort()
        
        count = pd.Series(m).value_counts(sort=True,ascending=True)
        # print(count.to_dict())
        from collections import OrderedDict
        od=OrderedDict(sorted(count.to_dict().items(),key =lambda x:months.index(x[0])))
        # print(od.keys())
        movies_month_label_release=list(od.keys())
        # print(movies_month_label_release)
        movies_month_count_release=list(od.values())
        # print(movies_month_count_release)
        context.update({'movies_month_label_release':movies_month_label_release})
        # print(movies_month_label_release)
        context.update({'movies_month_count_release':movies_month_count_release})



        # ----------------------------------------------
        # | MOVIES/COUNTRY                             |
        # ----------------------------------------------

        Country=netflix_Movies.objects.values('Country').annotate(Country_count=Count('Country'))  
        
        df=pd.DataFrame(Country)
        print(df)
        import re
        for i in df.index:
            df.loc[i,'Country']=re.sub('[^\w\s_]+','',str(df.loc[i,'Country'])).capitalize().strip().replace('\n','')
            print(df.loc[i,'Country'])
            if 'United states' == df.loc[i,'Country'] :
                df.loc[i,'Country']='USA'
            if 'United states ' == df.loc[i,'Country']:
                df.loc[i,'Country']='USA'
        df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Country'].values()))
        context.update({'Production_Country_1_label':list(df[:].to_dict()['Country'].values())})
        context.update({'Production_Country_1_label_count':list(df[:].to_dict()['Country_count'].values())})



        # ----------------------------------------------
        # | MOVIES/GENRE                             |
        # ----------------------------------------------



        d=netflix_Movies.objects.exclude(Name__in="-").values_list('Rating','Name','Points').order_by('-Points')
        cum_bo=netflix_Movies.objects.exclude(Name__in="-").values_list('Name','Rating').order_by('-Rating')
        cum_bol=netflix_Movies.objects.exclude(Name__in="-").values_list('Name','Points').order_by('-Points')
        cum_adm=netflix_Movies.objects.exclude(Name__in="-").exclude(Genre__in="-").values_list('Genre','Points').order_by('-Points')
        cum_admlo=netflix_Movies.objects.exclude(Lead_Actor_1_Name__in="-").exclude(Name__in="-").values_list('Lead_Actor_1_Name','Points').order_by('-Points')
        profit=netflix_Movies.objects.exclude(Lead_Actor_2_Name__in="-").values_list('Lead_Actor_2_Name','Points').order_by('-Points')
        profitlo=netflix_Movies.objects.exclude(Production_Company_1__in="-").values_list('Production_Company_1','Points').order_by('-Points')
        Profitability=netflix_Movies.objects.exclude(Production_Company_1__in="-").values_list('Production_Company_1','Points').order_by('-Points')
        Profitabilitylo=netflix_Movies.objects.exclude(Production_Company_1__in="-").values_list('Production_Company_1','Points').order_by('-Points')
        # DBO=global_box.objects.exclude(Name__in="-").values_list('Name','Domestic_Box_office').order_by('-Domestic_Box_office')
        # IBO=global_box.objects.exclude(Name__in="-").values_list('Name','International_Box_Office').order_by('-International_Box_Office')
        # World_Wide_Box_Office=global_box.objects.exclude(Name__in="-").values_list('Name','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        # Production_Country_1_World_Wide_Box_Office=global_box.objects.exclude(Production_Country_1__in="-").values_list('Production_Country_1','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        # Production_Country_2_World_Wide_Box_Office=global_box.objects.exclude(Production_Country_2__in="-").values_list('Production_Country_2','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        # Production_Country_3_World_Wide_Box_Office=global_box.objects.exclude(Production_Country_3__in="-").values_list('Production_Country_3','World_Wide_Box_Office').order_by('-World_Wide_Box_Office')
        
        # lead_actor1_cum_bo=global_box.objects.exclude(Lead_Actor_1_Name__in='-').exclude(Movie__in="-").values_list('Lead_Actor_1_Name','FILM','CUM_BO').order_by('-CUM_BO')
        # lead_actor2_cum_bo=global_box.objects.exclude(Lead_Actor_2_Name__in='-').exclude(Movie__in="-").values_list('Lead_Actor_2_Name','FILM','CUM_BO').order_by('-CUM_BO')
        # prod_comp_cum_bo=global_box.objects.exclude(Production_Company_1__in='-').exclude(Movie__in="-").values_list('Production_Company_1','FILM','CUM_BO').order_by('-CUM_BO')
        # distrubute_cum_bo=global_box.objects.exclude(DIST__in='-').exclude(Movie__in="-").values_list('DIST','FILM','CUM_BO').order_by('-CUM_BO')

        # print(cum_adm)
        context.update({
            'cum_bo':cum_bo,
            'cum_bol':cum_bol,
            'cum_adm':cum_adm,
            'cum_admlo':cum_admlo,
            'profit':profit,
            'profitlo':profitlo,
            'Profitability':Profitability,
            'Profitabilitylo':Profitabilitylo,
            # 'DBO':DBO,

            # 'IBO':IBO,
            # 'World_Wide_Box_Office':World_Wide_Box_Office,
            # 'Production_Country_1_World_Wide_Box_Office':Production_Country_1_World_Wide_Box_Office,
            # 'Production_Country_2_World_Wide_Box_Office':Production_Country_2_World_Wide_Box_Office,
            # 'Production_Country_3_World_Wide_Box_Office':Production_Country_3_World_Wide_Box_Office,

            # 'lead_actor1_cum_bo':lead_actor1_cum_bo,
            # 'lead_actor2_cum_bo':lead_actor2_cum_bo,
            # 'prod_comp_cum_bo':prod_comp_cum_bo,
            # 'distrubute_cum_bo':distrubute_cum_bo,

        })

        Movies_rating=data.objects.exclude(FILM__in='-').values_list('Rating','FILM','CUM_GBO_USD').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_Amazon=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Amazon').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        # print(pd.DataFrame(Movies_rating_Amazon))

        Series_rating=series.objects.values_list('Rating','Series_Name','Streamer').order_by('-Rating')
        prod_companies_num_mov=prod_companies.objects.values_list('Production_Companies','No_of_Movies').order_by('-No_of_Movies')
        prod_companies_WBO=prod_companies.objects.values_list('Production_Companies','Total_Worldwide_Box_Office').order_by('-Total_Worldwide_Box_Office')

        context.update({
            'Movies_rating_Amazon':Movies_rating_Amazon,
            'Movies_rating_netflix':Movies_rating_netflix,
            'Series_rating':Series_rating,
            'prod_companies_num_mov':prod_companies_num_mov,
            'prod_companies_WBO':prod_companies_WBO,
            'series':series.objects.all(),
            'ksatv':ksa_tv.objects.all(),
        })

        # COLORS- #3358f4 #00d0df
        
        # print(countries)

        # -----------------------
        # | Movie v/s STREAMER  |
        # -----------------------



        Movies_streamer=data.objects.values('Streamer')
        Movies_Netflix=0
        Movies_Amazone=0
        Movies_iTunes=0
        Movies_hulu=0
        Movies_Disney=0
        for i in Movies_streamer:
            # print(i['Streamer'])
            if 'netflix' in i['Streamer'].lower():
                Movies_Netflix+=1
            if 'amazon' in i['Streamer'].lower():
                Movies_Amazone+=1

            if 'itunes' in i['Streamer'].lower():
                Movies_iTunes+=1

            if 'hulu' in i['Streamer'].lower():
                Movies_hulu+=1
            if 'disney' in i['Streamer'].lower():
                Movies_Disney+=1
        Most_movies_on=pd.DataFrame([['Netflix','Amazon','iTunes','hulu','Disney'],[Movies_Netflix,
            Movies_Amazone,
            Movies_iTunes,
            Movies_hulu,
            Movies_Disney]],
            ).transpose().sort_values(by=1,ascending=False)[:1]
        # print()
        context.update({
            'Movies_Netflix':Movies_Netflix,
            'Movies_Amazone':Movies_Amazone,
            'Movies_iTunes':Movies_iTunes,
            'Movies_hulu':Movies_hulu,
            'Movies_Disney':Movies_Disney,
            'Most_movies_on':Most_movies_on.to_dict()[0][1],
            })


        




        # -----------------------
        # | Moives v/s Genre |
        # -----------------------



        movie_genre=netflix_Movies.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))  

        sgdf=pd.DataFrame(movie_genre)
        for i in sgdf.index:
            sgdf.loc[i,'Genre']=str(sgdf.loc[i,'Genre']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='genre_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_genre_label':list(sgdf[:].to_dict()['Genre'].values())})
        context.update({'movie_genre_label_count':list(sgdf[:].to_dict()['genre_count'].values())})
        # print(context)
       

        # -----------------------
        # | Moives v/s sub_Genre1|
        # -----------------------

         # ----------------------------------------------
        # | MOVIES/Year                             |
        # ----------------------------------------------

        Release_Year_m=global_box.objects.exclude(Release_Year__in='None').exclude(Release_Year__in='-').values('Release_Year').annotate(Country_count=Count('Release_Year'))  
        print(Release_Year_m)
        df=pd.DataFrame(Release_Year_m)
        print(df)
        import re
        
        # df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Release_Year'].values()))
        context.update({'Release_Year_label':list(df[:].to_dict()['Release_Year'].values())})
        context.update({'Release_Year_label_count':list(df[:].to_dict()['Country_count'].values())})

    
        movie_Sub_Genre_1=netflix_Movies.objects.exclude(Sub_Genre_1__in='-').values('Sub_Genre_1').annotate(Sub_Genre_1_count=Count('Sub_Genre_1'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_1)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_1']=str(sgdf.loc[i,'Sub_Genre_1']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_1_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_1_label':list(sgdf[:].to_dict()['Sub_Genre_1'].values())})
        context.update({'movie_Sub_Genre_1_label_count':list(sgdf[:].to_dict()['Sub_Genre_1_count'].values())})
        # print(context)
       
        # -------------------------
        # | Moives v/s sub_Genre2 |
        # -------------------------


    
        movie_Sub_Genre_2=netflix_Movies.objects.exclude(Sub_Genre_2__in='-').values('Sub_Genre_2').annotate(Sub_Genre_2_count=Count('Sub_Genre_2'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_2)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_2']=str(sgdf.loc[i,'Sub_Genre_2']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_2_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_2_label':list(sgdf[:].to_dict()['Sub_Genre_2'].values())})
        context.update({'movie_Sub_Genre_2_label_count':list(sgdf[:].to_dict()['Sub_Genre_2_count'].values())})
        # print(context)


        context.update(
            {'data':d,
            'segment':'index',
            'Movies_rating':Movies_rating
            }
            )
    



    if file_name=='OTT':
        context={'Dash':'OTT'}
        main_data=pd.DataFrame(series.objects.values())
        # print(main_data)

        # ----------------------------------------------
        # | MOVIES PER MONTH BY GENRE (TOP 5-6 GENRES) |
        # ----------------------------------------------


        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] 
        


        # ----------------------------------------------
        # | Total Movies                               |
        # ----------------------------------------------

        # ----------------------------------------------
        # | Highest CIM BO USD                         |
        # ----------------------------------------------
        CUM_GBO_USD___max=data.objects.aggregate(Max('CUM_GBO_USD'))
        
        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            }
            )




        # ----------------------------------------------
        # | MOST MOVIES FROM COUNTRY                   |
        # ----------------------------------------------
        Country___max=data.objects.aggregate(Max('Country'))


        context.update(
            {
            'CUM_GBO_USD___max':CUM_GBO_USD___max,
            'Country___max':Country___max,
            }
            )



        # ----------------------------------------------
        # | MOVIES PER MONTH                           |
        # ----------------------------------------------


        m=[]
        movies_months=data.objects.values('RELEASE_DATE')    
        for i in movies_months:
            # print(i['RELEASE_DATE'])
            if i['RELEASE_DATE']:
                m.append(i['RELEASE_DATE'].strftime('%b'))
            
        # m.sort()
        
        count = pd.Series(m).value_counts(sort=True,ascending=True)
        # print(count.to_dict())
        from collections import OrderedDict
        od=OrderedDict(sorted(count.to_dict().items(),key =lambda x:months.index(x[0])))
        # print(od.keys())
        movies_month_label_release=list(od.keys())
        # print(movies_month_label_release)
        movies_month_count_release=list(od.values())
        # print(movies_month_count_release)
        context.update({'movies_month_label_release':movies_month_label_release})
        # print(movies_month_label_release)
        context.update({'movies_month_count_release':movies_month_count_release})



        # ----------------------------------------------
        # | MOVIES/COUNTRY                             |
        # ----------------------------------------------

        countries=series.objects.exclude(Country__in='-').exclude(Country__in='None').values('Country').annotate(Country_count=Count('Country'))  
        
        df=pd.DataFrame(countries)
        print(df)
        import re
        for i in df.index:
            df.loc[i,'Country']=re.sub('[^\w\s_]+','',str(df.loc[i,'Country'])).capitalize().strip().replace('\n','')
            print(df.loc[i,'Country'])
            if 'United states' == df.loc[i,'Country'] :
                df.loc[i,'Country']='USA'
            if 'United states ' == df.loc[i,'Country']:
                df.loc[i,'Country']='USA'
        df.sort_values(by='Country_count',ascending=False,inplace=True,ignore_index=True)
    
        print(list(df[:].to_dict()['Country'].values()))
        context.update({'Country_label':list(df[:].to_dict()['Country'].values())})
        context.update({'Country_label_count':list(df[:].to_dict()['Country_count'].values())})



        # ----------------------------------------------
        # | MOVIES/GENRE                             |
        # ----------------------------------------------



        d=series.objects.all()
        prod_comp_worldBO=series.objects.exclude(Series_Name__in='-').values_list('Rating','Series_Name','Country').order_by('-Rating')
        prod_compDomesticBO=series.objects.exclude(Series_Name__in='-').exclude(Lead_Actor_1_Name__in='-').values_list('Series_Name','Lead_Actor_1_Name','Lead_Actor_1_Nationality').order_by('-Lead_Actor_1_Nationality')
        prod_compBynoOfMovies=series.objects.exclude(Series_Name__in='-').exclude(Lead_Actor_2_Name__in='-').values_list('Series_Name','Lead_Actor_2_Name','Lead_Actor_2_Nationality').order_by('-Lead_Actor_2_Nationality')
        # lead_actor1_cum_bo=data.objects.exclude(Lead2Actor_1_Name__in='-').exclude(Production_Companies__in='-').values_list('Lead_Actor_1_Name','Production_Companies','CUM_BO').order_by('-CUM_BO')
        # lead_actor2_cum_bo=data.objects.exclude(Lead_Actor_2_Name__in='-').exclude(FILM__in='-').values_list('Lead_Actor_2_Name','FILM','CUM_BO').order_by('-CUM_BO')
        # prod_comp_cum_bo=data.objects.exclude(Production_Company_1__in='-').exclude(FILM__in='-').exclude(Rating__in="nan").values_list('Production_Company_1','FILM','CUM_BO').order_by('-CUM_BO')
        # distrubute_cum_bo=data.objects.exclude(DIST__in='-').exclude(FILM__in='-').exclude(Rating__in="nan").values_list('DIST','FILM','CUM_BO').order_by('-CUM_BO')

        # print(Total_Domestic_Box_Office)
        context.update({
            'prod_comp_worldBO':prod_comp_worldBO,
            'prod_compDomesticBO':prod_compDomesticBO,
            'prod_compBynoOfMovies':prod_compBynoOfMovies,
            # 'lead_actor1_cum_bo':lead_actor1_cum_bo,
            # 'lead_actor2_cum_bo':lead_actor2_cum_bo,
            # 'prod_comp_cum_bo':prod_comp_cum_bo,
            # 'distrubute_cum_bo':distrubute_cum_bo,

        })

        Movies_rating=data.objects.exclude(FILM__in='-').values_list('Rating','FILM','CUM_GBO_USD').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_Amazon=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Amazon').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        Movies_rating_netflix=data.objects.exclude(FILM__in='-').filter(Streamer__contains='Netflix').values_list('Rating','FILM','Streamer').exclude(Rating__in=['','nan','none',None]).order_by('-Rating')
        # print(pd.DataFrame(Movies_rating_Amazon))

        Series_rating=series.objects.values_list('Rating','Series_Name','Streamer').order_by('-Rating')
        prod_companies_num_mov=prod_companies.objects.values_list('Production_Companies','No_of_Movies').order_by('-No_of_Movies')
        prod_companies_WBO=prod_companies.objects.values_list('Production_Companies','Total_Worldwide_Box_Office').order_by('-Total_Worldwide_Box_Office')

        context.update({
            'Movies_rating_Amazon':Movies_rating_Amazon,
            'Movies_rating_netflix':Movies_rating_netflix,
            'Series_rating':Series_rating,
            'prod_companies_num_mov':prod_companies_num_mov,
            'prod_companies_WBO':prod_companies_WBO,
            'series':series.objects.all(),
            'ksatv':ksa_tv.objects.all(),
        })

        # COLORS- #3358f4 #00d0df
        
        # print(countries)

        # -----------------------
        # | Movie v/s STREAMER  |
        # -----------------------



        Movies_streamer=data.objects.values('Streamer')
        Movies_Netflix=0
        Movies_Amazone=0
        Movies_iTunes=0
        Movies_hulu=0
        Movies_Disney=0
        for i in Movies_streamer:
            # print(i['Streamer'])
            if 'netflix' in i['Streamer'].lower():
                Movies_Netflix+=1
            if 'amazon' in i['Streamer'].lower():
                Movies_Amazone+=1

            if 'itunes' in i['Streamer'].lower():
                Movies_iTunes+=1

            if 'hulu' in i['Streamer'].lower():
                Movies_hulu+=1
            if 'disney' in i['Streamer'].lower():
                Movies_Disney+=1
        Most_movies_on=pd.DataFrame([['Netflix','Amazon','iTunes','hulu','Disney'],[Movies_Netflix,
            Movies_Amazone,
            Movies_iTunes,
            Movies_hulu,
            Movies_Disney]],
            ).transpose().sort_values(by=1,ascending=False)[:1]
        # print()
        context.update({
            'Movies_Netflix':Movies_Netflix,
            'Movies_Amazone':Movies_Amazone,
            'Movies_iTunes':Movies_iTunes,
            'Movies_hulu':Movies_hulu,
            'Movies_Disney':Movies_Disney,
            'Most_movies_on':Most_movies_on.to_dict()[0][1],
            })


        




        # -----------------------
        # | Moives v/s Genre |
        # -----------------------



        movie_genre=series.objects.exclude(Genre__in='-').values('Genre').annotate(genre_count=Count('Genre'))  

        sgdf=pd.DataFrame(movie_genre)
        for i in sgdf.index:
            sgdf.loc[i,'Genre']=str(sgdf.loc[i,'Genre']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='genre_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_genre_label':list(sgdf[:].to_dict()['Genre'].values())})
        context.update({'movie_genre_label_count':list(sgdf[:].to_dict()['genre_count'].values())})
        # print(context)
       
        # -----------------------
        # | Moives v/s Genre |
        # -----------------------



        movie_Production_Company_1=data.objects.exclude(Production_Company_1__in='-').values('Production_Company_1').annotate(Production_Company_1_count=Count('Production_Company_1'))  

        sgdf=pd.DataFrame(movie_Production_Company_1)
        for i in sgdf.index:
            sgdf.loc[i,'Production_Company_1']=str(sgdf.loc[i,'Production_Company_1']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Production_Company_1_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Production_Company_1_label':list(sgdf[:].to_dict()['Production_Company_1'].values())})
        context.update({'movie_Production_Company_1_label_count':list(sgdf[:].to_dict()['Production_Company_1_count'].values())})
        # print(context)
       
        # -------------------------------------
        # | Moives v/s subGenre_1|
        # --------------------------------------


    
        movie_Sub_Genre_1=series.objects.exclude(Sub_Genre_1__in='-').values('Sub_Genre_1').annotate(Sub_Genre_1_count=Count('Sub_Genre_1'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_1)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_1']=str(sgdf.loc[i,'Sub_Genre_1']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_1_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_1_label':list(sgdf[:].to_dict()['Sub_Genre_1'].values())})
        context.update({'movie_Sub_Genre_1_label_count':list(sgdf[:].to_dict()['Sub_Genre_1_count'].values())})
        # print(context)
       
        # -------------------------
        # | Moives v/s sub_Genre2 |
        # -------------------------


    
        movie_Sub_Genre_2=series.objects.exclude(Sub_Genre_2__in='-').values('Sub_Genre_2').annotate(Sub_Genre_2_count=Count('Sub_Genre_2'))  

        sgdf=pd.DataFrame(movie_Sub_Genre_2)
        for i in sgdf.index:
            sgdf.loc[i,'Sub_Genre_2']=str(sgdf.loc[i,'Sub_Genre_2']).capitalize().strip().replace('\n','')
            # print(sgdf.loc[i,'Country'])
        sgdf.sort_values(by='Sub_Genre_2_count',ascending=False,inplace=True,ignore_index=True)
        # print(df)
        context.update({'movie_Sub_Genre_2_label':list(sgdf[:].to_dict()['Sub_Genre_2'].values())})
        context.update({'movie_Sub_Genre_2_label_count':list(sgdf[:].to_dict()['Sub_Genre_2_count'].values())})
        # print(context)


        context.update(
            {'data':d,
            'segment':'index',
            'Movies_rating':Movies_rating
            }
            )

    return render(request,
    'home/index.html',context)


@login_required(login_url="/login/")
def tables(request,table_name):
    if 'data'==table_name:

        temp_name='home/ui-tables.html'
        model=data
        filter_name=MovieFilter
    elif 'global'==table_name:
        temp_name='home/global.html'
        model=global_box
        filter_name=globalFilter

    elif 'ksatv'==table_name:
        temp_name='home/ksatv.html'
        model=ksa_tv
        filter_name=ksatvFilter
    elif 'series'==table_name:
        temp_name='home/series.html'
        model=series
        filter_name=seriesFilter

    elif 'prod_companies'==table_name:
        temp_name='home/prod_companies.html'
        model=prod_companies
        filter_name=prodcompFilter
    elif 'netflix_series'==table_name:
        temp_name='home/netflix_series.html'
        model=netflix_series
        filter_name=Netflix_series_filter
    elif 'netflix_movies'==table_name:
        temp_name='home/netflix_movies.html'
        model=netflix_Movies
        filter_name=Netflix_movies_filter
    else:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render({}, request))
    # print(tuple(set((x['Country'] for x in data.objects.values('Country')))))
    d=model.objects.values().distinct()
    filter_s=filter_name(request.GET,queryset=d)
    d=filter_s.qs
    return render(request,temp_name,
        {
            'data':d,
            'segment':'tables',
            'MovieFilter':filter_s
        }
    )

def ALLSEARCH(request):
 
    # print("here")
    q=request.GET['q']
    # print(q)
    if ':' in q:
        table_name=q.split(':')[0]
        q=q.split(':')[1]
        # print(q)
        # print(q)
        
        if 'ksa'==table_name:
            temp_name='home/ui-tables.html'
            model=data
            filter_name=MovieFilter
        elif 'global'==table_name:
            temp_name='home/global.html'
            model=global_box
            filter_name=globalFilter

        elif 'ksatv'==table_name:
            temp_name='home/ksatv.html'
            model=ksa_tv
            filter_name=ksatvFilter
        elif 'series'==table_name:
            temp_name='home/series.html'
            model=series
            filter_name=seriesFilter

        elif 'prod_companies'==table_name:
            temp_name='home/prod_companies.html'
            model=prod_companies
            filter_name=prodcompFilter
        elif 'netflix_series'==table_name:
            temp_name='home/netflix_series.html'
            model=netflix_series
            filter_name=Netflix_series_filter
        elif 'netflix_movies'==table_name:
            temp_name='home/netflix_movies.html'
            model=netflix_Movies
            filter_name=Netflix_movies_filter
        else:
            html_template = loader.get_template('home/page-search-error.html')
            return HttpResponse(html_template.render({}, request))
    else:
        html_template = loader.get_template('home/page-search-error.html')
        return HttpResponse(html_template.render({}, request))
    all_fields=model._meta.get_fields()
    seacrh_fields=[x.name for x in all_fields]
    # print(seacrh_fields)
    search_text=q
    all_search=reduce(or_, (Q(**{'{}__contains'.format(f): search_text}) for f in seacrh_fields),Q())
    # print(all_search)
    d=model.objects.filter(all_search)

    # print(d)
    d=model.objects.values().distinct()
    filter_s=filter_name(request.GET,queryset=d)
    d=filter_s.qs
    d=model.objects.filter(all_search).values().distinct()
    return render(request,temp_name,
    {
        'data':d,
    'segment':'tables',
    'MovieFilter':filter_s
    }
    )

@login_required(login_url="/login/")
def dashboard_with_pivot(request):
    return render(request, 'home/ana.html', {})

@login_required(login_url="/login/")
def pivot_data(request):
    dataset = data.objects.all()
    dataa = serializers.serialize('json', dataset)
    return JsonResponse(dataa, safe=False)

@login_required(login_url="/login/")
def delete_row(request,model_name,id):
    if 'ksa'==model_name:
            temp_name='home/ui-tables.html'
            model=data
    elif 'global'==model_name:
        temp_name='home/global.html'
        model=global_box
    elif 'ksatv'==model_name:
        temp_name='home/ksatv.html'
        model=ksa_tv
    elif 'series'==model_name:
        temp_name='home/series.html'
        model=series
    elif 'prod_companies'==model_name:
        temp_name='home/prod_companies.html'
        model=prod_companies
    elif 'netflix_series'==model_name:
        temp_name='home/netflix_series.html'
        model=netflix_series
            
    elif 'netflix_movies'==model_name:
        temp_name='home/netflix_movies.html'
        model=netflix_Movies

    else:
        html_template = loader.get_template('home/page-search-error.html')
        return HttpResponse(html_template.render({}, request))
    # model=model_name
    ob=model.objects.get(Rank=id)
    ob.delete()
    return render(request,temp_name)



@login_required(login_url="/login/")
def filter(request,model_name,f,order):
    if 'data'==model_name:
            temp_name='home/ui-tables.html'
            model=data
    elif 'global'==model_name:
        temp_name='home/global.html'
        model=global_box
    elif 'ksatv'==model_name:
        temp_name='home/ksatv.html'
        model=ksa_tv
    elif 'series'==model_name:
        temp_name='home/series.html'
        model=series
    elif 'prod_companies'==model_name:
        temp_name='home/prod_companies.html'
        model=prod_companies
    elif 'netflix_series'==model_name:
        temp_name='home/netflix_series.html'
        model=netflix_series
            
    elif 'netflix_movies'==model_name:
        temp_name='home/netflix_movies.html'
        model=netflix_Movies
    else:
        html_template = loader.get_template('home/page-search-error.html')
        return HttpResponse(html_template.render({}, request))
    
    if order=='asc':
       o=''
    if order=='dsc':
        o='-'
     
    d=model.objects.all().order_by(o+f).values().distinct()
    return render(request,temp_name,
    {
        'data':d,
        'segment':'tables'
    })


@login_required(login_url="/login/")
def RangeFilterss(request,model_name,f,qrange):
    # print('here')
    if 'ksa'==model_name:
            temp_name='home/ui-tables.html'
            model=data
    elif 'global'==model_name:
        temp_name='home/global.html'
        model=global_box
    elif 'ksatv'==model_name:
        temp_name='home/ksatv.html'
        model=ksa_tv
    elif 'series'==model_name:
        temp_name='home/series.html'
        model=series
    elif 'prod_companies'==model_name:
        temp_name='home/prod_companies.html'
        model=prod_companies
    elif 'netflix_series'==model_name:
        temp_name='home/netflix_series.html'
        model=netflix_series
            
    elif 'netflix_movies'==model_name:
        temp_name='home/netflix_movies.html'
        model=netflix_Movies
    else:
        html_template = loader.get_template('home/page-search-error.html')
        return HttpResponse(html_template.render({}, request))
    
    srange=qrange.split('-')[0]

    erange=qrange.split('-')[1]

    if erange=='':
        range_search=(Q(**{'{}__gte'.format(f): srange}))

    else:
        range_search=(Q(**{'{}__range'.format(f): [srange,erange]}))
    # print(range_search)
    d=model.objects.filter(range_search).values().distinct()

    # print(d)
    return render(request,temp_name,
    {
        'data':d,
        'segment':'tables'
    })


@login_required(login_url="/login/")
def uploads(request):

    if request.method=='POST':
            file_type=request.POST['file_type'].lower()
            file_name=request.FILES.get('files')

            print(file_type)
            print(file_name)

            if 'global' == file_type:
                r=0
                print(file_name)
                sheetNames=pd.ExcelFile(file_name,engine='openpyxl')
                # print(sheet_names)
                for sheet in sheetNames.sheet_names:
                    df=pd.read_excel(file_name,engine='openpyxl',sheet_name=sheet)
                    print(df.columns)
                    df.columns = [c.strip().replace('  ',' ').replace('.','').replace('# ','').replace('#','').replace('1st','First') for c in df.columns.values.tolist()]
                    # print(df.columns)
                # ob=global_box()
                    df.fillna("-",inplace=True)
                    df['Production Budget'].replace(to_replace='-',value='0',inplace=True)
                    df['Other Costs'].replace(to_replace='-',value='0',inplace=True)
                    df['Profit'].replace(to_replace='-',value='0',inplace=True)
                    df['Profitability'].replace(to_replace='-',value='0',inplace=True)
                    df['Run Time'].replace(to_replace='-',value='-',inplace=True)
                    df['of Prod Companies'].replace(to_replace='-',value='0',inplace=True)
                    df['Domestic Box office'].replace(to_replace='-',value='0',inplace=True)
                    df['International Box Office'].replace(to_replace='-',value='0',inplace=True)
                    df['World Wide Box Office'].replace(to_replace='-',value='0',inplace=True)
                    print(df.columns)
                    # print(df['Genera '])
                    # print(df['Genre'])
                    for i in df.index:
                            try:
                                r+=1
                                print(df.loc[i,'Movie'])
                                ob=global_box()
                                ob.Rank=r
                                ob.Movie =str(df.loc[i,'Movie']).rstrip()
                                ob.Release_Year= df.loc[i,'Release Year']
                                ob.Genre=str(df.loc[i,'Genre']).lower().rstrip()
                                ob.Sub_Genera_1=str(df.loc[i,'Sub-Genera 1']).lower().rstrip()
                                ob.Sub_Genera_2=str(df.loc[i,'Sub-Genera 2']).lower().rstrip()
                                ob.Production_Budget= float(str(df.loc[i,'Production Budget']).replace(' ','').replace('$','').replace(',',''))
                                ob.Other_Costs =float(str(df.loc[i,'Other Costs']).replace(' ','').replace('$','').replace(',',''))
                                ob.Profit  =float(str(df.loc[i,'Profit']).replace('(','').replace(')','').replace(' ','').replace('$','').replace(',',''))
                                ob.Profitability =df.loc[i,'Profitability']
                                ob.Rating =str(df.loc[i,'Rating'])
                                ob.Run_Time =str(df.loc[i,'Run Time'])
                                ob.Franchise =str(df.loc[i,'Franchise'])
                                ob.Key_Word_1 =str(df.loc[i,'Key Word 1'])
                                ob.Key_Word_2=str(df.loc[i,'Key Word 2'])
                                ob.Key_Word_3=str(df.loc[i,'Key Word 3'])
                                ob.Key_Word_4=str(df.loc[i,'Key Word 4'])
                                ob.Key_Word_5=str(df.loc[i,'Key Word 5'])
                                ob.Source =str(df.loc[i,'Source'])
                                ob.Production_Method =str(df.loc[i,'Production Method'])
                                ob.Creative_Type =str(df.loc[i,'Creative Type'])
                                ob.Prod_Companies =str(df.loc[i,'of Prod Companies'])
                                ob.Prod_Company_1 =str(df.loc[i,'Prod Company 1'])
                                ob.Prod_Company_2=str(df.loc[i,'Prod Company 2'])
                                ob.Prod_Company_3=str(df.loc[i,'Prod Company 3'])
                                ob.Prod_Company_4=str(df.loc[i,'Prod Company 4'])
                                ob.Production_Country_1 =str(df.loc[i,'Production Country 1'])
                                ob.Production_Country_2=str(df.loc[i,'Production Country 2'])
                                ob.Production_Country_3=str(df.loc[i,'Production Country 3'])
                                ob.Language =str(df.loc[i,'Language'])
                                ob.Domestic_Box_office =float(str(df.loc[i,'Domestic Box office']).replace(' ','').replace('$','').replace(',',''))
                                ob.International_Box_Office =float(str(df.loc[i,'International Box Office']).replace(' ','').replace('$','').replace(',',''))
                                ob.World_Wide_Box_Office =float(str(df.loc[i,'World Wide Box Office']).replace(' ','').replace('$','').replace(',',''))
                                ob.save()
                        
                            except IntegrityError:
                                import sys
                                print(sys.exc_info())
                                continue
            
            if 'local' == file_type:
                r=0
                print(file_name)
                sheetNames=pd.ExcelFile(file_name,engine='openpyxl')
                # print(sheet_names)
                for sheet in sheetNames.sheet_names:
                    df=pd.read_excel(file_name,engine='openpyxl',sheet_name=sheet)
                    print(df.columns)
                    df.columns = [c.strip().replace('  ',' ').replace('.','').replace('# ','').replace('#','').replace('1st','First') for c in df.columns.values.tolist()]
                    # print(df.columns)
                # ob=global_box()
                    df.fillna("-",inplace=True)
                    df['of Seasons'].replace(to_replace='-',value='0',inplace=True)
                    df['of Episodes / Season'].replace(to_replace='-',value='0',inplace=True)
                    df['of Production Companies'].replace(to_replace='-',value='0',inplace=True)
                    df['Lead Actor 1 Age'].replace(to_replace='-',value='0',inplace=True)
                    df['Lead Actor 2 Age'].replace(to_replace='-',value='0',inplace=True)
                    df['Rating'].replace(to_replace='-',value='0',inplace=True)
                    # df['Domestic Box office'].replace(to_replace='-',value='0',inplace=True)
                    # df['International Box Office'].replace(to_replace='-',value='0',inplace=True)
                    # df['World Wide Box Office'].replace(to_replace='-',value='0',inplace=True)
                    print(df.columns)
                    # print(df['Genera '])
                    # print(df['Genre'])
                    for i in df.index:
                            try:
                                r+=1
                                print(df.loc[i,'Series Name'])
                                ob=series()
                                rating=str(df.loc[i,'Rating'])
                                if rating !='':
                                    if '/' in rating:
                                        rating=rating.split('/')[0]
                                
                                ob.Rank=r
                                ob.Series_Name=str(df.loc[i,'Series Name'])
                                ob.Genre =str(df.loc[i,'Genre']).lower().rstrip()
                                ob.Sub_Genre_1 =str(df.loc[i,'Sub Genre 1']).lower().rstrip()
                                ob.Sub_Genre_2 =str(df.loc[i,'Sub Genre 2']).lower().rstrip()
                                ob.Rating =float(rating)
                                ob.Year_of_Release =str(df.loc[i,'Year of Release'])
                                ob.Country =str(df.loc[i,'Country']).lower().rstrip()
                                ob.Seasons =float(str(df.loc[i,'of Seasons']).replace(' ','').replace('$','').replace(',',''))
                                ob.Episodes_Season =float(str(df.loc[i,'of Episodes / Season']).replace(' ','').replace('$','').replace(',',''))
                                ob.Length_of_Episodes =str(df.loc[i,'Length of Episodes'])
                                ob.Synopsis =str(df.loc[i,'Synopsis'])
                                ob.Keywords_1 =str(df.loc[i,'Keywords 1'])
                                ob.Keywords_2 =str(df.loc[i,'Keywords 2'])
                                ob.Keywords_3=str(df.loc[i,'Keywords 3'])
                                ob.Keywords_4=str(df.loc[i,'Keywords 4'])
                                ob.Production_Method =str(df.loc[i,'Production Method'])
                                ob.Creative_Type =str(df.loc[i,'Creative Type'])
                                ob.Production_Companies =float(str(df.loc[i,'of Production Companies']).replace(' ','').replace('$','').replace(',',''))
                                ob.Production_Company_1 =str(df.loc[i,'Production Company 1'])
                                ob.Production_Company_2=str(df.loc[i,'Production Company 2'])
                                ob.Production_Company_3=str(df.loc[i,'Production Company 3'])
                                ob.Production_Company_4=str(df.loc[i,'Production Company 4'])
                                ob.Director=str(df.loc[i,'Director'])
                                ob.Lead_Actor_1_Name =str(df.loc[i,'Lead Actor 1 Name'])
                                ob.Lead_Actor_1_Gender=str(df.loc[i,'Lead Actor 1 Gender'])
                                ob.Lead_Actor_1_Age =float(str(df.loc[i,'Lead Actor 1 Age']).replace(' ','').replace('$','').replace(',',''))
                                ob.Lead_Actor_1_Nationality=str(df.loc[i,'Lead Actor 1 Nationality'])
                                ob.Lead_Actor_2_Name =str(df.loc[i,'Lead Actor 2 Name'])
                                ob.Lead_Actor_2_Gender=str(df.loc[i,'Lead Actor 2 Gender'])
                                ob.Lead_Actor_2_Age =float(str(df.loc[i,'Lead Actor 2 Age']).replace(' ','').replace('$','').replace(',',''))
                                ob.Lead_Actor_2_Nationality=str(df.loc[i,'Lead Actor 2 Nationality'])
                                ob.Target_Audience =str(df.loc[i,'Target Audience'])
                                ob.Streamer=str(df.loc[i,'Streamer']).lower().rstrip()
                                ob.Awards_1 =str(df.loc[i,'Awards 1'])
                                ob.Awards_2=str(df.loc[i,'Awards 2'])
                                ob.Awards_3 =str(df.loc[i,'Awards 3'])
                                ob.Type_of_deal=str(df.loc[i,'Type of deal'])
                                ob.save()
                        
                            except IntegrityError:
                                import sys
                                print(sys.exc_info())
                                continue
            
            if 'ksa_tv' == file_type:
                r=0
                print(file_name)
                sheetNames=pd.ExcelFile(file_name,engine='openpyxl')
                # print(sheet_names)
                for sheet in sheetNames.sheet_names:
                    df=pd.read_excel(file_name,engine='openpyxl',sheet_name=sheet)
                    print(df.columns)
                    df.columns = [c.strip().replace('  ',' ').replace('.','').replace('# ','').replace('#','').replace('1st','First') for c in df.columns.values.tolist()]
                    # print(df.columns)
                # ob=global_box()
                    df.fillna("-",inplace=True)
                    df['Avg-Aud ALL'].replace(to_replace='-',value='0',inplace=True)
                    # df['of Episodes / Season'].replace(to_replace='-',value='0',inplace=True)
                    # df['of Production Companies'].replace(to_replace='-',value='0',inplace=True)
                    # df['Lead Actor 1 Age'].replace(to_replace='-',value='0',inplace=True)
                    # df['Lead Actor 2 Age'].replace(to_replace='-',value='0',inplace=True)
                    # df['Rating'].replace(to_replace='-',value='0',inplace=True)
                    # df['Domestic Box office'].replace(to_replace='-',value='0',inplace=True)
                    # df['International Box Office'].replace(to_replace='-',value='0',inplace=True)
                    # df['World Wide Box Office'].replace(to_replace='-',value='0',inplace=True)
                    print(df.columns)
                    # print(df['Genera '])
                    # print(df['Genre'])
                    for i in df.index:
                            try:
                                r+=1
                                print(df.loc[i,'Prog Name'])
                                ob=ksa_tv()
                                # rating=str(df.loc[i,'Rating'])
                                # if rating !='':
                                #     if '/' in rating:
                                #         rating=rating.split('/')[0]
                                
                                # ob.Rank=r

                                ob.Count_Order=r
                                ob.Prog_Name=str(df.loc[i,'Prog Name'])
                                ob.Station=str(df.loc[i,'Station'])
                                ob.Dow=str(df.loc[i,'Dow'])
                                ob.Month_Year=str(df.loc[i,'Month & Year'])
                                ob.Prog_Sub_Type=str(df.loc[i,'Prog Sub Type'])
                                ob.Prog_Type=str(df.loc[i,'Prog Type'])
                                ob.Prog_Domain=str(df.loc[i,'Prog Domain'])
                                ob.first_Actor=str(df.loc[i,'1rst Actor'])
                                ob.second_Actor=str(df.loc[i,'2nd Actor'])
                                ob.Prog_Producer=str(df.loc[i,'Prog Producer'])
                                ob.Prog_Distributor=str(df.loc[i,'Prog Distributor'])
                                ob.Survey_From=str(df.loc[i,'Survey-From'])
                                ob.Survey_To=str(df.loc[i,'Survey-To'])
                                ob.Avg_Aud_ALL=float(str(df.loc[i,'Avg-Aud ALL']).replace(' ','').replace('$','').replace(',',''))

                                ob.save()
                        
                            except IntegrityError:
                                import sys
                                print(sys.exc_info())
                                continue
            

            if 'number' == file_type:
                r=0
                print(file_name)
                sheetNames=pd.ExcelFile(file_name,engine='openpyxl')
                # print(sheet_names)
                for sheet in sheetNames.sheet_names:
                    df=pd.read_excel(file_name,engine='openpyxl',sheet_name=sheet)
                    print(df.columns)
                    df.columns = [c.strip().replace('  ',' ').replace('.','').replace('# ','').replace('#','').replace('1st','First') for c in df.columns.values.tolist()]
                    # print(df.columns)
                # ob=global_box()
                    df.fillna("-",inplace=True)
                    df['No of Movies'].replace(to_replace='-',value='0',inplace=True)
                    df['Total Domestic Box Office'].replace(to_replace='-',value='0',inplace=True)
                    df['Total Worldwide Box Office'].replace(to_replace='-',value='0',inplace=True)
                    # df['Lead Actor 1 Age'].replace(to_replace='-',value='0',inplace=True)
                    # df['Lead Actor 2 Age'].replace(to_replace='-',value='0',inplace=True)
                    # df['Rating'].replace(to_replace='-',value='0',inplace=True)
                    # df['Domestic Box office'].replace(to_replace='-',value='0',inplace=True)
                    # df['International Box Office'].replace(to_replace='-',value='0',inplace=True)
                    # df['World Wide Box Office'].replace(to_replace='-',value='0',inplace=True)
                    print(df.columns)
                    # print(df['Genera '])
                    # print(df['Genre'])
                    for i in df.index:
                            try:
                                r+=1
                                print(df.loc[i,'Production Companies'])
                                ob=prod_companies()
                                # rating=str(df.loc[i,'Rating'])
                                # if rating !='':
                                #     if '/' in rating:
                                #         rating=rating.split('/')[0]
                                
                                # ob.Rank=r

                                ob.Production_Companies=str(df.loc[i,'Production Companies'])
                                ob.No_of_Movies=float(str(df.loc[i,'No of Movies']).replace(' ','').replace('$','').replace(',',''))
                                ob.Total_Domestic_Box_Office=float(str(df.loc[i,'Total Domestic Box Office']).replace(' ','').replace('$','').replace(',',''))
                                ob.Total_Worldwide_Box_Office=float(str(df.loc[i,'Total Worldwide Box Office']).replace(' ','').replace('$','').replace(',',''))

                                ob.save()
                        
                            except IntegrityError:
                                import sys
                                print(sys.exc_info())
                                continue


            if 'ksa' == file_type:
                r=0
                print(file_name)
                sheetNames=pd.ExcelFile(file_name,engine='openpyxl',)
                # print(sheet_names)
                for sheet in sheetNames.sheet_names:
                    df=pd.read_excel(file_name,engine='openpyxl',sheet_name=sheet)

                    # print(df)

                    
                    df.columns = [c.strip().replace('  ',' ').replace('.','').replace('# ','').replace('#','').replace('1st','First') for c in df.columns.values.tolist()]
                    
                    
                    # for col in df.columns:
                    #     print(df[col])
                    # df = df.apply(lambda x: x.str.lower() if x.dtype=='object' else x)
                    # df = df.applymap(lambda s: s.lower() if type(s) == str else s)
                    print(df)
                    # print(df['Genre'])
                    df.fillna("-",inplace=True)
                    
                    df['RELEASE DATE'].replace(to_replace='-',value=None,inplace=True)
                    df['Opening Day Amd'].replace(to_replace='-',value=None,inplace=True)
                    df['First Weekend BO'].replace(to_replace='-',value=None,inplace=True)
                    df['First Weekend ADM'].replace(to_replace='-',value=None,inplace=True)
                    df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    df['First Week ADM'].replace(to_replace='-',value=None,inplace=True)
                    df['CUM BO'].replace(to_replace='-',value=None,inplace=True)
                    df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    df['CUM GBO USD'].replace(to_replace='-',value='0',inplace=True)
                    df['RELEASE DATE'].replace(to_replace='ONLY IN 2021',value=None,inplace=True)
                    df['RELEASE DATE'].replace(to_replace='ONLY IN 2022',value=None,inplace=True)
                    
                    for i in df.index:
                        # for col in df.columns:
                        #     dcol=col.lower().replace(' ','_')
                        #     data().objects[dcol]=df.loc[i,col]
                        # ob.save()
                            try:
                                try:
                                    No_Screens=df.loc[i,'NO Screens']
                                except KeyError:
                                    import sys
                                    print(sys.exc_info())
                                    No_Screens=0
                                try:
                                    No_Screens=int(No_Screens)
                                except ValueError:
                                    No_Screens=0
                                r+=1
                                print(df.loc[i,'FILM'])
                                ob=data()
                                ob.Rank=r
                                ob.FILM=df.loc[i,'FILM']
                                ob.Genre=str(df.loc[i,'Genre']).lower().rstrip()
                                ob.Sub_Genre_1=str(df.loc[i,'Sub Genre 1']).lower().rstrip()
                                ob.Sub_Genre_2=str(df.loc[i,'Sub Genre 2']).lower().rstrip()
                                ob.Rating=str(df.loc[i,'Rating']).replace('/10','')
                                ob.Year_of_Release =df.loc[i,'Year of Release']
                                ob.Country =str(df.loc[i,'Country']).lower().rstrip()
                                ob.Run_Time=df.loc[i,'Run Time']
                                ob.Franchise=str(df.loc[i,'Franchise']).lower().rstrip()
                                ob.Synopsis =df.loc[i,'Synopsis']
                                ob.Keywords_1=str(df.loc[i,'Keywords 1']).lower().rstrip()
                                ob.Keywords_2=str(df.loc[i,'Keywords 2']).lower().rstrip()
                                ob.Keywords_3=str(df.loc[i,'Keywords 3']).lower().rstrip()
                                ob.Keywords_4=str(df.loc[i,'Keywords 4']).lower().rstrip()
                                ob.Production_Method =str(df.loc[i,'Production Method']).lower().rstrip()
                                ob.Creative_Type =df.loc[i,'Creative Type']
                                ob.Production_Companies=df.loc[i,'Production Companies']
                                ob.Production_Company_1=df.loc[i,'Production Company 1'].lower().rstrip()
                                ob.Production_Company_2=df.loc[i,'Production Company 2'].lower().rstrip()
                                ob.Production_Company_3=df.loc[i,'Production Company 3'].lower().rstrip()
                                ob.Production_Company_4=df.loc[i,'Production Company 4'].lower().rstrip()
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
                                ob.Streamer =str(df.loc[i,'Streamer']).lower().rstrip()
                                ob.Awards_1  =df.loc[i,'Awards 1']
                                ob.Awards_2  =df.loc[i,'Awards 2']
                                ob.Awards_3  =df.loc[i,'Awards 3']
                                ob.Type_of_Deal =df.loc[i,'Type of Deal']
                                ob.RELEASE_DATE  =df.loc[i,'RELEASE DATE']
                                ob.DIST  =df.loc[i,'DIST']
                                ob.NO_Screens  =int(No_Screens)
                                ob.Opening_Day_Amd  =df.loc[i,'Opening Day Amd']
                                ob.First_Weekend_BO  =df.loc[i,'First Weekend BO']
                                ob.First_Weekend_Amd  =df.loc[i,'First Weekend ADM']
                                ob.First_Week_BO  =df.loc[i,'First Week BO']
                                ob.First_Week_ADM  =df.loc[i,'First Week ADM']
                                ob.CUM_BO  =df.loc[i,'CUM BO']
                                ob.CUM_ADM = df.loc[i,'CUM ADM']
                                ob.CUM_GBO_USD = str(df.loc[i,'CUM GBO USD']).replace('$','').replace('-','0').replace(',','')
                        
                                ob.save()
                        
                            except IntegrityError:
                                import sys
                                print(sys.exc_info())
                                continue
                    
                        
            if 'netflix_series' == file_type:
                r=0
                print(file_name)
                sheetNames=pd.ExcelFile(file_name,engine='openpyxl',)
                # print(sheet_names)
                for sheet in sheetNames.sheet_names:
                    df=pd.read_excel(file_name,engine='openpyxl',sheet_name=sheet)

                    # print(df)
                    df.columns = [c.strip().replace('  ',' ').replace('.','').replace('# ','').replace('#','').replace('1st','First') for c in df.columns.values.tolist()]
                    print(df)
                    # print(df['Genre'])
                    df.fillna("-",inplace=True)
                    
                    df['Points'].replace(to_replace='-',value=None,inplace=True)
                    # df['Opening Day Amd'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Weekend BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Weekend ADM'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Week ADM'].replace(to_replace='-',value=None,inplace=True)
                    # df['CUM BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['CUM GBO USD'].replace(to_replace='-',value='0',inplace=True)
                    # df['RELEASE DATE'].replace(to_replace='ONLY IN 2021',value=None,inplace=True)
                    # df['RELEASE DATE'].replace(to_replace='ONLY IN 2022',value=None,inplace=True)
                    
                    for i in df.index:
                        # for col in df.columns:
                        #     dcol=col.lower().replace(' ','_')
                        #     data().objects[dcol]=df.loc[i,col]
                        # ob.save()
                            try:
                                # try:
                                #     No_Screens=df.loc[i,'NO Screens']
                                # except KeyError:
                                #     import sys
                                #     print(sys.exc_info())
                                #     No_Screens=0
                                # try:
                                #     No_Screens=int(No_Screens)
                                # except ValueError:
                                #     No_Screens=0
                                r+=1
                                print(df.loc[i,'Name'])
                                ob=netflix_series()
             
                                ob.Year=df.loc[i,'Year']
                                ob.Week=df.loc[i,'Week']
                                ob.Name =df.loc[i,'Name']
                                ob.Points =df.loc[i,'Points']
                                ob.Rank=df.loc[i,'Rank']
                                ob.Genre =df.loc[i,'Genre'].lower().rstrip()
                                ob.Sub_Genre_1=df.loc[i,'Sub Genre 1'].lower().rstrip()
                                ob.Sub_Genre_2=df.loc[i,'Sub Genre 2'].lower().rstrip()
                                ob.Rating=df.loc[i,'Rating']
                                ob.Year_of_Release =df.loc[i,'Year of Release']
                                ob.Country =df.loc[i,'Country'].lower().rstrip()
                                ob.of_Seasons=df.loc[i,'of Seasons']
                                ob.of_episodes_Season=df.loc[i,'of episodes/ Season']
                                ob.Length_of_Episode=df.loc[i,'Length of Episode']
                                ob.Synopsis =df.loc[i,'Synopsis']
                                ob.Keywords_1=df.loc[i,'Keywords 1']
                                ob.Keywords_2=df.loc[i,'Keywords 2']
                                ob.Keywords_3=df.loc[i,'Keywords 3']
                                ob.Keywords_4=df.loc[i,'Keywords 4']
                                ob.Production_Method =df.loc[i,'Production Method']
                                ob.Creative_Type =df.loc[i,'Creative Type']
                                ob.Production_Companies=df.loc[i,'Production Companies']
                                ob.Production_Company_1=df.loc[i,'Production Company 1']
                                ob.Production_Company_2=df.loc[i,'Production Company 2']
                                ob.Production_Company_3=df.loc[i,'Production Company 3']
                                ob.Production_Company_4=df.loc[i,'Production Company 4']
                                ob.Directed_by=df.loc[i,'Directed by']
                                ob.Lead_Actor_1_Name =df.loc[i,'Lead Actor 1 Name']
                                ob.Lead_Actor_1_Gender=df.loc[i,'Lead Actor 1 Gender']
                                ob.Lead_Actor_1_Age =df.loc[i,'Lead Actor 1 Age']
                                ob.Lead_Actor_1_Nationality=df.loc[i,'Lead Actor 1 Nationality']
                                ob.Lead_Actor_2_Name =df.loc[i,'Lead Actor 2 Name']
                                ob.Lead_Actor_2_Gender=df.loc[i,'Lead Actor 2 Gender']
                                ob.Lead_Actor_2_Age =df.loc[i,'Lead Actor 2 Age']
                                ob.Lead_Actor_2_Nationality=df.loc[i,'Lead Actor 2 Nationality']
                                ob.Target_Audience =df.loc[i,'Target Audience']
                                ob.Streamer=df.loc[i,'Streamer'].lower().rstrip()
                                ob.Awards_1=df.loc[i,'Awards 1']
                                ob.Awards_2 =df.loc[i,'Awards 2']
                                ob.Awards_3 =df.loc[i,'Awards 3']

                                ob.save()
                        
                            except IntegrityError:
                                import sys
                                print(sys.exc_info())
                                continue
                    
                        
            if 'netflix_movies' == file_type:
                r=0
                print(file_name)
                sheetNames=pd.ExcelFile(file_name,engine='openpyxl',)
                # print(sheet_names)
                for sheet in sheetNames.sheet_names:
                    df=pd.read_excel(file_name,engine='openpyxl',sheet_name=sheet)

                    # print(df)
                    df.columns = [c.strip().replace('  ',' ').replace('.','').replace('# ','').replace('#','').replace('1st','First') for c in df.columns.values.tolist()]
                    print(df)
                    # print(df['Genre'])
                    df.fillna("-",inplace=True)
                    df['Points'].replace(to_replace='-',value=None,inplace=True)
                    
                    # df['RELEASE DATE'].replace(to_replace='-',value=None,inplace=True)
                    # df['Opening Day Amd'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Weekend BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Weekend ADM'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Week ADM'].replace(to_replace='-',value=None,inplace=True)
                    # df['CUM BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['First Week BO'].replace(to_replace='-',value=None,inplace=True)
                    # df['CUM GBO USD'].replace(to_replace='-',value='0',inplace=True)
                    # df['RELEASE DATE'].replace(to_replace='ONLY IN 2021',value=None,inplace=True)
                    # df['RELEASE DATE'].replace(to_replace='ONLY IN 2022',value=None,inplace=True)
                    
                    for i in df.index:
                        # for col in df.columns:
                        #     dcol=col.lower().replace(' ','_')
                        #     data().objects[dcol]=df.loc[i,col]
                        # ob.save()
                            try:
                                # try:
                                #     No_Screens=df.loc[i,'NO Screens']
                                # except KeyError:
                                #     import sys
                                #     print(sys.exc_info())
                                #     No_Screens=0
                                # try:
                                #     No_Screens=int(No_Screens)
                                # except ValueError:
                                #     No_Screens=0
                                r+=1
                                print(df.loc[i,'Name'])
                                ob=netflix_Movies()
             
                                ob.Year=df.loc[i,'Year']
                                ob.Week=df.loc[i,'Week']
                                ob.Name =str(df.loc[i,'Name']).rstrip()
                                ob.Points =df.loc[i,'Points']
                                ob.Rank=df.loc[i,'Rank']
                                ob.Genre =df.loc[i,'Genre'].lower().rstrip()
                                ob.Sub_Genre_1=df.loc[i,'Sub Genre 1'].lower().rstrip()
                                ob.Sub_Genre_2=df.loc[i,'Sub Genre 2'].lower().rstrip()
                                ob.Rating=float(str(df.loc[i,'Rating']).replace('/10','').replace('·','').replace('IMDb','').replace('MDb','').replace('mdb','').replace('MDB','').replace('I','').replace('-','0').replace('.o','.0').replace('y',''))
                                ob.Year_of_Release =df.loc[i,'Year of Release']
                                ob.Country =df.loc[i,'Country'].lower().rstrip()
                                ob.Run_Time=df.loc[i,'Run Time']
                                ob.Franchise=df.loc[i,'Franchise']
                                ob.Synopsis =df.loc[i,'Synopsis']
                                ob.Keywords_1=df.loc[i,'Keywords 1']
                                ob.Keywords_2=df.loc[i,'Keywords 2']
                                ob.Keywords_3=df.loc[i,'Keywords 3']
                                ob.Keywords_4=df.loc[i,'Keywords 4']
                                ob.Production_Method =df.loc[i,'Production Method']
                                ob.Creative_Type =df.loc[i,'Creative Type']
                                ob.Production_Companies=df.loc[i,'Production Companies']
                                ob.Production_Company_1=df.loc[i,'Production Company 1']
                                ob.Production_Company_2=df.loc[i,'Production Company 2']
                                ob.Production_Company_3=df.loc[i,'Production Company 3']
                                ob.Production_Company_4=df.loc[i,'Production Company 4']
                                ob.Directed_by=df.loc[i,'Director']
                                ob.Lead_Actor_1_Name =df.loc[i,'Lead Actor 1 Name']
                                ob.Lead_Actor_1_Gender=df.loc[i,'Lead Actor 1 Gender']
                                ob.Lead_Actor_1_Age =df.loc[i,'Lead Actor 1 Age']
                                ob.Lead_Actor_1_Nationality=df.loc[i,'Lead Actor 1 Nationality']
                                ob.Lead_Actor_2_Name =df.loc[i,'Lead Actor 2 Name']
                                ob.Lead_Actor_2_Gender=df.loc[i,'Lead Actor 2 Gender']
                                ob.Lead_Actor_2_Age =df.loc[i,'Lead Actor 2 Age']
                                ob.Lead_Actor_2_Nationality=df.loc[i,'Lead Actor 2 Nationality']
                                ob.Target_Audience =df.loc[i,'Target Audience']
                                ob.Streamer=df.loc[i,'Streamer'].lower().rstrip()
                                ob.Awards_1=df.loc[i,'Awards 1']
                                ob.Awards_2 =df.loc[i,'Awards 2']
                                ob.Awards_3 =df.loc[i,'Awards 3']

                                ob.save()
                        
                            except IntegrityError:
                                import sys
                                print(sys.exc_info())
                                continue
                    
                       
            return redirect('upload')

    return render(request,'home/file_uploads.html',{'segment':'uploads'})

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



