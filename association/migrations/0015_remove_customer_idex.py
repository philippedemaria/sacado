# Generated by Django 3.0.5 on 2022-08-09 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0014_customer_idex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='idex',
        ),
    ]