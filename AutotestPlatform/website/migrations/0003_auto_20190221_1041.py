# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-02-21 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20190220_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_test_case_step',
            name='run_times',
            field=models.IntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='api_test_case_step',
            name='try_for_failure',
            field=models.IntegerField(default='1'),
            preserve_default=False,
        ),
    ]
