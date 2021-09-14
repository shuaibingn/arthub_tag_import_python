import logging

import tkinter
import tkinter.messagebox

from tkinter import HORIZONTAL, DISABLED, NORMAL
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename

from excel import Excel
from api.arthub import ArtHub
from utils.const import top_folder, project, version, topic, libs, tags, is_recursion

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("./log.txt", mode="a", encoding="utf-8")
handler.setLevel(level=logging.INFO)

formatter = logging.Formatter("%(asctime)s %(levelname)s %(lineno)d: %(message)s")
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(level=logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)


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

        # 开始执行
        self.btn = tkinter.Button(self.root, text="开始执行", command=self.start, state=DISABLED)
        self.build_start()

    def start(self):
        # TopLevel
        top_level = tkinter.Toplevel()
        top_level.title("上传进度")
        tkinter.Label(top_level, text="上传进度: ").grid(row=0, column=0)

        # 将按钮设置为不可点击状态
        self.btn.configure(text="正在操作...", state=DISABLED)

        # 进度条
        pb = Progressbar(top_level, length=200, mode="determinate", orient=HORIZONTAL)
        pb.grid(row=0, column=1)

        depot_id = self.radio_button_value.get()

        try:
            ex = Excel(self.excel_path.get())
        except Exception as e:
            logger.error(f"file: {self.excel_path.get()}, error: {e}")
            top_level.destroy()
            tkinter.messagebox.showwarning(title="警告", message=e.__str__())
            self.btn.configure(text="开始执行", state=NORMAL)
            return

        excel_data = ex.read_data()

        pb["maximum"] = len(excel_data) * 2
        pb["value"] = 0

        i = 1
        success_data, failed_data = 0, 0
        is_sync_data = []
        for data in excel_data:
            path = self.fix_path(data)
            tag_name = [data.get(x) for x in tags]
            is_r = data.get(is_recursion) == "是"
            success = True
            for p in path:
                pb["value"] = i
                top_level.update()
                i += 1

                try:
                    self.arthub.add_tag(p, depot_id, tag_name, is_r)
                except Exception as e:
                    logger.error(f"path: {p}, error: {e.__str__()}")
                    success = False
                    if tkinter.messagebox.askokcancel(title="上传失败", message=f"路径: {'/'.join(p)}\n\n失败原因: {e.__str__()}\n\n是否继续?"):
                        continue
                    else:
                        top_level.destroy()
                        self.btn.configure(text="开始执行", state=NORMAL)
                        return

                logger.info(f"path: {p}, add tag success")

            if success:
                success_data += 1
                is_sync_data.append(data)
            else:
                failed_data += 1

        ex.write_data(is_sync_data)
        top_level.destroy()
        tkinter.messagebox.showinfo(title="上传结果", message=f"成功: {success_data}, 失败: {failed_data}, 共有: {success_data + failed_data}")
        self.btn.configure(text="开始执行", state=NORMAL)

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
        state = DISABLED
        if self.excel_path.get() != "":
            state = NORMAL

        self.btn.configure(text="开始执行", state=state)

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
        self.btn.grid(row=2, column=0)
