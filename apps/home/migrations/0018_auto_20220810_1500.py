# Generated by Django 3.2.6 on 2022-08-10 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_global_box_release_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ksa_tv',
            name='Survey_From',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ksa_tv',
            name='Survey_To',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
