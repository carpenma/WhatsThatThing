import numpy as np

def matrix2Char(matrix, fullRank):
    finalChar = []
    finalMatrix = np.zeros([fullRank,fullRank, fullRank])
    finalMatrix[:matrix.shape[0],:matrix.shape[1],:matrix.shape[2]] = matrix
    
    for i in range(fullRank):
        for j in range(fullRank):
            finalChar.append(row2int(finalMatrix[i,j]))

    return ','.join(finalChar)

def row2int(row):
    #TODO: Force to display full 4 hex places
    #TODO: Remove leading '0x'
    rowAsStr = ''.join(np.char.mod('%d',row))
    characters = hex(int(rowAsStr,2))
    #print(characters)
    return characters

if __name__ == "__main__":
    print("Unit Tests")
    res = matrix2Char(np.array([[[1, 0, 1],[0, 0, 1]], [[0, 1, 0],[1, 0, 0]]]), 16)
    print(res)


