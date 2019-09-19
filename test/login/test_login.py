#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: test_login.py
@time: 2019/9/6 13:44
@desc: 自动化测试：登陆用例
'''

from selenium import webdriver
from utils.config import Config
from utils.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains   # 鼠标操作
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *   # 导入所有异常类
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait   # 显性等待时间
from utils import assertion
from tools.common.BrowserDriver import BrowserDriver
from HTMLTestRunner_cn import HTMLTestRunner
from utils.file_read import YamlRead
from utils.file_write import YamlWrite

import unittest
import time
import os
import sys


logger = Logger('logger').getlog()

class Test_Login(unittest.TestCase):

    def setUp(self):
        self.sc = Config()
        self.b = BrowserDriver()
        self.driver = self.b.OpenBrowser()
        self.driver.implicitly_wait(30) # 全局隐形等待30S
        self.imgs = []
        self.ym = YamlWrite()

    def tearDown(self):
        self.b.QuitBrowser()

    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    def test_login_correct(self):
        """ 测试用户名密码正确登录"""
        try:
            # 将用例名称写入casename.yaml文件中
            self.ym.Write_Yaml(self.sc.getCasename_path(),{'casename':'用例%s执行开始'%sys._getframe().f_code.co_name})
            logger.info('开始执行用例%s'%sys._getframe().f_code.co_name)
            self.b.by_find_element('name','account').send_keys(self.sc.getConfig('User').get('username'))
            self.b.by_find_element('name','password').send_keys(self.sc.getConfig('User').get('password'))
            self.b.driver.implicitly_wait(30)     # 设置全局隐形等待时间
            self.addimg()
            self.assertEqual('无纸化会议1', self.b.get_page_title())
            logger.info('用例%s执行成功'%sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败'%sys._getframe().f_code.co_name)
            raise

    def test_login_error_1(self):
        """ 测试用户名正确密码错误登录"""
        try:
            # 将用例名称写入casename.yaml文件中
            self.ym.Write_Yaml(self.sc.getCasename_path(),{'casename':'用例%s执行开始'%sys._getframe().f_code.co_name})
            logger.info('开始执行用例%s'%sys._getframe().f_code.co_name)
            self.b.by_find_element('name','account').send_keys(self.sc.getConfig('User').get('username'))
            self.b.by_find_element('name','password').send_keys('123')
            self.b.driver.implicitly_wait(30)     # 设置全局隐形等待时间
            self.addimg()
            self.assertEqual('无纸化会议1', self.b.get_page_title())
            logger.info('用例%s执行成功'%sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败'%sys._getframe().f_code.co_name)
            raise


    # def test_login_


if __name__ == '__main__':
    suit1 = unittest.TestLoader().loadTestsFromTestCase(Test_Login)
    suit = unittest.TestSuite()
    suit.addTest(suit1)
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb")
                           )
    runer.run(suit)