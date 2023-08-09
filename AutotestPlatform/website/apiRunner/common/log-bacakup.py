#!/usr/bin/env python
# -*- coding:utf-8 -*-



import logging
# from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
import threading
import configparser
import os
import sys


class LogSignleton(object):
    def __init__(self, log_config, log_filename):
        pass

    def __new__(cls, log_config, log_filename):
        mutex=threading.Lock()
        mutex.acquire() # 上锁，防止多线程下出问题
        if not hasattr(cls, 'instance'):
            cls.instance = super(LogSignleton, cls).__new__(cls)
            config = configparser.ConfigParser()
            config.read(log_config, encoding='utf-8-sig')
            cls.instance.log_filename = config.get('LOGGING', 'log_file')
            if not cls.instance.log_filename.strip(' '):
                cls.instance.log_filename = log_filename
            elif os.path.exists(cls.instance.log_filename):
                if os.path.isdir(cls.instance.log_filename):
                    print('日志路径不能为目录，终止程序')
                    exit()
            else:
                print('日志路径不存在，终止程序')
                exit()
            cls.instance.max_bytes_each = int(config.get('LOGGING', 'max_bytes_each'))
            cls.instance.backup_count = int(config.get('LOGGING', 'backup_count'))
            cls.instance.fmt = config.get('LOGGING', 'fmt')
            cls.instance.log_level_in_console = int(config.get('LOGGING', 'log_level_in_console'))
            cls.instance.log_level_in_logfile = int(config.get('LOGGING', 'log_level_in_logfile'))
            cls.instance.logger_name = config.get('LOGGING', 'logger_name')
            cls.instance.console_log_on = int(config.get('LOGGING', 'console_log_on'))
            cls.instance.logfile_log_on = int(config.get('LOGGING', 'logfile_log_on'))
            cls.instance.logger = logging.getLogger(cls.instance.logger_name)
            cls.instance.__config_logger()
            cls.instance.logger.setLevel(1)
        mutex.release()
        return cls.instance

    def get_logger(self):
        return  self.logger

    def __config_logger(self):
        # 设置日志格式
        fmt = self.fmt.replace('|','%')
        formatter = logging.Formatter(fmt)


        if self.console_log_on == 1: # 如果开启控制台日志
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            console.setLevel(self.log_level_in_console)
            self.logger.addHandler(console)
            print('当前控制台生效的日志级别为：', self.logger.getEffectiveLevel())

        if self.logfile_log_on == 1: # 如果开启文件日志
            #rt_file_handler = RotatingFileHandler(self.log_filename, maxBytes=self.max_bytes_each, backupCount=self.backup_count)
            rt_file_handler = TimedRotatingFileHandler(self.log_filename, when='D', interval=1, backupCount=self.backup_count)
            rt_file_handler.setFormatter(formatter)
            rt_file_handler.setLevel(self.log_level_in_logfile)
            self.logger.addHandler(rt_file_handler)


co_filepath = sys._getframe().f_code.co_filename
head, tail = os.path.split(co_filepath)

conf_filepath = os.path.join(head, '../conf/log.conf')
conf_filepath = os.path.normpath(conf_filepath)

log_filename = os.path.join(head, '../logs/log.txt')
logsignleton = LogSignleton(conf_filepath, log_filename)
logger = logsignleton.get_logger()


