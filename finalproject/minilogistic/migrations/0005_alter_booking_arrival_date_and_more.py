# Generated by Django 4.1.4 on 2023-03-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minilogistic', '0004_alter_booking_arrival_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='arrival_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='departure_date',
            field=models.DateTimeField(),
        ),
    ]
