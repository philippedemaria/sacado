# Generated by Django 3.0.5 on 2023-04-27 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_edt_is_share'),
    ]

    operations = [
        migrations.AddField(
            model_name='template_edt',
            name='is_even',
            field=models.BooleanField(default=0),
        ),
    ]
