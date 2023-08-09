#!/usr/bin/env python
#-*-encoding:utf-8-*-



import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from UIAutotest.common.mydb import MyDB
from UIAutotest.test_report import TestReport

test_platform_db = MyDB('TESTPLATFORM')

db_related_to_project_dic = {}  # 存放与项目关联的数据库对象

test_reporter = TestReport(test_platform_db)

global_variable_dic = {}     # 存放与项目关联的全局变量

