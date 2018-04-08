# Generated by Django 2.0.1 on 2018-03-29 20:21

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('standings', '0004_race_round_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=10)),
                ('lap_number', models.IntegerField(default=1)),
                ('position', models.IntegerField(default=1)),
                ('pitstop', models.BooleanField(default=False)),
                ('sector_1', models.FloatField(default=0)),
                ('sector_2', models.FloatField(default=0)),
                ('sector_3', models.FloatField(default=0)),
                ('lap_time', models.FloatField(default=0)),
                ('race_time', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('length', models.FloatField(default=0)),
                ('version', models.CharField(max_length=25)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='pointsystem',
            name='points',
        ),
        migrations.RemoveField(
            model_name='team',
            name='css_class',
        ),
        migrations.AddField(
            model_name='division',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='division',
            name='order',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='division',
            name='url',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='driver',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='driver',
            name='helmet',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='driver',
            name='shortname',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='pointsystem',
            name='fastest_lap',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pointsystem',
            name='lead_lap',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pointsystem',
            name='most_laps_lead',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pointsystem',
            name='qualifying_points',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='pointsystem',
            name='race_points',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='result',
            name='car',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='result',
            name='car_class',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='result',
            name='finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='result',
            name='points_multiplier',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='result',
            name='points_multiplier_description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='result',
            name='qualifying_laps',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='qualifying_penalty_bog',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='result',
            name='qualifying_penalty_description',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='result',
            name='qualifying_penalty_grid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='qualifying_penalty_sfp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='qualifying_time',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='race_laps',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='race_penalty_description',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='result',
            name='race_penalty_positions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='race_penalty_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='race_time',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='classification_type',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='season',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='season',
            name='end_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='season',
            name='finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='season',
            name='laps_classified',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='percent_classified',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='team',
            name='url',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='driver',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='result',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='standings.Driver'),
        ),
        migrations.AlterField(
            model_name='result',
            name='note',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='result',
            name='position',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='result',
            name='qualifying',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='result',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='standings.Team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='lap',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standings.Driver'),
        ),
        migrations.AddField(
            model_name='lap',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standings.Race'),
        ),
        migrations.AddField(
            model_name='race',
            name='track',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='standings.Track'),
        ),
    ]
