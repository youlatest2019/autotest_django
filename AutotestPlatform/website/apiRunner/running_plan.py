#!/usr/bin/env python
#-*-encoding:utf-8-*-



import json
from collections import OrderedDict

from .common.log import logger
from .common.globalvar import global_variable_dic
from .common.globalvar import db_related_to_project_dic
from .common.globalvar import redis_related_to_project_dic
from .common.mydb import MyDB
from .common.redis_client import RedisClient
from .test_project import TestProject



class RunningPlan:
    def __init__(self, running_plan_num, running_plan_name, project_id, project_name, plan_name, plan_id_list, test_platform_db, log_websocket_consumer):
        self.running_plan_num = running_plan_num
        self.running_plan_name = running_plan_name
        self.project_id = project_id
        self.project_name = project_name
        self.plan_name = plan_name
        self.plan_id_list = plan_id_list
        self.test_platform_db = test_platform_db
        self.log_websocket_consumer = log_websocket_consumer

    def run(self, debug):
        try:
            msg = '正在查询项目[ID：%s,名称：%s]相关信息' % (self.project_id, self.project_name)
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            result = self.test_platform_db.select_one_record('SELECT protocol, host, port, environment_id, valid_flag '
                                                        'FROM `website_api_project_setting` WHERE id = %s', (self.project_id,))
            if result[0] and result[1]:
                protocol, host, port, environment_id, valid_flag = result[1]
                if valid_flag  == '启用':
                    msg = '正在查询与项目关联的数据库信息'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    result = self.test_platform_db.select_many_record("SELECT db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd "
                                                                 "FROM `website_database_setting` "
                                                                 "WHERE locate('API%s', project_id) != 0 AND environment_id= '%s'" %  (self.project_id, environment_id))
                    if result[0] and result[1]:
                        for record in result[1]:
                            db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd = record
                            if db_type == 'MySQL':
                                mydb = MyDB(self.log_websocket_consumer, db_name=db_name, db_host=db_host, port=db_port, user=db_user, password=db_passwd, charset='utf8')
                                db_related_to_project_dic[db_alias] = mydb
                            elif db_type == 'Redis':
                                if not db_passwd.strip():
                                    db_passwd = None
                                if db_name.strip() == '':
                                    db_name = '0'
                                myredis = RedisClient(self.log_websocket_consumer, host=db_host, port=db_port, password=db_passwd, db=db_name, charset='utf-8')
                                redis_related_to_project_dic[db_alias] = myredis
                    elif not result[0]:
                        msg = '查询项目相关的数据库配置信息出错：%s' % result[1]
                        logger.error(msg)
                        self.log_websocket_consumer.error(msg)
                        return [False, '运行失败', result[1]]

                    msg = '正在查询与项目关联的全局变量'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    result = self.test_platform_db.select_many_record("SELECT `name`, `value` "
                                                                 "FROM `website_global_variable_setting` "
                                                                 "WHERE  project_type='API项目' AND locate('%s', project_id) != 0 AND locate('%s', env_id) != 0 ", (self.project_id, environment_id))
                    if result[0] and result[1]:
                        for record in result[1]:
                            name, value = record
                            name = name
                            global_variable_dic[name] = value
                    elif not result[0]:
                        msg = '查询项目相关的全局变量配置信息出错：%s' % result[1]
                        logger.error(msg)
                        self.log_websocket_consumer.error(msg)
                        return [False, '运行失败', result[1]]

                    try:
                        if 'global_headers' in global_variable_dic.keys():
                            global_headers =  global_variable_dic['global_headers']
                            # 防止用户输入了中文冒号，替换为英文冒号,不然经过global_headers.encode("utf-8").decode("latin1")这样编码转换，
                            # 会把"key"：中的中文冒号解码为非英文冒号，导致执行json loads函数时会报错；
                            # 另外，请求头从数据库读取，可能涉及到换行符，需要去掉
                            global_headers = global_headers.replace('：', ':').replace('\t', '')
                            global_headers = json.loads(global_headers, object_pairs_hook=OrderedDict)

                        else:
                            global_headers = {}

                        test_project = TestProject(self.project_id, self.project_name, protocol, host, port, global_headers, self.plan_id_list, self.test_platform_db, self.log_websocket_consumer)
                        msg = '======================开始运行测试项目[名称：%s, ID：%s]======================' % (self.project_name, self.project_id)
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)
                        result = test_project.run(debug)

                        if not result[0]:
                            result = [False, '运行失败', result[1]]
                        else:
                            result = [True, '运行成功', '']
                    except Exception as e:
                        msg = '%s' % e
                        logger.error(msg)
                        self.log_websocket_consumer.error(msg)
                        result = [False, '运行失败', '%s' % e]
                else:
                    msg = '项目已被禁用，结束运行'
                    logger.warn(msg)
                    self.log_websocket_consumer.warn(msg)
                    result = [False, '运行失败', '项目已被禁用，结束运行']
            elif result[0] and not result[1]:
                msg = '未查询到项目相关的信息'
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                result = [False, '运行失败', '未查询到项目相关的信息']
            else:
                msg = '查询项目相关信息失败：%s' % result[1]
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                result = [False, '运行失败', '查询项目相关信息失败：%s' % result[1]]
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            result =  [False, '运行失败', '%s'% e]
        finally:
            msg = '正在释放资源'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '正在断开与项目关联的数据库连接'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            for key, db in db_related_to_project_dic.copy().items():
                db.close()
                del db_related_to_project_dic[key]

            msg = '正在清理与项目关联的全局变量'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            global_variable_dic.clear()
            return result






