# Generated by Django 2.1.5 on 2019-03-16 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0010_auto_20190316_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='wave_data',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='logs.Wave_Data'),
            preserve_default=False,
        ),
    ]