# Generated by Django 3.0.5 on 2022-12-13 21:31

from django.db import migrations, models
import qcm.models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0057_customvariable_is_notnull'),
    ]

    operations = [
        migrations.AddField(
            model_name='customexercise',
            name='figure',
            field=models.ImageField(blank=True, default='', upload_to=qcm.models.vignette_directory_path, verbose_name='Figure'),
        ),
    ]
