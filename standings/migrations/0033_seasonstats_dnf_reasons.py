# Generated by Django 2.0.4 on 2018-07-21 08:35

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standings', '0032_seasonstats_positions'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonstats',
            name='dnf_reasons',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
