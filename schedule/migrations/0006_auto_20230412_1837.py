# Generated by Django 3.0.5 on 2023-04-12 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20230411_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slotedt',
            old_name='user',
            new_name='users',
        ),
    ]
