# Generated by Django 3.0.5 on 2022-11-25 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0032_variableq_variableqimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variableqimage',
            name='variable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variableq_img', to='tool.Variableq'),
        ),
    ]
