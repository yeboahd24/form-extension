# Generated by Django 4.1.7 on 2023-04-25 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0019_alter_doctorappointment_appointment_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorappointment',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctorappointment',
            name='appointment_end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='doctorappointment',
            name='appointment_start_time',
            field=models.TimeField(),
        ),
    ]