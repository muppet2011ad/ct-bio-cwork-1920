lengths = [3, 4, 5, 6, 7, 8, 9, 10, 11]

import matrix


def findAlignment(A, B):  # Function find the alignment of the two string A and B (returns a list of actions that can be applied using align())
    alignments = 0
    # Base case
    if A == "":
        return -4 * len(B), "1" * len(B), 1
    if B == "":
        return -4 * len(A), "2" * len(A), 1
    # Match characters section
    if A != "" and B != "":  # If we have two characters available
        if A[-1] == B[-1]:  # If the two are equal
            charScore = {"A": 3, "C": 2, "G": 1, "T": 2}[A[-1]]  # Get the appropriate score
        else:
            charScore = -3  # Otherwise score is -3
        matchScore, matchAlign, child_alignments = findAlignment(A[:-1], B[:-1])  # Score from taking this approach needs recursion
        matchAlign += "0"  # Add the corresponding action (0 = match chars)
        matchScore += charScore  # Increase the score accordingly
        alignments += child_alignments
    else:
        matchAlign = ""  # If we can't do this alignment, it's impossible so set this to a blank
        matchScore = sys.maxsize * -2 + 1  # Set the score to the lowest possible (this makes it impossible for it to be selected)
    # Insert gap in A
    if B != "":
        gapAScore, gapAAlign, child_alignments = findAlignment(A, B[:-1])  # Get base score through recursion
        gapAAlign += "1"  # Add action (1 = gap in A)
        gapAScore -= 4  # Decrease score by gap penalty
        alignments += child_alignments
    else:
        gapAAlign = ""
        gapAScore = sys.maxsize * -2 + 1
    # Insert gap in B
    if A != "":
        gapBScore, gapBAlign, child_alignments = findAlignment(A[:-1], B)
        gapBAlign += "2"
        gapBScore -= 4
        alignments += child_alignments
    else:
        gapBAlign = ""
        gapBScore = sys.maxsize * -2 + 1
    # Calculate best option
    options = [[matchScore, matchAlign], [gapAScore, gapAAlign], [gapBScore, gapBAlign]]  # Array to store options
    best = max(options, key=lambda x: x[0])  # Finds the best option based on the score
    return best[0], best[1], alignments  # Return that best option


scores = matrix.Matrix(len(lengths), len(lengths))

for i in range(len(lengths)):
    for j in range(len(lengths)):
        print("Calculating A:", lengths[i], "B:", lengths[j])
        seq1 = open("TestFiles/length" + str(lengths[i]) + "_A.txt").read()
        seq2 = open("TestFiles/length" + str(lengths[j]) + "_B.txt").read()
        best_score, best_align_string, num_alignments = findAlignment(seq1, seq2)
        scores.matrix[j][i] = best_score

scores.printMatrix()
