from Markove_model import*
from Matrix import*
import csv

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
print("failure rates: - ",output2)
#print("delay time:- ",delayTime)
print("repair rate:- ",output3)

fRate = list(output2.values())
rRate = list(output3.values())

mat = Matrix(fRate,rRate,NumberOfSections)

print(mat.createMatrix())
getProbability(mat.matrixCalling())