# Generated by Django 4.2.6 on 2023-11-02 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
