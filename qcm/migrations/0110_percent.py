# Generated by Django 3.0.5 on 2023-10-15 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_auto_20230605_2102'),
        ('qcm', '0109_remove_relationship_type_i'),
    ]

    operations = [
        migrations.CreateModel(
            name='Percent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_total', models.PositiveIntegerField(blank=True, default=30, editable=False)),
                ('nb_done', models.PositiveIntegerField(blank=True, default=1, editable=False)),
                ('parcours', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='percents', to='qcm.Parcours')),
                ('student', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='percents', to='account.Student')),
            ],
            options={
                'unique_together': {('parcours', 'student')},
            },
        ),
    ]