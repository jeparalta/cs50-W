# Generated by Django 4.1.4 on 2023-02-01 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bid_active_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(max_length=200),
        ),
    ]