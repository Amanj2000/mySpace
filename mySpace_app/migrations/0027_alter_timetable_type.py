# Generated by Django 4.0.3 on 2022-04-07 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySpace_app', '0026_timetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='type',
            field=models.CharField(choices=[('Class', 'Class TimeTable'), ('Exam', 'Exam TimeTable')], default='Class', max_length=5),
        ),
    ]
