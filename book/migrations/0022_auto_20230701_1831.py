# Generated by Django 3.0.5 on 2023-07-01 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socle', '0010_auto_20230106_1002'),
        ('book', '0021_auto_20230629_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliquette',
            name='code',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='appliquette',
            name='level',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='appliquettes', to='socle.Level', verbose_name='Niveau'),
        ),
    ]