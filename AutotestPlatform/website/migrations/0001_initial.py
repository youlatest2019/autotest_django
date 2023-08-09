# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-02-20 07:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='API_case_tree',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=10)),
                ('parent_id', models.IntegerField()),
                ('iconCls', models.CharField(max_length=20)),
                ('attributes', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='API_case_tree_test_plan',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('plan_id', models.IntegerField()),
                ('node_name', models.CharField(max_length=50)),
                ('node_path', models.CharField(max_length=5000)),
                ('sub_node_num', models.IntegerField()),
                ('order', models.IntegerField(default=0)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.API_case_tree')),
            ],
        ),
        migrations.CreateModel(
            name='API_project_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=50)),
                ('protocol', models.CharField(max_length=10)),
                ('host', models.CharField(max_length=30)),
                ('port', models.IntegerField()),
                ('environment', models.CharField(max_length=20)),
                ('valid_flag', models.CharField(max_length=5)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='API_test_case_step',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('step_type', models.CharField(max_length=10)),
                ('op_object', models.CharField(max_length=5000)),
                ('object_id', models.BigIntegerField()),
                ('exec_operation', models.CharField(max_length=50)),
                ('request_header', models.CharField(max_length=2000)),
                ('request_method', models.CharField(max_length=10)),
                ('url_or_sql', models.CharField(max_length=2000)),
                ('input_params', models.CharField(max_length=3000)),
                ('response_to_check', models.CharField(max_length=10)),
                ('check_rule', models.CharField(max_length=20)),
                ('check_pattern', models.CharField(max_length=3000)),
                ('output_params', models.TextField(max_length=6000)),
                ('protocol', models.CharField(max_length=10)),
                ('host', models.CharField(max_length=30)),
                ('port', models.CharField(max_length=6)),
                ('status', models.CharField(max_length=5)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.API_case_tree')),
            ],
        ),
        migrations.CreateModel(
            name='API_test_plan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=100)),
                ('plan_name', models.CharField(max_length=50)),
                ('plan_desc', models.CharField(max_length=200)),
                ('valid_flag', models.CharField(max_length=5)),
                ('order', models.IntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.API_project_setting')),
            ],
        ),
        migrations.CreateModel(
            name='API_test_report_for_case',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('execution_num', models.CharField(max_length=30)),
                ('plan_id', models.IntegerField()),
                ('case_id', models.IntegerField()),
                ('case_path', models.CharField(max_length=1000)),
                ('case_name', models.CharField(max_length=100)),
                ('run_result', models.CharField(max_length=10)),
                ('run_time', models.CharField(max_length=30)),
                ('remark', models.CharField(max_length=3000)),
                ('time_took', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='API_test_report_for_case_step',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('execution_num', models.CharField(max_length=30)),
                ('plan_id', models.IntegerField()),
                ('case_id', models.IntegerField()),
                ('step_id', models.IntegerField()),
                ('order', models.IntegerField()),
                ('step_type', models.CharField(max_length=10)),
                ('op_object', models.CharField(max_length=5000)),
                ('object_id', models.BigIntegerField()),
                ('exec_operation', models.CharField(max_length=50)),
                ('protocol', models.CharField(max_length=10)),
                ('host', models.CharField(max_length=30)),
                ('port', models.CharField(max_length=6)),
                ('request_header', models.CharField(max_length=2000)),
                ('request_method', models.CharField(max_length=10)),
                ('url_or_sql', models.CharField(max_length=2000)),
                ('input_params', models.CharField(max_length=3000)),
                ('response_to_check', models.CharField(max_length=10)),
                ('check_rule', models.CharField(max_length=20)),
                ('check_pattern', models.CharField(max_length=3000)),
                ('output_params', models.TextField(max_length=7000)),
                ('run_result', models.CharField(max_length=10)),
                ('remark', models.CharField(max_length=3000)),
                ('run_time', models.CharField(max_length=30)),
                ('run_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='API_test_report_for_summary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('execution_num', models.CharField(max_length=30)),
                ('project_id', models.IntegerField()),
                ('plan_id', models.IntegerField()),
                ('project_name', models.CharField(max_length=100)),
                ('plan_name', models.CharField(max_length=50)),
                ('start_time', models.CharField(max_length=30)),
                ('end_time', models.CharField(max_length=30)),
                ('time_took', models.CharField(max_length=20)),
                ('case_total_num', models.IntegerField()),
                ('case_pass_num', models.IntegerField()),
                ('case_fail_num', models.IntegerField()),
                ('case_block_num', models.IntegerField()),
                ('remark', models.CharField(max_length=3000)),
            ],
        ),
        migrations.CreateModel(
            name='Assertion_type_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('op_type', models.CharField(max_length=10)),
                ('assertion_type', models.CharField(max_length=50)),
                ('assertion_pattern', models.CharField(max_length=2000)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Browser_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('browser', models.CharField(max_length=20)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Database_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('db_type', models.CharField(max_length=10)),
                ('db_alias', models.CharField(max_length=20)),
                ('db_name', models.CharField(max_length=20)),
                ('db_host', models.CharField(max_length=20)),
                ('db_port', models.IntegerField()),
                ('db_user', models.CharField(max_length=20)),
                ('db_passwd', models.CharField(max_length=20)),
                ('environment', models.CharField(max_length=20)),
                ('project_type', models.CharField(max_length=10)),
                ('project_name', models.CharField(max_length=50)),
                ('project_id', models.IntegerField()),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Function_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('function_name', models.CharField(max_length=20)),
                ('param_style', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Global_variable_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=3000)),
                ('environment', models.CharField(max_length=20)),
                ('project_type', models.CharField(max_length=10)),
                ('project_name', models.CharField(max_length=50)),
                ('project_id', models.IntegerField()),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Navigation',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('menu_name', models.CharField(max_length=20)),
                ('parent_id', models.IntegerField()),
                ('url', models.CharField(max_length=500)),
                ('icon', models.CharField(max_length=15)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Operation_for_object',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('object_type', models.CharField(max_length=10)),
                ('operation', models.CharField(max_length=50)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Page_element',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('element_name', models.CharField(max_length=100)),
                ('selector1', models.CharField(max_length=150)),
                ('selector2', models.CharField(max_length=150)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Page_tree',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=10)),
                ('parent_id', models.IntegerField()),
                ('iconCls', models.CharField(max_length=20)),
                ('attributes', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Project_chosen',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_id', models.IntegerField()),
                ('project_name', models.CharField(max_length=50)),
                ('tree_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Promble_feedback',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=300)),
                ('status', models.CharField(max_length=10)),
                ('issuer', models.CharField(max_length=10)),
                ('tracer', models.CharField(max_length=10)),
                ('handler', models.CharField(max_length=10)),
                ('record_time', models.CharField(max_length=20)),
                ('start_trace_time', models.CharField(max_length=20)),
                ('solved_time', models.CharField(max_length=20)),
                ('mark', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Running_plan',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('running_plan_num', models.BigIntegerField()),
                ('running_plan_name', models.CharField(max_length=50)),
                ('project_type', models.CharField(max_length=10)),
                ('project_id', models.IntegerField()),
                ('project_name', models.CharField(max_length=50)),
                ('plan_name', models.CharField(max_length=50)),
                ('plan_id', models.CharField(max_length=500)),
                ('script_dirpath', models.CharField(max_length=200)),
                ('python_path', models.CharField(max_length=200)),
                ('valid_flag', models.CharField(max_length=5)),
                ('running_status', models.CharField(max_length=10)),
                ('remark', models.CharField(max_length=1000)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sprint_tree',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=10)),
                ('parent_id', models.IntegerField()),
                ('iconCls', models.CharField(max_length=20)),
                ('attributes', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Test_project_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=50)),
                ('valid_flag', models.CharField(max_length=5)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Test_task_detail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('module', models.CharField(max_length=100)),
                ('requirement', models.CharField(max_length=100)),
                ('person_in_charge', models.CharField(max_length=20)),
                ('sub_task', models.CharField(max_length=100)),
                ('progress', models.CharField(max_length=10)),
                ('time_took', models.CharField(max_length=10)),
                ('deadline', models.CharField(max_length=20)),
                ('finish_time', models.CharField(max_length=20)),
                ('if_delay', models.CharField(max_length=4)),
                ('history_progress', models.CharField(max_length=400)),
                ('remark', models.CharField(max_length=200)),
                ('order', models.IntegerField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.Sprint_tree')),
            ],
        ),
        migrations.CreateModel(
            name='Test_task_overview',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('module', models.CharField(max_length=100)),
                ('progress', models.CharField(max_length=10)),
                ('requirement', models.CharField(max_length=100)),
                ('sub_task', models.CharField(max_length=100)),
                ('time_for_test', models.CharField(max_length=20)),
                ('real_time_for_test', models.CharField(max_length=20)),
                ('if_delay', models.CharField(max_length=2)),
                ('developer_in_charge', models.CharField(max_length=50)),
                ('tester_in_charge', models.CharField(max_length=20)),
                ('pm_in_charge', models.CharField(max_length=10)),
                ('mark', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.Sprint_tree')),
            ],
        ),
        migrations.CreateModel(
            name='UI_case_tree',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=10)),
                ('parent_id', models.IntegerField()),
                ('iconCls', models.CharField(max_length=20)),
                ('attributes', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UI_case_tree_test_plan',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('plan_id', models.IntegerField()),
                ('node_name', models.CharField(max_length=50)),
                ('node_path', models.CharField(max_length=1000)),
                ('sub_node_num', models.IntegerField()),
                ('order', models.IntegerField(default=0)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.UI_case_tree')),
            ],
        ),
        migrations.CreateModel(
            name='UI_project_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=50)),
                ('home_page', models.CharField(max_length=500)),
                ('environment', models.CharField(max_length=20)),
                ('valid_flag', models.CharField(max_length=5)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UI_test_case_step',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('object_type', models.CharField(max_length=10)),
                ('page_name', models.CharField(max_length=1000)),
                ('object', models.CharField(max_length=50)),
                ('exec_operation', models.CharField(max_length=50)),
                ('input_params', models.CharField(max_length=500)),
                ('output_params', models.CharField(max_length=100)),
                ('assert_type', models.CharField(max_length=20)),
                ('assert_pattern', models.CharField(max_length=1000)),
                ('run_times', models.IntegerField()),
                ('try_for_failure', models.IntegerField()),
                ('status', models.CharField(max_length=5)),
                ('object_id', models.IntegerField()),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.UI_case_tree')),
            ],
        ),
        migrations.CreateModel(
            name='UI_test_plan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=100)),
                ('plan_name', models.CharField(max_length=50)),
                ('plan_desc', models.CharField(max_length=200)),
                ('browsers', models.CharField(max_length=20)),
                ('valid_flag', models.CharField(max_length=5)),
                ('order', models.IntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.UI_project_setting')),
            ],
        ),
        migrations.CreateModel(
            name='UI_test_report_for_case',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('execution_num', models.CharField(max_length=30)),
                ('plan_id', models.IntegerField()),
                ('case_id', models.IntegerField()),
                ('case_path', models.CharField(max_length=1000)),
                ('case_name', models.CharField(max_length=100)),
                ('run_result', models.CharField(max_length=10)),
                ('run_time', models.CharField(max_length=30)),
                ('remark', models.CharField(max_length=3000)),
                ('time_took', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UI_test_report_for_case_step',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('execution_num', models.CharField(max_length=30)),
                ('plan_id', models.IntegerField()),
                ('case_id', models.IntegerField()),
                ('step_id', models.IntegerField()),
                ('order', models.IntegerField()),
                ('page', models.CharField(max_length=1000)),
                ('object', models.CharField(max_length=200)),
                ('exec_operation', models.CharField(max_length=10)),
                ('input_params', models.CharField(max_length=500)),
                ('output_params', models.CharField(max_length=500)),
                ('assert_type', models.CharField(max_length=100)),
                ('check_pattern', models.CharField(max_length=500)),
                ('run_times', models.IntegerField()),
                ('try_for_failure', models.IntegerField()),
                ('run_result', models.CharField(max_length=10)),
                ('remark', models.CharField(max_length=500)),
                ('run_time', models.CharField(max_length=30)),
                ('run_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UI_test_report_for_summary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('execution_num', models.CharField(max_length=30)),
                ('project_id', models.IntegerField()),
                ('plan_id', models.IntegerField()),
                ('project_name', models.CharField(max_length=100)),
                ('plan_name', models.CharField(max_length=50)),
                ('browser', models.CharField(max_length=20)),
                ('start_time', models.CharField(max_length=30)),
                ('end_time', models.CharField(max_length=30)),
                ('time_took', models.CharField(max_length=20)),
                ('case_total_num', models.IntegerField()),
                ('case_pass_num', models.IntegerField()),
                ('case_fail_num', models.IntegerField()),
                ('case_block_num', models.IntegerField()),
                ('remark', models.CharField(max_length=3000)),
            ],
        ),
        migrations.AddField(
            model_name='ui_case_tree',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.UI_project_setting'),
        ),
        migrations.AddField(
            model_name='sprint_tree',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Test_project_setting'),
        ),
        migrations.AddField(
            model_name='page_tree',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.UI_project_setting'),
        ),
        migrations.AddField(
            model_name='page_element',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.Page_tree'),
        ),
        migrations.AddField(
            model_name='api_case_tree',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.API_project_setting'),
        ),
    ]