﻿#!/usr/bin/env python
# -*- coding:utf-8 -*-



import time

from ..common.log import logger
from ..unittesttestcase import MyUnittestTestCase

__all__ = ['FuncUnittestTestCase']

class FuncUnittestTestCase(MyUnittestTestCase):
    def test_sleep(self):
        '''死等待'''
        try:
            if self.input_params != '':
                if self.input_params.isdigit():
                    self.input_params = int(self.input_params)
                    time.sleep(self.input_params)
                else:
                    msg = '输入参数非数字'
                    logger.error(msg)
                    self.log_websocket_consumer.error(msg)
                    self.assertEqual(1, 0, msg='输入参数非数字')
            else:
                logger.error('输入参数为空')
                self.log_websocket_consumer.error
                self.assertEqual(1, 0, msg='输入参数为空')
        except Exception as e:
            msg = 'fail#%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            self.assertEqual(1, 0, msg=msg)





