# Generated by Django 3.0.5 on 2023-10-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_auto_20230605_2102'),
        ('qcm', '0106_relationship_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relationship',
            name='done',
        ),
        migrations.AddField(
            model_name='relationship',
            name='students_done',
            field=models.ManyToManyField(blank=True, editable=False, related_name='students_done_relationship', to='account.Student'),
        ),
    ]