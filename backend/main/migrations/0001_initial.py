# Generated by Django 4.0.4 on 2022-05-01 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('date', models.DateTimeField(primary_key=True, serialize=False)),
                ('weather', models.CharField(max_length=500)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.calendar')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.day')),
            ],
        ),
        migrations.AddField(
            model_name='calendar',
            name='calendar',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.user'),
        ),
    ]
