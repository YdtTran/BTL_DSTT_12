import copy


def createIdentityMatrix(n):
    identityMatrix = []
    for i in range(0, n):
        row = []
        for j in range(0, n):
            if i == j:
                row.append(1)
            else:
                row.append(0)
        identityMatrix.append(row)
    return identityMatrix


def LUDecomposition(A, n):
    U = copy.deepcopy(A)
    L = createIdentityMatrix(n)
    for i in range(0, n):
        if U[i][i] == 0:
            return L, U, False
        for j in range(i + 1, n):
            L[j][i] = U[j][i] / U[i][i]
            for k in range(i, n):
                U[j][k] = U[j][k] - L[j][i] * U[i][k]
    return L, U, True


def PLUDecomposition(A, n):
    P = createIdentityMatrix(n)
    L = createIdentityMatrix(n)
    U = copy.deepcopy(A)
    for i in range(0, n):
        if U[i][i] == 0:
            # find pivot row
            pivot = i
            while pivot < n and U[i][pivot] == 0:
                pivot += 1
            # then we swap rows
            if pivot < n:
                U[i], U[pivot] = U[pivot], U[i]
                P[i], P[pivot] = P[pivot], P[i]
        for j in range(i + 1, n):
            L[j][i] = U[j][i] / U[i][i]
            for k in range(i, n):
                U[j][k] = U[j][k] - L[j][i] * U[i][k]
    return P, L, U, True


A = [[0, 1, 0], [-8, 8, 1], [2, -2, 0]]

P, L, U, success = PLUDecomposition(A, 3)
for i in range(0, 3):
    print(P[i])
print("")
for i in range(0, 3):
    print(L[i])
print("")
for i in range(0, 3):
    print(U[i])

print(success)
