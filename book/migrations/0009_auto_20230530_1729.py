# Generated by Django 3.0.5 on 2023-05-30 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_auto_20230529_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='ranking',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
