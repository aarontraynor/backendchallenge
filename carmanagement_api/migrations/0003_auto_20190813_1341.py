# Generated by Django 2.2.4 on 2019-08-13 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carmanagement_api', '0002_auto_20190813_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='middle_names',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
