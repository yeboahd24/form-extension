# Generated by Django 4.1.7 on 2023-05-02 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0027_appointment2'),
    ]

    operations = [
        migrations.AddField(
            model_name='nps',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]