# Generated by Django 2.0 on 2017-12-15 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20171207_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='IDCPostion',
        ),
        migrations.RemoveField(
            model_name='device',
            name='userAdmins',
        ),
        migrations.RemoveField(
            model_name='event',
            name='Device',
        ),
        migrations.DeleteModel(
            name='Device',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='IDCPostion',
        ),
        migrations.DeleteModel(
            name='userAdmin',
        ),
    ]