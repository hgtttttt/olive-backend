# Generated by Django 2.2 on 2020-12-15 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_auto_20201205_2206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('-created',)},
        ),
    ]