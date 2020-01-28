#!/usr/bin/python
import time
import sys

num_alignments = 0


def findAlignment(A, B):  # Function find the alignment of the two string A and B (returns a list of actions that can be applied using align())
    global num_alignments  # Make sure we access the global variable num_alignments
    num_alignments += 1
    # Base case
    if A == "" and B == "":
        return 0, ""
    # Match characters section
    if A != "" and B != "":  # If we have two characters available
        if A[-1] == B[-1]:  # If the two are equal
            charScore = {"A": 3, "C": 2, "G": 1, "T": 2}[A[-1]]  # Get the appropriate score
        else:
            charScore = -3  # Otherwise score is -3
        matchScore, matchAlign = findAlignment(A[:-1], B[:-1])  # Score from taking this approach needs recursion
        matchAlign += "0"  # Add the corresponding action (0 = match chars)
        matchScore += charScore  # Increase the score accordingly
    else:
        matchAlign = ""  # If we can't do this alignment, it's impossible so set this to a blank
        matchScore = sys.maxsize * -2 + 1  # Set the score to the lowest possible (this makes it impossible for it to be selected)
    # Insert gap in A
    if B != "":
        gapAScore, gapAAlign = findAlignment(A, B[:-1])  # Get base score through recursion
        gapAAlign += "1"  # Add action (1 = gap in A)
        gapAScore -= 4  # Decrease score by gap penalty
    else:
        gapAAlign = ""
        gapAScore = sys.maxsize * -2 + 1
    # Insert gap in B
    if A != "":
        gapBScore, gapBAlign = findAlignment(A[:-1],B)
        gapBAlign += "2"
        gapBScore -= 4
    else:
        gapBAlign = ""
        gapBScore = sys.maxsize * -2 + 1
    # Calculate best option
    options = [[matchScore, matchAlign], [gapAScore, gapAAlign], [gapBScore, gapBAlign]]  # Array to store options
    best = max(options, key=lambda x: x[0])  # Finds the best option based on the score
    return best  # Return that best option

def align(A,B,alignment):
    stringA = ""
    indexA = 0
    stringB = ""
    indexB = 0  # Set up vars and start counting from end of string
    for i in alignment:
        if i == "0":  # If we need to take chars from both
            stringA += A[indexA]
            indexA += 1
            stringB += B[indexB]
            indexB += 1  # Do that
        elif i == "1":
            stringA += "-"
            stringB += B[indexB]
            indexB += 1
        elif i == "2":
            stringA += A[indexA]
            indexA += 1
            stringB += "-"
    return stringA, stringB



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

# -------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# Call any functions you need here, you can define them above.
# To work with the printing functions below the best alignment should be called best_alignment and its score should be called best_score. 
# The number of alignments you have checked should be stored in a variable called num_alignments.

best_score, best_align_string = findAlignment(seq1,seq2)
best_alignment = align(seq1,seq2,best_align_string)

# -------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Alignments generated: '+str(num_alignments))
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------
