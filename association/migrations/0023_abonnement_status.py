# Generated by Django 3.0.5 on 2023-05-24 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0022_auto_20221019_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='abonnement',
            name='status',
            field=models.CharField(blank=True, choices=[(0, "Période d'essai"), (1, 'Abonnement')], default='', editable=False, max_length=255),
        ),
    ]