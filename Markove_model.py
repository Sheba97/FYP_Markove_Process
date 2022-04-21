#import libries
import csv
import numpy as np

#function to obtain all the setions, time off, time on, and delaytimes
temp =[]
def getLines(input_file):
    for line in input_file:
        temp.append(line[3:7])
    return temp

#function to validate size of data in sections and filling data
def sectionsValidation(sections):
    
    tempDictionary ={}

    def sectionsFilling(combinations):
        keyWords = list(sections.keys())
        for item in combinations:
            if item not in keyWords:
                sections[item] = 0
    
    def orderCorrecting(combinations):
        for key_value in combinations:
            sections[key_value] = sections[key_value]

    if NumberOfSections == 2:
        combinations = ['1','2','12']
        sectionsFilling(combinations)
        orderCorrecting(combinations)
    elif NumberOfSections == 3:
        combinations = ['1','2','3','12','13','23','123']
        sectionsFilling(combinations)
        orderCorrecting(combinations)

    #print(sections)
    return sections
    #return tempDictionary
    #return getFailureRate(sectionsDic)


#function to obtain number of section
sectionsDic = {}
def getSection(section_data):
    for data in section_data:
        section = data[3]
        if section not in sectionsDic:
            sectionsDic[section] = 0
        sectionsDic[section] += 1
    return sectionsValidation(sectionsDic)
    
#function to obtain delaytime in section wise
delayTime = {}
def getDelayTime(data):
    for item in data:
        if item[3] not in delayTime:
            delayTime[item[3]] = float(item[2])
        else:
            delayTime[item[3]] += float(item[2])
    return delayTime
    #return sectionsValidation(delayTime)

#function to obtain failure rate in section wise
failureRate = {}
def getFailureRate(data):
    for name,value in data.items():
        Lamba = value/years
        failureRate[name] = Lamba
    return failureRate
    #return sectionsValidation(delayTime)

#function to obtain repaire rate in section wise
repairRate = {}
def getRepairRate(sections,delaytime):
    for keys,values in delaytime.items():
        repairRate[keys] = round(((8760*sections[keys])/values)/5,3)
    #return repairRate
    return sectionsValidation(repairRate)

#selecting matrix for sections
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
        self.matSize = 2*(2**(self.num_sections)-1) 

        #add first row to the transition matrix
        self.transitionMatrix = [[i / i for i in range(1, self.matSize + 1)]]     

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

def getProbability(result):
    for i in result:
        print(i[0])
        
#open and read the data from csv file
if __name__ == '__main__':
    filename = input("Enter the filename with location: - ")
    years = int(input("Enter number of years:- "))
    NumberOfSections = int(input("Enter number of sections of the feeder:- "))
    with open(filename+'.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        getLines(csv_reader)
    
    #calling the functions
    getSection(temp[1:])
    getDelayTime(temp[1:])
    getFailureRate(sectionsDic)
    getRepairRate(sectionsDic, delayTime)

    print("Sections:- ",sectionsDic)
    print("failure rates: - ",failureRate)
    print("delay time:- ",delayTime)
    print("repair rate:- ",repairRate)
    
    fRate = list(failureRate.values())
    rRate = list(repairRate.values())

    mat = Matrix(fRate,rRate,NumberOfSections)

    print(mat.createMatrix())
    getProbability(mat.matrixCalling())