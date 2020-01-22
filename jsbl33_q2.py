#!/usr/bin/python
import time
import sys


def compareBases(a, b):
    if a == b:
        matchDict = {"A": 3,
                     "C": 2,
                     "G": 1,
                     "T": 2}
        return matchDict[a]
    else:
        return -3


def initMatrix(rows, cols):
    matrix = [[0 if j == 0 or i == 0 else None for j in range(cols)] for i in range(rows)]
    return matrix


def score(i, j, seq1, seq2, matrix):
    if matrix[i][j] != None:
        return matrix[i][j]
    s = max(compareBases(seq1[i - 1], seq2[j - 1]) + score(i - 1, j - 1, seq1, seq2, matrix),
            score(i - 1, j, seq1, seq2, matrix) - 2, score(i, j - 1, seq1, seq2, matrix) - 2, 0)
    matrix[i][j] = s
    return s


# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it

def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
start = time.time()

#-------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# To work with the printing functions below the best local alignment should be called best_alignment and its score should be called best_score.

scorematrix = initMatrix(len(seq1) + 1, len(seq2) + 1)
# score(len(seq1), len(seq2), seq1, seq2, scorematrix) # This approach doesn't work for large sequences because it hits recursion depth

best_score = 0

for i in range(0, len(scorematrix), 750):
    for j in range(0, len(scorematrix[i]), 750):
        score(i, j, seq1, seq2, scorematrix)

for i in range(750 * (len(scorematrix) // 750), len(scorematrix)):
    for j in range(0, len(seq2), 750):
        score(i, j, seq1, seq2, scorematrix)

for j in range(750 * (len(scorematrix[0])) % 750, len(scorematrix[0])):
    for i in range(0, len(seq1), 750):
        score(i, j, seq1, seq2, scorematrix)

score(len(seq1), len(seq2), seq1, seq2, scorematrix)

for i in range(len(scorematrix)):
    for j in range(len(scorematrix[i])):
        # score(i,j,seq1,seq2,scorematrix)
        if scorematrix[i][j] > best_score:
            best_score = scorematrix[i][j]

#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------

