# Generated by Django 4.0.3 on 2022-04-10 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySpace_app', '0034_alter_certreq_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminpublish',
            name='published_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='instpublish',
            name='published_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
