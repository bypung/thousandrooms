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
        for column in header:
            headerRow += (column).ljust(cellWidth)
        print(headerRow)

        for row in data:
            out = ""
            if row["_color"]:
                out += row["_color"]

            for field in row:
                if not field == "_color":
                    out += (row[field]).ljust(cellWidth)
            print(out)
