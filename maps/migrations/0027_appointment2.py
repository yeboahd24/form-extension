# Generated by Django 4.1.7 on 2023-05-01 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0026_alter_nps_nps'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('description', models.TextField()),
            ],
        ),
    ]
