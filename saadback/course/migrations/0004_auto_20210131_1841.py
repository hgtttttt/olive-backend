# Generated by Django 2.2 on 2021-01-31 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20210131_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetime',
            name='endTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='coursetime',
            name='startTime',
            field=models.DateTimeField(),
        ),
    ]
