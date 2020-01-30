import matrix

lengths = [3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 50, 100, 200, 500, 1000, 2000, 3000, 4000, 5000, 10000]


def compareBases(a, b):  # Function to get a score for matching bases
    if a == b:  # If the bases are identical
        return {"A": 3, "C": 2, "G": 1, "T": 2}[a]  # Score them according to their value
    else:  # Otherwise
        return -3  # Return the penalty of 3


def initMatrix(rows, cols):  # Function to initialise matrix
    matrix = [[0 if j == 0 or i == 0 else None for j in range(cols)] for i in range(rows)]  # Funky list comprehension to generate the matrix (this is faster than nested loops)
    return matrix  # Return the generated matrix


def score(i, j, seq1, seq2, matrix):  # Recursive scoring function
    if matrix[i][j] != None:  # Base case (we already have this score in the matrix)
        return matrix[i][j]  # Return the cached value
    s = max(compareBases(seq1[i - 1], seq2[j - 1]) + score(i - 1, j - 1, seq1, seq2, matrix), score(i - 1, j, seq1, seq2, matrix) - 4, score(i, j - 1, seq1, seq2, matrix) - 4,
            0)  # Calculates the score for all of the possible ways to get to this square and takes the maximum
    matrix[i][j] = s  # Stores the calculate score in the matrix
    return s  # And returns it


scores = matrix.Matrix(len(lengths), len(lengths))

for x in range(len(lengths)):
    for y in range(len(lengths)):
        print("Calculating A:", lengths[x], "B:", lengths[y])
        seq1 = open("TestFiles/length" + str(lengths[x]) + "_A.txt").read()
        seq2 = open("TestFiles/length" + str(lengths[y]) + "_B.txt").read()
        scorematrix = initMatrix(len(seq1) + 1, len(seq2) + 1)  # Initialise the scorematrix
        # score(len(seq1), len(seq2), seq1, seq2, scorematrix) # This approach doesn't work for large sequences because it hits recursion depth

        best_score = -1  # Keep a variable to track the best score - it cannot be lower than zero

        for i in range(0, len(scorematrix), 750):  # Iterate through the matrix filling it in blocks of 750x750
            for j in range(0, len(scorematrix[i]), 750):  # This seems really silly but CPython has a recursion depth limit of 1000, so I have to fill the matrix in like this
                score(i, j, seq1, seq2, scorematrix)

        for i in range(750 * (len(scorematrix) // 750), len(scorematrix)):  # Now fill in all of the bottom rows that didn't get filled in (<750)
            for j in range(0, len(seq2), 750):
                score(i, j, seq1, seq2, scorematrix)

        for j in range(750 * (len(scorematrix[0])) % 750, len(scorematrix[0])):  # Same for the columns
            for i in range(0, len(seq1), 750):
                score(i, j, seq1, seq2, scorematrix)

        score(len(seq1), len(seq2), seq1, seq2, scorematrix)  # Then we just fill in the last corner (a final block of < 750x750

        best_index = None  # Stores the index of the best score we find (we need it to align the variables

        for i in range(len(scorematrix)):
            for j in range(len(scorematrix[i])):  # Iterate through the matrix
                if scorematrix[i][j] > best_score:  # If the entry at the given location is the best score we've seen yet
                    best_score = scorematrix[i][j]  # Update the best_score variable to match
                    best_index = (i, j)  # Update the index

        scores.matrix[y][x] = best_score

scores.printMatrix()
