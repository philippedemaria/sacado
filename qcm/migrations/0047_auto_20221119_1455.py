# Generated by Django 3.0.5 on 2022-11-19 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socle', '0008_level_is_active'),
        ('qcm', '0046_relationship_is_calculator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testcreator',
            old_name='questions_effective',
            new_name='questions',
        ),
        migrations.CreateModel(
            name='Parcourscreator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveIntegerField(blank=True, default=0, editable=False, null=True)),
                ('score', models.PositiveIntegerField(blank=True, default=0, editable=False, null=True)),
                ('exercises', models.TextField(blank=True, editable=False, null=True)),
                ('knowledge', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='parcourscreators', to='socle.Knowledge')),
            ],
        ),
    ]
