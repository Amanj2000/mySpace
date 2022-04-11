# Generated by Django 4.0.3 on 2022-04-11 19:24

from django.db import migrations, models
import django.db.models.deletion
import mySpace_app.models
import mySpace_app.storage


class Migration(migrations.Migration):

    dependencies = [
        ('mySpace_app', '0035_adminpublish_published_on_instpublish_published_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.FileField(max_length=30, storage=mySpace_app.storage.OverwriteStorage(), upload_to=mySpace_app.models.CourseDetails.facultywise_upload_to)),
                ('inst_teaches', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mySpace_app.instteaches')),
            ],
            options={
                'unique_together': {('inst_teaches', 'details')},
            },
        ),
    ]
