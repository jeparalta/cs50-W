# Generated by Django 4.1.4 on 2023-04-17 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minilogistic', '0005_alter_comment_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='number_pax',
            field=models.IntegerField(default=1),
        ),
    ]