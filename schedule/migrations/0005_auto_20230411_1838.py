# Generated by Django 3.0.5 on 2023-04-11 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20230410_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slotedt',
            name='stop',
        ),
        migrations.AddField(
            model_name='slotedt',
            name='slot',
            field=models.PositiveIntegerField(default=1, editable=False),
        ),
        migrations.AlterField(
            model_name='edt',
            name='first_day',
            field=models.CharField(choices=[('0', 'Lundi'), ('1', 'Mardi'), ('2', 'Mercredi'), ('3', 'Jeudi'), ('4', 'Vendredi'), ('5', 'Samedi'), ('6', 'Dimanche')], default='0', max_length=250),
        ),
    ]