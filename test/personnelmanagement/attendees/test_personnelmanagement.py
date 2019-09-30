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
import os,re
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
        # 先前往用户列表判断是否用用户
        self.b.by_find_element('link_text', '用户列表').click()
        if self.b.isElementExist('xpath','//*[@id="datagrid-row-r1-1-0"]/td[4]/div') == False:  # 判断列表内是否有用户，如果没有就创建用户
            # 创建10个用户
            for i in range(1, 20):
                if i % 2:
                    self.b.by_find_element('class', 'l-btn-text').click()
                    self.b.by_find_element('name', 'account').send_keys('admin%s' % i)
                    self.b.by_find_element('name', 'password').send_keys('123456')
                    self.b.by_find_element('name', 'username').send_keys('测试用户')
                    self.b.by_find_element('xpath',
                                            '//*[@id="layui-layer%s"]/div[2]/form/div[2]/button[1]' % i).click()
                    time.sleep(1)
                else:
                    continue
        # 获取共x记录
        self.usercount = self.b.by_find_element('css', '.pagination-info').text
        self.usercount =  re.findall('\d+\.?\d*',self.usercount)[2]
        # 再进入会议列表
        self.b.by_find_element('link_text', '会议列表').click()
        # 获取总页数
        self.page = self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[8]/span').text
        self.page = self.page[1:-1]
        List = []
        if self.page == '0' or self.page == '1':
            for i in self.b.by_find_elements('css', '.datagrid-cell-c1-name'):
                List.append(i.text)
        else:
            for p in range(int(self.page)-1):
                for i in self.b.by_find_elements('css', '.datagrid-cell-c1-name'):
                    List.append(i.text)
                self.b.by_find_element('css', '.pagination-next').click()
                time.sleep(1)
        # 每次执行用例都判断会议列表中是否有数据
        if '测试参会人员' not in List:
            # 点击新增会议
            self.b.by_find_element('link_text', '新增会议').click()
            # 会议名称
            self.b.by_find_element('name', 'name').send_keys('测试参会人员')
            # 点击开始时间
            self.b.by_find_element('css', '#add_meeting > div > div:nth-child(2) > div.Participants_fr.fl > '
                                          'span:nth-child(2) > input.textbox-text.validatebox-text').click()
            # 点击结束时间
            self.b.by_find_element('css', '#add_meeting > div > div:nth-child(2) > div.Participants_fr.fl > '
                                          'span:nth-child(5) > input.textbox-text.validatebox-text').click()
            # 点击增加时间
            self.b.by_find_element('css', 'body > div:nth-child(26) > div > div:nth-child(2) > span > '
                                          'span > a > a.spinner-arrow-up').click()
            # 点击确定
            self.b.by_find_element('css', 'body > div:nth-child(26) > div > div.datebox-button > table > '
                                          'tbody > tr > td:nth-child(2) > a').click()
            # 点击新增确定
            self.b.by_find_element('css', '#add_meeting > div > div:nth-child(7) > div:nth-child(1) > button').click()
            time.sleep(1)
        else:
            self.b.by_find_element('link_text', '测试参会人员').click()
            time.sleep(2)

    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()

    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    def test_chry_at_01(self):
        """参会人员界面——标题显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言关键词搜索框是否存在
            self.assertEqual('参会人员', self.b.by_find_element('css', '.personnel.fl').text, '标题显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_02(self):
        """参会人员界面——参会人员顶部栏显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言关键词搜索框是否存在
            self.assertTrue(self.b.isElementExist('css', '#user-keyword'), '搜索框不存在错误')
            # 断言'按人员权重排列'功能是否存在
            self.assertEqual('按人员权重排列', self.b.by_find_element('css', '.batch-sort').text, '按人员权重排列不存在或显示错误')
            # 断言'选择参会人员'功能是否存在
            self.assertEqual('选择参会人', self.b.by_find_element('css', '.nav_one.n_1.fl.clear').text, '选择参会人员不存在或显示错误')
            # 断言'导出参会人员'功能是否存在
            self.assertEqual('导出参会人', self.b.by_find_element('css', '.nav_one.n_4.fl.batch-export').text, '导出参会人员不存在或显示错误')
            # 断言'删除'功能是否存在
            self.assertEqual('删除', self.b.by_find_element('css', '.nav_one.n_5.fl.batch-delete').text, '删除不存在或显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_03(self):
        """参会人员界面——参会人员字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言选择框是否存在
            self.assertTrue(self.b.isElementExist('css', '#chkall'), '选择框不存在')
            # 断言序号是否存在
            self.assertEqual('序号', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[2]/div/span[1]').text, '序号不存在或显示错误')
            # 断言名称是否存在
            self.assertEqual('名称', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[3]/div/span[1]').text, '名称不存在或显示错误')
            # 断言单位是否存在
            self.assertEqual('单位', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[4]/div/span[1]').text, '单位不存在或显示错误')
            # 断言职务是否存在
            self.assertEqual('职务', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[5]/div/span[1]').text, '职务不存在或显示错误')
            # 断言座位是否存在
            self.assertEqual('座位', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[6]/div/span[1]').text, '座位不存在或显示错误')
            # 断言终端是否存在
            self.assertEqual('终端', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[7]/div/span[1]').text, '终端不存在或显示错误')
            # 断言角色权限是否存在
            self.assertEqual('角色权限', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                     'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                     'table/tbody/tr/td[8]/div/span[1]').text, '角色权限不存在或显示错误')
            # 断言免密是否存在
            self.assertEqual('免密', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[9]/div/span[1]').text, '免密不存在或显示错误')
            # 断言广播是否存在
            self.assertEqual('广播', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[10]/div/span[1]').text, '广播不存在或显示错误')
            # 断言操作是否存在
            self.assertEqual('操作', self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                                                   'div/div/div/div[2]/div[2]/div[1]/div/'
                                                                   'table/tbody/tr/td[11]/div/span[1]').text, '操作不存在或显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_04(self):
        """参会人员界面——新增参会人员字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            self.addimg()
            # 断言选择框是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[1]/div/input'), '选择框不存在')
            # 断言序号是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[2]/div/span'),
                            '序号不存在或显示错误')
            # 断言名称是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[3]/div/span'),
                            '名称不存在或显示错误')
            # 断言单位是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[4]/div/span'),
                            '单位不存在或显示错误')
            # 断言职务是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[5]/div/span'),
                            '职务不存在或显示错误')
            # 断言座位是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[6]/div/span'),
                            '座位不存在或显示错误')
            # 断言终端是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[7]/div/span'),
                            '终端不存在或显示错误')
            # 断言角色权限'主持'是否存在
            self.assertEqual('主持', self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/'
                                                                   'td[8]/div/div/span[1]').text, '角色权限(主持)不存在或显示错误')
            # 断言角色权限'秘书'是否存在
            self.assertEqual('秘书', self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/'
                                                                   'td[8]/div/div/span[2]').text, '角色权限(秘书)不存在或显示错误')
            # 断言广播是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[10]/div/div/input'),
                            '广播不存在或显示错误')
            # 断言操作'编辑'是否存在
            self.assertEqual('编辑', self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/'
                                                                   'td[11]/div/div/span[1]').text, '操作(编辑)不存在或显示错误')
            # 断言操作'删除'是否存在
            self.assertEqual('删除', self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/'
                                                                   'td[11]/div/div/span[2]').text, '操作(删除)不存在或显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_05(self):
        """参会人员界面——操作选择框与全选框"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 点击第一条数据的选择框
            self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[1]/div/input').click()
            # 断言第一条数据是否被选中
            self.assertTrue(
                self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[1]/div/input').is_selected(),
                '勾选框未选中')
            self.addimg()
            time.sleep(1)

            # 取消第一条数据的选择
            self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[1]/div/input').click()
            # 断言第一条数据是否被取消选中
            self.assertFalse(
                self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[1]/div/input').is_selected(),
                '勾选框未取消')
            self.addimg()
            time.sleep(1)

            # 点击全选框
            self.b.by_find_element('css', '#chkall').click()

            # 断言全选框是否被选中
            self.assertTrue(self.b.by_find_element('css', '#chkall').is_selected(), '全选框未选中')
            self.addimg()
            time.sleep(1)
            # 取消全选框选择
            self.b.by_find_element('css', '#chkall').click()

            # 断言全选框是否被取消选中
            self.assertFalse(self.b.by_find_element('css', '#chkall').is_selected(), '全选框未取消')
            self.addimg()

            # 点击全选框，取消数据选择框，全选框被取消选中
            self.b.by_find_element('css', '#chkall').click()
            # 点击数据选择框
            self.b.by_find_element('xpath', '//*[@id="datagrid-row-r2-2-0"]/td[1]/div/input').click()
            time.sleep(1)
            # 断言全选框是否被取消选中
            self.assertFalse(self.b.by_find_element('css', '#chkall').is_selected(), '全选框未取消')
            self.addimg()
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_06(self):
        """参会人员界面——每页显示10条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 分页下拉框选择10条/页
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('10')
            self.addimg()
            List = []
            # 循环整个参会人员，添加进集合，计算本页有多少条数据
            for l in self.b.by_find_elements('css', '.getSortData-js'):
                List.append(l)
            self.assertTrue(len(List) <= 10, '超出10条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_07(self):
        """参会人员界面——每页显示20条数据"""
        # 选择10条数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('20')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.getSortData-js'):
                List.append(l)
            self.assertTrue(len(List) <= 20, '超出20条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_08(self):
        """参会人员界面——每页显示50条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('50')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.getSortData-js'):
                List.append(l)
            self.assertTrue(len(List) <= 50, '超出50条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_09(self):
        """参会人员界面——每页显示100条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('100')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.getSortData-js'):
                List.append(l)
            self.assertTrue(len(List) <= 100, '超出100条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_010(self):
        """参会人员界面——首页图标点击"""
        # 点击首页图标，需要回到第一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 点击首页图标
            self.b.by_find_element('css', '.pagination-first').click()
            time.sleep(1)
            self.addimg()
            # 断言跳转框内数字是否为1
            self.assertTrue(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '1',
                            '回到首页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_011(self):
        """参会人员界面——尾页图标点击"""
        # 点击尾页图标，需要前往最后一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.b.by_find_element('css', '.pagination-last').click()
            time.sleep(1)
            self.addimg()
            # 获取总页数
            count = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear > div > div.table '
                                           '> div > div > div > div.datagrid-pager.pagination > table > tbody > '
                                           'tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            count = count[1:-1]
            # 获取跳转框内的数字
            sum1 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            # # 断言共X页是否等于跳转框内的数字
            self.assertTrue(count == sum1, '前往尾页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_012(self):
        """参会人员界面——下一页图标点击"""
        # 点击下一页图标，需要回到下一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取页码输入框的数据
            sum1 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            # 点击下一页
            self.b.by_find_element('css', '.pagination-next').click()
            time.sleep(1)
            self.addimg()
            # 获取点击下一页后的输入框数据
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            # 获取总页数
            count = self.b.by_find_element('css', '#wrap > div > div.matter.clear > div.right_w.fr.clear > div '
                                                  '> div.table > div > div > div > div.datagrid-pager.pagination > '
                                                  'table > tbody > tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            count = count[1:-1]
            if count == '1' or count == '0':
                self.assertTrue(sum1 == sum2, '点击下一页失败')
            else:
                self.assertTrue(int(sum2) == int(sum1) + 1, '点击下一页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_013(self):
        """参会人员界面——上一页图标点击"""
        # 点击上一页图标，需要回到上一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取页码输入框的数据
            sum1 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            # 点击上一页
            self.b.by_find_element('css', '.pagination-prev').click()
            time.sleep(1)
            self.addimg()
            # 点击上一页后获取输入框的数据
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            if sum1 == '1' or sum1 == '0':
                self.assertTrue(sum1 == sum2, '点击上一页失败')
            else:
                self.assertTrue(int(sum2) == (int(sum1)-1), '点击上一页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_014(self):
        """参会人员界面——页数搜索（页数框输入小于1的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 页数框输入0
            self.b.by_find_element('css','.pagination-num').send_keys(0)
            self.addimg()
            # 模拟键盘回车
            self.b.by_find_element('css', '.pagination-num ').send_keys(Keys.ENTER)
            self.addimg()
            time.sleep(1)
            # 获取跳转后的输入框值
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            self.assertTrue(sum2 == '1', '跳转至0页，跳转框数字为%s' % sum2)

            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 页数框输入输入负数
            self.b.by_find_element('css','.pagination-num').send_keys(-1)
            self.addimg()
            # 模拟键盘回车
            self.b.by_find_element('css', '.pagination-num ').send_keys(Keys.ENTER)
            self.addimg()
            time.sleep(1)
            # 获取跳转后的输入框值
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            self.assertTrue(sum2 == '1', '跳转至-1页，跳转框数字为%s' % sum2)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_015(self):
        """参会人员界面——页数搜索（页数框输入大于总页数的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 获取总页数
            count = self.b.by_find_element('css', '#wrap > div > div.matter.clear > div.right_w.fr.clear > div '
                                                  '> div.table > div > div > div > div.datagrid-pager.pagination > '
                                                  'table > tbody > tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            count = count[1:-1]
            # 页数框输入总页数+1
            self.b.by_find_element('css','.pagination-num').send_keys(int(count)+1)
            self.addimg()
            # 模拟键盘回车
            self.b.by_find_element('css', '.pagination-num ').send_keys(Keys.ENTER)
            self.addimg()
            time.sleep(1)
            # 获取跳转后的输入框值
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            self.assertTrue(sum2 == count, '跳转至%s页，跳转框数字为%s' % (int(count)+1, sum2))
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_016(self):
        # 正确跳转界面暂时无法编写，数据无法创建过多
        pass

    def test_chry_at_017(self):
        """参会人员界面——总页数显示（查看用户分组页数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('css', '.pagination-last').click()  # 点击尾页
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.getSortData-js'):
                List.append(l)
            # 获取跳转框页码，
            sum2 = int(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value'))
            # 计算总数据：(页码-1)*每页数据条数+最后一页数据
            if sum2 == 0 or sum2 == 1:
                count = int(len(List))
            else:
                count = (sum2 - 1) * int(sum1) + int(len(List))
            # 获取总页数文字
            number = self.b.by_find_element('css', '#wrap > div > div.matter.clear > div.right_w.fr.clear > div '
                                                  '> div.table > div > div > div > div.datagrid-pager.pagination > '
                                                  'table > tbody > tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            numcount = number[1:-1]
            if count == 0:
                self.assertTrue(number == '共0页', '页面无数据，总页数显示共%s页'%numcount)
            elif count > 10:
                # 计算总页数
                pages = (count-int(len(List)))/10+1
                self.assertTrue(int(numcount) == pages, '共%s页,但显示共%s页' % (pages, numcount))
            elif count <= 10:
                self.assertTrue(int(numcount) == 1, '共1页,但显示共%s页' % numcount)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_018(self):
        """参会人员界面——分组条数显示（左下角的分组记录显示）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('css', '.pagination-last').click()  # 点击尾页
            time.sleep(1)
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.getSortData-js'):
                List.append(l)
            # 获取跳转框页码，
            sum2 = int(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value'))
            # 计算总数据：(页码-1)*每页数据条数+最后一页数据
            if sum2 == 0 or sum2 == 1:
                count = int(len(List))
            else:
                count = (sum2 - 1) * int(sum1) + int(len(List))

            # 点击首页图标
            self.b.by_find_element('css', '.pagination-first').click()
            time.sleep(1)
            self.addimg()

            # 获取左下角文字
            records = self.b.by_find_element('css','.pagination-info').text
            # 三种情况断言，页面无数据，页面数据小于每页数据量，页面数据大于每页数据量
            if count == 0:
                self.assertTrue(records == '显示0到0,共0记录', '页面无数据，左下角显示错误')
            elif count > int(sum1):
                self.assertTrue(records == '显示1到%s,共%s记录' % (int(sum1), count), '页面总数据大于10，左下角显示错误，详情请查看截图')
            else:
                self.assertTrue(records == '显示1到%s,共%s记录' % (count, count), '页面总数据小于或等于10，左下角显示错误，详情请查看截图')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_019(self):
        """参会人员界面——选择参会人界面（进入选择参会人界面）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            self.addimg()
            # 断言是否进入新增分组界面
            self.assertEqual('选择参会人', self.b.by_find_element('css', '.layui-layer-title').text, '进入新增分组页面失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_020(self):
        """参会人员界面——选择参会人界面（关键字搜索）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            self.addimg()
            oldList = []
            # 获取所有数据
            for c in self.b.by_find_elements('css', '.user-chose'):
                if c.text:
                    oldList.append(c.text)
                else:
                    # 滚动条滚动至可见的元素位置
                    self.driver.execute_script("arguments[0].scrollIntoView();", c)
                    oldList.append(c.text)
                    time.sleep(1)
            # 关键字搜索
            self.b.by_find_element('css', '#user-auto').send_keys('12')
            self.addimg()
            # 获取关键字搜索框的值
            name = self.b.by_find_element('css', '#user-auto').get_attribute('value')
            print('搜索内容：%s' % name)
            # 将符合搜索内容的值存入集合中
            List = []
            for o in oldList:
                if name in o:
                    List.append(o)
            print('符合搜索内容的数据：%s' % List)
            # 获取所有联系人数据
            newList = []
            # 获取搜索后的所有数据
            for c in self.b.by_find_elements('css', '.user-chose'):
                if c.text:
                    newList.append(c.text)
                else:
                    # 滚动条滚动至可见的元素位置
                    self.driver.execute_script("arguments[0].scrollIntoView();", c)
                    newList.append(c.text)
                    time.sleep(1)
            print('搜索后的数据：%s' % newList)
            # 断言符合搜索内容的值是否等于搜索后的所有数据
            self.assertTrue(List == newList, '符合搜索内容的数据在联系人中显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_021(self):
        """参会人员界面——选择参会人界面（不选择参会人员）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            time.sleep(1)
            # 点击确定
            self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('请选择用户', self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text,
                             '未选择用户，无错误提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_022(self):
        """参会人员界面——选择参会人界面（已选参会人：(增加)）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            time.sleep(1)
            # 获取所有数据
            List = []
            for c in self.b.by_find_elements('css', '.user-chose'):
                if c.text:
                    c.click()
                    List.append(c)
                else:
                    # 滚动条滚动至可见的元素位置
                    self.driver.execute_script("arguments[0].scrollIntoView();", c)
                    c.click()
                    List.append(c)
                    time.sleep(1)
            self.addimg()
            # 获取已选参会人数据
            count = self.b.by_find_element('css', '#user-total').text
            # 断言是否有提示
            self.assertTrue(len(List) == int(count), '参会人数据显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_023(self):
        """参会人员界面——选择参会人界面（已选参会人：(删除)）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取参会人员列表总数据
            count = self.b.by_find_element('css', '.pagination-info').text
            # 切片
            count = count[8:-2]
            # 判断参会人员数据是否大于或等于用户人员数据，大于或等于则删除一页数据
            if count >= self.usercount:
                # 点击全选框
                self.b.by_find_element('css', '#chkall').click()
                time.sleep(1)
                # 点击删除
                self.b.by_find_element('css', '.nav_one.n_5.fl.batch-delete').click()
                time.sleep(1)
                # 点击确定
                self.b.by_find_element('css', '.layui-layer-btn0').click()
                time.sleep(1)
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            time.sleep(1)
            # 鼠标悬浮在'请选择用户'上
            self.b.move_to_element(By.CSS_SELECTOR, '.manage_btn.clear')
            # 全选用户
            self.b.by_find_element('css', '#user-container > div > span > div.sprite_san.fr').click()
            self.addimg()
            # 获取已选参会人数据
            oldcount = self.b.by_find_element('css', '#user-total').text
            # 鼠标悬浮在被选中的第一个参会人上
            self.b.move_to_element(By.CSS_SELECTOR, '#mCSB_2_container > div:nth-child(1)')
            # 点击删除
            self.b.by_find_element('css', '#mCSB_2_container > div:nth-child(1) > i').click()
            self.addimg()
            # 获取删除第一个参会人后的参会人数据
            newcount = self.b.by_find_element('css', '#user-total').text
            self.assertTrue(int(oldcount) - 1 == int(newcount), '删除一个参会人后，参会人数据显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_024(self):
        """参会人员界面——选择单个参会人"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取参会人员列表总数据
            count = self.b.by_find_element('css', '.pagination-info').text
            # 切片
            count = count[8:-2]
            # 判断参会人员数据是否大于或等于用户人员数据，大于或等于则删除一页数据
            if count >= self.usercount:
                # 点击全选框
                self.b.by_find_element('css', '#chkall').click()
                time.sleep(1)
                # 点击删除
                self.b.by_find_element('css', '.nav_one.n_5.fl.batch-delete').click()
                time.sleep(1)
                # 点击确定
                self.b.by_find_element('css', '.layui-layer-btn0').click()
                time.sleep(1)
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            self.addimg()
            time.sleep(1)
            for i in self.b.by_find_elements('css', '.user-chose'):
                if i.text:
                    if i.get_attribute('style') == 'color: rgb(150, 160, 166);':
                        continue
                    else:
                        i.click()
                        break
                else:
                    # 滚动条滚动至可见的元素位置
                    self.driver.execute_script("arguments[0].scrollIntoView();", i)
                    if i.get_attribute('style') == 'color: rgb(150, 160, 166);':
                        continue
                    else:
                        i.click()
                        break
            # 获取选中的参会人的名称
            name = self.b.by_find_element('css', '#mCSB_2_container > div > span.append_1').text
            # 点击确定
            self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
            time.sleep(1)
            # 点击尾页
            self.b.by_find_element('css', '.l-btn-icon.pagination-last').click()
            time.sleep(1)
            # 循环获取参会人员列表的数据
            List = []
            for i in self.b.by_find_elements('css', '.datagrid-cell-c2-username'):
                List.append(i.text)
            self.assertTrue(name in List, '选择的参会人保存后，未显示在参会人员列表中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_025(self):
        """参会人员界面——选择被选中的参会人"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            self.addimg()
            time.sleep(1)
            for i in self.b.by_find_elements('css', '.user-chose'):
                if i.text:
                    if i.get_attribute('style') == 'color: rgb(150, 160, 166);':
                        i.click()
                        break
                    else:
                        continue
                else:
                    # 滚动条滚动至可见的元素位置
                    self.driver.execute_script("arguments[0].scrollIntoView();", i)
                    if i.get_attribute('style') == 'color: rgb(150, 160, 166);':
                        i.click()
                        break
                    else:
                        continue
            # 点击确定
            self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('请选择用户', self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text,
                             '未选择用户，无错误提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_026(self):
        """参会人员界面——选择参会人删除(单选)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 点击第一条数据的选择框
            self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(1) > div > input').click()
            # 获取第一条数据的名称
            name = self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(3) > div > span').text
            # 点击删除
            self.b.by_find_element('css', '.nav_one.n_5.fl.batch-delete').click()
            # 点击确定
            self.b.by_find_element('css', '.layui-layer-btn0').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('删除人员成功', self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text,
                             '删除人员，提示错误')
            time.sleep(1)
            # 循环所有页，获取所有参会人员数据
            # 获取总页数
            page = self.b.by_find_element('xpath',
                                               '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/div/div/div/div[3]/table/tbody/tr/td[8]/span').text
            page = page[1:-1]
            List = []
            for p in range(int(page)):
                for i in self.b.by_find_elements('css', '.datagrid-cell-c2-username'):
                    List.append(i.text)
                self.b.by_find_element('css', '.pagination-next').click()
                time.sleep(1)
                self.addimg()
            self.assertFalse(name in List, '删除后的参会人员任然在参会人员列表中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_027(self):
        """参会人员界面——选择参会人删除(全选)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 获取总页数
            oldpage = self.b.by_find_element('xpath',
                                               '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/div/div/div/div[3]/table/tbody/tr/td[8]/span').text
            oldpage = oldpage[1:-1]
            # 点击全选框
            self.b.by_find_element('css', '#chkall').click()
            # 点击删除
            self.b.by_find_element('css', '.nav_one.n_5.fl.batch-delete').click()
            # 点击确定
            self.b.by_find_element('css', '.layui-layer-btn0').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('删除人员成功', self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text,
                             '删除人员，提示错误')
            time.sleep(1)
            # 循环所有页，获取所有参会人员数据
            # 获取总页数
            newpage = self.b.by_find_element('xpath',
                                               '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/div/div/div/div[3]/table/tbody/tr/td[8]/span').text
            newpage = newpage[1:-1]
            self.assertFalse(int(oldpage)-1 == newpage, '删除一页数据后，总页数未改变')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_chry_at_028(self):
        """参会人员界面——选择参会人删除(不选)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击删除
            self.b.by_find_element('css', '.nav_one.n_5.fl.batch-delete').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('请至少选择一个项!', self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text,
                             '未选择参会人员，提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_029(self):
        """参会人员界面——单条参会人员操作（删除）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 获取第一条数据的名称
            name = self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(3) > div > span').text
            # 点击删除
            self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(11) > div > div > span:nth-child(2)').click()
            # 点击确定
            self.b.by_find_element('css', '.layui-layer-btn0').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('删除人员成功', self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text,
                             '删除人员，提示错误')
            time.sleep(1)
            # 获取总页数
            page = self.b.by_find_element('xpath',
                                               '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/div/div/div/div[3]/table/tbody/tr/td[8]/span').text
            page = page[1:-1]
            List = []
            for p in range(int(page)):
                for i in self.b.by_find_elements('css', '.datagrid-cell-c2-username'):
                    List.append(i.text)
                self.b.by_find_element('css', '.pagination-next').click()
                self.addimg()
                time.sleep(1)
            self.assertFalse(name in List, '删除一个参会人员后，任然显示在参会人员列表中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_030(self):
        """参会人员界面——进入参会人员编辑页面"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 获取第一个参会人员的名称，单位，职务
            name = self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(3) > div > span').text
            unit = self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(4) > div > span').text
            if unit == '-':
                unit = ''
            position = self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(5) > div > span').text
            if position == '-':
                position = ''
            # 点击第一个参会人员的编辑操作
            self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(11) > div > div > span:nth-child(1)').click()
            self.addimg()
            self.assertEqual('编辑参会人', self.b.by_find_element('css', '.layui-layer-title').text, '进入编辑页面失败')
            self.assertEqual(name, self.b.by_find_element('name', 'username').get_attribute('value'), '编辑框姓名信息与参会人姓名不同')
            self.assertEqual(unit, self.b.by_find_element('name', 'unit').get_attribute('value'), '编辑框单位信息与参会人单位不同')
            self.assertEqual(position, self.b.by_find_element('name', 'position').get_attribute('value'), '编辑框职务信息与参会人职务不同')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_031(self):
        """参会人员界面——进入参会人员编辑页面(清空姓名，点击确定)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 点击第一个参会人员的编辑操作
            self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(11) > div > div > span:nth-child(1)').click()
            self.addimg()
            # 清空用户名输入框
            self.b.by_find_element('name', 'username').clear()
            # 点击保存
            self.b.by_find_element('css', '.bottom_y.bottom_b3').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('该输入项为必输入项', self.b.by_find_element('css',
                                                                '.layui-layer.layui-anim.layui-layer-tips.default > div').text, '用户名为空，点击保存，提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_032(self):
        """参会人员界面——进入参会人员编辑页面(不修改数据，点击保存)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 点击第一个参会人员的编辑操作
            self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(11) > div > div > span:nth-child(1)').click()
            self.addimg()
            # 点击保存
            self.b.by_find_element('css', '.bottom_y.bottom_b3').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('暂无数据更新', self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text,
                             '未修改数据，点击保存后，提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_033(self):
        """参会人员界面——进入参会人员编辑页面(正常修改数据)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 点击第一个参会人员的编辑操作
            self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(11) > div > div > span:nth-child(1)').click()
            self.addimg()
            # 修改用户名
            self.b.by_find_element('name', 'username').send_keys('测试修改')
            # 获取用户名的值
            name = self.b.by_find_element('name', 'username').get_attribute('value')
            # 修改单位
            self.b.by_find_element('name', 'unit').send_keys('测试单位')
            # 获取单位的值
            unit = self.b.by_find_element('name', 'unit').get_attribute('value')
            # 修改职务
            self.b.by_find_element('name', 'position').send_keys('测试职务')
            # 获取职务的值
            position = self.b.by_find_element('name', 'position').get_attribute('value')
            # 点击保存
            self.b.by_find_element('css', '.bottom_y.bottom_b3').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('更新用户成功', self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text,
                             '修改数据，点击保存后，提示错误')
            time.sleep(1)
            # 获取第一个参会人员的名称
            name1 = self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(3) > div > span').text
            unit1 = self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(4) > div > span').text
            position1 = self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(5) > div > span').text
            # 断言是否与参会人员列表的数据相等
            self.assertTrue(name == name1, '修改用户名，保存后，参会人员列表用户名未改变')
            self.assertTrue(unit == unit1, '修改单位，保存后，参会人员列表单位未改变')
            self.assertTrue(position == position1, '修改职务，保存后，参会人员列表职务未改变')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_034(self):
        """参会人员界面——进入参会人员编辑页面(重置)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 点击第一个参会人员的编辑操作
            self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(11) > div > div > span:nth-child(1)').click()
            self.addimg()
            # 点击重置
            self.b.by_find_element('css', '.bottom_n.bottom_b3').click()
            self.addimg()
            # 获取用户名的值
            name = self.b.by_find_element('name', 'username').get_attribute('value')
            # 获取单位的值
            unit = self.b.by_find_element('name', 'unit').get_attribute('value')
            # 获取职务的值
            position = self.b.by_find_element('name', 'position').get_attribute('value')
            # 断言是否与参会人员列表的数据相等
            self.assertTrue(name == '' and unit == '' and position == '', '重置后，数据未清空')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_035(self):
        """参会人员界面——无参会人员开启会议"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取总页数
            page = self.b.by_find_element('xpath',
                                          '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                          'div/div/div/div[3]/table/tbody/tr/td[8]/span').text
            page = page[1:-1]
            # 判断是否存在参会人员,false创建
            if page != '0':
                for p in range(int(page)):
                    # 点击全选框
                    self.b.by_find_element('css', '#chkall').click()
                    # 点击删除
                    self.b.by_find_element('css', '.nav_one.n_5.fl.batch-delete').click()
                    # 点击确定
                    self.b.by_find_element('css', '.layui-layer-btn0').click()
                    time.sleep(1.5)
                # 点击开启会议
                self.b.by_find_element('css', '.meeting-start.fr').click()
                # 点击确定
                self.b.by_find_element('css', '.layui-layer-btn0').click()
                self.addimg()
            else:
                self.b.by_find_element('css', '.meeting-start.fr').click()
                self.b.by_find_element('css', '.layui-layer-btn0').click()
                self.addimg()
            self.assertEqual('参会人员为空', self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text,
                             '参会人员为空，提示%s' % self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_chry_at_036(self):
        """参会人员界面——未选择主席开启会议"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            # 获取总页数
            page = self.b.by_find_element('xpath',
                                          '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/'
                                          'div/div/div/div[3]/table/tbody/tr/td[8]/span').text
            page = page[1:-1]
            for p in range(int(page)):
                # 循环所有主席选择框，查看是否被选中
                for i in self.b.by_find_elements('name', 'moderator'):
                    if i.is_selected():
                        i.click()
                self.b.by_find_element('css', '.pagination-next').click()
                time.sleep(1)
                self.addimg()
            self.b.by_find_element('css', '.meeting-start.fr').click()
            self.b.by_find_element('css', '.layui-layer-btn0').click()
            self.addimg()
            self.assertEqual('启动会议异常，未设置主席', self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text,
                             '未设置主席，提示%s' % self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_chry_at_037(self):
        """参会人员界面——选择主席开启会议（已有会议开启）"""
        # try:
        #     logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
        #     logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        # except:
        #     logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
        #     raise
        print('暂时不做测试')
        pass


    def test_chry_at_038(self):
        """参会人员界面——正常开启会议"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在参会人员,false创建
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                # 选择第一个用户
                self.b.by_find_element('css', '.manage_ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
                self.addimg()
            if self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(8) > div > div > span > input').is_selected() == False:
                self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(8) > div > div > span > input').click()
                self.b.by_find_element('css', '.meeting-start.fr').click()
                self.b.by_find_element('css', '.layui-layer-btn0').click()
                self.addimg()
            else:
                self.b.by_find_element('css', '.meeting-start.fr').click()
                self.b.by_find_element('css', '.layui-layer-btn0').click()
                self.addimg()
            self.assertEqual('启用成功', self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text,
                             '启用成功，提示%s' % self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text)
            time.sleep(1)
            self.assertEqual('结束会议', self.b.by_find_element('css', '.meeting-end.fr').text,
                             '提示启用成功后会议未开启')
            self.assertEqual('重置人员', self.b.by_find_element('css', '.meeting-refresh.fr').text,
                             '提示启用成功后会议未开启')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test1(self):
        pass


if __name__ == '__main__':
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(Test_PersonneLmanagement)
    suit = unittest.TestSuite()
    # suit.addTest(suit1)
    # suit.addTest(Test_PersonneLmanagement('test_chry_at_010'))
    # suit.addTest(Test_PersonneLmanagement('test_chry_at_013'))
    suit.addTest(Test_PersonneLmanagement('test_chry_at_038'))
    # suit.addTest(Test_PersonneLmanagement('test_chry_at_09'))
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb"),
                           verbosity=2,
                           )
    runer.run(suit)
