# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-21 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20190319_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_test_case_step',
            name='retry_frequency',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
