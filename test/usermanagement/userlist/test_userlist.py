#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: test_userlist.py
@time: 2019/9/17 9:03
@desc: 用户列表测试用例
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

logger = Logger('Test_UserList').getlog()


class Test_UserList(unittest.TestCase):

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
        # 点击用户列表
        self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[1]/div/div[2]/div/ul/a[1]/li').click()
        # if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-1-0"]/td[4]/div'):
        #     self.b.by_find_element('css','.datagrid-header-check').click()
        #     self.b.by_find_element('css','a.easyui-linkbutton:nth-child(4) > span:nth-child(1) > span:nth-child(1)').click()
        #     self.b.by_find_element('css','.layui-layer-btn0').click()

    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()

    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    '''测试用例'''

    def test_yhlb_at_01(self):
        """用户列表界面——用户列表顶栏显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            self.assertEqual('新增用户',
                             self.b.by_find_element('xpath', '//*[@id="common_operate"]/a[1]/span/span[1]').text)
            self.assertEqual('导入用户',
                             self.b.by_find_element('xpath', '//*[@id="common_operate"]/a[2]/span/span[1]').text)
            self.assertEqual('导出用户',
                             self.b.by_find_element('xpath', '//*[@id="common_operate"]/a[3]/span/span[1]').text)
            self.assertEqual('删除', self.b.by_find_element('xpath', '//*[@id="common_operate"]/a[4]/span/span[1]').text)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_02(self):
        """用户列表界面——用户列表框字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            self.assertEqual('帐号', self.b.by_find_element('xpath',
                                                          '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[4]/div/span[1]').text,
                             '帐号字段不存在')
            self.assertEqual('姓名', self.b.by_find_element('xpath',
                                                          '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[1]/div/span[1]').text,
                             '姓名字段不存在')
            self.assertEqual('单位', self.b.by_find_element('xpath',
                                                          '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[2]/div/span[1]').text,
                             '单位字段不存在')
            self.assertEqual('部门', self.b.by_find_element('xpath',
                                                          '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[3]/div/span[1]').text,
                             '部门字段不存在')
            self.assertEqual('职务', self.b.by_find_element('xpath',
                                                          '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[4]/div/span[1]').text,
                             '职务字段不存在')
            self.assertEqual('欢迎词', self.b.by_find_element('xpath',
                                                           '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[5]/div/span[1]').text,
                             '欢迎词字段不存在')
            self.assertEqual('用户类型', self.b.by_find_element('xpath',
                                                            '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[6]/div/span[1]').text,
                             '用户类型字段不存在')
            self.assertEqual('操作', self.b.by_find_element('xpath',
                                                          '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[7]/div/span[1]').text,
                             '操作字段不存在')
            self.assertTrue(self.b.isElementExist('xpath',
                                                  '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/input'),
                            '勾选框不存在')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_03(self):
        """用户列表界面——显示新增用户字段"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            if self.b.isElementExist('xpath',
                                     '//*[@id="datagrid-row-r1-1-0"]/td[4]/div') == False:  # 判断列表内是否有用户，如果没有就创建用户
                # 点击新增用户按钮
                self.b.by_find_element('class', 'l-btn-text').click()
                # 输入账号
                self.b.by_find_element('name', 'account').send_keys('admin1')
                # 输入密码
                self.b.by_find_element('name', 'password').send_keys('123456')
                # 输入用户名
                self.b.by_find_element('name', 'username').send_keys('测试用户')
                # 　点击保存
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()

            self.addimg()

            if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-1-0"]/td[4]/div'):  # 判断新增的账号是否存在 下同
                self.assertTrue(
                    len(self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-1-0"]/td[4]/div').text) <= 20,
                    '账号字符超出长度')  # 断言账号长度是否超过10个字符 下同

            if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[1]/div/span'):
                self.assertTrue(
                    len(self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[1]/div/span').text) <= 10,
                    '用户名字符超出长度')

            if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[2]/div/span'):
                self.assertTrue(
                    len(self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[2]/div/span').text) <= 40,
                    '单位字符超出长度')

            if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[3]/div/span'):
                self.assertTrue(
                    len(self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[3]/div/span').text) <= 41,
                    '部门字符超出长度')

            if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[4]/div/span'):
                self.assertTrue(
                    len(self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[4]/div/span').text) <= 40,
                    '职务字符超出长度')

            if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[5]/div/span'):
                self.assertTrue(
                    len(self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[5]/div/span').text) <= 200,
                    '欢迎词长度超出长度')

            if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[6]/div/span'):
                self.assertTrue(self.b.by_find_element('xpath',
                                                       '//*[@id="datagrid-row-r1-2-0"]/td[6]/div/span').text == '普通用户' or '管理员' or '秘书',
                                '用户类型错误')

            if self.b.isElementExist('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[7]/div'):
                # 断言操作按钮是否有编辑和删除按钮
                self.assertTrue(
                    self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[7]/div/span/a[1]').text == '编辑',
                    '编辑操作显示错误')
                self.assertTrue(
                    self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-2-0"]/td[7]/div/span/a[2]').text == '删除',
                    '删除操作显示错误')

            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_04(self):
        """用户列表界面——操作选择框与全选框"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            if self.b.isElementExist('xpath',
                                     '//*[@id="datagrid-row-r1-1-0"]/td[4]/div') == False:  # 判断列表内是否有用户，如果没有就创建用户
                self.b.by_find_element('class', 'l-btn-text').click()
                self.b.by_find_element('name', 'account').send_keys('admin1')
                self.b.by_find_element('name', 'password').send_keys('123456')
                self.b.by_find_element('name', 'username').send_keys('测试用户')
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()  # 点击保存

            # 点击第一条数据的选择框
            self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-1-0"]/td[2]/div/input').click()
            # 断言第一条数据是否被选中
            self.assertTrue(
                self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-1-0"]/td[2]/div/input').is_selected(),
                '勾选框未选中')
            self.addimg()
            time.sleep(1)

            # 取消第一条数据的选择
            self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-1-0"]/td[2]/div/input').click()
            # 断言第一条数据是否被取消选中
            self.assertFalse(
                self.b.by_find_element('xpath', '//*[@id="datagrid-row-r1-1-0"]/td[2]/div/input').is_selected(),
                '勾选框未取消')
            self.addimg()
            time.sleep(1)

            # 点击全选框
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/input').click()

            # 断言全选框是否被选中
            self.assertTrue(self.b.by_find_element('xpath',
                                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/input').is_selected()
                            , '全选框未选中')
            self.addimg()
            time.sleep(1)
            # 取消全选框选择
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/input').click()

            # 断言全选框是否被取消选中
            self.assertFalse(self.b.by_find_element('xpath',
                                                    '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/input').is_selected()
                             , '全选框未取消')
            self.addimg()
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_05(self):
        """用户列表界面——每页显示10条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 分页下拉框选择10条/页
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('10')
            self.addimg()
            List = []
            # 循环整个用户列表，添加进集合，计算本页有多少条数据
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 10, '超出10条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_06(self):
        """用户列表界面——每页显示20条数据"""
        # 选择10条数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('20')
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 20, '超出20条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_07(self):
        """用户列表界面——每页显示50条数据"""
        # 选择10条数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('50')
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 50, '超出50条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_08(self):
        """用户列表界面——每页显示100条数据"""
        # 选择10条数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('100')
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 100, '超出100条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_09(self):
        """用户列表界面——首页图标点击"""
        # 点击首页图标，需要回到第一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            if self.b.isElementExist('xpath',
                                     '//*[@id="datagrid-row-r1-1-0"]/td[4]/div') == False:  # 判断列表内是否有用户，如果没有就创建用户
                self.b.by_find_element('class', 'l-btn-text').click()
                self.b.by_find_element('name', 'account').send_keys('admin1')
                self.b.by_find_element('name', 'password').send_keys('123456')
                self.b.by_find_element('name', 'username').send_keys('测试用户')
                self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()  # 点击保存
            # 点击首页图标
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[3]/a/span/span[2]').click()
            self.addimg()
            # 断言跳转框内数字是否为1
            self.assertTrue(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '1',
                            '回到首页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_010(self):
        """用户列表界面——尾页图标点击"""
        # 点击尾页图标，需要前往最后一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[11]/a/span/span[2]').click()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.addimg()
            self.assertTrue(len(List) <= 10, '前往尾页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_011(self):
        """用户列表界面——下一页图标点击图标点击"""
        # 点击下一页图标，需要回到下一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取页码输入框的数据
            sum1 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[10]/a/span/span[2]').click()
            self.addimg()
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            if sum2 == sum1:
                self.assertTrue(sum1 == sum2, '点击下一页失败')
            else:
                self.assertTrue(int(sum2) == int(sum1) + 1, '点击下一页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_012(self):
        """用户列表界面——上一页图标点击图标点击"""
        # 点击上一页图标，需要回到上一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取页码输入框的数据
            sum1 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[4]/a/span/span[2]').click()
            self.addimg()
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            if sum2 == sum1:
                self.assertTrue(sum1 == sum2, '点击上一页失败')
            else:
                self.assertTrue(int(sum2) == int(sum1 - 1), '点击上一页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_013(self):
        """用户列表界面——用户列表无数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            if len(List) == 0:
                self.assertTrue(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '0',
                                '用户列表无数据，当前页数显示错误')
                self.assertEqual(self.b.by_find_element('xpath',
                                                        '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[8]/span').text,
                                 '共0页', '用户列表无数据，总页数显示错误')
            else:
                raise AssertionError('用户列表数据不为空，用例无法执行')
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_014(self):
        """用户列表界面——用户列表总数据<每页数据，但列表数据！=0"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            if len(List) <= int(sum1) and len(List) != 0:
                self.assertTrue(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '1',
                                '页码显示错误')
                self.assertEqual(self.b.by_find_element('xpath',
                                                        '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[8]/span').text,
                                 '共1页', '总页数显示错误')
            else:
                raise AssertionError('列表无数据或总数据大于每页数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_015(self):
        """用户列表界面——用户列表总数据>每页数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[
                0].text  # 获取每页数据量
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[11]/a/span/span[2]').click()  # 点击尾页
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):  # 获取最后一页数据
                List.append(l)
            sum2 = int(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value'))  # 获取页码，
            count = (sum2 - 1) * int(sum1) + int(len(List))  # 计算总数据
            logger.info(sum2)
            if count > int(sum1):
                self.assertTrue(
                    self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '%s' % sum2,
                    '当前页数显示错误')
                self.assertEqual(self.b.by_find_element('xpath',
                                                        '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[8]/span').text,
                                 '共%s页' % sum2, '总页数显示错误')
            else:
                raise AssertionError('列表无数据或总数据小于每页数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_016(self):
        """用户列表界面——点击新增用户界面"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            self.addimg()
            self.assertEqual('新增用户', self.b.by_find_element('css', '.layui-layer-title').text, '新增用户界面错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_017(self):
        """用户列表界面——新增用户界面（帐号输入框长度限制测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 账号框输入21个字符
            self.b.by_find_element('name', 'account').send_keys('adminadminadminadmin1')
            self.addimg()
            account = self.b.by_find_element('name', 'account').get_attribute('value')
            # 断言账号是否超出20个字符的长度
            self.assertTrue(len(account) == 20, '长度超出20字符限制')

            # 清空输入框
            self.b.by_find_element('name', 'account').clear()
            # 账号框输入1个字符
            self.b.by_find_element('name', 'account').send_keys('addd')
            self.b.by_find_element('name', 'account').click()
            self.addimg()
            account = self.b.by_find_element('css', '.tooltip-content').text
            # 断言账号是否超出20个字符的长度
            self.assertTrue(account == '输入内容长度必须介于5和20之间', '长度低于2字符限制无提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_018(self):
        """用户列表界面——新增用户界面（帐号输入框输入限制测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 账号框输入中文字符
            self.b.by_find_element('name', 'account').send_keys('中文')
            self.b.by_find_element('name', 'account').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '无效帐号名：请输入英文字母数字以及下划线组合，不包含空格等特殊字符，且第一个字符为英文字母',
                             '输入字符为中文，无提示')
            self.b.by_find_element('name', 'account').clear()
            # 账号框输入特殊字符
            self.b.by_find_element('name', 'account').send_keys('admin%')
            self.b.by_find_element('name', 'account').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '无效帐号名：请输入英文字母数字以及下划线组合，不包含空格等特殊字符，且第一个字符为英文字母',
                             '输入字符包含特殊字符，无提示')
            self.b.by_find_element('name', 'account').clear()
            # 账号框输入空格字符
            self.b.by_find_element('name', 'account').send_keys('admi  n')
            self.b.by_find_element('name', 'account').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '无效帐号名：请输入英文字母数字以及下划线组合，不包含空格等特殊字符，且第一个字符为英文字母',
                             '输入包含空格，无提示')
            self.b.by_find_element('name', 'account').clear()
            # 账号框输入首位为数字
            self.b.by_find_element('name', 'account').send_keys('1admin')
            self.b.by_find_element('name', 'account').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '无效帐号名：请输入英文字母数字以及下划线组合，不包含空格等特殊字符，且第一个字符为英文字母',
                             '首位为数字，无提示')
            self.b.by_find_element('name', 'account').clear()
            # 账号框输入首位为下划线
            self.b.by_find_element('name', 'account').send_keys('_admin123')
            self.b.by_find_element('name', 'account').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '无效帐号名：请输入英文字母数字以及下划线组合，不包含空格等特殊字符，且第一个字符为英文字母',
                             '首位为下划线，无提示')
            self.b.by_find_element('name', 'account').clear()
            # 账号框输入正确账号
            self.b.by_find_element('name', 'account').send_keys('admin2')
            self.b.by_find_element('name', 'account').click()
            self.addimg()
            self.assertFalse(self.b.isElementExist('css', '.tooltip-content'),
                             '正确格式账号，提示错误')
            self.b.by_find_element('name', 'account').clear()
            # 点击输入框，提示该输入项为必输项
            self.b.by_find_element('name', 'account').click()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '该输入项为必输项',
                             '输入不能为空')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_019(self):
        """用户列表界面——新增用户界面（帐号输入同名测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 新建已存在的用户
            self.b.by_find_element('name', 'account').send_keys('admin')
            self.b.by_find_element('name', 'password').send_keys('123456')
            self.b.by_find_element('name', 'username').send_keys('测试用户')
            self.b.by_find_element('xpath', '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()  # 点击保存
            # 账号框输入特殊字符
            self.assertEqual(self.b.by_find_element('css', '.layui-layer-padding').text, '该帐号已存在！', '账号同名')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_020(self):
        """用户列表界面——新增用户界面（密码输入框长度限制测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 账号框输入21个字符
            self.b.by_find_element('name', 'password').send_keys('adminadminadminadmin1')
            self.addimg()
            account = self.b.by_find_element('name', 'password').get_attribute('value')
            logger.info(account)
            # 断言账号是否超出20个字符的长度
            self.assertTrue(len(account) == 20, '长度超出20字符限制')

            # 清空输入框
            self.b.by_find_element('name', 'password').clear()
            # 账号框输入1个字符
            self.b.by_find_element('name', 'password').send_keys('1')
            self.b.by_find_element('name', 'password').click()
            self.addimg()
            account = self.b.by_find_element('css', '.tooltip-content').text
            # 断言账号是否超出20个字符的长度
            self.assertTrue(account == '输入内容长度必须介于2和20之间', '长度低于2字符限制无提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_021(self):
        """用户列表界面——新增用户界面（密码输入框输入限制测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 账号框输入特殊字符
            self.b.by_find_element('name', 'password').send_keys('admin%')
            self.b.by_find_element('name', 'password').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '无效密码：请输入英文字母、数字或其组合，且不包含空格等特殊字符',
                             '输入字符包含特殊字符，无提示')
            self.b.by_find_element('name', 'password').clear()
            # 账号框输入空格字符
            self.b.by_find_element('name', 'password').send_keys('admi  n')
            self.b.by_find_element('name', 'password').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '无效密码：请输入英文字母数字组合，且不包含空格等特殊字符',
                             '输入包含空格，无提示')
            # 点击输入框，提示该输入项为必输项
            self.b.by_find_element('name', 'password').click()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '该输入项为必输项',
                             '输入为空，无提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_022(self):
        """用户列表界面——新增用户界面（姓名输入框长度限制测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 账号框输入21个字符
            self.b.by_find_element('name', 'username').send_keys('测试测试测试测试测试测试测试测试测试测试1')
            self.addimg()
            account = self.b.by_find_element('name', 'username').get_attribute('value')
            logger.info(account)
            # 断言账号是否超出20个字符的长度
            self.assertTrue(len(account) == 20, '长度超出20字符限制')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_023(self):
        """用户列表界面——新增用户界面（姓名输入框输入限制测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 点击输入框，提示该输入项为必输项
            self.b.by_find_element('name', 'username').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '该输入项为必输项',
                             '输入不能为空')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_024(self):
        """用户列表界面——新增用户界面（用户类型）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 获取用户类型数据
            radios = []
            radio1 = self.b.by_find_element('css',
                                            'form.add_meeting:nth-child(1) > div:nth-child(2) > div:nth-child(7) > div:nth-child(2) > span:nth-child(1)').text
            radios.append(radio1)
            radio2 = self.b.by_find_element('css',
                                            'form.add_meeting:nth-child(1) > div:nth-child(2) > div:nth-child(7) > div:nth-child(2) > span:nth-child(2)').text
            radios.append(radio2)
            radio3 = self.b.by_find_element('css',
                                            'form.add_meeting:nth-child(1) > div:nth-child(2) > div:nth-child(7) > div:nth-child(2) > span:nth-child(2)').text
            radios.append(radio3)
            # 获取后勤人员
            check = self.b.by_find_element('css',
                                           'form.add_meeting:nth-child(1) > div:nth-child(2) > div:nth-child(8) > div:nth-child(2) > span:nth-child(1)').text
            radios.append(check)
            logger.info(radios)
            self.addimg()
            self.assertTrue('管理员' and '秘书' and '普通用户' and '  z后勤人员' in radios, '用户类型错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_025(self):
        """用户列表界面——新增用户界面（清空欢迎词输入框测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 清空欢迎词输入框
            self.b.by_find_element('name', 'salutatory').clear()
            self.addimg()
            self.assertEqual(self.b.by_find_element('name', 'salutatory').get_attribute('placeholder'), '请输入欢迎词',
                             '默认提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_026(self):
        """用户列表界面——新增用户界面（清空欢迎词输入框测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 清空欢迎词输入框
            self.b.by_find_element('name', 'salutatory').clear()
            # 欢迎词输入框随机生成200个字符
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            val = f'{head:x}{body:x}'
            for i in range(202):
                str = bytes.fromhex(val).decode('gb2312')
                self.b.by_find_element('name', 'salutatory').send_keys(str)
            self.addimg()
            # 获取textear 标签的值，使用get_attribute('value')
            self.assertTrue(len(self.b.by_find_element('name', 'salutatory').get_attribute('value')) == 200, '字符超出限制')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_027(self):
        """用户列表界面——新增用户界面（重置按钮测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 输入用户名密码等数据
            self.b.by_find_element('name', 'account').send_keys('admin')
            self.b.by_find_element('name', 'password').send_keys('123456')
            self.b.by_find_element('name', 'username').send_keys('测试用户')
            self.b.by_find_element('name', 'salutatory').send_keys('123')
            # 点击重置按钮
            self.b.by_find_element('css',
                                   'form.add_meeting:nth-child(1) > div:nth-child(3) > button:nth-child(2)').click()
            # 断言各个输入框的值是否回到初始值
            self.assertTrue(self.b.by_find_element('name', 'account').text == '', '账号未重置成功')
            self.assertTrue(self.b.by_find_element('name', 'password').text == '', '密码未重置成功')
            self.assertTrue(self.b.by_find_element('name', 'username').text == '', '姓名未重置成功')
            self.assertTrue(Select(self.b.by_find_element('xpath',
                                                          '/html/body/div[1]/div/div[4]/div/div[2]/form/div[1]/div[4]/div/select')).
                            all_selected_options[0].text == '全部', '单位未重置成功')
            self.assertTrue(Select(self.b.by_find_element('xpath',
                                                          '/html/body/div[1]/div/div[4]/div/div[2]/form/div[1]/div[5]/div/select')).
                            all_selected_options[0].text == '全部', '部门未重置成功')
            self.assertTrue(Select(self.b.by_find_element('xpath',
                                                          '/html/body/div[1]/div/div[4]/div/div[2]/form/div[1]/div[6]/div/select')).
                            all_selected_options[0].text == '全部', '职位未重置成功')
            self.assertTrue(self.b.by_find_element('css',
                                                   'form.add_meeting:nth-child(1) > div:nth-child(2) > '
                                                   'div:nth-child(7) > div:nth-child(2) > span:nth-child(3) > input:nth-child(1)').is_selected(),
                            '用户类型未重置成功')
            self.assertTrue(self.b.by_find_element('css',
                                                   'form.add_meeting:nth-child(1) > div:nth-child(2) > div:nth-child(8) > '
                                                   'div:nth-child(2) > span:nth-child(1) > input:nth-child(1)').is_selected(),
                            '后勤人员未重置成功')
            self.assertTrue(self.b.by_find_element('name', 'salutatory').text == '欢迎您！', '后勤人员未重置成功')
            self.addimg()
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_028(self):
        """用户列表界面——新增用户界面（新增测试：账号为空，其他不为空）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 输入用户名密码等数据
            self.b.by_find_element('name', 'account').send_keys('')
            self.b.by_find_element('name', 'password').send_keys('123456')
            self.b.by_find_element('name', 'username').send_keys('测试用户')
            self.b.by_find_element('name', 'salutatory').send_keys('123')
            self.b.by_find_element('css','form.add_meeting:nth-child(1) > div:nth-child(3) > button:nth-child(1)').click()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '该输入项为必输项',
                             '账号输入为空，无提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_029(self):
        """用户列表界面——新增用户界面（新增测试：密码为空，其他不为空）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 输入用户名密码等数据
            self.b.by_find_element('name', 'account').send_keys('admin')
            self.b.by_find_element('name', 'password').send_keys('')
            self.b.by_find_element('name', 'username').send_keys('测试用户')
            self.b.by_find_element('name', 'salutatory').send_keys('123')
            self.b.by_find_element('css','form.add_meeting:nth-child(1) > div:nth-child(3) > button:nth-child(1)').click()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '该输入项为必输项',
                             '账号输入为空，无提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_030(self):
        """用户列表界面——新增用户界面（新增测试：姓名为空，其他不为空）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 输入用户名密码等数据
            self.b.by_find_element('name', 'account').send_keys('admin')
            self.b.by_find_element('name', 'password').send_keys('123456')
            self.b.by_find_element('name', 'username').send_keys('测试用户')
            self.b.by_find_element('name', 'salutatory').send_keys('123')
            # 点击确定
            self.b.by_find_element('css','form.add_meeting:nth-child(1) > div:nth-child(3) > button:nth-child(1)').click()
            self.assertEqual(self.b.by_find_element('css', '.tooltip-content').text, '该输入项为必输项',
                             '账号输入为空，无提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_yhlb_at_031(self):
        """用户列表界面——新增用户界面（新增测试：输入全部正确）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增用户按钮
            self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
            # 输入正确用户名密码等数据
            self.b.by_find_element('name', 'account').send_keys('admin22')
            self.b.by_find_element('name', 'password').send_keys('123456')
            self.b.by_find_element('name', 'username').send_keys('测试用户')
            self.b.by_find_element('name', 'salutatory').send_keys('123')
            account = self.b.by_find_element('name', 'account').get_attribute('value')
            self.b.by_find_element('css','form.add_meeting:nth-child(1) > div:nth-child(3) > button:nth-child(1)').click()
            self.addimg()
            if self.b.by_find_element('css', '.layui-layer-padding').text == '该帐号已存在！':
                self.assertEqual(self.b.by_find_element('css', '.layui-layer-padding').text, '该帐号已存在！', '账号同名，提示错误')
            else:
                self.b.by_find_element('xpath',
                                       '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[11]/a/span/span[2]').click() #点击尾页图标
                if self.b.isElementExist('xpath',
                                     '//*[@id="datagrid-row-r1-1-0"]/td[4]/div'):  # 判断是否完成了跳转到尾页
                    self.addimg()
                    List = []
                    for l in self.b.by_find_elements('css', '.datagrid-cell-c1-account'):  # 获取最后一页账号数据
                        List.append(l.text)
                    # 断言输入的数据是否在List里
                    self.assertTrue(account in List,'用户新建失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhlb_at_032(self):
        """用户列表界面——顶部删除功能测试：单个用户删除"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            if self.b.isElementExist('xpath',
                                     '//*[@id="datagrid-row-r1-1-0"]/td[4]/div') == False:  # 判断列表内是否有用户，如果没有就创建用户
                # 输入正确用户名密码等数据
                self.b.by_find_element('name', 'account').send_keys('admin22')
                self.b.by_find_element('name', 'password').send_keys('123456')
                self.b.by_find_element('name', 'username').send_keys('测试用户')
                self.b.by_find_element('name', 'salutatory').send_keys('123')
                self.b.by_find_element('css',
                                       'form.add_meeting:nth-child(1) > div:nth-child(3) > button:nth-child(1)').click()

            # 获取第一条数据的账号信息
            account1 = self.b.by_find_element('css','#datagrid-row-r1-2-0 > td:nth-child(1) > div > span').text
            # 点击第一条数据的选择框
            self.b.by_find_element('xpath','//*[@id="datagrid-row-r1-1-0"]/td[2]/div/input').click()
            self.addimg()
            # 点击顶部删除按钮
            self.b.by_find_element('xpath','//*[@id="common_operate"]/a[4]/span/span[1]').click()
            # 点击确定
            self.b.by_find_element('css','.layui-layer-btn0').click()
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-c1-account'):  # 获取最后一页数据
                List.append(l.text)
            self.assertTrue(account1 in List,'删除失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise
    # 逻辑较为复杂
    # def test_yhlb_at_016(self):
    #     """用户列表界面——关键词搜索"""
    #     try:
    #         logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
    #         if self.b.isElementExist('xpath','//*[@id="datagrid-row-r1-1-0"]/td[4]/div')==False:  # 判断列表内是否有用户，如果没有就创建用户
    #             # 新增10条用户数据
    #             for i in range(1, 20):
    #                 if i % 2:
    #                     self.b.by_find_element('class', 'l-btn-text').click()
    #                     self.b.by_find_element('name', 'account').send_keys('admin%s' % i)
    #                     self.b.by_find_element('name', 'password').send_keys('123456')
    #                     self.b.by_find_element('name', 'username').send_keys('测试用户')
    #                     self.b.by_find_element('xpath',
    #                                            '//*[@id="layui-layer%s"]/div[2]/form/div[2]/button[1]' % i).click()
    #                     time.sleep(1)
    #                 else:
    #                     continue
    #
    #         # 关键词搜索框输入ad
    #         self.b.by_find_element('css','#user-keyword').send_keys('ad')
    #         self.b.by_find_element('css','.sprite-sou').click()
    #         # 获取搜索后的列表框的账号
    #         List = []
    #         for ac in self.b.by_find_elements('css','.datagrid-cell-c1-account'):
    #             List.append(ac.text)
    #         List.remove('帐号')
    #         # 获取搜索后的姓名集合
    #         for u in self.b.by_find_elements('css','.datagrid-cell-c1-username'):
    #             List.append(u.text)
    #         List.remove('姓名')
    #         # 获取搜索后的单位集合
    #         for a in self.b.by_find_elements('css','.datagrid-cell-c1-o_id_a_name'):
    #             List.append(a.text)
    #         List.remove('单位')
    #         # 获取搜索后的部门集合
    #         for b in self.b.by_find_elements('css','.datagrid-cell-c1-o_id_b_name'):
    #             List.append(b.text)
    #         List.remove('部门')
    #         # 获取搜索后的职务集合
    #         for c in self.b.by_find_elements('css','.datagrid-cell-c1-o_id_c_name'):
    #             List.append(c.text)
    #         List.remove('职务')
    #         for i in List:
    #             logger.info(i)
    #             self.assertTrue('ad' in List,'帐号搜索错误')
    #         logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
    #     except:
    #         logger.info('用例%s执行失败' % sys._getframe().f_code.co_name)
    #         raise

    def test_xinzengshuju(self):
        """新增数据"""
        for i in range(1, 30):
            if i % 2:
                self.b.by_find_element('class', 'l-btn-text').click()
                self.b.by_find_element('name', 'account').send_keys('admin%s' % i)
                self.b.by_find_element('name', 'password').send_keys('123456')
                self.b.by_find_element('name', 'username').send_keys('测试用户')
                self.b.by_find_element('xpath', '//*[@id="layui-layer%s"]/div[2]/form/div[2]/button[1]' % i).click()
                time.sleep(1)
            else:
                continue


if __name__ == '__main__':
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(Test_UserList)
    suit = unittest.TestSuite()
    # suit.addTest(suit1)
    suit.addTest(Test_UserList('test_yhlb_at_032'))
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb"),
                           verbosity=2,
                           )
    runer.run(suit)
