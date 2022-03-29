# Generated by Django 4.0.3 on 2022-03-29 06:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySpace_app', '0002_certreq_course_dept_notice_section_tag_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studtakes',
            options={'verbose_name_plural': 'Students Takes'},
        ),
        migrations.AlterField(
            model_name='adminpublish',
            name='published_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 11, 53, 34, 266991)),
        ),
        migrations.AlterField(
            model_name='adminreview',
            name='review_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 11, 53, 34, 266330)),
        ),
        migrations.AlterField(
            model_name='instpublish',
            name='published_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 11, 53, 34, 267391)),
        ),
        migrations.AlterField(
            model_name='instreq',
            name='req_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 11, 53, 34, 265183)),
        ),
        migrations.AlterField(
            model_name='studreq',
            name='req_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 11, 53, 34, 265995)),
        ),
    ]
