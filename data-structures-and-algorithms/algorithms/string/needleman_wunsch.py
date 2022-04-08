import sys


def needleman_wunsch(seq1, seq2, scoring_func):
    """
    This finds the global alignment of two sequences according to a the needleman-wunsch algorithm and a scoring
    function.
    :param seq1: a sequence of symbols
    :param seq2: a sequence of symbols
    :param scoring_func: a scoring function for individual symbols
    :return: the alignment of sequences and the score
    """

    # initialize table
    best_score_matrix = [[0 for j in range(1 + len(seq2))] for i in range(1 + len(seq1))]
    for i in range(1 + len(seq1)):
        best_score_matrix[i][0] = -i
    for j in range(1 + len(seq2)):
        best_score_matrix[0][j] = -j

    # first fill in the alignment table
    for i in range(0, len(seq1)):
        for j in range(0, len(seq2)):
            indel1_score = best_score_matrix[i + 1][j] + scoring_func(None, seq2[j])
            indel2_score = best_score_matrix[i][j + 1] + scoring_func(seq1[i], None)
            match_score = best_score_matrix[i][j] + scoring_func(seq1[i], seq2[j])

            best_score_matrix[i + 1][j + 1] = max(indel1_score, indel2_score, match_score)

    # backtrace through the alignment table
    i, j = len(seq1), len(seq2)
    alignment1 = ""
    alignment2 = ""
    while i > 0 or j > 0:

        # if we have reached the end of the sequence 1, then we can only add symbols from sequence 2
        if i == 0:
            j -= 1
            alignment1 = "-" + alignment1
            alignment2 = seq2[j] + alignment2

        # if we have reached the end of the sequence 2, then we can only add symbols from sequence 1
        if j == 0:
            i -= 1
            alignment1 = seq1[i] + alignment1
            alignment2 = "-" + alignment2

        # find the an alignment that could have resulted in the current score
        if i > 0 and j > 0:
            curr_score = best_score_matrix[i][j]
            indel1_score = best_score_matrix[i][j - 1] + scoring_func(None, seq2[j - 1])
            indel2_score = best_score_matrix[i - 1][j] + scoring_func(seq1[i - 1], None)
            match_score = best_score_matrix[i - 1][j - 1] + scoring_func(seq1[i - 1], seq2[j - 1])
            if match_score == curr_score:
                i -= 1
                j -= 1
                alignment1 = seq1[i] + alignment1
                alignment2 = seq2[j] + alignment2
            elif indel2_score == curr_score:
                i -= 1
                alignment1 = seq1[i] + alignment1
                alignment2 = "-" + alignment2
            elif indel1_score == curr_score:
                j -= 1
                alignment1 = "-" + alignment1
                alignment2 = seq2[j] + alignment2

    alignment_score = best_score_matrix[len(seq1)][len(seq2)]
    return alignment1, alignment2, alignment_score


def main():
    seq1 = sys.argv[1]
    seq2 = sys.argv[2]
    alignment1, alignment2, alignment_score = needleman_wunsch(seq1, seq2, lambda x, y: 1 if x == y else -1)

    print(alignment1)
    print(alignment2)
    print(alignment_score)


if __name__ == "__main__":
    main()
