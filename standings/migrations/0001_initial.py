# Generated by Django 2.0.1 on 2018-03-11 02:53

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PointSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('points', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=3, null=True)),
                ('start_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualifying', models.IntegerField(default=0, null=True)),
                ('position', models.IntegerField(default=0, null=True)),
                ('fastest_lap', models.BooleanField(default=False)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standings.Division')),
                ('point_system', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='standings.PointSystem')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('css_class', models.CharField(max_length=50, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='allocate_points',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='points_allocation', to='standings.Team'),
        ),
        migrations.AddField(
            model_name='result',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='standings.Driver'),
        ),
        migrations.AddField(
            model_name='result',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standings.Race'),
        ),
        migrations.AddField(
            model_name='result',
            name='subbed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='substitute', to='standings.Driver'),
        ),
        migrations.AddField(
            model_name='result',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='standings.Team'),
        ),
        migrations.AddField(
            model_name='race',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standings.Season'),
        ),
        migrations.AddField(
            model_name='division',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standings.League'),
        ),
    ]
