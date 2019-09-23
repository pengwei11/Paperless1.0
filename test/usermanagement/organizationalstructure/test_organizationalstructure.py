#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: test_organizationalstructure.py
@time: 2019/9/23 10:42
@desc: 组织架构测试用例
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


class Test_OrganizationalStructure(unittest.TestCase):

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
        # 点击用户分组
        self.b.by_find_element('link_text', '组织架构').click()

    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()

    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    '''测试用例'''

    def test_zzjg_at_01(self):
        """组织架构界面——标题显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言顶标题是否存在
            self.assertEqual('组织架构',
                             self.b.by_find_element('css', '.personnel.fl').text,'标题显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_zzjg_at_02(self):
        """组织架构界面——组织架构顶部栏显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言顶部栏元素是否存在
            self.assertEqual('新增单位',
                             self.b.by_find_element('css', '.l-btn-text').text,'顶部栏，新增单位显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_zzjg_at_03(self):
        """组织架构界面——组织架构字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            self.assertEqual('名称', self.b.by_find_element('xpath',
                                                          '//*[@id="mCSB_1_container"]/div/div/div[2]/div[2]/div[1]'
                                                          '/div/table/tbody/tr/td[1]/div/span[1]').text, '名称字段显示错误')
            self.assertEqual('操作', self.b.by_find_element('xpath',
                                                          '//*[@id="mCSB_1_container"]/div/div/div[2]/div[2]/div[1]'
                                                          '/div/table/tbody/tr/td[2]/div/span[1]').text, '操作字段显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_zzjg_at_04(self):
        """组织架构界面——新增单位字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在单位,false创建
            if self.b.isElementExist('css', '.datagrid-row') == False:
                # 点击'新增单位'
                self.b.by_find_element('css', '.l-btn-text').click()
                # 单位名称输入
                self.b.by_find_element('name', 'name').send_keys('测试新增单位')
                # 点击确定
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()
                time.sleep(1)
                self.addimg()
            self.addimg()
            # 获取第一个部门的node-id
            value = self.b.by_find_element('css',
                                           '#mCSB_1_container > div > div > div.datagrid-view > div.datagrid-view2 > '
                                           'div.datagrid-body > table > tbody > tr:nth-child(1)').get_attribute('node-id')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(1) > div > span.tree-title' % value),
                '名称字段不存在')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(1)' % value),
                '新增部门字段不存在')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(2)' % value),
                '编辑字段不存在')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(3)' % value),
                '编辑字段不存在')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_zzjg_at_05(self):
        """组织架构界面——新增部门字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在单位,false创建
            if self.b.isElementExist('css' , '.datagrid-row') == False:
                # 点击'新增单位'
                self.b.by_find_element('css', '.l-btn-text').click()
                # 单位名称输入
                self.b.by_find_element('name', 'name').send_keys('测试新增单位')
                # 点击确定
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()
                time.sleep(1)
                self.addimg()
            # 获取第一个部门的node-id
            d_nodeid = self.b.by_find_element('css',
                                            '#mCSB_1_container > div > div > div.datagrid-view > div.datagrid-view2 > '
                                            'div.datagrid-body > table > tbody > tr:nth-child(1)').get_attribute('node-id')
            if self.b.isElementExist('css' , '.treegrid-tr-tree') == False:
                # 点击新增部门
                self.b.by_find_element('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(1)' % d_nodeid).click()
                # 部门名称输入
                self.b.by_find_element('name', 'name').send_keys('测试新增部门')
                # 点击确认
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()
                time.sleep(1)
                self.addimg()
            b_nodeid = self.b.by_find_element('css','#mCSB_1_container > div > div > div.datagrid-view > '
                                                    'div.datagrid-view2 > div.datagrid-body > table > tbody > '
                                                    'tr.treegrid-tr-tree > td > div > table > tbody > tr:nth-child(1)').get_attribute('node-id')
            self.addimg()
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(1) > div > span.tree-title' % b_nodeid),
                '名称字段不存在')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(1)' % b_nodeid),
                '新增职位字段不存在')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(2)' % b_nodeid),
                '编辑字段不存在')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(3)' % b_nodeid),
                '编辑字段不存在')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_zzjg_at_06(self):
        """组织架构界面——新增职位字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在单位,false创建
            if self.b.isElementExist('css' , '.datagrid-row') == False:
                # 点击'新增单位'
                self.b.by_find_element('css', '.l-btn-text').click()
                # 单位名称输入
                self.b.by_find_element('name', 'name').send_keys('测试新增单位')
                # 点击确定
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()
                time.sleep(1)
                self.addimg()
            # 获取第一个单位的node-id
            d_nodeid = self.b.by_find_element('css',
                                            '#mCSB_1_container > div > div > div.datagrid-view > div.datagrid-view2 > '
                                            'div.datagrid-body > table > tbody > tr:nth-child(1)').get_attribute('node-id')
            # 判断第一个单位内是否存在部门
            if self.b.isElementExist('css' , '.treegrid-tr-tree') == False:
                # 点击新增部门
                self.b.by_find_element('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(1)' % d_nodeid).click()
                # 部门名称输入
                self.b.by_find_element('name', 'name').send_keys('测试新增部门')
                # 点击确认
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()
                time.sleep(1)
                self.addimg()
            # 获取第一个部门的node-id
            b_nodeid = self.b.by_find_element('css','#mCSB_1_container > div > div > div.datagrid-view > '
                                                    'div.datagrid-view2 > div.datagrid-body > table > tbody > '
                                                    'tr.treegrid-tr-tree > td > div > table > tbody > tr:nth-child(1)').get_attribute('node-id')
            # 判断第一个部门内是否存在职位
            if self.b.isElementExist('xpath' , '//*[@id="mCSB_1_container"]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[2]') == False:
                # 点击新增职位
                self.b.by_find_element('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(1)' % b_nodeid).click()
                # 职位名称输入
                self.b.by_find_element('css', '#layui-layer1 > div.layui-layer-content > form > div.middle > div > div > input').send_keys('测试新增职位')
                # 点击确认
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()
                time.sleep(1)
                self.addimg()

            z_nodeid = self.b.by_find_element('xpath',
                                              '//*[@id="mCSB_1_container"]/div/div/div[2]/div[2]/div[2]/table/tbody/'
                                              'tr[2]/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]').get_attribute('node-id')
            self.addimg()
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(1) > div > span.tree-title' % z_nodeid),
                '名称字段不存在')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(1)' % z_nodeid),
                '新增职位字段不存在')
            self.assertTrue(
                self.b.isElementExist('css', '#datagrid-row-r1-2-%s > td:nth-child(2) > div > a:nth-child(3)' % z_nodeid),
                '编辑字段不存在')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_zzjg_at_07(self):
        """组织架构界面——新增单位测试"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击'新增单位'
            self.b.by_find_element('css', '.l-btn-text').click()
            # 单位名称输入
            self.b.by_find_element('name', 'name').send_keys('测试新增单位')
            # 获取输入的单位名称
            name = self.b.by_find_element('name', 'name').get_attribute('value')
            # 点击确定
            self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()
            time.sleep(1)
            self.addimg()
            List = []
            for t in self.b.by_find_elements('css', '.tree-title'):
                List.append(t.text)
            logger.info(List)
            self.assertTrue(name in List, '新增单位未显示在列表中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_zzjg_at_08(self):
        """组织架构界面——新增单位重置按钮测试"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击'新增单位'
            self.b.by_find_element('css', '.l-btn-text').click()
            # 单位名称输入
            self.b.by_find_element('name', 'name').send_keys('测试新增单位')
            # 点击重置
            self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[2]').click()
            # 获取输入框的值
            name = self.b.by_find_element('name', 'name').get_attribute('value')
            self.assertTrue(name == '', '重置功能无效')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise
if __name__ == '__main__':
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(Test_UserGruop)
    suit = unittest.TestSuite()
    # suit.addTest(suit1)
    suit.addTest(Test_OrganizationalStructure('test_zzjg_at_08'))


    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb"),
                           verbosity=2,
                           )
    runer.run(suit)