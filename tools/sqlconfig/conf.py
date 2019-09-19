#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1249294960@qq.com
@software: pengwei
@file: conf.py
@time: 2019/9/2 10:10
@desc: 实现数据库连接以及各个基础操作方法的封装,
'''

import pymysql


class MySqlLib(object):

    # 连接数据库
    def __init__(self, ip, user, password, db_name, charset='utf8'):
        try:
            self.ip = ip
            self.user = user
            self.password = password
            self.db_name = db_name
            self.charset = charset

            self.MySQL_db = pymysql.connect(
                host = self.ip,
                user = self.user,
                password = self.password,
                db = self.db_name,
                charset = self.charset,
            )
            print('连接成功')
        except TypeError as e:
            print('Error:connect is error')



    # 执行sql语句
    def sql_exe(self,sql):
        cursor = self.MySQL_db.cursor()
        Mysql_sql = sql
        try:
            cursor.execute(Mysql_sql)
            self.MySQL_db.commit()
        except:
            print('Error:unable to fetch data')
            self.MySQL_db.close()
        cursor.close()
        self.MySQL_db.close()


    # 创建sql表,字段可自选
    def create_table(self,table_name):
        # 创建一张表
        cursor = self.MySQL_db.cursor()
        try:
            # 判断表是否存在，存在则删除，并重新创建，不存在则直接创建
            cursor.execute("DROP TABLE IF EXISTS %s"%table_name)
            sql = """
                  CREATE TABLE %s(
                  ID INT,
                  NAME VARCHAR(100) NOT NULL
                  )CHARACTER SET utf8 COLLATE utf8_general_ci
                    """%table_name
            cursor.execute(sql)
            print("创建成功")
            return True
        except:
            print('创建失败')
            return False

    # 删除指定表格
    def drop_table(self,table_name):
        try:
            cursor = self.MySQL_db.cursor()
            sql = 'DROP TABLE %s'%table_name
            cursor.execute(sql)
            print("删除成功")
        except:
            print("未找到该表")

    # 修改表名字
    def updata_table(self,old_table_name,new_table_name):
        try:
            cursor = self.MySQL_db.cursor()
            sql = 'alter table %(old)s rename to %(new)s'%{'old':old_table_name,'new':new_table_name}
            cursor.execute(sql)
            print("表名修改成功")
        except:
            print('表名修改失败')



    '''表格数据增，删，改，查（暂时不写，需要封装的方法有点多）'''

    # def query_table_field(self,table_name,db_name):
    #     global field
    #     field = []
    #     cursor = self.MySQL_db.cursor()
    #     sql1 = "select COLUMN_NAME from information_schema.COLUMNS
    #     where table_name = '%s' and table_schema = '%s'"%(table_name,db_name)
    #     cursor.execute(sql1)
    #     data = cursor.fetchall()
    #     for i in data:
    #         field.append(i)
    #     return field

    # # 查询表格所有数据
    # def query_all_sql(self,table_name):
    #     '''用于查询表格字段'''
    #     # sql1 = "select COLUMN_NAME from information_schema.COLUMNS
    #     # where table_name = '%s' and table_schema = '%s'"%(table_name,db_name)
    #     cursor = self.MySQL_db.cursor()
    #     sql = 'SELECT * FROM %s'%table_name
    #     try:
    #         cursor.execute(sql)
    #         data = cursor.fetchall()
    #         print(data)
    #     except:
    #         print("没有该表")
    # # 根据条件查询表格单个数据
    # def query_one_sql(self,table_name,field,value):
    #     cursor = self.MySQL_db.cursor()
    #     sql = "SELECT * FROM %s WHERE %s = '%s'"%(table_name,field,value)
    #     try:
    #         cursor.execute(sql)
    #         data = cursor.fetchall()
    #         print(data)
    #     except:
    #         print("查询失败")
    # # 修改表格数据
    # def update(self,table_name,field,value):
    #     cursor = self.MySQL_db.cursor()
    #     sql = 'UPDATE %s SET '





if __name__ == '__main__':
    p = ['localhost','root','admin','test']
    m = MySqlLib(p[0],p[1],p[2],p[3])
    '''表格增删改查
    print(m)
    m.create_table('t1')
    m.drop_table('t1')
    m.updata_table('t1','ddd')'''

    '''表格数据增删改查'''
    # m.query_all_sql('ddd')

    # m.query_all_sql('t1')

    # m.query_one_sql('t1','id','2')