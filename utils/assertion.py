#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: assertion.py
@time: 2019/9/4 14:05
@desc: 自定义断言方法,断言失败抛出AssertionError
'''


def assertEqual(first,sencond,*msg):
    if first == sencond:
        return True
    else:
        raise AssertionError('%s!=%s'%(first,sencond))

def assertIsNotNone(first,*msg):
    if first is not None:
        return True
    else:
        raise AssertionError('%s is None' % first)
