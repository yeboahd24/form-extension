# Generated by Django 4.1.7 on 2023-04-29 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0024_feedback_nps'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nps', models.FloatField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='nps',
        ),
    ]
