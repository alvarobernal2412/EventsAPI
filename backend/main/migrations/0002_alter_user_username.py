# Generated by Django 4.0.4 on 2022-05-01 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
