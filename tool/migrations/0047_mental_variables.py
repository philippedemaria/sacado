# Generated by Django 3.0.5 on 2022-12-10 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0046_auto_20221208_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='mental',
            name='variables',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Variables'),
        ),
    ]
