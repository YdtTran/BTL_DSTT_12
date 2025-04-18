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
    matrixU = basematrix.copy()
    matrixL = createIdentityMatrix(n)
    matrixStore = []
    matrixStore.append(copy.deepcopy(matrixU))
    for i in range(0, n):
        for j in range(i + 1, n):
            try:
                factor = matrixU[j][i] / matrixU[i][i]
            except:
                return matrixL, matrixU, matrixStore, False
            matrixL[j][i] = factor
            for k in range(i, n):
                matrixU[j][k] = matrixU[j][k] - factor * matrixU[i][k]
        matrixStore.append(copy.deepcopy(matrixU))
    matrixStore.remove(matrixStore[len(matrixStore) - 1])
    # check if matrixU is upper triangular
    if calculateRank(matrixU) != n:
        return matrixL, matrixU, matrixStore, False
    return matrixL, matrixU, matrixStore, True


def PLUDecomposition(basematrix, n):
    matrixU = basematrix.copy()
    matrixL = createIdentityMatrix(n)
    matrixP = createIdentityMatrix(n)
    matrixStore = []
    for i in range(0, n):
        for j in range(i + 1, n):
            try:
                factor = matrixU[j][i] / matrixU[i][i]
            except:
                # có số 0 trên đường chéo chính thì đổi hàng

                return matrixL, matrixU, matrixStore, False
            matrixL[j][i] = factor
            for k in range(i, n):
                matrixU[j][k] = matrixU[j][k] - factor * matrixU[i][k]
        matrixStore.append(copy.deepcopy(matrixU))
    matrixStore.remove(matrixStore[len(matrixStore) - 1])
    # check if matrixU is upper triangular
    if calculateRank(matrixU) != n:
        return matrixL, matrixU, matrixStore, False
    return matrixL, matrixU, matrixStore, True


def calculateRank(matrix):
    rank = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                rank += 1
                break
    return rank
