# Generated by Django 3.0.5 on 2023-01-21 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0088_remove_supportfile_canvasimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportfile',
            name='is_written',
        ),
        migrations.RemoveField(
            model_name='supportfile',
            name='precision',
        ),
        migrations.RemoveField(
            model_name='supportfile',
            name='subtick',
        ),
        migrations.RemoveField(
            model_name='supportfile',
            name='tick',
        ),
        migrations.RemoveField(
            model_name='supportfile',
            name='xmax',
        ),
        migrations.RemoveField(
            model_name='supportfile',
            name='xmin',
        ),
        migrations.AddField(
            model_name='supportchoice',
            name='is_written',
            field=models.BooleanField(default=0, verbose_name='Mots à écrire ?'),
        ),
        migrations.AddField(
            model_name='supportchoice',
            name='precision',
            field=models.FloatField(blank=True, null=True, verbose_name='Précision'),
        ),
        migrations.AddField(
            model_name='supportchoice',
            name='subtick',
            field=models.FloatField(blank=True, null=True, verbose_name='Graduation'),
        ),
        migrations.AddField(
            model_name='supportchoice',
            name='tick',
            field=models.FloatField(blank=True, null=True, verbose_name='Graduation principale'),
        ),
        migrations.AddField(
            model_name='supportchoice',
            name='xmax',
            field=models.FloatField(blank=True, null=True, verbose_name='x max '),
        ),
        migrations.AddField(
            model_name='supportchoice',
            name='xmin',
            field=models.FloatField(blank=True, null=True, verbose_name='x min '),
        ),
    ]
