#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: testcl.py
@time: 2019/9/9 16:24
@desc:
'''

from selenium import webdriver
from utils.config import Config
from utils.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains   # 鼠标操作
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *   # 导入所有异常类
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait   # 显性等待时间
from selenium.webdriver.common.by import By
from utils import assertion
from BeautifulReport import BeautifulReport
from visualization.PaperlessClient import PaperlessClient

import time
import os

class testcl():
    def __init__(self):
        self.pc = PaperlessClient()


    def test(self):
        print(self.pc.getUrl())
        print(self.pc.getBrowserValue())


if __name__ == '__main__':
    t = testcl()
    t.test()