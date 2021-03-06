# Generated by Django 2.1.5 on 2019-03-18 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0011_report_wave_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSummary',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('photo', models.FileField(default='profile-photos/None/no-img.jpg', upload_to='surflogs-photos')),
                ('homespot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logs.Spot')),
            ],
        ),
    ]
