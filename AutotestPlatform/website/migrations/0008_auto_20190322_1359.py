# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-22 05:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_api_test_case_step_retry_frequency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Env_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('env', models.CharField(max_length=50)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='global_variable_setting',
            name='remark',
            field=models.CharField(default='', max_length=3000),
            preserve_default=False,
        ),
    ]
