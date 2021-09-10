import logging
import tkinter

from tkinter.filedialog import askopenfilename

from excel import Excel
from api.arthub import ArtHub
from utils.const import top_folder, project, version, topic, libs, tags, is_recursion
from utils.exception import ArtHubException


class TkGUI(object):

    def __init__(self, title, domain, depot, token, asset):
        self.asset = asset
        self.depot = depot
        self.arthub = ArtHub(token, domain, depot)

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
        self.excel_path = tkinter.StringVar()
        self.file_select()

        # # 域名
        # self.tk_domain = tkinter.StringVar()
        # self.build_domain(domain)
        #
        # # 资源库
        # self.tk_depot = tkinter.StringVar()
        # self.build_depot(depot)
        #
        # # token
        # self.tk_token = tkinter.StringVar()
        # self.build_token(token)

        self.build_start()

    def start(self):
        ex = Excel(self.excel_path.get())
        excel_data = ex.read_data()

        is_sync_data = []
        for data in excel_data:
            path = self.fix_path(data)
            tag_name = [data.get(x) for x in tags]
            is_r = data.get(is_recursion)
            success = True
            for p in path:
                try:
                    self.arthub.add_tag(p, self.asset.get(self.depot), tag_name, is_r)
                except Exception as e:
                    print(f"path: {p}, error: {e.__str__()}")
                    success = False
                    continue

                print(f"path: {p}, add tag success")

            if success:
                is_sync_data.append(data)

        ex.write_data(is_sync_data)

    @staticmethod
    def fix_path(data) -> list:
        ver: str = data.get(version)
        path = [top_folder, "原画", project, version, topic]
        if ver.find("年") >= 0:
            path = [top_folder, "原画", project, version, version, "商业化", topic]

        for i in range(len(path)):
            path[i] = data.get(path[i]) or path[i]

        if path.count(ver) > 1:
            path[path.index(ver)] = ver[:5]

        res = []
        for lib in libs:
            p = path[:3] + [lib] + path[3:]
            res.append(p)

        return res

    def select_path(self):
        self.excel_path.set(askopenfilename())

    def file_select(self):
        tkinter.Label(self.root, text="文件路径: ").grid(row=0, column=0, ipady=5)
        tkinter.Entry(self.root, textvariable=self.excel_path, width=30).grid(row=0, column=1)
        tkinter.Button(self.root, text="选择文件", command=self.select_path).grid(row=0, column=2)

    # def build_domain(self, domain):
    #     self.tk_domain.set(domain)
    #     tkinter.Label(self.root, text="域名: ").grid(row=1, column=0, ipady=5)
    #     tkinter.Entry(self.root, textvariable=self.tk_domain, width=30).grid(row=1, column=1)
    #
    # def build_depot(self, depot):
    #     self.tk_depot.set(depot)
    #     tkinter.Label(self.root, text="资源库: ").grid(row=2, column=0, ipady=5)
    #     tkinter.Entry(self.root, textvariable=self.tk_depot, width=30).grid(row=2, column=1)
    #
    # def build_token(self, token):
    #     self.tk_token.set(token)
    #     tkinter.Label(self.root, text="token: ").grid(row=3, column=0, ipady=5)
    #     tkinter.Entry(self.root, textvariable=self.tk_token, width=30).grid(row=3, column=1)

    def build_start(self):
        tkinter.Button(self.root, text="开始执行", command=self.start).grid(row=1, column=0)
