# Generated by Django 3.2.6 on 2022-08-10 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20220810_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prod_companies',
            name='Production_Companies',
            field=models.CharField(max_length=5000, unique=True),
        ),
    ]
