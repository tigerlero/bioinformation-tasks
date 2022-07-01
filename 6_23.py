infinity = float("inf")


def f(v, w):
    # Build table
    n = len(v)
    m = len(w)

    if S[n][m][1]:
        # Already found solution for n, m, return it
        return S[n][m][0]

    if w == "" or v == "":
        # Encountered empty sequence
        return 0

    same = -1
    if v[-1] == w[-1]:
        same = 1

    a = f(v[:-1], w[:-1]) + same
    b = f(v[:-1], w) - 1
    c = f(v, w[:-1]) - 1

    S[n][m] = (max(a, b, c), True)
    return S[n][m][0]


def trace_seq(mIndex):
    # Trace sequence from maximum node to upper left corner
    A = []
    i, j = mIndex, m-1
    index = -1
    for k in range(mIndex+1):
        A.append((i, j))

        # Find optimal move from (i, j)
        moves = [T[i-1][j-1],
                 T[i][j-1],
                 T[i-1][j]]

        Max = max(moves)
        index = moves.index(Max)

        if index == 0:
            # Encountered diagonal move
            i -= 1
            j -= 1
        elif index == 1:
            # Encountered left move
            j -= 1
        else:
            # Encountered upward move
            i -= 1

    return A


def align(A):
    # Given list A of optimal moves, find optimal alignment
    # by comparing successive moves in A
    seqV = ''
    seqW = ''
    for i, (a1, a2) in enumerate(A[:-1]):
        b1, b2 = A[i + 1]

        if a1 == b1:
            # Left move
            seqV += '-'
            seqW += w[b2]
        elif a2 == b2:
            # Upward move
            seqV += v[b1]
            seqW += '-'
        else:
            # Diagonal move
            seqV += v[b1]
            seqW += w[b2]


    # Add missing letters/gaps from left side
    if A[-1] != (0, 0):
        if A[-1][0] == 0:
            seqW += w[:A[-1][1]][::-1]
            seqV += A[-1][1]*'-'
        elif A[-1][1] == 0:
            seqV += w[:A[-1][0]][::-1]
            seqW += A[-1][0]*'-'

    return seqV[::-1], seqW[::-1]


def calculate_score(A, B):
    s = 0
    for a, b in zip(A, B):
        if a == b and a != '-':
            s += 1
        else:
            s -= 1

    return s


# Comment out one example to test the other
v, w = "AAGC", "AGT" # trivial example
v, w = "CAGCACTTGGATTCTCGG", "CAGCGTGG" # example from book
v, w = "ACGTCAT", "TCATGCA" # example from book

n, m = len(v) + 1, len(w) + 1

S = [[(0, False) for i in range(m)] for j in range(n)]

f(v, w)

mScore = max([s[-1][0] for s in S]) # max score in last column

# last (closer to the bottom) node with max score
mIndex = n-1 - list(reversed([s[-1][0] for s in S])).index(mScore)

# Print and store table with scores only
print("Table:")
T = []
for s in S:
    t = [r[0] for r in s]
    T.append(t)
    print(t)

A = trace_seq(mIndex)
s1, s2 = align(A)
print("\nScore:", calculate_score(s1, s2))
print("\nAlignment:")
print(s1)
print(s2)
