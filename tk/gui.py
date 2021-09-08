import json
import tkinter

from tkinter.filedialog import askopenfilename

from excel import Excel
from utils.yaml_tools import write_yaml


class TkGUI(object):

    def __init__(self, title, domain, depot, path, token):
        self.root = tkinter.Tk()
        self.root.title(title)
        self.root.wm_attributes("-alpha", 1.0)
        self.root.wm_attributes("-topmost", True)

        width = 500  # 宽度
        height = 300  # 高度

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # 打开文件
        self.path = tkinter.StringVar()
        self.file_select(path)

        # 域名
        self.domain = tkinter.StringVar()
        self.build_domain(domain)

        # 资源库
        self.depot = tkinter.StringVar()
        self.build_depot(depot)

        # token
        self.token = tkinter.StringVar()
        self.build_token(token)

        self.build_start()

    def start(self):
        data = {
            "depot": self.depot.get(),
            "domain": self.domain.get(),
            "path": self.path.get(),
            "token": self.token.get(),
        }
        write_yaml(".\\config.yaml", data)

        ex = Excel(data.get("path"))
        excel_data = ex.read_data()
        print(json.dumps(excel_data))

    def select_path(self):
        self.path.set(askopenfilename())

    def file_select(self, path):
        self.path.set(path)
        tkinter.Label(self.root, text="文件路径: ").grid(row=0, column=0, ipady=5)
        tkinter.Entry(self.root, textvariable=self.path, width=30).grid(row=0, column=1)
        tkinter.Button(self.root, text="选择文件", command=self.select_path).grid(row=0, column=2)

    def build_domain(self, domain):
        self.domain.set(domain)
        tkinter.Label(self.root, text="域名: ").grid(row=1, column=0, ipady=5)
        tkinter.Entry(self.root, textvariable=self.domain, width=30).grid(row=1, column=1)

    def build_depot(self, depot):
        self.depot.set(depot)
        tkinter.Label(self.root, text="资源库: ").grid(row=2, column=0, ipady=5)
        tkinter.Entry(self.root, textvariable=self.depot, width=30).grid(row=2, column=1)

    def build_token(self, token):
        self.token.set(token)
        tkinter.Label(self.root, text="token: ").grid(row=3, column=0, ipady=5)
        tkinter.Entry(self.root, textvariable=self.token, width=30).grid(row=3, column=1)

    def build_start(self):
        tkinter.Button(self.root, text="开始执行", command=self.start).grid(row=4, column=0)
