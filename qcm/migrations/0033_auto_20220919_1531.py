# Generated by Django 3.0.5 on 2022-09-19 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0032_course_forme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastering',
            name='exercise',
            field=models.ForeignKey(blank=True, default='', editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise', to='qcm.Exercise'),
        ),
        migrations.AlterField(
            model_name='mastering',
            name='relationship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationship_mastering', to='qcm.Relationship', verbose_name='Exercice'),
        ),
        migrations.AlterField(
            model_name='mastering_done',
            name='mastering',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='mastering_done', to='qcm.Mastering', verbose_name='Exercice'),
        ),
        migrations.AlterField(
            model_name='masteringcustom',
            name='customexercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customexercise_mastering_custom', to='qcm.Customexercise', verbose_name='Exercice'),
        ),
        migrations.AlterField(
            model_name='masteringcustom',
            name='exercise',
            field=models.ForeignKey(blank=True, default='', editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise_mastering_custom', to='qcm.Exercise'),
        ),
    ]