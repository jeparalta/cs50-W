# Generated by Django 4.1.4 on 2023-04-24 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minilogistic', '0008_alter_clean_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='comment',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='cleaner',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='cleaner',
            name='title',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]