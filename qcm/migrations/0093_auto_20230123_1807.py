# Generated by Django 3.0.5 on 2023-01-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0092_auto_20230123_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writtenanswerbystudent',
            name='answer',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]