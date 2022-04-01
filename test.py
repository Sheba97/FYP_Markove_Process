def createMatrix(fRate,rRate,sections):
    sRate = 8760
    matSize = 2*(2**(len(sections)-1)-1)

    transitionMatrix = [[i / i for i in range(1, matSize + 1)]]

    #get first raw item since second raw
    for i in range(2,matSize+1):
        if i%2 == 0:
            row_item = fRate[int(i/2)-1]
            transitionMatrix.append([row_item])
        else:
            row_item = 0
            transitionMatrix.append([row_item])

    #create zero matrix
    zero_matrix = []
    for j in range(matSize-2):
        row = [0*k for k in range(matSize-1)]

        #change diagonal of zero matrix
        if j%2 == 0:
            row[j] = -sRate
        else:
            row[j] = -rRate[int(j/2)]
        zero_matrix.append(row)
    #create last row of the zero matrix and append it to zero matrix
    last_row = [0*i for i in range(matSize-2)] + [-rRate[len(rRate)-1]]
    zero_matrix.append(last_row)

    count = 0
    for items in zero_matrix[1:len(zero_matrix)-1]:
        if count%2 == 0:
            items[count] = sRate
        count+=1

    #transition matrix creation
    for k in range(1,matSize):
        transitionMatrix[k] = transitionMatrix[k] + zero_matrix[k-1]

    return (transitionMatrix)

if __name__ == '__main__':

    failureRate = {'Section 1': 42.2, 'Section 2': 28.4, 'Section 1 & 2': 17.4}
    repairRate = {'Section 1': 4029.123, 'Section 2': 5907.955, 'Section 1 & 2': 5113.183}
    sections = {'Section 1': 211, 'Section 2': 142, 'Section 1 & 2': 87}
   
    fRate = list(failureRate.values())
    rRate = list(repairRate.values())

    print(createMatrix(fRate,rRate,sections))