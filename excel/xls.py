import xlrd

from xlutils.copy import copy

from utils.const import is_sync


class XLS(object):

    def __init__(self, filename):
        self.filename = filename
        self.xlrd_wb = xlrd.open_workbook(filename=filename)
        self.xlrd_ws = self.xlrd_wb.sheet_by_index(0)

        self.xlwt_wb = copy(self.xlrd_wb)
        self.xlwt_ws = self.xlwt_wb.get_sheet(0)

    def read_data(self) -> list:
        res = []
        for i in range(self.xlrd_ws.nrows):
            d = {}
            for j in range(self.xlrd_ws.ncols):
                k = self.xlrd_ws.cell(0, j).value
                if i != 0 and k == is_sync:
                    d["index"] = [i, j]

                if i != 0:
                    v = self.xlrd_ws.cell(i, j).value
                    if isinstance(v, float):
                        v = int(v)

                    d[k] = str(v)

            if d and d.get(is_sync) == "否":
                res.append(d)

        return res

    def write_data(self, data: dict):
        index = data.get("index")
        self.xlwt_ws.write(index[0], index[1], "是")
        self.xlwt_wb.save(self.filename)
