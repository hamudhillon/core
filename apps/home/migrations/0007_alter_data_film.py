# Generated by Django 3.2.6 on 2022-08-07 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20220806_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='FILM',
            field=models.CharField(max_length=5000, null=True, unique=True),
        ),
    ]
