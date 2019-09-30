#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: test_meetingdocument.py
@time: 2019/9/29 14:57
@desc: 会议资料测试用例
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

import re
import unittest
import time
import os
import sys
import random

logger = Logger('logger').getlog()


class Test_meetingdocument(unittest.TestCase):

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
        self.usercount = self.usercount[8:-2]
        # 再进入会议列表
        self.b.by_find_element('link_text', '会议列表').click()
        # 获取总页数
        self.page = self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/div/div[3]/table/tbody/tr/td[8]/span').text
        self.page = self.page[1:-1]
        List = []
        # 判断会议列表数据是否为空，或只有1页
        if self.page == '0' or self.page == '1':
            # 将列表所有的会议名称添加进集合
            for i in self.b.by_find_elements('css', '.datagrid-cell-c1-name'):
                List.append(i.text)
        else:
            for p in range(int(self.page)-1):
                for i in self.b.by_find_elements('css', '.datagrid-cell-c1-name'):
                    List.append(i.text)
                self.b.by_find_element('css', '.pagination-next').click()
                time.sleep(1)
        # 每次执行用例都判断会议列表中是否有数据
        if '测试铭牌设置' not in List:
            # 点击新增会议
            self.b.by_find_element('link_text', '新增会议').click()
            # 会议名称
            self.b.by_find_element('name', 'name').send_keys('测试铭牌设置')
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
            '''选择参会人'''
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            time.sleep(1)
            # 鼠标悬浮在'请选择用户'上
            self.b.move_to_element(By.CSS_SELECTOR, '.manage_btn.clear')
            # 全选用户
            self.b.by_find_element('css', '#user-container > div > span > div.sprite_san.fr').click()
            # 点击确定
            self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
            time.sleep(1)
            # 进入会议资料界面
            self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/ul/a[5]').click()
            time.sleep(1)
        else:
            self.b.by_find_element('link_text', '测试铭牌设置').click()
            # 判断参会人界面中是否有参会人
            if self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div > span') == False:
                # 点击'选择参会人'
                self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
                time.sleep(1)
                # 鼠标悬浮在'请选择用户'上
                self.b.move_to_element(By.CSS_SELECTOR, '.manage_btn.clear')
                # 全选用户
                self.b.by_find_element('css', '#user-container > div > span > div.sprite_san.fr').click()
                # 点击确定
                self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
                time.sleep(2)
            # 进入会议资料界面
            self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/ul/a[5]').click()
            time.sleep(1)


    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()


    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True


    def test_hyzl_at_01(self):
        """会议资料界面——检查页面标题"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 获取页面title
            title = self.b.by_find_element('css', '.personnel.fl').text
            self.assertEqual('会议资料', title, '页面标题显示错误：%s' % title)
            print('\n页面标题：%s' % title)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_02(self):
        """会议资料界面——会议资料顶部栏显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言'按名称排序'功能是否存在
            self.assertEqual('按名称排序', self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(1)').text, '按名称排序不存在或显示错误')
            # 断言'按时间排序'功能是否存在
            self.assertEqual('按时间排序', self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(2)').text, '按时间排序不存在或显示错误')
            # 断言'加入文件夹'功能是否存在
            self.assertEqual('加入文件夹', self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').text, '加入文件夹不存在或显示错误')
            # 断言'上传文件夹'功能是否存在
            self.assertEqual('上传文件', self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(4)').text, '上传文件不存在或显示错误')
            # 断言'删除'功能是否存在
            self.assertEqual('删除', self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(3)').text, '删除不存在或显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_03(self):
        """会议资料界面——会议资料字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言选择框是否存在
            self.assertTrue(self.b.isElementExist('css', '#all-checked'), '选择框不存在')
            # 断言排序是否存在
            self.assertEqual('排序', self.b.by_find_element('css', '.f-flex-content.table_n.clear > li:nth-child(2)').text, '排序不存在或显示错误')
            # 断言名称是否存在
            self.assertEqual('名称', self.b.by_find_element('css', '.f-flex-content.table_n.clear > li:nth-child(3)').text, '名称不存在或显示错误')
            # 断言上传人是否存在
            self.assertEqual('上传人', self.b.by_find_element('css', '.f-flex-content.table_n.clear > li:nth-child(4)').text, '上传人不存在或显示错误')
            # 断言参与/查看是否存在
            self.assertEqual('参与/查看', self.b.by_find_element('css', '.f-flex-content.table_n.clear > li:nth-child(5)').text, '参与/查看不存在或显示错误')
            # 断言上传时间是否存在
            self.assertEqual('上传时间', self.b.by_find_element('css', '.f-flex-content.table_n.clear > li:nth-child(6)').text, '上传时间不存在或显示错误')
            # 断言操作是否存在
            self.assertEqual('操作', self.b.by_find_element('css', '.f-flex-content.table_n.clear > li:nth-child(7)').text, '操作不存在或显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_04(self):
        """会议资料界面——新增文件夹字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在会议资料,false创建
            if self.b.isElementExist('css', '#theadView > div:nth-child(1) > ul > li:nth-child(2) > div > span.f-one-level-span') == False:
                # 点击'加入文件夹'
                self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
                # 输入文件夹名称
                self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').send_keys('测试新增文件夹')
                # 点击确定
                self.b.by_find_element('css', '.div_btn.cz').click()
                time.sleep(1)
                self.addimg()
            self.addimg()
            # 断言选择框是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="theadView"]/div[1]/ul/li[1]/input'), '选择框不存在')
            # 断言序号是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="theadView"]/div[1]/ul/li[2]/div/span[1]'),
                            '序号不存在或显示错误')
            # 断言名称是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="theadView"]/div[1]/ul/li[3]/div/span'),
                            '名称不存在或显示错误')
            # 断言上传人是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="theadView"]/div[1]/ul/li[4]'),
                            '上传人不存在或显示错误')
            # 断言参与/查看人数是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="theadView"]/div[1]/ul/li[5]'),
                            '参与/查看人数不存在或显示错误')
            # 断言上传时间是否存在
            self.assertTrue(self.b.isElementExist('xpath', '//*[@id="theadView"]/div[1]/ul/li[6]'),
                            '上传时间不存在或显示错误')
            # 断言操作'文件夹'是否存在
            self.assertEqual('文件夹', self.b.by_find_element('xpath', '//*[@id="theadView"]/div[1]/ul/li[7]/span[1]').text, '操作(文件夹)不存在或显示错误')
            # 断言操作'上传'是否存在
            self.assertEqual('上传', self.b.by_find_element('xpath', '//*[@id="theadView"]/div[1]/ul/li[7]/span[2]').text, '操作(上传)不存在或显示错误')
            # 断言操作'编辑'是否存在
            self.assertEqual('编辑', self.b.by_find_element('xpath', '//*[@id="theadView"]/div[1]/ul/li[7]/span[3]').text, '操作(编辑)不存在或显示错误')
            # 断言操作'删除'是否存在
            self.assertEqual('删除', self.b.by_find_element('xpath', '//*[@id="theadView"]/div/ul/li[7]/span[10]').text, '操作(删除)不存在或显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_05(self):
        """会议资料界面——操作选择框与全选框"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在会议资料,false创建
            if self.b.isElementExist('css', '#theadView > div:nth-child(1) > ul > li:nth-child(2) > div > span.f-one-level-span') == False:
                # 点击'加入文件夹'
                self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
                # 输入文件夹名称
                self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').send_keys('测试新增文件夹')
                # 点击确定
                self.b.by_find_element('css', '.div_btn.cz').click()
                time.sleep(1)
                self.addimg()
            # 点击第一条数据的选择框
            self.b.by_find_element('xpath', '//*[@id="theadView"]/div/ul/li[1]/input').click()
            # 断言第一条数据是否被选中
            self.assertTrue(
                self.b.by_find_element('xpath', '//*[@id="theadView"]/div[1]/ul/li[1]/input').is_selected(),
                '勾选框未选中')
            self.addimg()
            time.sleep(1)

            # 取消第一条数据的选择
            self.b.by_find_element('xpath', '//*[@id="theadView"]/div[1]/ul/li[1]/input').click()
            # 断言第一条数据是否被取消选中
            self.assertFalse(
                self.b.by_find_element('xpath', '//*[@id="theadView"]/div[1]/ul/li[1]/input').is_selected(),
                '勾选框未取消')
            self.addimg()
            time.sleep(1)

            # 点击全选框
            self.b.by_find_element('css', '#all-checked').click()

            # 断言全选框是否被选中
            self.assertTrue(self.b.by_find_element('css', '#all-checked').is_selected(), '全选框未选中')
            self.addimg()
            time.sleep(1)
            # 取消全选框选择
            self.b.by_find_element('css', '#all-checked').click()

            # 断言全选框是否被取消选中
            self.assertFalse(self.b.by_find_element('css', '#all-checked').is_selected(), '全选框未取消')
            self.addimg()

            # 点击全选框，取消数据选择框，全选框被取消选中
            self.b.by_find_element('css', '#all-checked').click()
            # 点击数据选择框
            self.b.by_find_element('xpath', '//*[@id="theadView"]/div[1]/ul/li[1]/input').click()
            time.sleep(1)
            # 断言全选框是否被取消选中
            self.assertFalse(self.b.by_find_element('css', '#all-checked').is_selected(), '全选框未取消')
            self.addimg()
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_hyzl_at_06(self):
        """会议资料界面——每页显示10条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 分页下拉框选择10条/页
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('10')
            self.addimg()
            List = []
            # 循环整个会议资料，添加进集合，计算本页有多少条数据
            for l in self.b.by_find_elements('css', '.f-one-level-span'):
                List.append(l)
            self.assertTrue(len(List) <= 10, '超出10条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_hyzl_at_07(self):
        """会议资料界面——每页显示20条数据"""
        # 选择10条数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('20')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.f-one-level-span'):
                List.append(l)
            self.assertTrue(len(List) <= 20, '超出20条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_hyzl_at_08(self):
        """会议资料界面——每页显示50条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('50')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.f-one-level-span'):
                List.append(l)
            self.assertTrue(len(List) <= 50, '超出50条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_hyzl_at_09(self):
        """会议资料界面——每页显示100条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('100')
            time.sleep(1)
            self.addimg()
            List = []
            for l in self.b.by_find_elements('css', '.f-one-level-span'):
                List.append(l)
            self.assertTrue(len(List) <= 100, '超出100条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

    def test_hyzl_at_010(self):
        """会议资料界面——首页图标点击"""
        # 点击首页图标，需要回到第一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在会议资料,false创建
            if self.b.isElementExist('css', '#theadView > div:nth-child(1) > ul > li:nth-child(2) > div > span.f-one-level-span') == False:
                # 点击'加入文件夹'
                self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
                # 输入文件夹名称
                self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').send_keys('测试新增文件夹')
                # 点击确定
                self.b.by_find_element('css', '.div_btn.cz').click()
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

    def test_hyzl_at_011(self):
        """会议资料界面——尾页图标点击"""
        # 点击尾页图标，需要前往最后一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.b.by_find_element('css', '.pagination-last').click()
            time.sleep(1)
            self.addimg()
            # 获取总页数
            count = self.b.by_find_element('css', '#pp > table > tbody > tr > td:nth-child(8) > span').text
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

    def test_hyzl_at_012(self):
        """会议资料界面——下一页图标点击"""
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
            count = self.b.by_find_element('css', '#pp > table > tbody > tr > td:nth-child(8) > span').text
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

    def test_hyzl_at_013(self):
        """会议资料界面——上一页图标点击"""
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
                self.assertTrue(int(sum2) == (int(sum1) - 1), '点击上一页失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise

        
    def test_hyzl_at_014(self):
        """会议资料界面——页数搜索（页数框输入小于1的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在会议资料,false创建
            if self.b.isElementExist('css', '#theadView > div:nth-child(1) > ul > li:nth-child(2) > div > span.f-one-level-span') == False:
                # 点击'加入文件夹'
                self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
                # 输入文件夹名称
                self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').send_keys('测试新增文件夹')
                # 点击确定
                self.b.by_find_element('css', '.div_btn.cz').click()
                time.sleep(1)
                self.addimg()
            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 页数框输入0
            self.b.by_find_element('css','.pagination-num').send_keys(0)
            self.addimg()
            # 模拟键盘回车
            self.b.by_find_element('css', '.pagination-num').send_keys(Keys.ENTER)
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


    def test_hyzl_at_015(self):
        """会议资料界面——页数搜索（页数框输入大于总页数的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在会议资料,false创建
            if self.b.isElementExist('css', '#theadView > div:nth-child(1) > ul > li:nth-child(2) > div > span.f-one-level-span') == False:
                # 点击'加入文件夹'
                self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
                # 输入文件夹名称
                self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').send_keys('测试新增文件夹')
                # 点击确定
                self.b.by_find_element('css', '.div_btn.cz').click()
                time.sleep(1)
                self.addimg()
            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 获取总页数
            count = self.b.by_find_element('css', '#pp > table > tbody > tr > td:nth-child(8) > span').text
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

    def test_hyzl_at_016(self):
        # 正确跳转界面暂时无法编写，数据无法创建过多
        print('暂未编写')
        pass

    def test_hyzl_at_017(self):
        """会议资料界面——总页数显示（查看用户分组页数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('css', '.pagination-last').click()  # 点击尾页
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.f-one-level-span'):
                List.append(l)
            # 获取跳转框页码，
            sum2 = int(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value'))
            # 计算总数据：(页码-1)*每页数据条数+最后一页数据
            if sum2 == 0 or sum2 == 1:
                count = int(len(List))
            else:
                count = (sum2 - 1) * int(sum1) + int(len(List))
            # 获取总页数文字
            number = self.b.by_find_element('css', '#pp > table > tbody > tr > td:nth-child(8) > span').text
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

    def test_hyzl_at_018(self):
        """会议资料界面——分组条数显示（左下角的分组记录显示）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('css', '.pagination-last').click()  # 点击尾页
            time.sleep(1)
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.f-one-level-span'):
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


    def test_hyzl_at_019(self):
        """会议资料界面——进入加入文件夹界面"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.b.by_find_element('link_text', '参会人员').click()
            # 获取总页数
            page = self.b.by_find_element('xpath',
                                               '//*[@id="wrap"]/div/div[3]/div[3]/div/div[2]/div/'
                                               'div/div/div[3]/table/tbody/tr/td[8]/span').text
            page = page[1:-1]
            List = []
            # 判断参会人员列表数据是否为空，或只有1页
            if page == '0' or page == '1':
                # 将列表所有的参会人员名称添加进集合
                for i in self.b.by_find_elements('css', '.datagrid-cell-c2-username'):
                    List.append(i.text)
            else:
                for p in range(int(page)):
                    for i in self.b.by_find_elements('css', '.datagrid-cell-c2-username'):
                        List.append(i.text)
                    self.b.by_find_element('css', '.pagination-next').click()
                    time.sleep(1)
            for i in List:
                if i == '名称':
                    List.remove(i)
            # 点击会议资料
            self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/ul/a[5]').click()
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 断言标题
            self.assertEqual('加入文件夹', self.b.by_find_element('css', '.layui-layer-title').text, '进入加入文件夹失败')
            # 断言用户是否与参会人员相同
            newList = []
            for n in self.b.by_find_elements('css', 'div.m-meet-datum-popup-right-bd > div > div > ul > li'):
                newList.append(n.text)
            self.assertTrue(List == newList, '用户与参会人员不同')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_020(self):
        """会议资料界面——不输入文件夹名称，点击确定"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 点击确定
            self.b.by_find_element('css', '.div_btn.cz').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('请添加文件夹名称', self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text,
                             '未输入文件夹名称，无错误提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_021(self):
        """会议资料界面——不输入文件夹名称，点击确定"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 点击确定
            self.b.by_find_element('css', '.div_btn.cz').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('请添加文件夹名称', self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text,
                             '未输入文件夹名称，无错误提示')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_022(self):
        """会议资料界面——查看全选（全选），点击用户，查看选择框是否可以操作"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 判断查看全选是否选中全选
            if self.b.by_find_element('css', 'div.m-meet-datum-popup-right-hd > div:nth-child(3) > input[type=radio]').is_selected() == False:
                # 选中'全选'权限
                self.b.by_find_element('css', 'div.m-meet-datum-popup-right-hd > div:nth-child(3) > input[type=radio]').click()
            for n in self.b.by_find_elements('css', 'div.m-meet-datum-popup-right-bd > div > div > ul > li > input'):
                n.click()
                self.assertTrue(n.is_selected(), '%s在全选权限状态被取消选中' % n.find_element_by_xpath('following-sibling::span').text)
                self.assertTrue(n.is_displayed(), '%s在全选权限状态中，选中框可以操作' % n.find_element_by_xpath('following-sibling::span').text)
            self.addimg()
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_hyzl_at_023(self):
        """会议资料界面——查看全选（手选），点击用户，查看是否可以被取消选中"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 判断查看手选是否选中全选
            if self.b.by_find_element('css', 'div.m-meet-datum-popup-right-hd > div:nth-child(2) > input[type=radio]').is_selected() == False:
                # 选中'手选'权限
                self.b.by_find_element('css', 'div.m-meet-datum-popup-right-hd > div:nth-child(2) > input[type=radio]').click()
            # 循环所有用户的选择框选中状态
            for n in self.b.by_find_elements('css', 'div.m-meet-datum-popup-right-bd > div > div > ul > li > input'):
                n.click()
                self.assertFalse(n.is_selected(), '%s在手选权限状态无法被取消选中' % n.find_element_by_xpath('following-sibling::span').text)
            # 点击'手选'权限下的全选操作
            self.b.by_find_element('css', 'div.m-meet-datum-popup-right-bd > div > div > h2 > input').click()
            # 断言是否可以操作，以及出于被选中状态
            self.assertTrue(self.b.by_find_element('css','div.m-meet-datum-popup-right-bd > div > div > h2 > input').is_selected(), '全选框无法被选中')
            self.addimg()
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_hyzl_at_024(self):
        """会议资料界面——删除部分参会人，查看加入文件夹界面右下角人数显示是否正常"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 进入参会人员界面，删除部分参会人员
            self.b.by_find_element('link_text', '参会人员').click()
            # 选择第一个和第二个参会人员删除
            self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(1) > div > input').click()
            self.b.by_find_element('css', '#datagrid-row-r2-2-1 > td:nth-child(1) > div > input').click()
            # 点击删除
            self.b.by_find_element('css', '.nav_one.n_5.fl.batch-delete').click()
            # 点击确定
            self.b.by_find_element('css', '.layui-layer-btn0').click()
            time.sleep(2)
            self.addimg()
            # 获取参会人员总数
            count = self.b.by_find_element('css', '.pagination-info').text
            count = re.findall('\d+\.?\d*',count)[2]
            # 切换到会议资料界面
            self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/ul/a[5]').click()
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 获取加入文件夹中的总人数
            jcount = self.b.by_find_element('css', 'span.f-fc-blue').text
            jcount = jcount[:-1]
            self.assertTrue(count == jcount, '加入文件夹的人数与参会人员的总数相等')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_025(self):
        """会议资料界面——新增部分参会人，查看加入文件夹界面右下角人数显示是否正常"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 进入参会人员界面，删除部分参会人员
            self.b.by_find_element('link_text', '参会人员').click()
            # 点击'选择参会人'
            self.b.by_find_element('css', '.nav_one.n_1.fl.clear').click()
            time.sleep(1)
            # 鼠标悬浮在'请选择用户'上
            self.b.move_to_element(By.CSS_SELECTOR, '.manage_btn.clear')
            # 全选用户
            self.b.by_find_element('css', '#user-container > div > span > div.sprite_san.fr').click()
            # 点击确定
            self.b.by_find_element('css', '.bottom_y.bottom_b1').click()
            time.sleep(2)
            self.addimg()
            # 获取参会人员总数
            count = self.b.by_find_element('css', '.pagination-info').text
            count = re.findall('\d+\.?\d*',count)[2]
            # 切换到会议资料界面
            self.b.by_find_element('xpath', '//*[@id="wrap"]/div/div[3]/div[2]/div/div[2]/div/ul/a[5]').click()
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 获取加入文件夹中的总人数
            jcount = self.b.by_find_element('css', 'span.f-fc-blue').text
            jcount = jcount[:-1]
            self.assertTrue(count == jcount, '加入文件夹的人数与参会人员的总数相等')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_hyzl_at_026(self):
        """会议资料界面——进入加入文件夹界面，鼠标悬浮在?上，查看是否有提示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            self.b.move_to_element(By.CSS_SELECTOR, 'div.m-check-power-tips-box > i')
            self.assertTrue(self.b.by_find_element('css', 'div.m-check-power-tips-box > p').is_displayed(), '鼠标悬浮在?上，无提示显示')
            countent1 = self.b.by_find_element('css', 'div.m-check-power-tips-box > p > span:nth-child(1)').text
            countent2 = self.b.by_find_element('css', 'div.m-check-power-tips-box > p > span:nth-child(2)').text
            self.assertEqual('手选：后期新增用户需要手动勾选该查看权限', countent1, '悬浮后，显示提示错误')
            self.assertEqual('全选：后期新增用户自动勾选该查看权限', countent2, '悬浮后，显示提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_hyzl_at_027(self):
        """会议资料界面——输入同名文件夹名称"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 判断是否存在文件夹
            if self.b.isElementExist('css', '#theadView > div:nth-child(1) > ul > li:nth-child(2) > div > span.f-one-level-span'):
                name = self.b.by_find_element('css', '#theadView > div:nth-child(1) > ul > '
                                                     'li.f-flex-item-5.f-align_item.down.f-text_ellipsis.f-ex > '
                                                     'div > span').text
                # 点击加入文件夹
                self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
                # 输入文件夹名称
                self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').send_keys(name)
                # 点击确定
                self.b.by_find_element('css', '.div_btn.cz').click()
                self.addimg()
                # 断言是否有提示
                self.assertTrue(self.b.isElementExist('css', '.layui-layer-dialog'), '文件夹名称重复，保存后无提示框弹出')
                self.assertEqual('文件夹名称不能重复', self.b.by_find_element('css', '.layui-layer-dialog > .layui-layer-content').text,
                                 '文件夹名称重复，提示错误')
            else:
                for i in range(2):
                    # 点击加入文件夹
                    self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
                    # 输入文件夹名称
                    self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').send_keys('测试新增文件夹')
                    # 点击确定
                    self.b.by_find_element('css', '.div_btn.cz').click()
                    time.sleep(1)
                self.addimg()
                # 断言是否有提示
                self.assertTrue(self.b.isElementExist('css', '.layui-layer-dialog'), '文件夹名称重复，保存后无提示框弹出')
                self.assertEqual('文件夹名称不能重复',
                                 self.b.by_find_element('css', '.layui-layer-dialog > .layui-layer-content').text,
                                 '文件夹名称重复，提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_028(self):
        """会议资料界面——进入加入文件夹界面，选择全选全选，正常保存"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 输入文件夹名称
            self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').send_keys('这个文件夹没人使用')
            name = self.b.by_find_element('css', '#view > div:nth-child(1) > div:nth-child(1) > textarea').get_attribute('value')
            # 判断查看全选是否选中全选
            if self.b.by_find_element('css', 'div.m-meet-datum-popup-right-hd > div:nth-child(3) > input[type=radio]').is_selected() == False:
                # 选中'全选'权限
                self.b.by_find_element('css',
                                       'div.m-meet-datum-popup-right-hd > div:nth-child(3) > input[type=radio]').click()
            # 点击确定
            self.b.by_find_element('css', '.div_btn.cz').click()
            self.addimg()
            # # 断言是否有提示
            # self.assertEqual('保存成功！', self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text,
            #                  '新建文件夹，提示错误')
            # 点击尾页
            self.b.by_find_element('css', '.pagination-last').click()
            # 获取最后一页所有的文件夹名称
            List = []
            for i in self.b.by_find_elements('css', '.f-text_ellipsis.f-flex-item'):
                List.append(i.text)
            # 断言最后一页是否有新建的文件夹
            self.assertTrue(name in List, '提示新增成功，但列表中无文件夹名称')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_hyzl_at_029(self):
        """会议资料界面——进入加入文件夹界面，选择手选，取消所有参会人员"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 判断查看全选是否选中全选
            if self.b.by_find_element('css', 'div.m-meet-datum-popup-right-hd > div:nth-child(2) > input[type=radio]').is_selected() == False:
                # 选中'全选'权限
                self.b.by_find_element('css',
                                       'div.m-meet-datum-popup-right-hd > div:nth-child(2) > input[type=radio]').click()

            # 点击全选，取消所有参会人员的选择
            self.b.by_find_element('css', 'div.m-meet-datum-popup-right-bd > div > div > h2 > input').click()
            # 点击确定
            self.b.by_find_element('css', '.div_btn.cz').click()
            self.addimg()
            # 断言是否有提示
            self.assertEqual('至少选择一个参会人员', self.b.by_find_element('css', '.layui-layer-content.layui-layer-padding').text,
                             '未选择参会人员，提示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_hyzl_at_030(self):
        """会议资料界面——进入加入文件夹界面，选择手选，取消参会人员，右下角人数更随变化"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击加入文件夹
            self.b.by_find_element('css', '.m-tb-title-btn > div:nth-child(5)').click()
            self.addimg()
            # 判断查看全选是否选中全选
            if self.b.by_find_element('css', 'div.m-meet-datum-popup-right-hd > div:nth-child(2) > input[type=radio]').is_selected() == False:
                # 选中'全选'权限
                self.b.by_find_element('css',
                                       'div.m-meet-datum-popup-right-hd > div:nth-child(2) > input[type=radio]').click()

            # 获取加入文件夹中的总人数
            jcount = self.b.by_find_element('css', 'span.f-fc-blue').text
            jcount = int(jcount[:-1])
            # for n in self.b.by_find_elements('css', 'div.m-meet-datum-popup-right-bd > div > div > ul > li > input'):
            #     n.click()
            #     self.assertEqual(jcount == , '未选择参会人员，提示错误')
            #     if not n.is_selected():
            TO DO
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise




if __name__ == '__main__':
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(Test_PersonneLmanagement)
    suit = unittest.TestSuite()
    # suit.addTest(suit1)
    # suit.addTest(Test_PersonneLmanagement('test_hyzl_at_010'))
    # # suit.addTest(Test_PersonneLmanagement('test_hyzl_at_013'))
    # suit.addTest(Test_meetingdocument('test_hyzl_at_014'))
    # suit.addTest(Test_meetingdocument('test_hyzl_at_015'))
    # suit.addTest(Test_meetingdocument('test_hyzl_at_017'))
    suit.addTest(Test_meetingdocument('test_hyzl_at_029'))
    # suit.addTest(Test_PersonneLmanagement('test_hyzl_at_09'))
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb"),
                           verbosity=2,
                           )
    runer.run(suit)