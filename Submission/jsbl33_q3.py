#!/usr/bin/python
class Matrix(object):  # Class for a normal matrix
    def __init__(self, m=0, n=0, data=[]):  # Init method - it's best to define at least one of m/n and data otherwise you'll just get a 0x0 matrix
        if data != []:  # If the data has been specified
            self.matrix = data  # Take the array as the matrix
            self.m = len(data)
            self.n = len(data[0])  # Set m and n based on its dimensions
        else:  # If no data has been specified
            self.matrix = [[0 for j in range(n)] for i in range(m)]  # Create the matrix as the m*n zero matrix
            self.m = m
            self.n = n

    def removeRow(self, x):  # Function to remove a row
        del self.matrix[x]  # Easy peasy lemon squeazy
        self.m -= 1  # Decrement m

    def removeCol(self, x):  # Function to remove a column
        for i in range(self.m):
            del self.matrix[i][x]
        self.n -= 1

    def __getitem__(self, key):  # Function to override getting - not really used here
        row, col = key  # Unpack the key (which should be a tuple or other iterable)
        return self.matrix[row][col]  # Return the value in the matrix at that location

    def __setitem__(self, key, value):  # Function to override setting
        row, col = key  # Unpack the key
        self.matrix[row][col] = value  # Update the value

    def __str__(self):  # Function to override string conversion (this gets used when printing)
        colwidths = [len(max([str(self.matrix[i][j]) for j in range(self.n)], key=lambda x: len(x))) for i in range(self.m)]  # Cursed list comprehension to calculate the number of
        # digits in each column of the matrix
        string = ""  # Creates an empty string
        for i in range(len(self.matrix)):  # Iterate over rows
            for j in range(len(self.matrix[i])):  # Iterate over columns
                if self.matrix[i][j] is not None:  # If entry isn't none
                    string += str(self.matrix[i][j]).rjust(colwidths[j]) + " "  # Add the entry and right justify it (this lines up the columns)
                else:  # Otherwise
                    string += "-".rjust(colwidths[j]) + " "  # Add "-"
            string += "\n"  # Add a newline at the end of the row
        return string[:-1]  # Remove the final newline


class NJMatrix(Matrix):  # Class for a matrix supporting the neighbour joining algorithm (extends the Matrix class)
    def __init__(self, m=0, n=0, data=[],
                 headers=[]):  # Init is as before but with the extra optional parameter of headers. Not specifying the headers will cause the values 0-n to be used
        super().__init__(m, n, data)  # Call the init method of the parent class
        self.sumRows()  # Get the initial row sums
        if headers != []:  # If headers has been defined
            self.headers = headers  # Set the given headers as an attribute
        else:
            self.headers = [str(i) for i in range(self.m)]  # Create the headers as the numbers 0-n

    def sumRows(self):  # Function to sum the rows of the matrix
        self.rowsums = [sum(row) for row in self.matrix]  # List comprehension generates list of the sum of all rows

    def getQScores(self):  # Function to calculate q scores for the entire matrix
        r = self.m  # Sets r as the size of the matrix
        qData = [[(r - 1) * self.matrix[a][b] - (self.rowsums[a] + self.rowsums[b]) if a != b else None for b in range(self.n)] for a in range(self.m)]
        # List comprehension calculates q value for every value and fills in matrix, using None where we should have no qscore (i.e. when a == b)
        return Matrix(data=qData)  # Return a matrix object containing the data

    def cluster(self):  # Method to perform a single step of the NJ algorithm
        self.qMatrix = self.getQScores()  # Get a matrix of q scores
        minval = float("inf")  # Now we need to find a minimum of the matrix, so start with minval as a really big number
        mindex = (0, 0)  # Placeholder value for index
        for i in range(len(self.qMatrix.matrix)):
            for j in range(i + 1, len(self.qMatrix.matrix[i])):  # Iterate over every element in the upper triangular but of the matrix
                if self.qMatrix[i, j] < minval:  # If this is lower than anything we've seen before
                    minval = self.qMatrix[i, j]  # Update the minimum value
                    mindex = (i, j)  # Update the minimum index
        a, b = mindex  # Unpack the minimum index
        # Now we've identified the species that we need to cluster, we need to actually cluster them. I do this in-place, overwriting the data for species a with the new ab
        self.headers[a] = self.headers[a] + self.headers[b]  # Combine the headers of the species (this can get long with combined species)
        del self.headers[b]  # Delete b from the headers (we're about to shrink the matrix too)
        distAB = self[a, b]  # Get the distance between a and b in the matrix (we need this in the calculation but it gets overwritten since we're working in-place, so we
        # have to copy it.
        for i in range(0, self.m):  # Iterate from 0 to m (since m == n as this should be a square matrix, we can iterate over both rows and columns)
            self[i, a] = (self[i, a] + self[i, b] - distAB) / 2  # Calculate the new distances for the combined species
            self[a, i] = self[i, a]  # Copy it into the lower triangular part of the matrix
        self.removeRow(b)  # Remove row b
        self.removeCol(b)  # Remove column b
        self.sumRows()  # Update the rowsums with the new information in the matrix

    def __str__(self):  # Override of str() method
        colwidths = [len(max([self.headers[i]] + [str(self[i, j]) for j in range(self.n)], key=lambda x: len(x))) for i in range(self.m)]
        # Calculate the width each column needs to be using the most cursed of list comprehensions
        headcolwidth = len(max(self.headers, key=lambda x: len(x)))  # Works out the width of the first column (of headers)
        sumcolwidth = len(max([str(s) for s in self.rowsums] + ["Sums"]))
        string = "\\".rjust(headcolwidth) + " "  # Places a backslash to mark the intersection of the row and column headers
        for i in range(self.m):  # Iterate through the array's dimensions
            string += self.headers[i].rjust(colwidths[i]) + " "  # Add the first row of headers to the string
        string += "| Sums".rjust(sumcolwidth) + "\n"  # Add a newline
        for i in range(len(self.matrix)):  # Now iterate through the rows of the matrix
            string += self.headers[i].rjust(headcolwidth) + " "  # Print the header for that row
            for j in range(len(self.matrix[i])):  # Iterate through the row
                if self.matrix[i][j] is not None:  # If the contents of the entry are defined
                    string += str(self.matrix[i][j]).rjust(colwidths[j]) + " "  # Add the value of the entry to the string
                else:
                    string += "-".rjust(colwidths[j]) + " "  # Add "-" to the string
            string += "| " + str(self.rowsums[i]).rjust(sumcolwidth) + "\n"  # Add a newline at the end of each row
        return string[:-1]  # Remove the final newline


def loadMatrix(filename):  # Function to load a matrix ready for NJ algorithm from a file
    with open(filename) as f:  # Open the file
        lines = f.readlines()  # Read out the lines of the file
        headers = lines[0][1:].split()  # Load in the headers of the matrix (i.e. the names of the species)
        data = [[float(char) for char in line.split()[1:]] for line in lines[1:]]  # Fetch the data using some cursed list comprehensions
        return NJMatrix(data=data, headers=headers)  # Create an NJMatrix from the data loaded


def NJ(file):  # Takes a filename and goes through the whole NJ algorithm
    matrix = loadMatrix(file)  # Gets the NJ matrix from the file
    while (matrix.m >= 2):  # Whilst the matrix is at least a 2x2
        print("The similarity matrix is as follows:")
        print(matrix)  # Output the matrix
        matrix.cluster()  # Go through a clustering step
        print("The associated qScores for this matrix are as follows:")
        print(matrix.qMatrix)  # Output the calculated qscores
        print()  # Leave a line