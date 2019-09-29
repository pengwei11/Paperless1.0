#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: test_nameplatescreen.py
@time: 2019/9/27 14:25
@desc: 铭牌界面设计测试用例
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


class Test_NamePlateScreen(unittest.TestCase):

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
            self.b.by_find_element('link_text', '铭牌设置').click()
            # 进入铭牌界面设计
            self.b.by_find_element('css', '.nameplate_nav.clear > span:nth-child(2)').click()
            time.sleep(1)
        else:
            self.b.by_find_element('link_text', '测试铭牌设置').click()
            # 进入铭牌设置界面
            self.b.by_find_element('link_text', '铭牌设置').click()
            # 进入铭牌界面设计
            self.b.by_find_element('css', '.nameplate_nav.clear > span:nth-child(2)').click()
            time.sleep(1)


    def tearDown(self):
        # 结束用例后先退出浏览器，防止cooking保存
        self.b.QuitBrowser()


    def addimg(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True


    '''铭牌界面设计'''
    def test_mpjm_at_01(self):
        """铭牌界面设计——检查页面标题"""
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


    def test_mpjm_at_02(self):
        """铭牌界面设计——检查顶部标题文字（设计页面）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 获取铭牌设计title
            nametitle = self.b.by_find_element('css', '.nameplate_nav.clear > span:nth-child(2)').text
            self.assertEqual('铭牌界面设计', nametitle, '铭牌界面设计标题显示错误：%s' % nametitle)
            print('铭牌界面设计标题：%s' % nametitle)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_03(self):
        """欢迎界面设计——检查欢迎界面设计功能"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 背景标题
            bgtitle = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[1]/span').text
            self.assertEqual('背景', bgtitle, '背景标题显示错误：%s' % bgtitle)
            # 更换背景颜色
            ghbgs = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[1]/div[1]/label[1]').text
            self.assertEqual('更换背景色', ghbgs, '更换背景颜色文字显示错误：%s' % ghbgs)
            # 更换背景
            ghbg = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[1]/div[1]/label[2]').text
            self.assertEqual('更换背景', ghbg, '更换背景文字显示错误：%s' % ghbg)
            # 更换背景(按钮)
            ghbgan = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[1]/div[2]/div[1]').text
            self.assertEqual('更换背景', ghbgan, '更换背景（按钮）文字显示错误：%s' % ghbgan)


            # 内容标题
            contenttitle = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[2]/span').text
            self.assertEqual('内容', contenttitle, '内容标题显示错误：%s' % contenttitle)
            # 显示职位
            xxzw = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[2]/div/div[1]/div[1]').text
            self.assertEqual('显示职位', xxzw, '显示职位文字显示错误：%s' % xxzw)
            # 显示单位
            xxdw = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[2]/div/div[1]/div[2]').text
            self.assertEqual('显示单位', xxdw, '显示单位文字显示错误：%s' % xxdw)
            # 参会人
            chy = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[2]/div/div[2]/div').text
            self.assertEqual('参会人', chy, '参会人文字显示错误：%s' % chy)


            # 姓名
            xmtitle = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[3]/div[1]/span').text
            self.assertEqual('姓名', xmtitle, '欢迎词标题显示错误：%s' % xmtitle)
            # 字号大小
            zhdx = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[3]/div[1]/div/div[1]').text
            self.assertTrue('字号大小' in zhdx, '字号大小文字显示错误：%s' % zhdx)
            # 字体类型
            zhlx = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[3]/div[1]/div/div[2]').text
            self.assertTrue('字体类型' in zhlx, '字体类型文字显示错误：%s' % zhlx)
            # 文本颜色
            wbys = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[3]/div[1]/div/div[3]').text
            self.assertTrue('文本颜色' in wbys, '文本颜色文字显示错误：%s' % wbys)


            # 操作
            cztitle = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[4]/i').text
            self.assertEqual('操作', cztitle, '操作标题显示错误：%s' % cztitle)
            # 保存
            bc = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[4]/div/button[1]').text
            self.assertEqual('保存', bc, '保存文字显示错误：%s' % bc)
            # 重置
            cz = self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[4]/div/button[2]').text
            self.assertEqual('重置', cz, '重置文字显示错误：%s' % cz)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_04(self):
        """铭牌界面设计——查看'更换背景','更换背景色'是否被选中其中一个"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            self.assertTrue(self.b.by_find_element('css', '.label_one > input[name=usebcolor]').is_selected() or
                            self.b.by_find_element('css', '.label_two > input[name=usebcolor]').is_selected(),
                            '更换背景和更换背景色都未被选中')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_05(self):
        """铭牌界面设计——'更换背景色'选中（后方出现颜色选择器）"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 判断'更换背景色'是否被选中
            if self.b.by_find_element('css', '.label_one > input[name=usebcolor]').is_selected():
                self.assertTrue(self.b.isElementExist('css', '#cp1'), '更换背景色被选中,颜色选择器不存在')
                self.assertTrue(self.b.isElementExist('css', '#color-background'), '更换背景色被选中,颜色下拉框不存在')
            else:
                self.b.by_find_element('css', '.label_one > input[name=usebcolor').click()
                self.addimg()
                self.assertTrue(self.b.isElementExist('css', '#cp1'), '更换背景色被选中,颜色选择器不存在')
                self.assertTrue(self.b.isElementExist('css', '#color-background'), '更换背景色被选中,颜色下拉框不存在')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_06(self):
        """铭牌界面设计——更换背景色(该用例请运行结果未必准确，请查看截图)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 判断'更换背景色'是否被选中
            if self.b.by_find_element('css', '.label_one > input[name=usebcolor]').is_selected():
                # 点击颜色选择器
                self.b.by_find_element('css', '#color-background').click()
            else:
                # 点击更换背景颜色选择按钮
                self.b.by_find_element('css', '.label_one > input[name=usebcolor]').click()
                # 点击颜色选择器
                self.b.by_find_element('css', '#color-background').click()
            # 循环所有的colorpicker选择器
            for i in self.b.by_find_elements('css', '.colorpicker'):
                if i.is_displayed():
                    # 清空颜色输入框
                    i.find_element_by_css_selector('.colorpicker_hex > input').clear()
                    # 颜色输入
                    i.find_element_by_css_selector('.colorpicker_hex > input').send_keys('0066ff')
                    i.find_element_by_css_selector('.colorpicker_submit').click()
                    self.addimg()
                    # 点击颜色选择器，获取RGB数值
                    self.b.by_find_element('css', '#color-background').click()
                    # 获取R值
                    R = i.find_element_by_css_selector('.colorpicker_rgb_r > input').get_attribute('value')
                    # 获取G值
                    G = i.find_element_by_css_selector('.colorpicker_rgb_g > input').get_attribute('value')
                    # 获取B值
                    B = i.find_element_by_css_selector('.colorpicker_rgb_b > input').get_attribute('value')
                    # 获取设计面板的背景颜色
                    style = self.b.by_find_element('css', '#bgDiv').get_attribute('style')
                    self.assertTrue(R and G and B in style, '设计面板颜色未改变')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_07(self):
        """铭牌界面设计——点击更换背景，查看是否出现背景选择框"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 判断'更换背景'是否被选中
            if self.b.by_find_element('css', '.label_two > input[name=usebcolor]').is_selected():
                # 点击'更换背景'
                self.b.by_find_element('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                              'div.nax_one.f-flex-content > '
                                              'div.clear.f-flex-item.f-nameplate-left-btn-box > div.o_o').click()
            else:
                # 点击更换背景选择按钮
                self.b.by_find_element('css', '.label_two > input[name=usebcolor]').click()
                # 点击'更换背景'
                self.b.by_find_element('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                              'div.nax_one.f-flex-content > '
                                              'div.clear.f-flex-item.f-nameplate-left-btn-box > div.o_o').click()
            self.addimg()
            self.assertTrue(self.b.isElementExist('css', '.layer-ext-espresso'), '点击更换背景，未出现背景选择框')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_08(self):
        """铭牌界面设计——更换自带背景(该用例请运行结果未必准确，请查看截图)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 判断'更换背景'是否被选中
            if self.b.by_find_element('css', '.label_two > input[name=usebcolor]').is_selected():
                # 点击'更换背景'
                self.b.by_find_element('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                              'div.nax_one.f-flex-content > '
                                              'div.clear.f-flex-item.f-nameplate-left-btn-box > div.o_o').click()
            else:
                # 点击更换背景选择按钮
                self.b.by_find_element('css', '.label_two > input[name=usebcolor]').click()
                # 点击'更换背景'
                self.b.by_find_element('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                              'div.nax_one.f-flex-content > '
                                              'div.clear.f-flex-item.f-nameplate-left-btn-box > div.o_o').click()
            # 选择第三个背景
            self.b.by_find_element('css', '#mCSB_1_container > ul > li:nth-child(3) > a > img').click()
            # 点击确定
            self.b.by_find_element('css', '#nameplate-img').click()
            self.addimg()
            # 获取背景的src
            src = self.b.by_find_element('css', '#mCSB_1_container > ul > li:nth-child(3) > a > img').get_attribute('src')
            # 获取背景板的style
            style = self.b.by_find_element('css', '#bgDiv').get_attribute('style')
            src = src[-14:]
            self.assertTrue(src in style, '背景更换失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_09(self):
        """铭牌界面设计——更换本地背景(该用例请运行结果未必准确，请查看截图)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 判断'更换背景'是否被选中
            if self.b.by_find_element('css', '.label_two > input[name=usebcolor]').is_selected():
                # 点击'更换背景'
                self.b.by_find_element('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                              'div.nax_one.f-flex-content > '
                                              'div.clear.f-flex-item.f-nameplate-left-btn-box > div.o_o').click()
            else:
                # 点击更换背景选择按钮
                self.b.by_find_element('css', '.label_two > input[name=usebcolor]').click()
                # 点击'更换背景'
                self.b.by_find_element('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                              'div.nax_one.f-flex-content > '
                                              'div.clear.f-flex-item.f-nameplate-left-btn-box > div.o_o').click()
            # 选择本地背景
            self.b.by_find_element('css', '.webuploader-element-invisible').send_keys('D:\\无纸化测试文件\\测试图片.png')
            self.addimg()
            # 获取背景板的style
            style = self.b.by_find_element('css', '#bgDiv').get_attribute('style')
            self.assertTrue('/public/prapeless/img/' in style, '背景更换失败')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_010(self):
        """铭牌界面设计——'显示职位'显示与隐藏(该用例请运行结果未必准确，请查看截图)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击显示职务
            self.b.by_find_element('css', '#showrank').click()
            self.addimg()
            # 判断'显示职位'是否被选中
            if self.b.by_find_element('css', '#showrank').is_selected():
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextB').is_displayed() == True, '显示职位被选中，背景板未显示职务')
            else:
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextB').is_displayed() == False, '显示职位未选中，背景板显示职务')
            # 点击显示职务
            self.b.by_find_element('css', '#showrank').click()
            self.addimg()
            # 判断'显示职位'是否被选中
            if self.b.by_find_element('css', '#showrank').is_selected():
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextB').is_displayed() == True, '显示职位被选中，背景板未显示职务')
            else:
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextB').is_displayed() == False, '显示职位未选中，背景板显示职务')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_011(self):
        """铭牌界面设计——'显示单位'显示与隐藏(该用例请运行结果未必准确，请查看截图)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击显示单位
            self.b.by_find_element('css', '#showcompany').click()
            self.addimg()
            # 判断'显示单位'是否被选中
            if self.b.by_find_element('css', '#showcompany').is_selected():
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextC').is_displayed() == True, '显示单位被选中，背景板未显示单位')
            else:
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextC').is_displayed() == False, '显示单位未选中，背景板显示单位')
            # 点击显示单位
            self.b.by_find_element('css', '#showcompany').click()
            self.addimg()
            # 判断'显示单位'是否被选中
            if self.b.by_find_element('css', '#showcompany').is_selected():
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextC').is_displayed() == True, '显示单位被选中，背景板未显示单位')
            else:
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextC').is_displayed() == False, '显示单位未选中，背景板显示单位')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_012(self):
        """铭牌界面设计——'参会人'显示与隐藏(该用例请运行结果未必准确，请查看截图)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            # 点击参会人
            self.b.by_find_element('css', '#showusername').click()
            self.addimg()
            # 判断'参会人'是否被选中
            if self.b.by_find_element('css', '#showusername').is_selected():
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextA').is_displayed() == True, '参会人被选中，背景板未显示参会人')
            else:
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextA').is_displayed() == False, '参会人未选中，背景板显示参会人')
            # 点击参会人
            self.b.by_find_element('css', '#showusername').click()
            self.addimg()
            # 判断'参会人'是否被选中
            if self.b.by_find_element('css', '#showusername').is_selected():
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextA').is_displayed() == True, '参会人被选中，背景板未显示参会人')
            else:
                self.assertTrue(self.b.by_find_element('css', '#dragDivTextA').is_displayed() == False, '参会人未选中，背景板显示参会人')
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_013(self):
        """欢迎界面设计——铭牌保存(更换背景，取消内容显示后保存)"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 判断'更换背景'是否被选中
            if self.b.by_find_element('css', '.label_two > input[name=usebcolor]').is_selected():
                # 点击'更换背景'
                self.b.by_find_element('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                              'div.nax_one.f-flex-content > '
                                              'div.clear.f-flex-item.f-nameplate-left-btn-box > div.o_o').click()
            else:
                # 点击更换背景选择按钮
                self.b.by_find_element('css', '.label_two > input[name=usebcolor]').click()
                # 点击'更换背景'
                self.b.by_find_element('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                              'div.nax_one.f-flex-content > '
                                              'div.clear.f-flex-item.f-nameplate-left-btn-box > div.o_o').click()
            self.addimg()
            # 选择本地背景
            self.b.by_find_element('css', '.webuploader-element-invisible').send_keys('D:\\无纸化测试文件\\测试图片.png')
            # 循环取消所有的内容显示
            for i in self.b.by_find_elements('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > div.nax_two.clear.f-flex-content > div > div > div > input'):
                logger.info('进入了吗')
                if i.is_selected():
                    logger.info('进入了')
                    i.click()
                    self.addimg()
            # 点击保存
            self.b.by_find_element('xpath', '//*[@id="form_rename"]/div[2]/div[1]/div[4]/div/button[1]').click()
            self.addimg()
            # 循环内容显示选中状态，并断言
            for i in self.b.by_find_elements('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                                    'div.nax_two.clear.f-flex-content > div > div > input'):
                self.assertTrue(i.is_selected() == False, '保存刷新页面后，%s显示选中状态' % i.find_element_by_xpath('..').text)
            for j in self.b.by_find_elements('css', '#bgDiv > div'):
                self.assertTrue(j.is_displayed() == False, '保存刷新页面后，%s显示在背景板中' % j.text)
            logger.info('用例%s执行成功' % sys._getframe().f_code.co_name)
        except:
            logger.exception('用例%s执行失败' % sys._getframe().f_code.co_name)
            raise


    def test_mpjm_at_014(self):
        """欢迎界面设计——重置"""
        try:
            logger.info('开始执行用例%s' % sys._getframe().f_code.co_name)
            self.addimg()
            # 点击重置
            self.b.by_find_element('css', '#namplate-reset').click()
            # 点击确定
            self.b.by_find_element('css', '.layui-layer-btn0').click()
            time.sleep(1)
            # 进入铭牌界面设计
            self.b.by_find_element('css', '.nameplate_nav.clear > span:nth-child(2)').click()
            time.sleep(1)
            self.addimg()
            # 循环内容显示选中状态，并断言
            for i in self.b.by_find_elements('css', '#form_rename > div.nax > div.m-nameplate-left-content.fl > '
                                                    'div.nax_two.clear.f-flex-content > div > div > input'):
                self.assertTrue(i.is_selected() == True, '保存刷新页面后，%s显示选中状态' % i.find_element_by_xpath('..').text)
            for j in self.b.by_find_elements('css', '#bgDiv > div'):
                if j.get_attribute('id') == 'dragDivM':
                    continue
                self.assertTrue(j.is_displayed() == True, '保存刷新页面后，%s未显示在背景板中' % j.text)
            # 获取设计面板的背景
            style = self.b.by_find_element('css', '#bgDiv').get_attribute('style')
            self.assertTrue('/image/005.png' in style, '背景未重置')
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
    suit.addTest(Test_NamePlateScreen('test_mpjm_at_014'))

    # suit.addTest(Test_NamePlateScreen('test_mpjm_at_012'))
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report1.html", "wb"),
                           verbosity=2,
                           )
    runer.run(suit)