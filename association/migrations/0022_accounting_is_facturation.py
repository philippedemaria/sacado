# Generated by Django 3.0.5 on 2022-08-06 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0021_remove_accounting_is_cpca'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounting',
            name='is_facturation',
            field=models.BooleanField(default=0, verbose_name="Affiche la facture sur l'interface client ?"),
        ),
    ]