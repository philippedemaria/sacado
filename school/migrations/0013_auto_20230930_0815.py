# Generated by Django 3.0.5 on 2023-09-30 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_auto_20221018_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='nbstudents',
            field=models.PositiveIntegerField(choices=[(150, 'moins de 150 - Version gratuite'), (500, 'Entre 150 et 500 : 100 €'), (1000, 'Entre 500 et 1000 : 200 € ()'), (1500, 'Entre 1000 et 1500 : 300 €'), (2000, 'Entre 1500 et 2000 : 400 €'), (2500, 'Entre 2000 et 2500 : 500 €'), (3000, 'Entre 2500 et 3000 : 600 €'), (3500, 'Entre 3000 et 3500 : 700 €'), (4000, 'Entre 3500 et 4000 : 800 €'), (4500, 'Entre 4000 et 4500 : 900 €'), (10000, '+ de 4500 : 1000 €')], default=150, verbose_name="Nombre d'élèves"),
        ),
    ]
