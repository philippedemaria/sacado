# Generated by Django 3.0.5 on 2023-02-02 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotex', '0017_auto_20220220_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='exotex',
            name='is_annals',
            field=models.BooleanField(default=0, verbose_name='Annale ?'),
        ),
    ]
