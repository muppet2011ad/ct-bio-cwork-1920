import cProfile


class DimensionError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Matrix(object):
    def __init__(self, m, n, data=[]):
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
                string += str(value) + "\t"
            string += "\n"
        return string[:-1]

    def __add__(self, other):
        if self.m != other.m or self.n != other.n:
            raise DimensionError("Cannot add two matrices with different dimensions!")
        return Matrix(self.m, self.n, [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.n)] for i in range(self.m)])
