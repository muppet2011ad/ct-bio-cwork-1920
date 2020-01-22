#!/usr/bin/python
import time
import sys

num_alignments = 0

def findAlignment(A,B):
    global num_alignments
    # Base case
    if A == "" and B == "":
        return 0, ""
    # Match characters section
    if A != "" and B != "":
        matchDict = {"A": 3,
                     "C": 2,
                     "G": 1,
                     "T": 2}
        if A[-1] == B[-1]:
            charScore = matchDict[A[-1]]
        else:
            charScore = -3
        matchScore, matchAlign = findAlignment(A[:-1],B[:-1])
        num_alignments += 1
        matchAlign += "0"
        matchScore += charScore
    else:
        matchAlign = ""
        matchScore = sys.maxsize * -2 + 1
    # Insert gap in A
    if B != "":
        gapAScore, gapAAlign = findAlignment(A,B[:-1])
        num_alignments += 1
        gapAAlign += "1"
        gapAScore -= 4
    else:
        gapAAlign = ""
        gapAScore = sys.maxsize * -2 + 1
    # Insert gap in B
    if A != "":
        gapBScore, gapBAlign = findAlignment(A[:-1],B)
        num_alignments += 1
        gapBAlign += "2"
        gapBScore -= 4
    else:
        gapBAlign = ""
        gapBScore = sys.maxsize * -2 + 1
    # Calculate best option
    options = [[matchScore,matchAlign],[gapAScore,gapAAlign],[gapBScore,gapBAlign]]
    best = max(options, key=lambda x: x[0])
    return best

def align(A,B,alignment):
    stringA = ""
    indexA = len(A) - 1
    stringB = ""
    indexB = len(B) - 1
    for i in alignment:
        if i == "0":
            stringA += A[indexA]
            indexA -= 1
            stringB += B[indexB]
            indexB -= 1
        elif i == "1":
            stringA += "-"
            stringB += B[indexB]
            indexB -= 1
        elif i == "2":
            stringA += A[indexA]
            indexA -= 1
            stringB += "-"
    return stringA,stringB



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
