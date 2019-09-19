import tkinter
import tkinter.messagebox
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
from selenium import webdriver
import re
from tkinter import filedialog
import unittest
import  time
import HTMLTestRunner_cn



class Tkinter(object):
    def __init__(self):
        # 窗口
        self.tk = tkinter.Tk()
        self.tk.geometry("400x500")
        self.tk.title("无纸化自动化测试")

        # 控件
        self.label_IP = tkinter.Label(master=self.tk, text="IP地址:", fg='#9400D3',bg = '#228B22', font=("Arial", 10),width = 9)
        self.label_IP.grid(row=0, column=0)

        self.label_l = tkinter.Label(master=self.tk,text="浏览器:",fg = '#9400D3',bg = '#228B22',font=("Arial",10),width = 9)
        self.label_l.grid(row = 1,column = 0)

        self.label_yl = tkinter.Label(master=self.tk, text="选择用例:", fg='#9400D3', bg='#228B22', font=("Arial", 10),width = 9)
        self.label_yl.grid(row=2, column=0)

        # IP地址输入框
        self.entry_IP = tkinter.Entry(master=self.tk,borderwidth = 3,width = 25)
        self.entry_IP.grid(row=0, column=1)
        # 清空输入框
        self.entry_IP.delete(0,"end")

        # 浏览器选
        # 创建下拉菜单
        self.box = ttk.Combobox(self.tk,width = 23)
        self.box.grid(row=1,column = 1,pady = 20)
        self.box["state"] = "readonly"
         # 设置下拉菜单中的值
        self.box['value'] = ('Google Chrome','Firefox')
        # # 设置默认值，即默认下拉框中的内容
        self.box.current(0)


        # 选择用例执行
        self.case = ttk.Combobox(self.tk, width=23)
        self.case.grid(row=2, column=1)
        self.case["state"] = "readonly"
        # 设置下拉菜单中的值
        self.case['value'] = ('全部', '登录模块','会议信息模块', '会议资料模块')
        # # 设置默认值，即默认下拉框中的内容
        self.case.current(0)

        # 执行测试用例入口
        self.button_yl = tkinter.Button(master=self.tk,text="执行用例",fg = "#9400D3",bg = '#228B22',font=("Arial",12),command= (self.boxvalue))   # command 绑定sample文件
        self.button_yl.grid(row= 3,column =0,pady= 20)

        # 保存测试报告
        self.button_yl = tkinter.Button(master=self.tk, text="保存测试报告路径", fg="#9400D3", bg='#228B22', font=("Arial", 12),command=(self.savePath))
        self.button_yl.grid(row=3, column=1)

        # 列表框控件
        self.listbox = tkinter.Listbox(master=self.tk, width=55, height=16)
        self.listbox.grid(rowspan=5, columnspan=5,padx= 5,pady=10)


        """下拉框函数调用"""
        # 默认选择Google Chrome浏览器
        self.value = "Google Chrome"
        def go(*args):  # 处理事件，*args表示可变参数
            print(self.box.get())
            self.value = self.box.get()
        self.box.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)


        # 用例默认选择为全部
        self.cases = "None"
        def cs(*args):  # 处理事件，*args表示可变参数
            print(self.case.get())
            self.cases = self.case.get()
        self.case.bind("<<ComboboxSelected>>", cs)


        # 默认测试报告路径为空
        self.path = ""

        self.tk.mainloop()


    """点击case判断输入的服务器IP和浏览器选择，默认浏览器为Google Chrome"""
    def boxvalue(self):

        text = self.entry_IP.get()
        box = self.value
        case = self.cases
        if text == "":
            tkinter.messagebox.showinfo('提示', '请输入IP地址')
            return "break"

        if self.path == "":
            tkinter.messagebox.showinfo("提示","请先选择测试报告保存路径")
            return "break"

          #   匹配ip地址
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", text):
            if box == "Google Chrome":  # 调用Google Chrome浏览器
                # 调用浏览器并窗口最大化
                self.driver = webdriver.Chrome()
                self.driver.maximize_window()
                self.operation()
                if case == "None":
                    print("执行所有测试用例")
                elif case == "登录":
                    print("执行登录测试用例")
            elif box == "Firefox":  # 调用Firefox浏览器

                # 调用浏览器并窗口最大化
                self.driver = webdriver.Firefox()
                self.driver.maximize_window()
                self.operation()
        else:
            tkinter.messagebox.showinfo('提示', 'IP地址格式错误')




    """保存测试报告路径方法"""
    def savePath(self):

      # 选择保存测试用例的路径
      self.path = tkinter.filedialog.asksaveasfilename(filetypes=[("HTML",".html")],defaultextension= ".html")

      print(self.path)



      # 在浏览器执行测试
    def  operation(self):

        self.driver.get('http://%s'%self.entry_IP.get())
        # 全局隐式等待30秒
        self.driver.implicitly_wait(30)

        # 面板输出执行操作
        self.listbox.insert('end', "1、无纸化Web端登录test01 账号为空 测试用例已完成") #使用for循环循环添加输出
        self.listbox.see('end')
        self.listbox.update()


if __name__ == '__main__':
    Tkinter()


