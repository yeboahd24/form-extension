# Generated by Django 4.1.7 on 2023-04-01 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]