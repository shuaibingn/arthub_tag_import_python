import os
import shutil

from excel.xls import XLS
from excel.xlsx import XLSX

from utils.exception import ArtHubException, NotSupportedFileType


class Excel(object):

    def __init__(self, filename: str):
        filetype = filename.split(".")[-1]
        if filetype not in ["xls", "xlsx"]:
            raise ArtHubException(NotSupportedFileType)

        if not os.path.exists("./bak"):
            os.mkdir("./bak")

        filename_without_path = filename.split('/')[-1]
        shutil.copy(filename, f"./bak/{filename_without_path}")

        excel_class = XLS if filetype == "xls" else XLSX
        self.instance = excel_class(filename)

    def read_data(self) -> list:
        return self.instance.read_data()

    def write_data(self, data: list):
        return self.instance.write_data(data)
