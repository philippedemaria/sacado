# Generated by Django 3.0.5 on 2023-09-28 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0010_auto_20230821_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='ranking',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False, null=True),
        ),
    ]