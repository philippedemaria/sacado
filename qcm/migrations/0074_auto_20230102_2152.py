# Generated by Django 3.0.5 on 2023-01-02 20:52

from django.db import migrations, models
import qcm.models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0073_auto_20221227_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportfile',
            name='imagefile',
            field=models.ImageField(blank=True, default='qtype_img/underlayer.png', upload_to=qcm.models.image_directory_path, verbose_name="Vignette d'accueil"),
        ),
    ]