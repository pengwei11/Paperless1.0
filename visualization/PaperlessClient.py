import tkinter
import tkinter.messagebox
import os,time
import re
import threading
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
from tkinter import filedialog
from utils.logger import Logger
from utils.file_write import YamlWrite
from test.sample.sample import Run_All
from utils.config import Config
from threading import Timer
from apscheduler.schedulers.background import BackgroundScheduler


logger = Logger(logger='logger').getlog()


class PaperlessClient(object):

    def __init__(self):
        self.tk = tkinter.Tk()
        screenwidth = self.tk.winfo_screenwidth()
        screenheight = self.tk.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (400, 500, (screenwidth - 400) / 2, (screenheight - 500) / 2)
        self.tk.resizable(0, 0)
        self.tk.geometry(alignstr)
        self.tk.title("无纸化自动化测试")
        self.ipvar = tkinter.StringVar()
        self.brwoservar = tkinter.StringVar()
        self.modulevar = tkinter.StringVar()
        self.path = ""
        self.r = Run_All()
        self.sc = Config()
        self.oldv = None
        YamlWrite().Write_Yaml(self.sc.getCasename_path(),{'casename':self.oldv})

    def createpage(self):
        self.label_IP = tkinter.Label(master=self.tk, text="IP地址:", fg='#9400D3', bg='#228B22', font=("Arial", 10),
                                      width=9)
        self.label_IP.grid(row=0, column=0, pady=10)

        self.label_l = tkinter.Label(master=self.tk, text="浏览器:", fg='#9400D3', bg='#228B22', font=("Arial", 10),
                                     width=9)
        self.label_l.grid(row=1, column=0)

        self.label_yl = tkinter.Label(master=self.tk, text="选择用例:", fg='#9400D3', bg='#228B22', font=("Arial", 10),
                                      width=9)
        self.label_yl.grid(row=2, column=0, pady=10)

        # IP地址输入框
        self.entry_IP = tkinter.Entry(master=self.tk, borderwidth=3, width=25, textvariable=self.ipvar)
        self.entry_IP.grid(row=0, column=1)
        # 清空输入框
        self.entry_IP.delete(0, "end")

        # 浏览器选
        # 创建下拉菜单
        self.box = ttk.Combobox(self.tk, width=23, textvariable=self.brwoservar)
        self.box.grid(row=1, column=1)
        self.box["state"] = "readonly"
        # 设置下拉菜单中的值
        self.box['value'] = (self.getBrwoserValue()[0],self.getBrwoserValue()[1])
        # # 设置默认值，即默认下拉框中的内容
        self.box.current(0)

        # 选择用例执行
        self.case = ttk.Combobox(self.tk, width=23, textvariable=self.modulevar)
        self.case.grid(row=2, column=1)
        self.case["state"] = "readonly"
        # 设置下拉菜单中的值
        self.case['value'] = (self.getMoudleValue()[0],self.getMoudleValue()[1],self.getMoudleValue()[2],self.getMoudleValue()[3])
        # # 设置默认值，即默认下拉框中的内容
        self.case.current(0)

        # 执行测试用例入口
        self.button_yl = tkinter.Button(master=self.tk, text="执行用例", fg="#9400D3", bg='#228B22', font=("Arial", 12),
                                        command=(self.btn))  # command 绑定sample文件
        self.button_yl.grid(row=3, column=0, pady=10)

        # 保存测试报告
        self.button_yl = tkinter.Button(master=self.tk, text="保存测试报告路径", fg="#9400D3", bg='#228B22', font=("Arial", 12),
                                        command=(self.save_path))
        self.button_yl.grid(row=3, column=1)

        # 显示测试报告路径
        self.lable_bg = tkinter.Label(master=self.tk, text=self.path, fg='#000000', font=("Arial", 10),
                                      width=30)
        self.lable_bg.grid(row=4, column=1)

        # 列表框控件
        self.listbox = tkinter.Listbox(master=self.tk, width=55, height=16)
        self.listbox.grid(rowspan=5, columnspan=5, padx=5, pady=20)

        """下拉框函数调用"""
        # 默认选择Google Chrome浏览器
        self.value = "Google Chrome"

        def go(*args):  # 处理事件，*args表示可变参数
            print(self.box.get())
            self.value = self.box.get()

        self.box.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)

        # 用例默认选择为全部
        self.cases = "全部"

        def cs(*args):  # 处理事件，*args表示可变参数
            print(self.case.get())
            self.cases = self.case.get()

        self.case.bind("<<ComboboxSelected>>", cs)

    def start(self):
        self.createpage()
        self.tk.mainloop()

    '''保存测试报告路径'''
    def save_path(self):
        # 选择保存测试用例的路径
        self.path = tkinter.filedialog.askdirectory()
        # 显示报告路径赋值给lable
        self.path = self.path.replace('/','\\')
        self.lable_bg.config(text=self.path)


    '''buttton绑定时间'''
    def btn(self):
        if self.ipvar.get()=='' or self.ipvar.get()==None:
            tkinter.messagebox.showinfo('提示', 'IP地址不能为空')
        elif not re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",self.ipvar.get()):
            tkinter.messagebox.showinfo('提示','IP地址格式不正确')
        elif self.path=='' or self.path==None:
            self.save_path()    # 报告地址为空时，点击Case会弹出路径选择
        else:
            value = {'ip': self.ipvar.get(), 'browser': self.brwoservar.get(),'reportPath':self.path+'\\','moudle':self.modulevar.get()}
            YamlWrite().Write_Yaml(self.sc.getWriteIP(),value)  # 将value写入ip.yaml文件中
            # threads = []
            # threads.append(threading.Thread(target=Run_All().Run_test_case_all))
            # threads.append(threading.Thread(target=pc.listout))
            # for t in threads:
            #     t.daemon = True
            #     t.start()
            self.listout()
            Run_All().Run_test_case_all()

        


    '''从brwoseryaml文件读取浏览器信息'''
    def getBrwoserValue(self):
        brwoserValue = []
        for key,value in self.sc.getConfig('Browser').items():
            brwoserValue.append(value)
        return brwoserValue


    '''从browser.yaml文件中读取模块信息'''
    def getMoudleValue(self):
        moudleValue = []
        for key,value in self.sc.getConfig('Moudle').items():
            moudleValue.append(value)
        return moudleValue

    def listout(self):
        print('测试')
        newv = self.sc.getReadCasename('casename')
        if newv != self.oldv:
            self.listbox.insert('end',self.sc.getReadCasename('casename'))
            self.listbox.see('end')
            self.listbox.update()
            self.oldv = newv
            print('一致')
        # 面板输出执行操作
        # info = os.stat(self.sc.getCasename_path())
        t = Timer(3, self.listout)
        t.start()
        # if time.time()-info.st_mtime <1:
        #     self.listbox.insert('end', '无纸化Web端测试用例%s测试开始....' % self.sc.getReadCasename('casename'))
        #     self.listbox.see('end')
        #     self.listbox.update()
        # for i in range(30):
        #     self.listbox.insert('end','开始运行test_0%s'%(i+1))
        #     time.sleep(1)
        #     self.listbox.insert('end', '...')
        #     self.listbox.see('end')
        #     self.listbox.update()
        #     time.sleep(7)
        #     self.listbox.insert('end','test_0%s运行完成\n'%(i+1))


        # if int(os.stat(self.sc.getCasename_path()).st_ctime) != int(os.stat(self.sc.getCasename_path()).st_mtime):
        #     self.listbox.insert('end', '无纸化Web端测试用例%s测试开始....' % self.sc.getReadCasename('casename'))
        #     self.listbox.see('end')
        #     self.listbox.update()


if __name__ == '__main__':
    pc = PaperlessClient()
    pc.start()
    # threads = []
    # threads.append(threading.Thread(target=pc.btn))
    # threads.append(threading.Thread(target=pc.listout))
    # for t in threads:
    #     t.daemon = True
    #     t.start()



