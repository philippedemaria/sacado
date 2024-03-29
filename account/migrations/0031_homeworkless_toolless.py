# Generated by Django 3.0.5 on 2023-06-05 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_connexion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Toolless',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, editable=False, null=True)),
                ('student', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toolless', to='account.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Homeworkless',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, editable=False, null=True)),
                ('student', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='homeworkless', to='account.Student')),
            ],
        ),
    ]
