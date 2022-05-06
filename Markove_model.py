#import libraries
import csv
from combinations import *
from Matrix import *
from indices import *

#initial declaretion of dictionaries
sectionsDict = {}
failureRate = {}
repairRate = {}
delayTime = {}
output1 = {}
output2 = {}
output3 = {}

#function to obtain all the setions, time off, time on, and delaytimes
temp =[]
def getLines(input_file):
    for line in input_file:
        temp.append(line[3:7])
    return temp

#function to validate size of data in sections and filling data
def sectionsValidation(sections,id):
    
    def sectionsFilling(combinations):
        keyWords = list(sections.keys())
        for item in combinations:
            if item not in keyWords:
                sections[item] = 0
    
    def orderCorrecting(combinations):
        for key_value in combinations:
            if id ==1:
                output1[key_value] = sections[key_value]
            elif id == 2:
                output2[key_value] = sections[key_value]
            else:
                output3[key_value] = sections[key_value]
    
    combinations = getCombinations(NumberOfSections)

    sectionsFilling(combinations)
    orderCorrecting(combinations)

#function to obtain number of section
def getSection(section_data):
    id = 1

    for data in section_data:
        section = data[3]
        if section not in sectionsDict:
            sectionsDict[section] = 0
        sectionsDict[section] += 1
    return sectionsValidation(sectionsDict,id)
    
#function to obtain delaytime in section wise

def getDelayTime(data):
    for item in data:
        if item[3] not in delayTime:
            delayTime[item[3]] = float(item[2])
        else:
            delayTime[item[3]] += float(item[2])
    return delayTime

#function to obtain failure rate in section wise
def getFailureRate(data):
    id =2
    for name,value in data.items():
        Lamba = value/years
        failureRate[name] = Lamba
    return sectionsValidation(failureRate,id)
    #return failureRate

#function to obtain repaire rate in section wise
def getRepairRate(sections,delaytime):
    id =3
    for keys,values in delaytime.items():
        repairRate[keys] = round(((8760*sections[keys])/values)/5,3)
    return sectionsValidation(repairRate,id)

#function to obtain 
def getProbability(result):
    probabilities = []
    for i in result:
        probabilities.append(i[0])
    return probabilities
         
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
    getFailureRate(sectionsDict)
    getRepairRate(sectionsDict, delayTime)

    print("Sections:- ",output1)
    print("failure rates:- ",output2)
    print("repair rate:- ",output3)
    

    fRate = list(output2.values())
    rRate = list(output3.values())

    mat = Matrix(fRate,rRate,NumberOfSections)

    for item in (mat.createMatrix()):
        print(item)
    probabilities = getProbability(mat.matrixCalling())

    print(probabilities)

    print(getIndices(probabilities,output2,output3,NumberOfSections))