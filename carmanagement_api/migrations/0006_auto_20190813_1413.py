# Generated by Django 2.2.4 on 2019-08-13 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carmanagement_api', '0005_auto_20190813_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='at_branch',
        ),
        migrations.RemoveField(
            model_name='car',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='car',
            name='driver',
        ),
    ]
