# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_data', '0003_auto_20171011_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='solve_task_user',
            name='province',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]