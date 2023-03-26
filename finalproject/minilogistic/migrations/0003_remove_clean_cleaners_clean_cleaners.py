# Generated by Django 4.1.4 on 2023-03-25 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minilogistic', '0002_alter_booking_location_clean'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clean',
            name='cleaners',
        ),
        migrations.AddField(
            model_name='clean',
            name='cleaners',
            field=models.ManyToManyField(related_name='cleans', to='minilogistic.cleaner'),
        ),
    ]
