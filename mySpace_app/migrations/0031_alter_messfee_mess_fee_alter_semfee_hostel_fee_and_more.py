# Generated by Django 4.0.3 on 2022-04-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySpace_app', '0030_alter_fines_options_alter_fines_fine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messfee',
            name='mess_fee',
            field=models.IntegerField(default=4000),
        ),
        migrations.AlterField(
            model_name='semfee',
            name='hostel_fee',
            field=models.IntegerField(default=12500),
        ),
        migrations.AlterField(
            model_name='semfee',
            name='tuition_fee',
            field=models.IntegerField(default=125000),
        ),
    ]