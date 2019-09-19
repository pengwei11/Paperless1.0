#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: file_write.py
@time: 2019/8/30 14:46
@desc: 用于操控yaml,excel文件写入,
'''

import os
import yaml
import xlrd
import xlwt
from ruamel import yaml
from openpyxl import workbook
from xlutils import copy
from utils.logger import Logger
from utils.config import Config

logger = Logger('logger').getlog()

class ExcelWrite:

    '''用于新建工作簿'''
    def create_excel_xlsx(self,filename,sheet_name):
        if os.path.exists(filename):
            print('文件已经存在')
            return
        else:
            workbook=xlwt.Workbook(encoding='UTF-8')
            sheet = workbook.add_sheet(sheet_name)
            workbook.save(filename)


    def write_excel_xlsx(self,filename,*value):
        index = len(value)
        workbook1 = xlrd.open_workbook(filename)
        sheets = workbook1.sheet_names()
        worksheet = workbook1.sheet_by_name(sheets[0])
        rows_old = worksheet.nrows
        new_workbook1 = copy.copy(workbook1)
        new_worksheet = workbook1.get_sheet(0)
        for i in range(0,index):
            for j in range(0,len(value[i])):
                new_worksheet.write(i+rows_old,j,value[i][j])
                new_workbook1.sava(filename)


class YamlWrite(object):

    def __init__(self):
        self.sc = Config()

    def Write_Yaml(self,filename,value):
        try:
            if filename in '\\':
                filename.replace('\\','/')
                if not os.path.exists(filename):
                    os.system(r'type nul>{}'.format(filename))
                    logger.info('新建文件：%s'%filename)
                else:
                    logger.info('文件已存在')
        finally:
            with open(filename, 'w+', encoding='gbk') as f:
                yaml.dump(value,f,Dumper=yaml.RoundTripDumper)
                try:
                    f.close()
                    print('文件关闭')
                except:
                    print('文件未关闭')




if __name__ == '__main__':
    excel = ExcelWrite()
    y = YamlWrite()
    value = {
        'ip':'172.16.45.5',
        'name':'彭威'
    }
    y.Write_Yaml(value)

    # value_title = [["姓名", "性别", "年龄", "城市", "职业"], ]
    # value = [["Tom", "男", "21", "西安", "测试工程师"],
    #           ["Jones", "女", "34", "上海", "产品经理"],
    #           ["Cat", "女", "56", "上海", "教师"], ]
    #
    # excel.write_excel_xlsx('E:\\Vantpy1.0\\config\\user1.xls', value_title,value)

    # excel.create_excel_xlsx('E:\\Vantpy1.0\\config\\user1.py','sb1')
    # value1 = ['姓名','年龄','性别']
    # value2 = ['彭威','25','男']
    # value3 = ['彭威1', '25', '男']
    # excel.write_excel_xlsx('E:\\Vantpy1.0\\config\\user1.xls',value1)
    # excel.write_excel_xlsx('E:\\Vantpy1.0\\config\\user1.xls', value2)
    # excel.write_excel_xlsx('E:\\Vantpy1.0\\config\\user1.xls', value3)