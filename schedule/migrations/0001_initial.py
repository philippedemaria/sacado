# Generated by Django 3.0.5 on 2020-06-01 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='name')),
                ('color', models.CharField(default='', max_length=50, verbose_name='color')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'calendar',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('start', models.DateTimeField(verbose_name='start')),
                ('end', models.DateTimeField(verbose_name='end')),
                ('is_allday', models.BooleanField(blank=True, default=False, verbose_name='is_allday?')),
                ('notification', models.BooleanField(blank=True, default=False, verbose_name='Notification?')),
                ('notification_day', models.PositiveIntegerField(blank=True, default=False)),
                ('place', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Place')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Commentaire')),
                ('display', models.BooleanField(default=0, verbose_name='Publication')),
                ('color', models.CharField(default='#00819F', max_length=50, verbose_name='color')),
                ('type_of_event', models.PositiveIntegerField(default=0, editable=False)),
                ('link', models.PositiveIntegerField(default=0, editable=False)),
                ('calendar', models.ManyToManyField(blank=True, to='schedule.Calendar', verbose_name='Calendrier')),
                ('users', models.ManyToManyField(blank=True, default='', related_name='event_with', related_query_name='event_with', to=settings.AUTH_USER_MODEL, verbose_name='Partagée avec')),
            ],
            options={
                'verbose_name': 'event',
                'ordering': ['start', 'end'],
            },
        ),
        migrations.CreateModel(
            name='Automatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(blank=True, editable=False, max_length=255)),
                ('insert', models.BooleanField(blank=True, default=1, editable=False)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_automatic', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]