# Generated by Django 3.2.6 on 2022-09-27 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_alter_netflix_movies_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prod_companies',
            name='Total_Domestic_Box_Office',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prod_companies',
            name='Total_Worldwide_Box_Office',
            field=models.FloatField(null=True),
        ),
    ]