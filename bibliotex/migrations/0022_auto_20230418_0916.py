# Generated by Django 3.0.5 on 2023-04-18 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotex', '0021_auto_20230326_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='exotex',
            name='point',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Points'),
        ),
        migrations.AddField(
            model_name='relationtex',
            name='point',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Points'),
        ),
    ]