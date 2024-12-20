# Generated by Django 3.0.5 on 2022-08-08 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_school_tiers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('code_acad', models.CharField(default='999efe', max_length=255, verbose_name='Code UAI')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Adresse')),
                ('complement', models.CharField(blank=True, max_length=255, verbose_name="Complément d'adresse")),
                ('zip_code', models.CharField(blank=True, default='99999', max_length=255, verbose_name='Code postal')),
                ('country', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, related_name='towns', related_query_name='towns', to='school.Country', verbose_name='Pays')),
            ],
        ),
    ]
