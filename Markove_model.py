#import libries
import csv
import numpy as np

#function to obtain all the setions, time off, time on, and delaytimes
temp =[]
def getLines(input_file):
    for line in input_file:
        temp.append(line[3:7])

#function to obtain number of section
sectionsDic = {}
def getSection(section_data):
    for data in section_data:
        section = data[3]
        if section not in sectionsDic:
            sectionsDic[section] = 0
        sectionsDic[section] += 1
    return getFailureRate(sectionsDic)

#function to obtain delaytime in section wise
delayTime = {}
def getDelayTime(data):
    for item in data:
        if item[3] not in delayTime:
            delayTime[item[3]] = float(item[2])
        else:
            delayTime[item[3]] += float(item[2])
    return delayTime

#function to obtain failure rate in section wise
failureRate = {}
def getFailureRate(data):
    for name,value in data.items():
        Lamba = value/years
        failureRate[name] = Lamba
    return failureRate

#function to obtain repaire rate in section wise
repairRate = {}
def getRepairRate(sections,delaytime):
    for keys,values in delaytime.items():
        repairRate[keys] = round(((8760*sections[keys])/values)/5,3)
    return repairRate

#selecting matrix for sections
class Matrix:

    def __init__(self,failureRates,repairRates,num_sections):
        self.failureRates = failureRates
        self.repairRates = repairRates
        self.num_sections = num_sections


    def matrixCalling(self):

        #intialize the matrix size (nxn matrix)
        matSize = (self.num_sections+1) * 2

        #obtain
        fRate = list(self.failureRates.values())
        rRate = list(self.repairRates.values())

        if num_sections == 2:
            sRate = 400  # set temporary switching rate as 400

            # create transitioon matrix for two sections feeder
            transMat = [[i / i for i in range(1, matSize + 1)], [fRate[0], -sRate] + [i * 0 for i in range(4)],
                        [0, sRate, -rRate[0]] + [i * 0 for i in range(3)],
                        [fRate[1], 0, 0 ,-sRate, 0, 0], [i * 0 for i in range(3)] + [sRate, -rRate[1], 0],
                        [fRate[2]] + [i * 0 for i in range(4)] + [-rRate[2]]]
            matA = [[1], [0], [0], [0], [0], [0]]

            # obtain invers of transition matrix
            Inv_transmat = np.linalg.inv(transMat)

            # obtaing probability matrix
            solution = np.dot(Inv_transmat,matA)
        return solution

#open and read the data from csv file
if __name__ == '__main__':
    filename = input("Enter the filename with location: - ")
    years = int(input("Enter number of years:- "))
    with open(filename+'.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        getLines(csv_reader)
    getSection(temp[1:])
    getDelayTime(temp[1:])
    getRepairRate(sectionsDic, delayTime)
    num_sections = len(sectionsDic) - 1
    mat = Matrix(failureRate,repairRate,num_sections)

    print(mat.matrixCalling())
    print(failureRate)