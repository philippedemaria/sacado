# Generated by Django 3.0.5 on 2023-01-17 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0060_quizz_mentaltitle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizz',
            old_name='mentaltitle',
            new_name='mentaltitles',
        ),
    ]