import sys


class Matrix(object):
    def __init__(self, m=0, n=0, data=[]):
        if data != []:
            self.matrix = data
            self.m = len(data)
            self.n = len(data[0])
        else:
            self.matrix = [[0 for j in range(n)] for i in range(m)]
            self.m = m
            self.n = n

    def removeRow(self, x):
        del self.matrix[x]
        self.m -= 1

    def removeCol(self, x):
        self.matrix[:] = [i[:x] + i[x + 1:] for i in self.matrix]
        self.n -= 1

    def __getitem__(self, key):
        row, col = key
        return self.matrix[row][col]

    def __setitem__(self, key, value):
        row, col = key
        self.matrix[row][col] = value

    def __str__(self):
        string = ""
        for row in self.matrix:
            for value in row:
                string += str(value) + "\t\t"
            string += "\n"
        return string[:-1]

    def indexMin(self):
        minval = 2 * sys.maxsize + 1
        mindex = (0, 0)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] is not None:
                    if self.matrix[i][j] < minval:
                        mindex = (i, j)
        return mindex


class NJMatrix(Matrix):
    def __init__(self, m=0, n=0, data=[], headers=[]):
        super().__init__(m, n, data)
        self.sumRows()
        if headers != []:
            self.headers = headers
        else:
            self.headers = [str(i) for i in range(self.m)]

    def sumRows(self):
        self.rowsums = [sum([val if val is not None else 0 for val in row]) for row in self.matrix]

    def getQScores(self):
        r = self.m
        qData = [[(r - 1) * self.matrix[a][b] - (self.rowsums[a] + self.rowsums[b]) if b > a else None for b in range(self.n)] for a in range(self.m)]
        return Matrix(data=qData)

    def cluster(self):
        self.qMatrix = self.getQScores()
        minval = 2 * sys.maxsize + 1
        mindex = (0, 0)
        for i in range(len(self.qMatrix.matrix)):
            for j in range(len(self.qMatrix.matrix[i])):
                if j > i:
                    if self.qMatrix[i, j] < minval:
                        minval = self.qMatrix[i, j]
                        mindex = (i, j)
        a, b = mindex
        self.headers[a] = self.headers[a] + self.headers[b]
        del self.headers[b]
        for i in range(0, self.m):
            self.matrix[i][a] = (self.distance(i, a) + self.distance(i, b) - self.distance(a, b)) / 2
        for j in range(0, self.n):
            self.matrix[a][j] = (self.distance(b, j) + self.distance(j, b) - self.distance(a, b)) / 2
        self.removeRow(b)
        self.removeCol(b)
        self.sumRows()

    def distance(self, a, b):
        if a > b:
            return self.matrix[b][a]
        else:
            return self.matrix[a][b]

    def __str__(self):
        string = "\\\t\t" + "".join("{:6} ".format(header) for header in self.headers) + "\n"
        for i in range(len(self.matrix)):
            string += self.headers[i] + "\t\t"
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] is not None:
                    string += "{:6} ".format(str(self.matrix[i][j]))
                else:
                    string += "{:6} ".format("-")
            string += "\n"
        return string[:-1]


def loadMatrix(filename):
    with open(filename) as f:
        lines = f.readlines()
        headers = lines[0][1:].split()
        data = []
        for line in lines[1:]:
            data.append([int(char) for char in line[1:].split()])
        return NJMatrix(data=data, headers=headers)


mat1 = loadMatrix("q3t2")
print(mat1)
mat1.cluster()
print(mat1)
mat1.cluster()
print(mat1)
