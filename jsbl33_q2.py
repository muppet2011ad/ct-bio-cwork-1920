#!/usr/bin/python
import time
import sys


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
    s = max(compareBases(seq1[i - 1], seq2[j - 1]) + score(i - 1, j - 1, seq1, seq2, matrix),
            score(i - 1, j, seq1, seq2, matrix) - 4, score(i, j - 1, seq1, seq2, matrix) - 4,
            0)  # Calculates the score for all of the possible ways to get to this square and takes the maximum
    matrix[i][j] = s  # Stores the calculate score in the matrix
    return s  # And returns it


def align(seq1, seq2, matrix, index):  # Function to calculate local alignment given two strings, a score matrix and the index of the highest value
    i, j = index  # Unpacks the index (it should arrive as a two-value tuple or list)
    local_align1 = ""
    local_align2 = ""  # Create two strings to store the local alignment
    while i >= 1 and j >= 1 and matrix[i][
        j] != 0:  # While we haven't reached the edge of the matrix (that store the gap scores)
        if matrix[i][j] - compareBases(seq1[i - 1], seq2[j - 1]) == matrix[i - 1][j - 1]:  # If the difference in score indicates we got here by matching bases
            local_align1 = seq1[i-1] + local_align1
            local_align2 = seq2[j - 1] + local_align2  # Add a character to both local alignments
            i -= 1
            j -= 1  # Decrement our counters
        elif matrix[i][j] == matrix[i][j - 1] - 4:  # If the matrix indicates we got here by introducing a gap in seq1
            local_align1 = "-" + local_align1  # Add the gap in seq1
            local_align2 = seq2[j - 1] + local_align2  # Take a character from seq2
            j -= 1  # Decrement the appropriate counter
        elif matrix[i][j] == matrix[i - 1][j] - 4:  # If the matrix indicates we got here by introducing a gap in seq2
            local_align1 = seq1[i - 1] + local_align1  # Take a character from seq1
            local_align2 = "-" + local_align2  # Add the gap in seq2
            i -= 1
        else:  # If we run into an error - we shouldn't get here with a correct scorematrix
            print("REEE")  # Output it
    return local_align1, local_align2  # Return the two strings (these are compatible with display_alignment)


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

scorematrix = initMatrix(len(seq1) + 1, len(seq2) + 1)  # Initialise the scorematrix
# score(len(seq1), len(seq2), seq1, seq2, scorematrix) # This approach doesn't work for large sequences because it hits recursion depth

best_score = -1  # Keep a variable to track the best score - it cannot be lower than zero

for i in range(0, len(scorematrix), 750):  # Iterate through the matrix filling it in blocks of 750x750
    for j in range(0, len(scorematrix[i]),
                   750):  # This seems really silly but CPython has a recursion depth limit of 1000, so I have to fill the matrix in like this
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

best_alignment = align(seq1, seq2, scorematrix, best_index)  # Calculate the local alignment of the two strings

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

