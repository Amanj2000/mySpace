# Generated by Django 4.0.3 on 2022-04-10 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySpace_app', '0029_fines'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fines',
            options={'verbose_name_plural': 'Fines'},
        ),
        migrations.AlterField(
            model_name='fines',
            name='fine',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='messfee',
            name='mess_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='semfee',
            name='hostel_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='semfee',
            name='tuition_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
