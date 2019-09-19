#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: DQ.py
@time: 2019/9/12 15:16
@desc:
'''

import os
import importlib
import glob
from test.login import test_login


def get_modules(self,package="."):
        """
        获取包名下所有非__init__的模块名
        """
        modules = []
        files = os.listdir(package)

        for file in files:
            if not file.startswith("__"):
                name, ext = os.path.splitext(file)
                modules.append("." + name)

        return modules

def getmembers(self,klass, members=None):
        # get a list of all class members, ordered by class
        if members is None:
            members = []
        for k in klass.__bases__:
            self.getmembers(k, members)
        for m in dir(klass):
            if m not in members:
                members.append(m)
                return members

def getchfoldpath(root_path, n = 1):
    root_depth = len(root_path.split(os.path.sep))
    c = []
    for root, dirs, files in os.walk(root_path, topdown=True):
        for name in dirs:
            dir_path = os.path.join(root, name)
            dir_depth = len(dir_path.split(os.path.sep))
            if  dir_depth == root_depth + n:
                c.append(dir_path)
            else:
                break
    return c


if __name__ == '__main__':
    # package = "E:\\Paperless1.0\\test\\login"
    # modules = get_modules(package)
    #
    # # 将包下的所有模块，逐个导入，并调用其中的函数
    # for module in modules:
    #     module = importlib.import_module(module, package)
    #
    #     for attr in dir(module):
    #         if not attr.startswith("__"):
    #             func = getattr(module, attr)
    #             func()

    for f in glob.iglob('E:\\Paperless1.0\\test\\*',recursive=True):
       for a in glob.iglob(f+'\\test_*',recursive=True):
           print(dir(a))
    print(dir(test_login))
    print(getchfoldpath('E:\\Paperless1.0\\test\\login\\',0))