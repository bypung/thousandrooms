class Utils:
    @staticmethod
    def printStats(data, cellWidth = 20):
        for row in data:
            out = ""
            for field in row:
                out += (field + ": " + row[field]).ljust(cellWidth)
            print(out)

    @staticmethod
    def printTable(header, data, cellWidth = 20):
        headerRow = ""
        if type(cellWidth) is int:
            cellWidth = [cellWidth] * len(header)

        for i, column in enumerate(header):
            headerRow += column.ljust(cellWidth[i])
        print(headerRow)

        for row in data:
            out = ""
            try:
                out += row["_color"]
            except KeyError:
                pass
            dataFields = [key for key in list(row.keys()) if key != "_color"]
            for i, field in enumerate(dataFields):
                out += (row[field]).ljust(cellWidth[i])
            print(out)

    @staticmethod
    def flattenTuple(tuple):
        return "-".join(tuple)