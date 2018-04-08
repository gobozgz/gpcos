# Generated by Django 2.0.1 on 2018-04-03 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standings', '0011_auto_20180402_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='SortCriteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_finish', models.IntegerField(default=0)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standings.Driver')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standings.Season')),
            ],
        ),
        migrations.AlterModelOptions(
            name='division',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='league',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='race',
            options={'ordering': ['round_number']},
        ),
    ]
