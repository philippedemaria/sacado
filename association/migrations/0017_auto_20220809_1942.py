# Generated by Django 3.0.5 on 2022-08-09 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0016_activeyear_solde'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeyear',
            name='is_active',
            field=models.BooleanField(default=0, verbose_name='Année active'),
        ),
        migrations.AlterField(
            model_name='activeyear',
            name='solde',
            field=models.IntegerField(default=0, verbose_name="Solde de l'exercice"),
        ),
    ]
