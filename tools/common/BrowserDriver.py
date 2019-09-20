#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: BrowserDriver.py
@time: 2019/9/2 16:54
@desc: 浏览器操作封装
'''

from selenium import webdriver
from utils.config import Config
from utils.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains   # 鼠标操作
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *   # 导入所有异常类
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait   # 显性等待时间
from selenium.webdriver.common.by import By

import time
import os

logger = Logger(logger='BrowserDriver').getlog()

class BrowserDriver(object):

    def __init__(self):
        self.sc = Config()
        self.imgs = []


    '''浏览器操作'''

    def OpenBrowser(self):
        '''
        打开浏览器，从Browser.yaml文件中读取浏览器和网址
        :return:
        '''
        # browser = self.sc.getReadIP('browser')  # 从tkinter中的输入框获取浏览器类型
        browser = self.sc.getConfig('Browser').get('browser')   # 从Browser.yaml文件中获取浏览器类型
        logger.info("选择的浏览器为:%s浏览器"%browser)
        # url = self.sc.getReadIP('ip')   # 从tkinter中的输入框获取浏览器地址
        url = self.sc.getConfig('pathUrl').get('URL') # 从Browser.yaml文件中获取网址
        if browser == 'Google Chrome':
            option = Options()
            option.add_experimental_option('w3c', False)
            self.driver = webdriver.Chrome(options=option)
            self.driver.maximize_window()
            logger.info('启动谷歌浏览器')
        elif browser == 'Firefox':
            self.driver = webdriver.Firefox()
            self.driver.maximize_window()
            logger.info('启动火狐浏览器')


        self.driver.get('http://%s'%url)
        logger.info('进入%s'%url)
        self.driver.maximize_window()
        logger.info('最大化浏览器')
        self.driver.implicitly_wait(5)
        logger.info('5秒隐形等待时间')
        return self.driver


    def QuitBrowser(self):
        '''
        关闭浏览器
        :return:
        '''
        self.driver.close()
        logger.info('关闭浏览器')


    def quit(self):
        '''
        退出浏览器
        :return:
        '''
        self.driver.quit()
        logger.info('退出浏览器')


    def back(self):
        '''
        退回浏览器上一个页面
        :return:
        '''
        if self.driver.current_url == 'data:,':
            self.driver.back()
            logger.info('返回到%s'%self.driver.current_url)
        else:
            logger.info('已经是第一个页面')
            return



    def foword(self):
        '''
        前进浏览器上一个页面
        :return:
        '''
        self.driver.forward()
        logger.info('前进到%s'%self.driver.current_url)


    def js_scroll_top(self):
        '''滚动到顶部'''
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)


    def js_scroll_end(self):
        '''滚动到底部'''
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)

    '''selenium框架二次封装'''

    # 获取页面title
    def get_page_title(self):
        logger.info('当前页面的title为:%s'%self.driver.title)
        return self.driver.title


    def wait_find_element(self, *loc):
        '''
        显性等待30S判断单个元素是否可见，可见返回元素，否则抛出异常
        :param loc: 传入参数为By.xx(xx为元素定位方式),Value(为元素定位内容)
        :return:
        '''
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of(self.driver.find_element(*loc)))
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            logger.exception('找不到元素')
        except TimeoutException:
            logger.exception('元素查找超时')
        except:
            logger.exception('查找失败')


    def wait_find_elements(self, *loc):
        '''
        显性等待30S判断元素组是否可见，可见返回元素，否则抛出异常
        :param loc: 传入参数为By.xx(xx为元素定位方式),Value(为元素定位内容)
        :return:
        '''
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of(self.driver.find_elements(*loc)))
            return self.driver.find_elements(*loc)
        except NoSuchElementException:
            logger.exception('找不到元素')
        except TimeoutException:
            logger.exception('元素查找超时')

    #   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def isElementExist(self,*loc):
        flag = True
        try:
            if loc[0] == 'id' or loc[0] == 'ID':
                return self.driver.find_element_by_id(loc[1])
            elif loc[0] == 'name' or loc[0] == 'NAME':
                return self.driver.find_element_by_name(loc[1])
            elif loc[0] == 'class' or loc[0] == 'CLASS':
                return self.driver.find_element_by_class_name(loc[1])
            elif loc[0] == 'xpath' or loc[0] == 'XPATH':
                return self.driver.find_element_by_xpath(loc[1])
            elif loc[0] == 'link_text' or loc[0] == 'LINK_TEXT':
                return self.driver.find_element_by_link_text(loc[1])
            elif loc[0] == 'css' or loc[0] == 'CSS':
                return self.driver.find_element_by_css_selector(loc[1])
            elif loc[0] == 'tag_name' or loc[0] == 'TAG_NAME':
                return self.driver.find_element_by_tag_name(loc[1])
            return flag
        except:
            flag = False
            return flag

    def get_screent_img(self,value):
        '''
        获取页面截图方法
        :param value: 截图名称
        :return:
        注：HTMLTestRunner自带失败截图
        '''
        image_path = self.sc.getScreenshots_path()
        now = time.strftime('%Y-%m-%d_%H_%M_%S_')
        # screen_name = now+value+'.png'
        try:
            self.imgs.append(self.driver.get_screenshot_as_file(image_path+'%s%s.png'%(now,value)))
            logger.info('截图成功，图片在%s中'%image_path)
        except NameError as ne:
            self.get_screent_img(value)
            logger.exception('截图失败')

    def save_img(self,img_name):
        '''
        :return:BeauifulReport截图方法
        '''
        image_path = self.sc.getScreenshots_path()
        now = time.strftime('%Y-%m-%d_%H_%M_%S_')
        try:
            self.driver.get_screenshot_as_file('{}/{}.png'.format(os.path.abspath(image_path),(now+img_name)))
            logger.info('截图成功，图片在%s中'%image_path)
        except:
            self.save_img(img_name)
            logger.info('截图失败')


    def move_to_element(self,*loc):
        '''
        :param loc:loc = (By.xx,element)
        :return:
        '''
        try:
            element = self.driver.find_element(*loc)
            t = self.driver.find_element(*loc).text
            ActionChains(self.driver).move_to_element(element).perform()
            logger.info("鼠标悬浮在%s"%t)
        except:
            logger.exception("未找到元素")


    def by_find_element(self,*loc):
        '''
        封装单个元素定位
        :param loc: *loc=(type,element)
        :return:
        '''
        try:
            if loc[0] == 'id' or loc[0] == 'ID':
                return self.driver.find_element_by_id(loc[1])
            elif loc[0] == 'name' or loc[0] == 'NAME':
                return self.driver.find_element_by_name(loc[1])
            elif loc[0] == 'class' or loc[0] == 'CLASS':
                return self.driver.find_element_by_class_name(loc[1])
            elif loc[0] == 'xpath' or loc[0] == 'XPATH':
                return self.driver.find_element_by_xpath(loc[1])
            elif loc[0] == 'link_text' or loc[0] == 'LINK_TEXT':
                return self.driver.find_element_by_link_text(loc[1])
            elif loc[0] == 'css' or loc[0] == 'CSS':
                return self.driver.find_element_by_css_selector(loc[1])
            elif loc[0] == 'tag_name' or loc[0] == 'TAG_NAME':
                return self.driver.find_element_by_tag_name(loc[1])
        except:
            logger.exception('请检查定位方式或元素')

    def by_find_elements(self,*loc):
        '''
        封装元素定位
        :param loc: *loc=(type,element)
        :return:
        '''
        try:
            if loc[0] == 'id' or loc[0] == 'ID':
                return self.driver.find_elements_by_id(loc[1])
            elif loc[0] == 'name' or loc[0] == 'NAME':
                return self.driver.find_elements_by_name(loc[1])
            elif loc[0] == 'class' or loc[0] == 'CLASS':
                return self.driver.find_elements_by_class_name(loc[1])
            elif loc[0] == 'xpath' or loc[0] == 'XPATH':
                return self.driver.find_elements_by_xpath(loc[1])
            elif loc[0] == 'link_text' or loc[0] == 'LINK_TEXT':
                return self.driver.find_elements_by_link_text(loc[1])
            elif loc[0] == 'css' or loc[0] == 'CSS':
                return self.driver.find_elements_by_css_selector(loc[1])
            elif loc[0] == 'tag_name' or loc[0] == 'TAG_NAME':
                return self.driver.find_elements_by_tag_name(loc[1])
        except:
            logger.exception('请检查定位方式或元素')








if __name__ == '__main__':
    b = BrowserDriver()
    b.OpenBrowser()
    print(b.get_page_title())
    # assertion.assertEqual('无纸化会议1',b.get_page_title())
    b.by_find_element('name','account').send_keys('admin')
    b.by_find_element('name','password').send_keys('admin')
    # b.by_find_element('id','login').click()
    # time.sleep(3)
    # b.by_find_element('xpath','//*[@id="wrap"]/div/div[1]/div/div[3]/i[1]').click()
    # b.by_find_element('xpath','//*[@id="layui-layer1"]/div[3]/a[1]').click()
    # print(b.wait_find_element(By.ID, 'logi1n'))
    # b.get_screent_img('进入网址')
    # b.QuitBrowser()
    # b.move_to_element(By.CLASS_NAME,'registe1r')
    # b.get_screent_img('进入网址')b
    # b.by_find_element('id','login').click()

    # b.foword()
    # b.back()

