# Generated by Django 3.0.5 on 2023-01-06 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socle', '0009_theme_canvasimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theme',
            old_name='canvasimage',
            new_name='image',
        ),
    ]
