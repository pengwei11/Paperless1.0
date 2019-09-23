#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: test_personnelmanagement.py
@time: 2019/9/23 15:41
@desc: 参会人员测试用例
'''

from selenium import webdriver
from utils.config import Config
from utils.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标操作
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
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


class Test_PersonneLmanagement(unittest.TestCase):

    def setUp(self):
        self.sc = Config()
        self.b = BrowserDriver()
        self.driver = self.b.OpenBrowser()
        self.driver.implicitly_wait(5)  # 全局隐形等待30S
        self.imgs = []
        self.ym = YamlWrite()
        # 每次执行用例前都登陆网页
        self.b.by_find_element('name', 'account').send_keys(self.sc.getConfig('User').get('username'))
        self.b.by_find_element('name', 'password').send_keys(self.sc.getConfig('User').get('password'))
        self.b.by_find_element('id', 'login').click()
        # 每次执行用例都判断会议列表中是否有数据
        if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div > a') == False:
            # 点击新增会议
            self.b.by_find_element('link_text', '新增会议').click()
            # 会议名称
            self.b.by_find_element('name', 'name').send_keys('会议')
            # 获取结束时间
            endtime = self.b.by_find_element('css', '#add_meeting > div > div:nth-child(2) > div.Participants_fr.fl > span:nth-child(5) > input.textbox-value').get_attribute('value')
            newtime = int(endtime[8:10])+1
            endtime = endtime[0:10]
            endtime = endtime.replace(endtime[8:10],str(newtime))
            endtime = endtime.replace('-',',')
            endtime = endtime[0:5]+endtime[6:10]
            logger.info(endtime)
            # logger.info(endtime[-1:-2])
            # newtime = int(endtime[-1:-2])+1
            # newtime = endtime.replace(endtime[8:10],str(newtime))
            self.b.by_find_element('css', '#add_meeting > div > div:nth-child(2) > div.Participants_fr.fl > span:nth-child(5) > input.textbox-text.validatebox-text').click()
            s = self.b.by_find_element('xpath', "//td[@abbr='%s']" % endtime)
            self.b.by_find_element('css', 'body > div:nth-child(26) > div > div.datebox-button > table > tbody > tr > td:nth-child(2) > a').click()

        #
        # # 点击用户分组
        # self.b.by_find_element('link_text', '组织架构').click()

    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()

    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    def test1(self):
        pass


if __name__ == '__main__':
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(Test_PersonneLmanagement)
    suit = unittest.TestSuite()
    # suit.addTest(suit1)
    suit.addTest(Test_PersonneLmanagement('test1'))

    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb"),
                           verbosity=2,
                           )
    runer.run(suit)