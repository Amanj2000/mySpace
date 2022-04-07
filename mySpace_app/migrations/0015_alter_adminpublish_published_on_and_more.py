# Generated by Django 4.0.3 on 2022-04-07 08:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySpace_app', '0014_alter_adminpublish_published_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminpublish',
            name='published_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 13, 43, 2, 965725)),
        ),
        migrations.AlterField(
            model_name='adminreview',
            name='review_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 13, 43, 2, 964725)),
        ),
        migrations.AlterField(
            model_name='instpublish',
            name='published_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 13, 43, 2, 965725)),
        ),
        migrations.AlterField(
            model_name='instreq',
            name='req_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 13, 43, 2, 964725)),
        ),
        migrations.AlterField(
            model_name='result',
            name='result',
            field=models.FileField(upload_to='media/<django.db.models.fields.PositiveSmallIntegerField>/'),
        ),
        migrations.AlterField(
            model_name='studreq',
            name='req_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 13, 43, 2, 964725)),
        ),
    ]
