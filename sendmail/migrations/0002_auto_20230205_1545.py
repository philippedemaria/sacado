# Generated by Django 3.0.5 on 2023-02-05 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendmail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='texte',
            field=models.TextField(verbose_name='Texte'),
        ),
    ]