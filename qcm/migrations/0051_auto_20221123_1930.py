# Generated by Django 3.0.5 on 2022-11-23 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0050_knowledgegroup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knowledgegroup',
            old_name='is_homogene',
            new_name='is_heterogene',
        ),
    ]