#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: file_read.py
@time: 2019/8/30 10:35
@desc: 读取ymal文件以及excel文件
'''


import yaml
import os
from xlrd import open_workbook

class YamlRead:

    '''
    YAML中允许表示三种格式，分别是常量值，对象和数组
    #即表示url属性值；
    url: http://www.baidu.com
    #即表示server.host属性的值；
    server:
        host: http://www.baidu.com
    #数组，即表示server为[a,b,c]
    server:
        - 172.16.45.5
        - 172.16.45.6
        - 172.16.45.7
    #常量
    pi: 3.14   #定义一个数值3.14
    hasChild: true  #定义一个boolean值
    name: 'pengwei'   #定义一个字符串
    '''

    '''判断yaml文件是否存在，存在返回True，不存在返回False并抛出异常'''
    def __init__(self,yamlfile):
        if os.path.exists(yamlfile):
            self.yamlfile = yamlfile
        else:
            raise FileNotFoundError('文件不存在')
        self._data = None  # 初始化None

    @property
    def data(self):
        # 如果是第一次调用data，则打开yaml，否则返回之前保存的数据
        if not self._data:
            with open(self.yamlfile,'rb') as f:
                self._data = list(yaml.safe_load_all(f))   # 将读取到的yaml文件写入list，并赋值给_data
        return self._data


'''该类用于excel中sheet输入不符合类型时所需要抛出的一场,不过没啥用，还是捕捉Exception'''
class SheetTypeError(Exception):
    pass


class ExcelRead:
    """
    读取excel文件中的内容。返回list。

    如：
    excel中内容为：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |

    如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """

    '''判断excel文件是否存在，存在返回True，不存在返回False并抛出异常'''
    def __init__(self,excelfile,sheet=0,title_link=True):
        if os.path.exists(excelfile):
            self.excelfile = excelfile
        else:
            raise FileNotFoundError('文件不存在')
        self.sheet = sheet
        self.title_link = title_link
        self._data = list()   # 赋值_data给list，之后读取到的excel值会添加到list中

    @property
    def data(self):
        global s
        if not self._data:
            workbook = open_workbook(self.excelfile)         #打开excel
            if type(self.sheet) not in [int,str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            elif type(self.sheet) == str:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_link:
                # 获取excel表第一样为title
                title = s.row_values(0)
                # 遍历其余行，将标题拼接为title_link为True时的情况
                for col in range(1,s.nrows):
                    self._data.append(dict(zip(title,s.row_values(col))))
            else:
                # 遍历所有行，添加到_data中，title_link为False时的情况
                for col in range(0,s.nrows):
                    self._data.append(s.row_values(col))
        return self._data



if __name__ == "__main__":
    # yaml文件读取测试
    # sc = Config()
    s = "E:\\Paperless1.0\\config\\ip.yaml"
    sb = YamlRead(s)
    # print(sc.getConfig(''))
    # excel文件读取测试
    # s1 = "E:\\Vantpy1.0\\config\\user.xlsx"
    # sb1 = ExcelRead(s1,0,title_link=False)
    # print(sb1.data[1][0])
    # for i in sb1.data:
    #     a = list()
    #     a.append(i)
    #     print(i)