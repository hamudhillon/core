# Generated by Django 3.2.6 on 2022-08-09 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_data_cum_gbo_usd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='CUM_ADM',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='CUM_BO',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='First_Week_ADM',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='First_Week_BO',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='First_Weekend_Amd',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='First_Weekend_BO',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Opening_Day_Amd',
            field=models.IntegerField(null=True),
        ),
    ]