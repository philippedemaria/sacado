# Generated by Django 3.0.5 on 2023-01-08 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0058_qtype_template_ans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qtype',
            name='template_ans',
        ),
    ]