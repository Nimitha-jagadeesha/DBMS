# Generated by Django 3.1.4 on 2020-12-24 13:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForestManagement', '0005_auto_20201224_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='last_created_date',
            field=models.DateField(default=datetime.date(2020, 12, 24), null=True),
        ),
    ]
