# Generated by Django 3.0.5 on 2023-05-24 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0023_abonnement_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'En suspens'), (2, 'Paiement en attente'), (3, 'Abonné')], default=3),
        ),
    ]