# Generated by Django 4.1.4 on 2023-03-25 23:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minilogistic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='minilogistic.location'),
        ),
        migrations.CreateModel(
            name='Clean',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('duration', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('date_created', models.DateTimeField(default=datetime.datetime.today)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cleans', to='minilogistic.booking')),
                ('cleaners', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cleans', to='minilogistic.cleaner')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cleans', to='minilogistic.location')),
            ],
        ),
    ]