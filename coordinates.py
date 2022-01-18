class Coordinates:
    def __init__(self):
        self.row = -1
        self.column = -1

    def getRowNo(self):
        return self.row

    def getColumnNo(self):
        return self.column

    def setRowNo(self, rowNo):
        self.row = rowNo

    def setColumnNo(self, columnNo):
        self.column = columnNo