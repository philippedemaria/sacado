# Generated by Django 3.0.5 on 2022-11-14 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0045_auto_20221114_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='relationship',
            name='is_calculator',
            field=models.BooleanField(default=0, editable=False),
        ),
    ]
