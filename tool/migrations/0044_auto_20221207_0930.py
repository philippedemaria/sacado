# Generated by Django 3.0.5 on 2022-12-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0043_auto_20221204_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mental',
            name='script',
            field=models.TextField(blank=True, null=True, verbose_name='script éventuel'),
        ),
    ]