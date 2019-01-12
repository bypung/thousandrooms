class Utils:
    @staticmethod
    def colorPadding(string):
        count = 0
        colorSequence = False
        for a in string: 
            if a == '\x1b':
                colorSequence = True 
                count += 1
            elif colorSequence and a != 'm':
                count += 1
            elif colorSequence and a == 'm':
                count += 1
                colorSequence = False
        return count

    @staticmethod
    def printStats(data, cellWidth = 25):
        for row in data:
            out = ""
            for field in row:
                value = row[field]
                out += (field + ": " + value).ljust(cellWidth + Utils.colorPadding(value))
            print(out)

    @staticmethod
    def printTable(header, data, cellWidth = 20):
        headerRow = ""
        if type(cellWidth) is int:
            cellWidth = [cellWidth] * len(header)

        for i, column in enumerate(header):
            headerRow += column.ljust(cellWidth[i] + Utils.colorPadding(column))
        print(headerRow)

        for row in data:
            out = ""
            try:
                out += row["_color"]
            except KeyError:
                pass
            dataFields = [key for key in list(row.keys()) if key != "_color"]
            for i, field in enumerate(dataFields):
                value = row[field]
                out += (value).ljust(cellWidth[i] + Utils.colorPadding(value))
            print(out)

    @staticmethod
    def flattenTuple(tuple):
        return "-".join(tuple)