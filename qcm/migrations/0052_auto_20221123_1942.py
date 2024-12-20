# Generated by Django 3.0.5 on 2022-11-23 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0051_auto_20221123_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledgegroup',
            name='knowledges',
        ),
        migrations.AddField(
            model_name='knowledgegroup',
            name='knowledges',
            field=models.TextField(blank=True, default='', editable=False),
        ),
        migrations.RemoveField(
            model_name='knowledgegroup',
            name='parcours',
        ),
        migrations.AddField(
            model_name='knowledgegroup',
            name='parcours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='knowledge_groups', to='qcm.Parcours'),
        ),
        migrations.RemoveField(
            model_name='knowledgegroup',
            name='students',
        ),
        migrations.AddField(
            model_name='knowledgegroup',
            name='students',
            field=models.TextField(blank=True, default='', editable=False),
        ),
    ]
