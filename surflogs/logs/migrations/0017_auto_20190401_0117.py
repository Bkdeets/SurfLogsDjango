# Generated by Django 2.1.5 on 2019-04-01 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0016_auto_20190331_2057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spot',
            old_name='ideal_wind',
            new_name='ideal_wind_dir',
        ),
        migrations.AlterField(
            model_name='wave_data',
            name='tide',
            field=models.CharField(max_length=200),
        ),
    ]