# Generated by Django 3.0.5 on 2023-05-26 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0030_auto_20230526_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gestion',
            field=models.CharField(blank=True, choices=[('En direct', 'Directe'), ('eMLS', 'eMLS')], default='En direct', max_length=255),
        ),
    ]