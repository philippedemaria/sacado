# Generated by Django 3.0.5 on 2022-12-15 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0050_qtype_is_sub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qtype',
            name='is_sub',
        ),
        migrations.AddField(
            model_name='qtype',
            name='extra',
            field=models.PositiveIntegerField(default=0),
        ),
    ]