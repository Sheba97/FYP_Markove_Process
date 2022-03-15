import csv
import numpy as np

#function to obtain all the setion and delaytimes
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

#function to obtain repaire rate in section wise
repairRate = {}
def getRepairRate(sections,delaytime):
    for keys,values in delaytime.items():
        repairRate[keys] = round(((8760*sections[keys])/values)/5,3)
    return repairRate

#open and read the data from csv file

if __name__ == '__main__':
    filename = input("Enter the filename with location: - ")
    years = int(input("Enter number of years:- "))
    with open(filename+'.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        getLines(csv_reader)


getSection(temp[1:])
print(sectionsDic)
print(getDelayTime(temp[1:]))
print(failureRate)
print(getRepairRate(sectionsDic,delayTime))
