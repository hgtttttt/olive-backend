# Generated by Django 2.2 on 2021-01-31 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='addtime',
            new_name='addTime',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='expirytime',
            new_name='expiryTime',
        ),
        migrations.RenameField(
            model_name='coursetime',
            old_name='endtime',
            new_name='endTime',
        ),
        migrations.RenameField(
            model_name='coursetime',
            old_name='starttime',
            new_name='startTime',
        ),
        migrations.RenameField(
            model_name='courseuser',
            old_name='addtime',
            new_name='addTime',
        ),
    ]
