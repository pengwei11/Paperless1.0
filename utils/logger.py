#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: logger.py
@time: 2019/9/3 9:49
@desc: 用于生成日志文件
'''

from utils.config import Config
import logging
import time
import os
import sys
sys.setrecursionlimit(1000000) #例如这里设置为一百万

class Logger(object):

    def __init__(self,logger):
        '''
        将日志保存到指定的路径文件中
        指定日志的级别，以及调用文件
        '''
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 及时清除handlers 防止重复打印日志
        self.logger.handlers.clear()
        self.sc = Config()
        # 设置输出到日志的头文件
        now = time.strftime("%Y-%m-%d_%H_%M_%S_")
        log_path = self.sc.getLogs_path()
        log_name = log_path+now+'.log'
        filehandles = logging.FileHandler(log_name,encoding='utf-8')
        filehandles.setLevel(logging.INFO)

        # 创建一个输入到控制台的日志文件头
        consolehandles = logging.StreamHandler()
        consolehandles.setLevel(logging.INFO)

        # 将handles进行格式转化
        formaterr = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        filehandles.setFormatter(formaterr)
        consolehandles.setFormatter(formaterr)
        # 将头文件添加至loggin中
        self.logger.addHandler(filehandles)
        self.logger.addHandler(consolehandles)





    def getlog(self):
        return self.logger


if __name__ == '__main__':
    l = Logger('Logger').getlog()
    l.info('a')