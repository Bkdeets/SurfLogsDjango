# Generated by Django 2.1.5 on 2019-03-16 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0009_auto_20190316_2052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='wave_data_id',
            new_name='wave_data',
        ),
    ]