# Generated by Django 3.0.5 on 2022-12-14 21:59

from django.db import migrations, models
import qcm.models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0059_auto_20221213_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='customexercise',
            name='canvasimage',
            field=models.ImageField(blank=True, default='', null=True, upload_to=qcm.models.vignette_directory_path, verbose_name='Image support'),
        ),
    ]
