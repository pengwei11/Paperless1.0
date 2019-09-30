#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: test_copywritingdesign.py
@time: 2019/9/29 10:44
@desc:文案设计测试用例
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


class Test_CopywritingDesign(unittest.TestCase):

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
            # 进入铭牌设置界面
            self.b.by_find_element('link_text', '铭牌设置').click()
            # 进入文案界面设计
            self.b.by_find_element('css', '.nameplate_nav.clear > span:nth-child(3)').click()
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
            # 进入铭牌设置界面
            self.b.by_find_element('link_text', '铭牌设置').click()
            # 进入文案界面设计
            self.b.by_find_element('css', '.nameplate_nav.clear > span:nth-child(3)').click()
            time.sleep(1)


    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()


    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True


    '''文案界面设计'''
    def test_wajm_at_01(self):
        """文案界面设计——检查页面标题"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 获取页面title
            title = self.b.by_find_element('css', '.personnel.fl').text
            self.assertEqual('铭牌设置', title, '页面标题显示错误：%s' % title)
            print('\n页面标题：%s' % title)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_wajm_at_02(self):
        """文案界面设计——检查页面标题"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 获取文案设计title
            documenttitle = self.b.by_find_element('css', '.nameplate_nav.clear > span:nth-child(3)').text
            self.assertEqual('文案设计', documenttitle, '文案设计标题显示错误：%s' % documenttitle)
            print('\n文案界面标题：%s' % documenttitle)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_wajm_at_03(self):
        """文案界面设计——文案设计字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言姓名显示是否存在
            self.assertEqual('姓名显示', self.b.by_find_element('css', 'div.datagrid-view2 > div.datagrid-header > div '
                                                                    '> table > tbody > tr > td:nth-child(1) > '
                                                                    'div > span:nth-child(1)').text, '姓名显示不存在或显示错误')
            # 断言单位显示是否存在
            self.assertEqual('单位显示', self.b.by_find_element('css', 'div.datagrid-view2 > div.datagrid-header > div '
                                                                    '> table > tbody > tr > td:nth-child(2) > '
                                                                    'div > span:nth-child(1)').text, '单位显示不存在或显示错误')
            # 断言职务显示是否存在
            self.assertEqual('职务显示', self.b.by_find_element('css', 'div.datagrid-view2 > div.datagrid-header > div '
                                                                    '> table > tbody > tr > td:nth-child(3) > '
                                                                    'div > span:nth-child(1)').text, '职务显示不存在或显示错误')
            # 断言预览是否存在
            self.assertEqual('预览', self.b.by_find_element('css', 'div.datagrid-view2 > div.datagrid-header > div '
                                                                    '> table > tbody > tr > td:nth-child(4) > '
                                                                    'div > span:nth-child(1)').text, '预览不存在或显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise



    def test_wajm_at_04(self):
        """文案界面设计——文案设计参会人员字段显示"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 断言序号是否存在
            self.assertTrue(self.b.isElementExist('css', '#datagrid-row-r2-1-0 > td > div'),
                            '序号不存在或显示错误')
            # 断言姓名是否存在
            self.assertTrue(self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(1) > div'),
                            '姓名不存在或显示错误')
            # 断言单位是否存在
            self.assertTrue(self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(2) > div'),
                            '单位不存在或显示错误')
            # 断言职务是否存在
            self.assertTrue(self.b.isElementExist('css', '#datagrid-row-r2-2-0 > td:nth-child(3) > div'),
                            '职务不存在或显示错误')
            # 断言操作'欢迎界面'是否存在
            self.assertEqual('欢迎界面', self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(4) '
                                                                 '> div > a:nth-child(1)').text, '操作(欢迎界面)不存在或显示错误')
            # 断言操作'铭牌'是否存在
            self.assertEqual('铭牌', self.b.by_find_element('css', '#datagrid-row-r2-2-0 > td:nth-child(4) '
                                                                 '> div > a:nth-child(2)').text, '操作(铭牌)不存在或显示错误')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_wajm_at_05(self):
        """文案界面设计——每页显示10条数据"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 分页下拉框选择10条/页
            Select(self.b.by_find_element('css', '.pagination-page-list')).select_by_visible_text('10')
            self.addimg()
            List = []
            # 循环整个参会人员，添加进集合，计算本页有多少条数据
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            self.assertTrue(len(List) <= 10, '超出10条数据')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_wajm_at_06(self):
        """文案界面设计——每页显示20条数据"""
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

    def test_wajm_at_07(self):
        """文案界面设计——每页显示50条数据"""
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


    def test_wajm_at_08(self):
        """文案界面设计——每页显示100条数据"""
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


    def test_wajm_at_09(self):
        """文案界面设计——首页图标点击"""
        # 点击首页图标，需要回到第一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
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


    def test_wajm_at_010(self):
        """文案界面设计——尾页图标点击"""
        # 点击尾页图标，需要前往最后一页数据
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击尾页
            self.b.by_find_element('css', '.pagination-last').click()
            self.addimg()
            time.sleep(1)
            # 获取总页数
            count = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear >'
                                           ' div > div.nameplate_box > div > div.nameplate_w > div > '
                                           'div:nth-child(3) > div > div > div > div.datagrid-pager.pagination >'
                                           ' table > tbody > tr > td:nth-child(8) > span').text
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



    def test_wajm_at_011(self):
        """文案界面设计——下一页图标点击"""
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
            count = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear >'
                                           ' div > div.nameplate_box > div > div.nameplate_w > div > '
                                           'div:nth-child(3) > div > div > div > div.datagrid-pager.pagination >'
                                           ' table > tbody > tr > td:nth-child(8) > span').text
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


    def test_wajm_at_012(self):
        """文案界面设计——上一页图标点击"""
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


    def test_wajm_at_013(self):
        """文案界面设计——页数搜索（页数框输入小于1的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 页数框输入0
            self.b.by_find_element('css','.pagination-num').send_keys(0)
            self.addimg()
            # 模拟键盘回车
            self.b.by_find_element('css', '.pagination-num ').send_keys(Keys.ENTER)
            time.sleep(1)
            self.addimg()
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


    def test_wajm_at_014(self):
        """文案界面设计——页数搜索（页数框输入大于总页数的数）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 清空页数框
            self.b.by_find_element('css','.pagination-num').clear()
            # 获取总页数
            count = self.b.by_find_element('css',
                                           '#wrap > div > div.matter.clear > div.right_w.fr.clear >'
                                           ' div > div.nameplate_box > div > div.nameplate_w > div > '
                                           'div:nth-child(3) > div > div > div > div.datagrid-pager.pagination >'
                                           ' table > tbody > tr > td:nth-child(8) > span').text
            # 截取共X页中的数字
            count = count[1:-1]
            # 页数框输入总页数+1
            self.b.by_find_element('css', '.pagination-num').send_keys(int(count)+1)
            self.addimg()
            # 模拟键盘回车
            self.b.by_find_element('css', '.pagination-num ').send_keys(Keys.ENTER)
            time.sleep(1)
            self.addimg()
            # 获取跳转后的输入框值
            sum2 = self.b.by_find_element('css', 'input.pagination-num').get_attribute('value')
            self.assertTrue(sum2 == count, '跳转至%s页，跳转框数字为%s' % (int(count)+1, sum2))
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_wajm_at_015(self):
        # 正确跳转界面暂时无法编写，数据无法创建过多
        print('暂时未编写')
        pass

    def test_wajm_at_016(self):
        """文案界面设计——总X数显示（总页数测试）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('css', '.pagination-last').click()  # 点击尾页
            time.sleep(1)
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
                List.append(l)
            # 获取跳转框页码，
            sum2 = int(self.b.by_find_element('css', 'input.pagination-num').get_attribute('value'))
            # 计算总数据：(页码-1)*每页数据条数+最后一页数据
            if sum2 == 0 or sum2 == 1:
                count = int(len(List))
            else:
                count = (sum2 - 1) * int(sum1) + int(len(List))
            # 获取总页数
            number = self.b.by_find_element('css', '#wrap > div > div.matter.clear > div.right_w.fr.clear >'
                                           ' div > div.nameplate_box > div > div.nameplate_w > div > '
                                           'div:nth-child(3) > div > div > div > div.datagrid-pager.pagination >'
                                           ' table > tbody > tr > td:nth-child(8) > span').text
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


    def test_wajm_at_017(self):
        """文案界面设计——分组条数显示（左下角的分组记录显示）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 获取每页数据量,默认为10条/页
            sum1 = Select(self.b.by_find_element('css', '.pagination-page-list')).all_selected_options[0].text
            self.b.by_find_element('css', '.pagination-last').click()  # 点击尾页
            time.sleep(1)
            self.addimg()
            List = []
            # 获取最后一页数据
            for l in self.b.by_find_elements('css', '.datagrid-cell-rownumber'):
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

if __name__ == '__main__':
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(Test_PersonneLmanagement)
    suit = unittest.TestSuite()
    # suit.addTest(suit1)
    # suit.addTest(Test_PersonneLmanagement('test_chry_at_010'))
    # suit.addTest(Test_PersonneLmanagement('test_chry_at_013'))
    # suit.addTest(Test_CopywritingDesign('test_wajm_at_09'))
    # suit.addTest(Test_CopywritingDesign('test_wajm_at_010'))
    # suit.addTest(Test_CopywritingDesign('test_wajm_at_011'))
    suit.addTest(Test_CopywritingDesign('test_wajm_at_017'))
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report2.htm", "wb"),
                           verbosity=2,
                           )
    runer.run(suit)