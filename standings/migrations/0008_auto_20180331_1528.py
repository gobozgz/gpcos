# Generated by Django 2.0.1 on 2018-03-31 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standings', '0007_auto_20180331_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lap',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='lap',
            name='race',
        ),
        migrations.AddField(
            model_name='lap',
            name='result',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='standings.Result'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='dnf_reason',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
