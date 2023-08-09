#!/usr/bin/env python
#-*-encoding:utf-8-*-



import time
import json
from .common.log import logger
from .test_case_step import TestCaseStep
from .test_report import TestReport


class TestCase:
    def __init__(self, execution_num, plan_id, case_id, case_path, case_name, protocol, host, port, global_headers, log_websocket_consumer, test_platform_db):
        self.execution_num = execution_num
        self.plan_id = plan_id
        self.case_id = case_id
        self.case_path = case_path
        self.case_name = case_name
        self.protocol = protocol
        self.host = host
        self.port = port
        self.global_headers = global_headers
        self.log_websocket_consumer = log_websocket_consumer
        self.test_platform_db = test_platform_db
        self.test_reporter = TestReport(self.test_platform_db, log_websocket_consumer)


    def run(self, debug):
        try:
            # 获取开始运行时间
            timestamp_for_start = time.time()
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            msg = '正在查询测试用例[ID：%s, 名称：%s]关联的测试步骤' % (self.case_id, self.case_name)
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            query = 'SELECT id, `order`, step_type, op_object, object_id, exec_operation, request_header, request_method, url_or_sql, input_params, ' \
                    'response_to_check, check_rule, check_pattern,  output_params, protocol, host, port, run_times, try_for_failure, retry_frequency ' \
                    'FROM `website_api_test_case_step`  WHERE case_id=%s AND  status=\'启用\' ORDER BY `order` ASC'
            data = (self.case_id,)
            result = self.test_platform_db.select_many_record(query, data)

            if result[0] and result[1]:
                records = result[1]
                msg = '开始执行测试步骤'
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                result = [False, '阻塞', '没有找到与用例关联的测试步骤']
                for record in records:
                    step_id, order, step_type, op_object, object_id, exec_operation, request_header, \
                    request_method, url_or_sql, input_params, response_to_check, check_rule, \
                    check_pattern,  output_params, protocol, host, port, run_times, try_for_failure, retry_frequency = record
                    if protocol != '':
                        protocol = protocol
                    else:
                        protocol = self.protocol
                    if host != '':
                        self.host = host
                    if port != '':
                        self.port = port

                    run_times, try_for_failure, retry_frequency = int(run_times), int(try_for_failure), int(retry_frequency)
                    flag = False # 标记步骤重复运行过程中是否出错
                    for i in range(0, run_times): # 运行指定次数
                        if step_type == '执行用例':
                            # 获取开始运行时间
                            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            level_list = op_object.split('->') # op_object即为case_path
                            case_name = level_list[len(level_list) - 1]
                            test_case = TestCase(self.execution_num, self.plan_id, object_id, op_object, case_name, self.protocol, self.host, self.port, self.global_headers, self.log_websocket_consumer, self.test_platform_db)
                            msg = '======================开始执行测试用例步骤（第 %s 步, 步骤ID: %s, 用例ID：%s, 用例名称：%s）======================' % (order, step_id, self.case_id, self.case_name)
                            logger.info(msg)
                            self.log_websocket_consumer.info(msg)

                            msg='步骤类型：执行用例'
                            logger.info(msg)
                            self.log_websocket_consumer.info(msg)

                            msg= '步骤操作对象：%s, ID：%s' % (op_object, object_id)
                            logger.info(msg)
                            self.log_websocket_consumer.info(msg)
                            retry = 0 # 失败重试次数
                            result = test_case.run(debug)
                            while not result[0] and retry <= try_for_failure:
                                time.sleep(retry_frequency) # 频率
                                retry += 1
                                msg = '执行测试用例步骤失败，正在进行第 %s 次重试（第 %s 步, 步骤ID: %s, 用例ID：%s, 用例名称：%s）======================' % (str(retry), order, step_id, self.case_id, self.case_name)
                                logger.error(msg)
                                self.log_websocket_consumer.error(msg)
                                result = test_case.run(debug, True)

                            if not debug: # 不是调试运行，
                                msg='======================正在记录测试用例步骤运行结果到测试报告-用例步骤执行明细表======================'
                                logger.info(msg)
                                self.log_websocket_consumer.info(msg)

                                request_header = '<xmp>%s</xmp>' % str(request_header)
                                input_params = '<xmp>%s</xmp>' % str(input_params)
                                output_params = '<xmp>%s</xmp>' % str(output_params)
                                check_pattern = '<xmp>%s</xmp>' % json.dumps(check_pattern, ensure_ascii=False, indent=4)
                                remark = '<xmp>%s</xmp>' % result[2]
                                data = (self.execution_num, self.plan_id, self.case_id, step_id, order, step_type, op_object, object_id, exec_operation,
                                        protocol, self.host, self.port, request_header, request_method, url_or_sql, input_params,
                                        response_to_check, check_rule, check_pattern, output_params, result[1], remark, start_time, 0)
                                self.test_reporter.insert_report_for_case_step(data)
                        else:
                            test_case_step = TestCaseStep(self.execution_num, self.plan_id, self.case_id, step_id, order, step_type, op_object, object_id, exec_operation, request_header, \
                                                          request_method, url_or_sql, input_params, response_to_check, check_rule, \
                                                          check_pattern,  output_params, protocol, self.host, self.port, self.global_headers, self.log_websocket_consumer)
                            msg='======================开始执行测试用例步骤（第 %s 步, 步骤ID： %s,  用例ID：%s, 用例名称：%s）======================' % (order, step_id, self.case_id, self.case_name)
                            logger.info(msg)
                            self.log_websocket_consumer.info(msg)
                            result = test_case_step.run(debug)

                            retry = 0
                            while not result[0] and retry < try_for_failure:
                                time.sleep(retry_frequency) # 频率
                                retry += 1
                                msg='执行用例测试步骤失败，正在进行第 %s 次重试（第 %s 步, 步骤ID: %s, 用例ID：%s, 用例名称：%s）' % (str(retry), order, step_id, self.case_id, self.case_name)
                                logger.error(msg)
                                self.log_websocket_consumer.error(msg)
                                result = test_case_step.run(debug, True)
                            if not debug:
                                logger.info('======================正在记录测试用例步骤运行结果到测试报告-用例步骤执行明细表======================')
                                self.test_reporter.insert_report_for_case_step(result[3])


                        if not result[0]:
                            msg = '执行用例测试步骤运行失败（第 %s 步, 步骤ID: %s， 用例ID：%s, 用例名称：%s）======================' % (order, step_id, self.case_id, self.case_name)
                            logger.error(msg)
                            self.log_websocket_consumer.error(msg)
                            if not debug:
                                result = [result[0], result[1], '步骤(第 %s 步, 步骤ID: %s)运行失败' % (order, step_id)]
                            else:
                                result =  [result[0], result[1], '步骤(第 %s 步, 步骤ID: %s)运行失败:%s' % (order, step_id, result[2])]
                            flag = True
                            break
                    if flag: # 有步骤运行出错，停止执行剩余步骤
                        break
            elif result[0] and not result[1]:
                msg = '未查找到同测试用例关联的测试步骤'
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                result = [False, '阻塞', '未找到与用例关联的测试步骤']
            else:
                msg = '查找与测试用例(名称：%s, ID：%s)关联的用例步骤失败：%s' % (self.case_name, self.case_id, result[1])
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                result = [False, '阻塞',  '查找与测试用例(名称：%s, ID：%s)关联的用例步骤失败：%s' % (self.case_name, self.case_id, result[1])]
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            result = [False, '阻塞', '%s' % e]
        finally:
            if not debug:
                msg = '正在计算运行耗时'
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                timestamp_for_end = time.time()
                time_took = int(timestamp_for_end - timestamp_for_start)
                days, hours, minutes, seconds = str(time_took//86400), str((time_took%86400)//3600), str(((time_took%86400)%3600)//60), str(((time_took%86400)%3600)%60)
                time_took = days + '天 '+ hours +'小时 '+ minutes + '分 ' +  seconds +'秒' # 运行耗时

                msg = '正在记录用例运行结果到测试报告-用例执行明细表'
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                data = (self.execution_num, self.plan_id, self.case_id, self.case_path, self.case_name, result[1], result[2], start_time, time_took)
                self.test_reporter.insert_report_for_case(data)
            return [result[0], result[1], result[2]]