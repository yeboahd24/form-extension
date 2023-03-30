# Generated by Django 4.1.7 on 2023-03-30 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_image2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=50)),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
    ]
