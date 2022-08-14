
import django_filters
from django import forms
from .models import *
class MovieFilter(django_filters.FilterSet):
   
    FILM = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Film Name', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Director = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Director', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Lead_Actor_1_Name = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Lead Male Actor', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Lead_Actor_2_Name = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Lead Female Actor', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Streamer = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Streamer', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Awards_1 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Awards', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Genre = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Genre', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Production_Company_1 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Production Company', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    # Production_Method = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    #     'placeholder': 'Search by Production Method', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))

    Country=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Country',
        lookup_expr='icontains',
        empty_label=('Select Country'),
        queryset=data.objects.values_list('Country',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Country', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    Genre=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Genre',
        lookup_expr='icontains',
        empty_label=('Select Genre'),
        queryset=data.objects.values_list('Genre',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Genre', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    # Sub_Genre_1=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='Sub_Genre_1',
    #     lookup_expr='icontains',
    #     empty_label=('Select Sub_Genre_1'),
    #     queryset=data.objects.values_list('Sub_Genre_1',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by Sub_Genre_1', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))
    # Sub_Genre_2=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='Sub_Genre_2',
    #     lookup_expr='icontains',
    #     empty_label=('Select Sub_Genre_2'),
    #     queryset=data.objects.values_list('Sub_Genre_2',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by Sub_Genre_2', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))
    # Year_of_Release=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='Year_of_Release',
    #     lookup_expr='icontains',
    #     empty_label=('Select Year_of_Release'),
    #     queryset=data.objects.values_list('Year_of_Release',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by Year_of_Release', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))
    # Creative_Type=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='Creative_Type',
    #     lookup_expr='icontains',
    #     empty_label=('Select Creative_Type'),
    #     queryset=data.objects.values_list('Creative_Type',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by Creative_Type', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))
    # Lead_Actor_1_Nationality=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='Lead_Actor_1_Nationality',
    #     lookup_expr='icontains',
    #     empty_label=('Select Lead_Actor_1_Nationality'),
    #     queryset=data.objects.values_list('Lead_Actor_1_Nationality',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by Lead_Actor_1_Nationality', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))
    # Lead_Actor_2_Nationality=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='Lead_Actor_2_Nationality',
    #     lookup_expr='icontains',
    #     empty_label=('Select Lead_Actor_2_Nationality'),
    #     queryset=data.objects.values_list('Lead_Actor_2_Nationality',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by Lead_Actor_2_Nationality', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))
    # Lead_Actor_1_Gender=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='Lead_Actor_1_Gender',
    #     lookup_expr='icontains',
    #     empty_label=('Select Lead_Actor_1_Gender'),
    #     queryset=data.objects.values_list('Lead_Actor_1_Gender',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by Lead_Actor_1_Gender', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))
    # Lead_Actor_2_Gender=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='Lead_Actor_2_Gender',
    #     lookup_expr='icontains',
    #     empty_label=('Select Lead_Actor_2_Gender'),
    #     queryset=data.objects.values_list('Lead_Actor_2_Gender',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by Lead_Actor_2_Gender', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))
    # DIST=django_filters.ModelChoiceFilter(
    #     label='',
    #     to_field_name='DIST',
    #     lookup_expr='icontains',
    #     empty_label=('Select DIST'),
    #     queryset=data.objects.values_list('DIST',flat=True).distinct(),
    #     widget=forms.Select(
    #         attrs={
    #         'placeholder': 'Search by DIST', 
    #         'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
    #         'id':'inlineFormInputGroup'
    #         }))

    RELEASE_DATE=django_filters.DateFromToRangeFilter(label='', widget=django_filters.widgets.RangeWidget(attrs={
        'type': 'date',
        'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup',
        'title':'Release Date'
    }))

    Rating = django_filters.CharFilter(label='', lookup_expr='lte', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Rating', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    # NO_Screens = django_filters.NumberFilter(label='', lookup_expr='exact', widget=forms.NumberInput(attrs={
    #     'placeholder': 'Search by NO_Screens', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    # CUM_GBO_USD = django_filters.NumberFilter(label='', lookup_expr='lte', widget=forms.NumberInput(attrs={
    #     'placeholder': 'Search by CUM_GBO_USD', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))

    class Meta:
        model=data
        fields=['FILM',
        'Director',
        'Lead_Actor_1_Name',
        'Lead_Actor_2_Name',
        'Streamer',
        'Awards_1',
        'Genre',
        'Production_Company_1',
        # 'Production_Method',
        'Country',
        # 'Genre',
        # 'Sub_Genre_1',
        # 'Sub_Genre_2',
        # 'Year_of_Release',
        # 'Creative_Type',
        # 'Lead_Actor_1_Nationality',
        # 'Lead_Actor_2_Nationality',
        # 'Lead_Actor_1_Gender',
        # 'Lead_Actor_2_Gender',
        # 'DIST',
        'Rating',
        # 'NO_Screens',
        # 'CUM_GBO_USD',
        'RELEASE_DATE',
           
        ]

    # def __init__(self, *args, **kwargs):
    #     super(MovieFilter, self).__init__(*args, **kwargs)
    #     self.filters['Country'].extra.update(
    #         {
    #             'choices': tuple(set((x['Country'] for x in data.objects.values('Country'))))
    #         })

    
f = MovieFilter({'RELEASE_DATE_0': '2016-01-01', 'RELEASE_DATE_0': '2016-02-01'})




class ksatvFilter(django_filters.FilterSet):

    Prog_Name = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Program Name', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    
    first_Actor = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Actor Name', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    
    Station=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Station',
        lookup_expr='icontains',
        empty_label=('Select Station'),
        queryset=ksa_tv.objects.values_list('Station',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Stations', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    Prog_Type=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Prog_Type',
        lookup_expr='icontains',
        empty_label=('Select Prog_Type'),
        queryset=ksa_tv.objects.values_list('Prog_Type',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Prog_Types', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    class meta:
        model=ksa_tv
        fields=[
            'Prog_Name',
            'Station',
            'Prog_Type',
            'first_Actor',
        ]

class globalFilter(django_filters.FilterSet):

    Movie = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Program Name', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Rating = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Rating', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Key_Word_1 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Key Word 1', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Key_Word_2 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Key Word 2', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Key_Word_3 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Key Word 3', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Key_Word_4 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Key Word 4', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))

    Genre=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Genre',
        lookup_expr='icontains',
        empty_label=('Select Genre'),
        queryset=global_box.objects.values_list('Genre',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Genre', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    Language=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Language',
        lookup_expr='icontains',
        empty_label=('Select Language'),
        queryset=global_box.objects.values_list('Language',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Language', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    class meta:
        model=global_box
        fields=[
            'Movie',
            'Genre',
            'Language',
            'Rating',
            'Key_Word_1',
            'Key_Word_2',
            'Key_Word_3',
            'Key_Word_4',
        ]

class prodcompFilter(django_filters.FilterSet):

    Production_Companies = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Production Companies Name', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    No_of_Movies = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by No of Movies', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    
    class meta:
        model=prod_companies
        fields=[
            'Production_Companies',
            'No_of_Movies',
        ]


class seriesFilter(django_filters.FilterSet):

    Series_Name = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Program Name', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Rating = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search by Rating', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Key_Word_1 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Key Word 1', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Key_Word_2 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Key Word 2', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Key_Word_3 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Key Word 3', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))
    Key_Word_4 = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Key Word 4', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))

    Lead_Actor_1_Name = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
    'placeholder': 'Search by Lead Actor Name', 'class': 'form-control col-lg-5 col-md-12 m-2','id':'inlineFormInputGroup'}))

    Genre=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Genre',
        lookup_expr='icontains',
        empty_label=('Select Genre'),
        queryset=series.objects.values_list('Genre',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Genre', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    Country=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Country',
        lookup_expr='icontains',
        empty_label=('Select Country'),
        queryset=series.objects.values_list('Country',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Country', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    Streamer=django_filters.ModelChoiceFilter(
        label='',
        to_field_name='Streamer',
        lookup_expr='icontains',
        empty_label=('Select Streamer'),
        queryset=series.objects.values_list('Streamer',flat=True).distinct(),
        widget=forms.Select(
            attrs={
            'placeholder': 'Search by Streamer', 
            'class': 'filter_op form-control col-lg-5 col-md-12 m-2',
            'id':'inlineFormInputGroup'
            }))
    class meta:
        model=series
        fields=[
            'Series_Name',
            'Genre',
            'Country',
            'Rating',
            'Lead_Actor_1_Name',
            'Streamer',
            'Key_Word_1',
            'Key_Word_2',
            'Key_Word_3',
            'Key_Word_4',
        ]
