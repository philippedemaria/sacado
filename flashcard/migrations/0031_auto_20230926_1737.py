# Generated by Django 3.0.5 on 2023-09-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0105_auto_20230926_1737'),
        ('flashcard', '0030_auto_20230925_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashpack',
            name='folders',
            field=models.ManyToManyField(blank=True, related_name='flashpacks', to='qcm.Folder'),
        ),
        migrations.AlterField(
            model_name='flashpack',
            name='parcours',
            field=models.ManyToManyField(blank=True, related_name='flashpacks', to='qcm.Parcours'),
        ),
    ]