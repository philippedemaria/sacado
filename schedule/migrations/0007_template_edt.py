# Generated by Django 3.0.5 on 2023-04-12 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0008_auto_20230202_1527'),
        ('schedule', '0006_auto_20230412_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template_Edt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField(verbose_name='start')),
                ('groups', models.ManyToManyField(blank=True, editable=False, related_name='template_edts', to='group.Group')),
                ('slot', models.ManyToManyField(blank=True, editable=False, related_name='template_edts', to='schedule.Slotedt')),
                ('user', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='template_edts', to='schedule.Edt')),
            ],
        ),
    ]
