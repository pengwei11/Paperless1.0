#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: config.py
@time: 2019/8/30 16:41
@desc: 读取yaml文件中的配置
'''

import os
from utils import file_read
from utils.file_read import YamlRead
import sys
sys.setrecursionlimit(5000)


# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(BASE_PATH ,'config','browser.yaml')
IP_PATH = os.path.join(BASE_PATH,'config\\','ip.yaml')
CASENAME_PATH = os.path.join(BASE_PATH,'config\\','casename.yaml')
DRIVER_PATH = os.path.join(BASE_PATH,'drivers','chromedriver.exe')
LOGS_PATH = os.path.join(BASE_PATH,'logs\\')
REPORT_PATH = os.path.join(BASE_PATH,'report\\')
SCREENSHOTS_PATH = os.path.join(BASE_PATH,'screenshots\\')
TEST_PATH = os.path.join(BASE_PATH,'test')
UTILS_PATH = os.path.join(BASE_PATH,'utils')


# test各个目录下的绝度路径
WEB_URL_PATH = os.path.join(TEST_PATH,'page','Web_Url.yaml')
AUTOLT_PATH = os.path.join(TEST_PATH,'Autolt')
CASE_PATH = os.path.join(TEST_PATH,'case')
COMMON_PATH = os.path.join(TEST_PATH,'common')
PAGE_PATH = os.path.join(TEST_PATH,'page')
SQLCONF_PATH = os.path.join(TEST_PATH,'sqlconf')

class Config:

    def __init__(self, config=CONFIG_PATH, chrome=DRIVER_PATH, screenshots=SCREENSHOTS_PATH, report=REPORT_PATH,
                 test=TEST_PATH, logs=LOGS_PATH, ip=IP_PATH, casename=CASENAME_PATH):
        self.config = YamlRead(config).data
        self.ipconfig = YamlRead(ip).data
        self.casenameconfig = YamlRead(casename).data
        self.driver_pt = chrome
        self.sc = screenshots
        self.report_path = report
        self.test_path = test
        self.logs_path = logs
        self.ip_path = ip
        self.casename_path = casename


    # 读取browser.yaml文件的内容
    def getConfig(self,element,index = 0):

        """
        yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。可以在框架中实现多个项目的测试。
        获取config文件夹中yaml文件的值
        """
        return self.config[index].get(element)

    # 获取ip.yaml文件的内容
    def getReadIP(self,element,index=0):
        return self.ipconfig[index].get(element)

    # 获取casename.yaml文件的内容
    def getReadCasename(self,element,index=0):
        return self.casenameconfig[index].get(element)

    def getDriver_path(self):
        return self.driver_pt

    def getScreenshots_path(self):
        return self.sc

    def getReport_path(self):
        return self.report_path

    def getTest_path(self):
        return self.test_path

    def getLogs_path(self):
        return self.logs_path
    #
    # def getCreateIP_path(self):
    #     return self.ip_path.replace('\\','/')

    # 命名有点问题，暂时先不改
    def getWriteIP(self):
        return self.ip_path

    def getCasename_path(self):
        return self.casename_path






if __name__ == '__main__':
    c = Config()
    print(c.getConfig('pathUrl').get('URL'))
    print(type(c.getConfig('Browser')))
    browsers = c.getConfig('Browser')
    print(c.getReadIP('IP'))
    ListValue = []
    for key,value in browsers.items():
        ListValue.append(value)
    print(ListValue[0])
    # print(c.getLogs_path())
    # print(c.methods())
    # print(dir(file_read))
    # for root, dirs, files in os.walk(c.getTest_path()):
    #         print(root)  # 当前目录路径
    #         print(dirs)  # 当前路径下所有子目录
    #         print(files)  # 当前路径下所有非目录子文件
    # print(c.getDriver_path())
    # # print(c.getScreenshots())
    # print(c.getReport_paht())
    L = []
    # s = []
    # for root, dirs, files in os.walk(c.getTest_path()):
    #     for file in files:
    #         if os.path.splitext(file)[1] == '.py':
    #         #     if os.path.split(file)[1] in 'test':
    #                 L.append(os.path.join(root, file))
    # print(L)



