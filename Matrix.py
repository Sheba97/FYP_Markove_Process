import numpy as np

class Matrix:

    def __init__(self,failureRates,repairRates,num_sections):
        #define attributes for failure rate, repair rate, no. of sections and transition matrix 
        self.failureRates = failureRates
        self.repairRates = repairRates
        self.num_sections = num_sections
        self.transitionMatrix = []
        self.matSize = 0

    def createMatrix(self):
        #default switching rate (deafult switching time is 1hr)
        sRate = 8760  
        
        #size of transition matrix
        self.matSize = 2*(pow(2,self.num_sections)-1) 

        #add first row to the transition matrix
        self.transitionMatrix = [[int(i / i) for i in range(1, self.matSize + 1)]]     

        #get first raw item since second raw
        for i in range(2,self.matSize+1):
            if i%2 == 0:
                row_item = self.failureRates[int(i/2)-1]
                self.transitionMatrix.append([row_item])
            else:
                row_item = 0
                self.transitionMatrix.append([row_item])

        #create zero matrix
        zero_matrix = []
        for j in range(self.matSize-2):

            #define row for zero matrix
            row = [0*k for k in range(self.matSize-1)]

            #change diagonal of zero matrix
            if j%2 == 0:
                row[j] = -sRate
            else:
                row[j] = -self.repairRates[int(j/2)]
            zero_matrix.append(row)

        #create last row of the zero matrix and append it to zero matrix
        last_row = [0*i for i in range(self.matSize-2)] + [-self.repairRates[len(self.repairRates)-1]]
        zero_matrix.append(last_row)

        count = 0
        for items in zero_matrix[1:len(zero_matrix)-1]:
            if count%2 == 0:
                items[count] = sRate
            count+=1

        #transition matrix creation
        for k in range(1,self.matSize):
            self.transitionMatrix[k] = self.transitionMatrix[k] + zero_matrix[k-1]

        return self.transitionMatrix

    #function for matrix inverse and multiplication
    def matrixCalling(self):
        
        matA = [[1]]
        for i in range(1,self.matSize):
            matA.append([0])
        
        # obtain invers of transition matrix
        Inv_transmat = np.linalg.inv(self.transitionMatrix)

        # obtaing probability matrix
        result = np.dot(Inv_transmat,matA)
        return result