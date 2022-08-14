# Generated by Django 3.2.6 on 2022-08-04 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220804_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='Awards_1',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Awards_2',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Awards_3',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='CUM_ADM',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='CUM_BO',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='CUM_GBO_USD',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Country',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Creative_Type',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='DIST',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Director',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='FILM',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='First_Week_ADM',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='First_Week_BO',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='First_Weekend_Amd',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='First_Weekend_BO',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Franchise',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Genre',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Keywords_1',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Keywords_2',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Keywords_3',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Keywords_4',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Lead_Actor_1_Age',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Lead_Actor_1_Gender',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Lead_Actor_1_Name',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Lead_Actor_1_Nationality',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Lead_Actor_2_Age',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Lead_Actor_2_Gender',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Lead_Actor_2_Name',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Lead_Actor_2_Nationality',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='NO_Screens',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Opening_Day_Amd',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Production_Companies',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Production_Company_1',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Production_Company_2',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Production_Company_3',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Production_Company_4',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Production_Method',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='RELEASE_DATE',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Rating',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Run_Time',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Streamer',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Sub_Genre_1',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Sub_Genre_2',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Synopsis',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Target_Audience',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Type_of_Deal',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Year_of_Release',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
    ]
