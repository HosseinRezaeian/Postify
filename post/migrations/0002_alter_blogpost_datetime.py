# Generated by Django 5.0.8 on 2024-08-06 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
