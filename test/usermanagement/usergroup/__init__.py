#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: __init__.py.py
@time: 2019/9/19 17:10
@desc: 用户分组测试用例
'''

from selenium import webdriver
from utils.config import Config
from utils.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标操作
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *  # 导入所有异常类
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # 显性等待时间
from utils import assertion
from tools.common.BrowserDriver import BrowserDriver
from HTMLTestRunner_cn import HTMLTestRunner
from utils.file_read import YamlRead
from utils.file_write import YamlWrite

import unittest
import time
import os
import sys
import random

logger = Logger('logger').getlog()


class Test_UserGroup(unittest.TestCase):

    def setUp(self):
        self.sc = Config()
        self.b = BrowserDriver()
        self.driver = self.b.OpenBrowser()
        self.driver.implicitly_wait(10)  # 全局隐形等待30S
        self.imgs = []
        self.ym = YamlWrite()
        # 每次执行用例前都登陆网页
        self.b.by_find_element('name', 'account').send_keys(self.sc.getConfig('User').get('username'))
        self.b.by_find_element('name', 'password').send_keys(self.sc.getConfig('User').get('password'))
        self.b.by_find_element('id', 'login').click()
        # 点击用户分组
        self.b.by_find_element('css', '#wrap > div > div.matter.clear > div.left_b.clear.fl.pob > div > div:nth-child(2) > div > ul > a:nth-child(2)').click()
        # if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-1-0"]/td[4]/div'):
        #     self.b.by_find_element('css','.datagrid-header-check').click()
        #     self.b.by_find_element('css','a.easyui-linkbutton:nth-child(4) > span:nth-child(1) > span:nth-child(1)').click()
        #     self.b.by_find_element('css','.layui-layer-btn0').click()

    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()

    # 截图
    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True


    def test_yhfz_at_01(self):
        """用户分组界面——用户列表顶栏显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            self.assertEqual('新增分组',
                             self.b.by_find_element('css', '#add-win > span > span.l-btn-text').text)
            self.assertEqual('删除',
                             self.b.by_find_element('css', '#common_operate > a:nth-child(2) > span > span.l-btn-text').text)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise
