# Generated by Django 3.0.5 on 2021-09-04 15:13

from django.db import migrations, models
import school.models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20210718_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='logo',
            field=models.ImageField(blank=True, default='', upload_to=school.models.image_directory_path, verbose_name='Logo établissement'),
        ),
    ]
