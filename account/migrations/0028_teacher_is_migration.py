# Generated by Django 3.0.5 on 2022-09-09 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_auto_20220902_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='is_migration',
            field=models.BooleanField(default=0, editable=False),
        ),
    ]
