# Generated by Django 3.0.5 on 2023-08-01 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0022_auto_20230701_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='ranking',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]