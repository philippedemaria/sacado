# Generated by Django 3.0.5 on 2023-08-28 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0029_auto_20230820_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloc',
            name='is_correction',
            field=models.BooleanField(default=0, editable=False),
        ),
    ]
