from excel.xls import XLS
from excel.xlsx import XLSX


class Excel(object):

    def __init__(self, filename: str):
        filetype = filename.split(".")[-1]
        excel_class = XLS if filetype == "xls" else XLSX
        self.instance = excel_class(filename)

    def read_data(self) -> list:
        return self.instance.read_data()

    def write_data(self, data: dict):
        return self.instance.write_data(data)
