import cProfile


class Matrix(object):
    def __init__(self, m, n, data=[]):
        if data != []:
            self.matrix = data
            self.m = len(data)
            self.n = len(data[0])
        else:
            self.matrix = [[0 for i in range(n)] for j in range(m)]
            self.m = m
            self.n = n

    def removeRow(self, x):
        del self.matrix[x]
        self.m -= 1

    def removeCol(self, x):
        self.matrix[:] = [i[:x] + i[x + 1:] for i in self.matrix]
        self.n -= 1

    def printMatrix(self):
        for row in self.matrix:
            for item in row:
                print(item, end="\t")
            print()
        print()
