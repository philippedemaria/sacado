# Generated by Django 3.0.5 on 2022-08-08 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_town'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='town',
            name='address',
        ),
        migrations.RemoveField(
            model_name='town',
            name='code_acad',
        ),
        migrations.RemoveField(
            model_name='town',
            name='complement',
        ),
    ]