# Generated by Django 4.0.4 on 2022-05-23 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_event_done'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='done',
            new_name='completed',
        ),
    ]
