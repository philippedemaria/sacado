# Generated by Django 3.0.5 on 2023-09-04 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socle', '0013_auto_20230830_1633'),
        ('bibliotex', '0024_exotex_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exotex',
            name='knowledge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='knowledge_exotexs', to='socle.Knowledge', verbose_name='Savoir faire associé'),
        ),
    ]