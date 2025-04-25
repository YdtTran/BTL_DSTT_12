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


def LUDecomposition(basematrix, n):
    U = basematrix.copy()
    L = createIdentityMatrix(n)
    store = []
    store.append(copy.deepcopy(U))
    for i in range(0, n):
        for j in range(i + 1, n):
            try:
                factor = U[j][i] / U[i][i]
            except:
                return L, U, store, False
            L[j][i] = factor
            for k in range(i, n):
                U[j][k] = U[j][k] - factor * U[i][k]
        store.append(copy.deepcopy(U))
    store.remove(store[len(store) - 1])
    # check if U is upper triangular
    if calculateRank(U) != n:
        return L, U, store, False
    return L, U, store, True


def PLUDecomposition(basematrix, n):
    U = basematrix.copy()
    L = createIdentityMatrix(n)
    matrixP = createIdentityMatrix(n)
    store = []
    store.append(copy.deepcopy(U))


def calculateRank(matrix):
    rank = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                rank += 1
                break
    return rank
