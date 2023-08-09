#!/usr/bin/env python
#-*- encoding:utf-8 -*-



import time
import re
import unittest
import json
from collections import OrderedDict

from .common.log import logger

from .common.globalvar import global_variable_dic, global_plugin_func_name_list
from .httpprotocol import MyHttp

from .interface.APIUnittestTestCase import *
from .database.DBUnittestTestCase import *
from .function.FuncUnittestTestCase import *
from .myredis.RedisUnittestTestCase import *
from .function.plugin import pluginfunc


class TestCaseStep:
    def __init__(self, execution_num, plan_id, case_id, step_id, order, step_type, op_object, object_id, exec_operation, request_headers,
                    request_method, url_or_sql, input_params, response_to_check, check_rule, check_pattern,  output_params, protocol, host, port, global_headers, log_websocket_consumer):
        self.execution_num = execution_num
        self.plan_id = plan_id
        self.case_id = case_id
        self.step_id = step_id
        self.order = order
        self.step_type = step_type
        self.op_object = op_object
        self.object_id = object_id
        self.exec_operation = exec_operation.lower()
        self.exec_operation2 = exec_operation.lower()
        self.request_headers = request_headers
        self.request_headers2 = request_headers
        self.request_method = request_method
        self.url_or_sql = url_or_sql
        self.url_or_sql2 = url_or_sql
        self.input_params = input_params
        self.input_params2 = input_params
        self.response_to_check = response_to_check
        self.check_rule = check_rule.strip()
        self.check_pattern = check_pattern
        self.check_pattern2 = check_pattern
        self.output_params = output_params
        self.output_params2 = self.output_params
        self.protocol = protocol
        self.host = host
        self.host2 = host
        self.port = port
        self.global_headers = global_headers
        self.http = MyHttp(log_websocket_consumer, protocol, host, port)
        self.func_map = {'死等待':'test_sleep'} # 存放函数中文名称及代码层函数的映射关系
        self.log_websocket_consumer = log_websocket_consumer
        self.class_name = ''


    def set_check_pattern(self, check_pattern):
        self.check_pattern = check_pattern


    # 该函数用于替换动态变量（ 后台控制，参数名不能带空格
    def replace_variable(self, src_string):
        try:
            variable_list = re.findall('\${(.+?)}', src_string, re.DOTALL)
            variable_list = ['${%s}' % item for item in variable_list if not item.strip().startswith('_')]

            msg = '检查到目标内容中待替换的动态变量有:%s' % variable_list
            logger.info(msg)
            self.log_websocket_consumer.info(msg)

            msg = '已保存的全局变量有：%s' % global_variable_dic
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            for item in variable_list:
                msg = '正在替换动态变量：%s' % item
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                variable = str(item.strip('${').strip('}').strip())
                if type(global_variable_dic[variable]) == type(1):
                    src_string = src_string.replace(item, str(global_variable_dic[variable]))
                else:
                    src_string = src_string.replace(item, global_variable_dic[variable])

            msg  = '替换动态变量后的内容：%s'% src_string
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
        except Exception as e:
            msg  = '替换动态变量出错：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
        finally:
            return  src_string


    def replace_plugin_func(self, src_string):
        '''
        该函数用于替换插件函数
        '''

        def call_func(plugin_func):
            try:
                result = re.findall('\${\s*(_.+?)\((.*)\)\s*}', plugin_func)
                if result:
                    plugin_func_name, plugin_func_args = result[0]

                    temp_list = re.findall('\${.+?}',plugin_func_args) # 存放“插件函数”参数

                    i = 0
                    temp_dict = {} # 存放被临时替换的“插件函数”的映射
                    for item in temp_list:
                        plugin_func_args = plugin_func_args.replace(item, 'plugin_func_%s' % str(i)) # 先临时替换“插件函数”，以免执行下述split代码时，把插件函数中的参数也分隔出来，当成当前函数的参数
                        temp_dict['plugin_func_%s' % str(i)] = item

                    plugin_func_args_list = plugin_func_args.strip().split(',') # 获取逗号分隔的参数列表
                    plugin_func_args_list = [item.strip() for item in plugin_func_args_list] # 去掉参数前后空白字符

                    # 还原被替换的“插件函数”
                    for i in range(0, len(plugin_func_args_list)):
                        if plugin_func_args_list[i] in temp_dict.keys():
                            plugin_func_args_list[i] = temp_dict[plugin_func_args_list[i]]

                    index = 0
                    for item in plugin_func_args_list:
                        plugin_func_list = re.findall('\${\s*_.+}', item)
                        if plugin_func_list: # 如果参数本身也是个函数，则执行递归调用
                            temp = ''
                            for item in plugin_func_list:
                                result = call_func(item)
                                if result[0]:
                                    temp += str(result[1])
                                else:
                                    return [False, result[1]]
                        else:
                            temp = item
                        plugin_func_args_list[index] = eval(temp) # 替换参数列表中的 “插件函数”
                        index += 1
                    return [True, getattr(globals()['pluginfunc'], plugin_func_name)(plugin_func_args_list, self.log_websocket_consumer)]
                else:
                    msg = '正则表达式没有匹配到函数名称和函数参数'
                    logger.error(msg)
                    self.log_websocket_consumer.error(msg)
                    return [False, '正则表达式没有匹配到函数名称和函数参数']
            except Exception as e:
                msg  = '执行 call_func(%s) 出错：%s' % (plugin_func, e)
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                return [False, '执行 call_func(%s) 出错：%s' % (plugin_func, e)]

        src_string_copy = src_string
        try:
            plugin_func_list = re.findall('\${\s*_.+[^}\"]\s*}', src_string)
            msg  = '检查到目标内容中待替换的插件函数有:%s' % plugin_func_list
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '支持的插件函数有：%s' % global_plugin_func_name_list
            logger.debug(msg)
            self.log_websocket_consumer.debug(msg)
            for item in plugin_func_list:
                msg = '正在替换插件函数：%s' % item
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                result = call_func(item)
                if result[0]:
                    if type(result[1]) == type(b''):
                        result[1] = str(result[1]).lstrip('b')
                    if len(str(result[1])) < 30: # 防止内容过长
                        src_string_copy = src_string_copy.replace(item, str(result[1]))

                    src_string = src_string.replace(item, result[1])
                else:
                    msg  = '替换插件函数出错：%s' % result[1]
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    continue
        except Exception as e:
            msg = '替换插件函数出错：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
        finally:
            return [src_string, src_string_copy]


    def run(self, debug, retry=False):
        try:
            # 获取开始运行时间
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            msg = '步骤类型：%s' % self.step_type
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '步骤操作对象：%s' % self.op_object
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '执行操作：%s' % self.exec_operation
            logger.info(msg)
            self.log_websocket_consumer.info(msg)               
            if not retry:
                if self.step_type == '请求接口':
                    if self.request_headers:
                        msg = '正在替换“请求头”中的动态参数'
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)
                        self.request_headers = self.replace_variable(self.request_headers)
                        self.request_headers = json.loads(self.request_headers, object_hook=OrderedDict)
                        self.request_headers2 = self.request_headers.copy()
                    else:
                        self.request_headers2 = {}

                    for host in self.global_headers:
                        # 判断该host下是否有全局请求头
                        host_of_interface = self.host
                        if host == host_of_interface:
                           self.request_headers2.update(self.global_headers[host])
                    self.http.set_headers(self.request_headers2)

                    self.class_name = self.op_object
                    self.exec_operation2 = self.exec_operation
                elif self.step_type == '操作数据库':
                    self.class_name = 'DBUnittestTestCase'
                    self.exec_operation2 = 'test_' + self.exec_operation
                    self.request_headers2 = ''
                elif self.step_type == '执行函数':
                    self.class_name = 'FuncUnittestTestCase'
                    self.exec_operation2 = self.func_map.get(self.op_object)
                    self.request_headers2 = ''
                elif self.step_type == '操作Redis':
                    self.class_name = 'RedisUnittestTestCase'
                    self.exec_operation2 = 'test_' + self.exec_operation
                    self.request_headers2 = ''

                self.input_params2 = self.input_params
                self.url_or_sql2 = self.url_or_sql
                self.host2 = self.host

                if self.input_params:
                    msg  = '正在替换“输入参数”中的动态参数'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    self.input_params = self.replace_variable(self.input_params)

                    msg = '正在替换“输入参数”中的插件函数'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    result = self.replace_plugin_func(self.input_params)
                    self.input_params, self.input_params2 = result
                if self.url_or_sql:
                    msg = '正在替换“URL/SQL”中的动态参数'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    self.url_or_sql = self.replace_variable(self.url_or_sql)

                    msg = '正在替换“URL/SQL”中的插件函数'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    result = self.replace_plugin_func(self.url_or_sql)
                    self.url_or_sql, self.url_or_sql2 = result

                if self.host:
                    msg  = '正在替换“主机地址”中的动态参数'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    self.host = self.replace_variable(self.host)

                    msg = '正在替换“主机地址”中的插件函数'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    result = self.replace_plugin_func(self.host)
                    self.host, self.host2 = result
                    self.http.set_host(self.host)


                if self.output_params:
                    self.output_params = json.loads(self.output_params) # 转为字典

            runner = unittest.TextTestRunner()
            test_step_action = unittest.TestSuite()
            test_step_action.addTest((globals()[self.class_name])(self.op_object, self.request_headers2, self.request_method, self.url_or_sql, self.input_params,
                                                                 self.check_rule, self.check_pattern, self.response_to_check,
                                                                 self.output_params, self.http, self, self.log_websocket_consumer, self.exec_operation2))
            step_run_result = runner.run(test_step_action)

            msg = 'step_run_result：%s, errors：%s，failures：%s' % (step_run_result, step_run_result.errors, step_run_result.failures)
            logger.debug(msg)
            self.log_websocket_consumer.debug(msg)

            if 0 != len(step_run_result.errors):
                error = step_run_result.errors[0][1]
                result = [False, '失败', error]
            elif 0 != len(step_run_result.failures):
                failure = step_run_result.failures[0][1]
                pattern = re.compile('AssertionError:(.+)', re.I)
                result = re.findall(pattern, failure)
                if result:
                    result = [False, '失败', result[0]]
                else:
                    result = [False, '失败', failure]
            else:
                result = [True, '成功', '']

            remark = result[2]
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            result = [False, '失败', msg]
        finally:
            msg = '正在收集用例步骤运行结果数据'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            if not debug:
                # logger.info('======================正在记录用例步骤运行结果到测试报告-用例步骤执行明细表======================')
                if not retry:
                    if self.step_type in ['操作数据库', '执行函数', '操作Redis']:
                        self.http.protocol, self.host2, self.port = '', '', ''

                request_headers2 = '<xmp>%s</xmp>' % str(self.request_headers2)
                input_params2 = '<xmp>%s</xmp>' % str(self.input_params2)
                output_params2 = '<xmp>%s</xmp>' % str(self.output_params2)
                check_pattern = '<xmp>%s</xmp>' % json.dumps(self.check_pattern, ensure_ascii=False, indent=4)
                remark = '<xmp>%s</xmp>' % remark
                data = (self.execution_num, self.plan_id, self.case_id, self.step_id, self.order, self.step_type, self.op_object, self.object_id, self.exec_operation,
                            self.http.protocol, self.host2, self.port, request_headers2, self.request_method, self.url_or_sql2,
                            input_params2, self.response_to_check, self.check_rule, check_pattern, output_params2, result[1], remark, start_time, 0)
                #  去掉插入数据库操作，以防止记录失败重试过程中的步骤运行结果
                result.append(data)
            else:
                pass
            return  result

