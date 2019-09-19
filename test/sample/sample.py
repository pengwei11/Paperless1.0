#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: sample.py
@time: 2019/9/6 14:38
@desc: 执行所有测试用例
'''

import unittest
from HTMLTestRunner_cn import HTMLTestRunner
import time
import os
from utils.config import Config
from utils.logger import Logger
logger = Logger('logger').getlog()

class Run_All():
    def __init__(self):
        self.sc = Config()
        self.test_path = self.sc.getTest_path()
        self.case_path = self.sc.getReadIP('moudle')
        if self.case_path == '全部':
            self.case_path = self.test_path
        elif self.case_path == '登录模块':
            self.case_path = os.path.join(self.test_path, 'login')
        elif self.case_path == '会议信息模块':
            self.case_path = os.path.join(self.test_path, 'meetinginformation')
        elif self.case_path == '会议资料模块':
            self.case_path = os.path.join(self.test_path, 'meetingdata')
        self.report_path = self.sc.getReadIP('reportPath') # 报告存放位置
        self.timestr = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        self.filename = self.report_path+self.timestr+'.html'
        print(self.filename)


    def Run_test_case_all(self):
        self.fp = open(self.filename, 'wb')
        suites = unittest.defaultTestLoader.discover(self.case_path, pattern='test*.py')
        result = unittest.TestSuite()
        result.addTest(suites)
        runner = HTMLTestRunner(
            title='无纸化测试报告',
            description='无纸化测试',
            stream=self.fp,
            verbosity=2,
        )
        runner.run(result)
        logger.info("运行完成，生成测试报告在：%s中"%self.report_path)

if __name__ == '__main__':
    r = Run_All()
    r.Run_test_case_all()
