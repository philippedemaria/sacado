# Generated by Django 3.0.5 on 2023-10-18 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0112_percent_today'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcours',
            name='is_display_relation',
            field=models.BooleanField(blank=True, default=1, editable=False),
        ),
    ]
