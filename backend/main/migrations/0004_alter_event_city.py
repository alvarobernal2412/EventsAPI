# Generated by Django 4.0.4 on 2022-05-19 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_event_weather'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]