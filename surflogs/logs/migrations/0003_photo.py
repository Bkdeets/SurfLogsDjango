# Generated by Django 2.1.5 on 2019-02-26 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_auto_20190218_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('photo_id', models.AutoField(primary_key=True, serialize=False)),
                ('referencing_id', models.IntegerField()),
                ('image', models.ImageField(default='media/None/no-img.jpg', upload_to='media/')),
            ],
        ),
    ]