#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: test_usergroup.py
@time: 2019/9/19 17:11
@desc:用户分组测试用例
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


class Test_UserGruop(unittest.TestCase):

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
        self.b.by_find_element('link_text', '用户分组').click()

    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()

    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    '''测试用例'''

    def test_yhfz_at_01(self):
        """用户分组界面——用户分组顶栏显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言顶部栏元素是否存在
            self.assertEqual('新增分组',
                             self.b.by_find_element('css', '#add-win > span > span.l-btn-text').text,'顶部栏，新增分组显示错误')
            self.assertEqual('删除',
                             self.b.by_find_element('css', '#common_operate > a:nth-child(2) > span > span.l-btn-text').text,'顶部栏，删除显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_02(self):
        """用户分组界面——分组列表框字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            time.sleep(1)
            # 断言列表标题栏元素是否存在
            self.assertEqual('分组名称', self.b.by_find_element('xpath',
                                                            '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[3]/div/span[1]').text,
                             '分组名称不存在')
            self.assertEqual('用户数', self.b.by_find_element('xpath',
                                                          '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[1]/div/span[1]').text,
                             '用户数不存在')
            self.assertEqual('操作', self.b.by_find_element('xpath',
                                                          '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr/td[2]/div/span[1]').text,
                             '操作字段不存在')
            self.assertTrue(self.b.isElementExist('xpath',
                                                  '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/input'),
                            '勾选框不存在')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_03(self):
        """用户分组——检查新增分组字段"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在分组，没有则创建一个联系人为管理员的分组
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 截图
                self.addimg()
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 截图
                self.addimg()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
            self.addimg()
            # 如果存在分组，则直接断言元素是否存在

            # 断言第一个分组的编号是否为1
            self.assertTrue(self.b.by_find_element('css', '#datagrid-row-r1-1-0 > td.datagrid-td-rownumber > div').text
                            == '1', '第一个分组的编号错误')
            # 断言第一个分组的分组名称是否存在
            self.assertTrue(self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div')
                            , '第一个分组的分组名称不存在')
            # 断言第一个分组的用户数是否存在
            self.assertTrue(self.b.isElementExist('css', '#datagrid-row-r1-2-0 > td:nth-child(1) > div')
                            , '第一个分组的用户数不存在')
            # 断言第一个分组的两个操作按钮是否存在
            self.assertTrue(
                self.b.by_find_element('css','#datagrid-row-r1-2-0 > td:nth-child(2) > div > a:nth-child(1)').text
                == '编辑', '第一个分组的编辑操作不存在')
            self.assertTrue(
                self.b.by_find_element('css', '#datagrid-row-r1-2-0 > td:nth-child(2) > div > a:nth-child(3)').text
                == '删除', '第一个分组的删除操作不存在')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_04(self):
        """用户分组——全选以及单选框点击和取消"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在分组，没有则创建一个联系人为管理员的分组
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 截图
                self.addimg()
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 截图
                self.addimg()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
            # 点击第一个分组的选择框
            self.b.by_find_element('css', '#datagrid-row-r1-1-0 > td:nth-child(2) > div > input[type=checkbox]').click()
            self.addimg()
            # 断言是否被选中
            self.assertTrue(
                self.b.by_find_element('css',
                                       '#datagrid-row-r1-1-0 > td:nth-child(2) > div > input[type=checkbox]').is_selected(),
                '点击选择框后数据没有被选中')
            # 取消第一个选中框的选择
            self.b.by_find_element('css', '#datagrid-row-r1-1-0 > td:nth-child(2) > div > input[type=checkbox]').click()
            # 点击全选框
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/input').click()
            self.addimg()
            # 断言是否被选中
            for i in self.b.by_find_elements('css', '.datagrid-cell-check > input[type=checkbox ]'):
                self.assertTrue(
                    i.is_selected(),
                    '点击全选框后数据没有被全部选中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_05(self):
        """用户分组界面——每页显示10条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 分页下拉框选择10条/页
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('10')
            self.addimg()
            List = []
            # 循环整个用户分组，添加进集合，计算本页有多少条数据
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 10, '超出10条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_06(self):
        """用户分组界面——每页显示20条数据"""
        # 选择10条数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('20')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 20, '超出20条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_07(self):
        """用户分组界面——每页显示50条数据"""
        # 选择10条数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('50')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 50, '超出50条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise
        
    def test_yhfz_at_08(self):
        """用户分组界面——每页显示100条数据"""
        # 选择10条数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('100')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 100, '超出100条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_09(self):
        """用户分组界面——首页图标点击"""
        # 点击首页图标，需要回到第一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
            # 点击首页图标
            self.b.by_find_element('css', '.pagination-first').click()
            self.addimg()
            # 断言跳转框内数字是否为1
            self.assertTrue(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '1',
                            '回到首页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_010(self):
        """用户分组界面——尾页图标点击"""
        # 点击尾页图标，需要前往最后一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.b.by_find_element('css',  '.pagination-last').click()
            # 获取总页数
            count = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear > div > div.sheet > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span').text
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


    def test_yhfz_at_011(self):
        """用户分组界面——下一页图标点击"""
        # 点击下一页图标，需要回到下一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取页码输入框的数据
            sum1 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            # 点击下一页
            self.b.by_find_element('css', '.pagination-next').click()
            self.addimg()
            # 获取点击下一页后的输入框数据
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            # 获取总页数
            count = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear > div > div.sheet > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span').text
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


    def test_yhfz_at_012(self):
        """用户分组界面——上一页图标点击"""
        # 点击上一页图标，需要回到上一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取页码输入框的数据
            sum1 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            # 点击上一页
            self.b.by_find_element('css', '.pagination-prev').click()
            self.addimg()
            # 点击下一页后获取输入框的数据
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            # 获取总页数
            count = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear > div > div.sheet > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            count = count[1:-1]
            if count == '1' or count == '0':
                self.assertTrue(sum1 == sum2, '点击上一页失败')
            else:
                self.assertTrue(int(sum2) == (int(sum1)-1), '点击上一页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_yhfz_at_013(self):
        """用户分组界面——用户列表无数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 获取用户分组的数据
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)

            # 判断分组是否为空
            if len(List) == 0:
                # 断言跳转框数字为0
                self.assertTrue(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '0',
                                '用户列表无数据，当前页数显示错误')
                # 断言共x页为共0页
                self.assertEqual(self.b.by_find_element('xpath',
                                                        '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[8]/span').text,
                                 '共0页', '用户列表无数据，总页数显示错误')
            else:
                # 列表不为空直接返回fail，用例无法执行
                raise AssertionError('用户列表数据不为空，用例无法执行，请稍后手动执行用例')
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_014(self):
        """用户分组界面——用户列表总数据<每页数据，但列表数据！=0"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取分页数据,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.addimg()
            # 获取用户分组数据
            List = []
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            # 判断分组数据是否小于或等于分页数据,并且分组数据不等于0
            if len(List) <= int(sum1) and len(List) != 0:
                self.assertTrue(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '1',
                                '页码显示错误')
                self.assertEqual(self.b.by_find_element('xpath',
                                                        '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[8]/span').text,
                                 '共1页', '总页数显示错误')
            else:
                raise AssertionError('列表无数据或总数据大于每页数据，用例无法执行，请稍后手动执行用例')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_015(self):
        """用户分组界面——用户列表总数据>每页数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[11]/a/span/span[2]').click()  # 点击尾页
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            # 获取跳转框页码，
            sum2 = int(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value'))
            # 计算总数据：(页码-1)*每页数据条数+最后一页数据
            count = (sum2 - 1) * int(sum1) + int(len(List))
            # 判断总数据是否大于每页数据量
            if count > int(sum1):
                self.assertTrue(
                    self.b.by_find_element('css', 'input.pagination-num').get_attribute('value') == '%s' % sum2,
                    '当前页数显示错误')
                self.assertEqual(self.b.by_find_element('xpath',
                                                        '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[8]/span').text,
                                 '共%s页' % sum2, '总页数显示错误')
            else:
                raise AssertionError('列表无数据或总数据小于每页数据，用例无法执行，请稍后手动执行用例')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_016(self):
        """用户分组界面——页数搜索（页数框输入小于1的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
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


    def test_yhfz_at_017(self):
        """用户分组界面——页数搜索（页数框输入大于总页数的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(1)
            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 获取总页数
            count = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear > div > div.sheet > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span').text
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


    def test_yhfz_at_018(self):
        """用户分组界面——页数搜索（页数框输入小于总页数且不小于0的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取总页数
            oldcount = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear > div > div.sheet > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            oldcount = oldcount[1:-1]
            # 判断用户分组界面是否有数据
            if oldcount == '0' or oldcount == '1' or oldcount == '2':
                for i in range(21):
                    # 点击新增会议
                    self.b.by_find_element('link_text', '新增分组').click()
                    # 分组名称输入
                    self.b.by_find_element('name', 'group_name').send_keys('测试分组%s' % i)
                    # 点击'所有联系人'按钮
                    self.b.by_find_element('css', '.sprite_dv.fl').click()
                    # 点击'管理员'用户
                    self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                    # 点击确定
                    self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                    time.sleep(1)
            # 获取总页数
            newcount = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear > div > div.sheet > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            newcount = newcount[1:-1]
            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 页数框输入总页数-1
            self.b.by_find_element('css','.pagination-num').send_keys(int(newcount)-1)
            self.addimg()
            # 模拟键盘回车
            self.b.by_find_element('css', '.pagination-num ').send_keys(Keys.ENTER)
            self.addimg()
            time.sleep(1)
            # 获取跳转后的输入框值
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            self.assertTrue(int(sum2) == int(newcount)-1, '跳转至%s页，跳转框数字为%s' % (int(newcount)-1, sum2))
            # 断言后删除所有数据，反正影响下条用例运行
            for i in range(int(newcount)):
                self.b.by_find_element('xpath','//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/input').click()
                self.b.by_find_element('link_text','删除').click()
                self.b.by_find_element('css','.layui-layer-btn0').click()
                time.sleep(1)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_019(self):
        """用户分组界面——总页数显示（查看用户分组页数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[11]/a/span/span[2]').click()  # 点击尾页
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            # 获取跳转框页码，
            sum2 = int(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value'))
            # 计算总数据：(页码-1)*每页数据条数+最后一页数据
            if sum2 == 0:
                count = int(len(List))
            else:
                count = (sum2 - 1) * int(sum1) + int(len(List))
            # 获取总页数文字
            number = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear > div > div.sheet > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            numcount = number[1:-1]
            if count == 0:
                self.assertTrue(number == '共0页','页面无数据，总页数显示共%s页'%numcount)
            elif count > 10:
                # 计算总页数
                pages = (count-int(len(List)))/10
                self.assertTrue(int(numcount) == pages, '共%s页,但显示共%s页' % (pages, numcount))
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_020(self):
        """用户分组——分组条数显示（左下角的分组记录显示）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('xpath',
                                   '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[11]/a/span/span[2]').click()  # 点击尾页
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            # 获取跳转框页码，
            sum2 = int(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value'))
            # 计算总数据：(页码-1)*每页数据条数+最后一页数据
            if sum2 == 0:
                count = int(len(List))
            else:
                count = (sum2 - 1) * int(sum1) + int(len(List))

            # 获取左下角文字
            records = self.b.by_find_element('css','.pagination-info').text
            # 三种情况断言，页面无数据，页面数据小于每页数据量，页面数据大于每页数据量
            if count == 0:
                self.assertTrue(records == '显示0到0,共0记录', '页面无数据，左下角显示错误')
            elif count>int(sum1):
                logger.info('显示1到%s,共%s记录' % (sum1, count))
            else:
                logger.info('显示1到%s,共%s记录' % (count, count))
                self.assertTrue(records == '显示1到%s,共%s记录' % (count, count))
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_021(self):
        """用户分组——新增分组界面（进入新增分组界面）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增会议
            self.b.by_find_element('link_text', '新增分组').click()
            self.addimg()
            # 断言是否进入新增分组界面
            self.assertEqual('新增分组', self.b.by_find_element('css', '.layui-layer-title').text, '进入新增分组页面失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_022(self):
        """用户分组——新增分组界面（关键词搜索）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增会议
            self.b.by_find_element('link_text', '新增分组').click()
            self.addimg()
            # 点开所有隐藏的分组
            for i in self.b.by_find_elements('css', '.sprite_dv.fl'):
                if i.text:
                    i.click()
                    time.sleep(2)
                else:
                    self.driver.execute_script("arguments[0].scrollIntoView();", i)
                    i.click()

            # 获取所有分组内的成员信息
            oldList = []
            for c in self.b.by_find_elements('css', ' .user-chose'):
                if c.text:
                    oldList.append(c.text)
                else:
                    # 滚动条滚动至可见的元素位置
                    self.driver.execute_script("arguments[0].scrollIntoView();", c)
                    oldList.append(c.text)
                    time.sleep(1)

            # 关键词搜索输入'管理'
            self.b.by_find_element('id','user-auto').send_keys('管理')
            self.addimg()

            # 获取输入的值
            name = self.b.by_find_element('id','user-auto').get_attribute('value')
            print('搜索的内容：%s' % name )

            # 循环所有分组内的成员信息，并将符合搜索内容的成员信息存入集合
            List = []
            oldList = list(set(oldList))
            for i in oldList:
                if name in i:
                    List.append(i)
            print('符合搜索内容的数据：%s' % List)

            # 获取搜索后的成员信息
            newList = []
            for c in self.b.by_find_elements('css', ' .user-chose'):
                if c.text:
                    newList.append(c.text)
                else:
                    # 滚动条滚动至可见的元素位置
                    self.driver.execute_script("arguments[0].scrollIntoView();", c)
                    newList.append(c.text)
                    time.sleep(1)
            print('搜索后的数据：%s' % newList)
            # 断言是否存在
            self.assertTrue(List == newList, '符合搜索内容的数据在联系人中显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_023(self):
        """用户分组——新增分组界面（不输入分组名称保存）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增会议
            self.b.by_find_element('link_text', '新增分组').click()
            # 不输入分组名称
            self.b.by_find_element('css','.bottom_b1').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual(self.b.by_find_element('css', '.layui-layer-tips').text, '请填写分组名称', '不输入分组名称点击保存，提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_024(self):
        """用户分组——新增分组界面（选择参会人员后，查看已选参会人员）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增会议
            self.b.by_find_element('link_text', '新增分组').click()
            # 循环所有分组,并点开
            self.b.by_find_element('css', '#user-container > div:nth-child(1) > span > div.sprite_dv.fl').click()
            self.addimg()
            # 点击第一个所有联系人 > 管理员
            self.b.by_find_element('css','#user-container > div:nth-child(1) > ul > li:nth-child(1)').click()
            self.addimg()
            # 获取已选参会人员的数字
            num = self.b.by_find_element('id','user-total').text
            self.assertTrue(num == '1', '选择一个联系人，但已选参会人显示%s' % num)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_025(self):
        """用户分组——新增分组界面（同名测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                for i in range(2):
                    # 点击新增会议
                    self.b.by_find_element('link_text', '新增分组').click()
                    # 分组名称输入
                    self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                    # 点击'所有联系人'按钮
                    self.b.by_find_element('css', '.sprite_dv.fl').click()
                    # 点击'管理员'用户
                    self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                    # 点击确定
                    self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                self.addimg()
                self.assertTrue(self.b.by_find_element('css','.layui-layer-content.layui-layer-padding').text == '添加分组失败','已存在同名用户，任然创建成功')
            # 获取第一条数据的分组名称
            name = self.b.by_find_element('css','#datagrid-row-r1-1-0 > td:nth-child(3) > div').text
            # 点击新增会议
            self.b.by_find_element('link_text', '新增分组').click()
            # 分组名称输入
            self.b.by_find_element('name', 'group_name').send_keys(name)
            # 点击'所有联系人'按钮
            self.b.by_find_element('css', '.sprite_dv.fl').click()
            # 点击'管理员'用户
            self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
            # 点击确定
            self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
            self.assertEqual(self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text, '添加分组失败',
                            '已存在同名用户，任然创建成功')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_026(self):
        """用户分组——新增分组界面（新增分组是否显示在联系人中）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                self.addimg()
            # 获取第一条数据的分组名称
            name = self.b.by_find_element('css','#datagrid-row-r1-1-0 > td:nth-child(3) > div').text
            # 点击新增会议
            self.b.by_find_element('link_text', '新增分组').click()
            # 获取所有联系人分组名称
            List = []
            for i in self.b.by_find_elements('css','.sprite_dv.fl'):
                List.append(i.text)
            self.assertTrue(name in List, '分组名称不显示在新建分组中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_027(self):
        """用户分组——新增分组界面（正常添加分组）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击新增会议
            self.b.by_find_element('link_text', '新增分组').click()
            # 分组名称输入
            self.b.by_find_element('name', 'group_name').send_keys('测试分组44')
            # 输入分组名称后获取输入的分组名称
            self.b.by_find_element('name', 'group_name').get_attribute('value')
            # 点击'所有联系人'按钮
            self.b.by_find_element('css', '.sprite_dv.fl').click()
            # 点击'管理员'用户
            self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
            # 点击确定
            self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
            self.addimg()
            time.sleep(1)
            # 点击尾页，由于新添加的分组默认添加在最后，需要获取尾页数据
            self.b.by_find_element('css','.pagination-last').click()

            # 获取第一条数据的分组名称
            name = self.b.by_find_element('css','#datagrid-row-r1-1-0 > td:nth-child(3) > div').text
            # 点击新增会议
            self.b.by_find_element('link_text', '新增分组').click()
            # 获取所有联系人分组名称
            List = []
            for i in self.b.by_find_elements('css','.sprite_dv.fl'):
                List.append(i.text)
            self.assertTrue(name in List, '分组名称不显示在新建分组中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_028(self):
        """用户分组——进入编辑分组页面"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                self.addimg()
            # 点击编辑按钮
            self.b.by_find_element('css', '#datagrid-row-r1-2-0 > td:nth-child(2) > div > a:nth-child(1)').click()
            self.addimg()
            self.assertTrue(self.b.by_find_element('css', '.layui-layer-title').text == '编辑分组界面' ,'进入编辑页面失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_029(self):
        """用户分组——编辑分组页面（修改分组名称）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                self.addimg()
            # 点击编辑按钮
            self.b.by_find_element('css', '#datagrid-row-r1-2-0 > td:nth-child(2) > div > a:nth-child(1)').click()
            self.addimg()
            # 修改分组名称
            self.b.by_find_element('name', 'group_name').send_keys('110')
            # 获取修改后的分组名称
            name = self.b.by_find_element('name','group_name').get_attribute('value')
            # 点击确定
            self.b.by_find_element('css', '.bottom_b1').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text, '更新分组成功' ,'更新分组提示错误')
            time.sleep(1)
            # 获取所有联系人分组名称
            List = []
            for i in self.b.by_find_elements('css','.datagrid-cell-c1-name'):
                List.append(i.text)
            self.assertTrue(name in List, '修改分组名称后，分组列表内的名称没有改变')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_yhfz_at_030(self):
        """用户分组——编辑分组页面（增加联系人）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 进入用户列表界面
            self.b.by_find_element('link_text', '用户列表').click()
            # 判断列表内是否有用户，如果没有就创建用户
            if self.b.isElementExist('xpath',
                                     '//*[@id="datagrid-row-r1-1-0"]/td[4]/div') == False:
                # 输入正确用户名密码等数据
                    self.b.by_find_element('css', 'a.easyui-linkbutton:nth-child(1)').click()
                    self.b.by_find_element('name', 'account').send_keys('admin1')
                    self.b.by_find_element('name', 'password').send_keys('123456')
                    self.b.by_find_element('name', 'username').send_keys('测试用户')
                    self.b.by_find_element('xpath',
                                               '//*[@id="layui-layer1"]/div[2]/form/div[2]/button[1]').click()
            # 进入用户界面
            self.b.by_find_element('link_text', '用户分组').click()
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                self.addimg()
            # 获取当前分组的用户数
            count = self.b.by_find_element('css', '#datagrid-row-r1-2-0 > td:nth-child(1) > div').text
            # 点击编辑按钮
            self.b.by_find_element('css', '#datagrid-row-r1-2-0 > td:nth-child(2) > div > a:nth-child(1)').click()
            self.addimg()
            # 增加分组联系人

            # 点开'所有联系人'
            self.b.by_find_element('css', '#user-container > div:nth-child(1) > span > div.sprite_dv.fl').click()
            i = 0
            for c in self.b.by_find_elements('css', '.user-chose'):
                if i <= int(count):
                    c.click()
                    i += 1
                else:
                    break
            # 获取修改后的联系人数量
            name = self.b.by_find_element('css','#user-total').text
            self.addimg()
            # 点击确定
            self.b.by_find_element('css', '.bottom_b1').click()
            self.addimg()
            self.assertEqual(self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text, '更新分组成功' ,'更新分组提示错误')
            time.sleep(1)
            # 获取所有联系人分组名称
            count1 = self.b.by_find_element('css', '#datagrid-row-r1-2-0 > td:nth-child(1) > div').text
            self.assertTrue(name == count1, '增加联系人数量后，分组列表内的用户数没有改变')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_031(self):
        """用户分组——删除分组"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                self.addimg()
            # 获取第一条数据的分组
            oldname = self.b.by_find_element('css','#datagrid-row-r1-1-0 > td:nth-child(3) > div').text
            # 点击删除按钮
            self.b.by_find_element('css', '#datagrid-row-r1-2-0 > td:nth-child(2) > div > a:nth-child(3)').click()
            self.addimg()
            # 点击确定
            self.b.by_find_element('css','.layui-layer-btn0').click()
            self.assertEqual(self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text, '删除分组成功',
                            '删除分组提示错误')
            time.sleep(1)
            # 获取所有联系人分组名称
            List = []
            for i in self.b.by_find_elements('css', '.datagrid-cell-c1-name'):
                List.append(i.text)
            logger.info(List)
            self.assertTrue(oldname not in List, '删除分组名称，分组任然存在列表中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_032(self):
        """用户分组——不选择分组点击顶部删除"""
        try:
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
            # 点击删除按钮
            self.b.by_find_element('css', '#common_operate > a:nth-child(2) > span').click()
            self.assertEqual(self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text, '请至少选择一个项!',
                            '无数据点击删除，提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_yhfz_at_033(self):
        """用户分组——顶部删除分组"""
        try:
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
            # 判断用户分组界面是否有数据
            if self.b.isElementExist('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div') == False:
                # 点击新增会议
                self.b.by_find_element('link_text', '新增分组').click()
                # 分组名称输入
                self.b.by_find_element('name', 'group_name').send_keys('测试分组')
                # 点击'所有联系人'按钮
                self.b.by_find_element('css', '.sprite_dv.fl').click()
                # 点击'管理员'用户
                self.b.by_find_element('css', '#user-container > div > ul > li:nth-child(1)').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                self.addimg()
                time.sleep(1)
            # 勾选第一条数据
            self.b.by_find_element('css', '#datagrid-row-r1-1-0 > td:nth-child(2) > div > input[type=checkbox]').click()
            # 获取第一条数据的分组名称
            name = self.b.by_find_element('css', '#datagrid-row-r1-1-0 > td:nth-child(3) > div').text
            # 点击删除按钮
            self.b.by_find_element('css', '#common_operate > a:nth-child(2) > span').click()
            self.addimg()
            # 点击确定
            self.b.by_find_element('css','.layui-layer-btn0').click()
            self.addimg()
            time.sleep(1)
            # 获取所有联系人分组名称
            List = []
            for i in self.b.by_find_elements('css','.datagrid-cell-c1-name'):
                List.append(i.text)
            self.assertFalse(name in List, '修改分组名称后，分组列表内的名称没有改变')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


if __name__ == '__main__':
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(Test_UserGruop)
    suit = unittest.TestSuite()
    # suit.addTest(suit1)
    suit.addTest(Test_UserGruop('test_yhfz_at_022'))


    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb"),
                           verbosity=2,
                           )
    runer.run(suit)
    # print('\n'.join([''.join([('Love'[(x - y) % len('Love')] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))