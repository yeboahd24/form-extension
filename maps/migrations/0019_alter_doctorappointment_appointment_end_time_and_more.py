# Generated by Django 4.1.7 on 2023-04-24 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0018_alter_doctorappointment_appointment_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorappointment',
            name='appointment_end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='doctorappointment',
            name='appointment_start_time',
            field=models.DateTimeField(),
        ),
    ]
