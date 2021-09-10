import tkinter

from tkinter.filedialog import askopenfilename

from excel import Excel
from api.arthub import ArtHub
from utils.const import top_folder, project, version, topic, libs, tags, is_recursion


class TkGUI(object):

    def __init__(self, title, domain, depot, token, asset):
        self.asset = asset
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

        # 单选框
        self.radio_button_value = tkinter.StringVar()
        self.radio_button_value.set(self.asset.get(depot))
        self.check_button()

        # 进度条

        self.build_start()

    def start(self):
        depot = self.radio_button_value.get()
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
                    self.arthub.add_tag(p, self.asset.get(depot), tag_name, is_r)
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

    def check_button(self):
        i = 0
        for k, v in self.asset.items():
            tkinter.Radiobutton(self.root, text=k, variable=self.radio_button_value, value=v).grid(row=1, column=i, ipady=5)
            i += 1

    def build_start(self):
        tkinter.Button(self.root, text="开始执行", command=self.start).grid(row=2, column=0)
