# Generated by Django 2.0 on 2018-01-01 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0004_event_reportuserinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='model',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='event',
            name='rackPostion',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
