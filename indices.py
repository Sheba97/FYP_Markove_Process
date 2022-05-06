def getIndices(probabilityLst,failurerRate,repaireRate,numberOfSections):
    totalFailureRate = sum(list(failurerRate.values()))
    p_zero = probabilityLst[0]
    p_last = probabilityLst[-1]
    lambdaEq = []
    mdtEq = []
    numerator = 0

    frequencyOfFailure = p_zero * totalFailureRate 
    combinations = list(failurerRate.keys())
    probabilityDict = {}

    iterations = (pow(2,numberOfSections)-1)


    #to create probability dictionary from combination 1 to combination (n-1) 
    for i in range(iterations-1):
        temp = probabilityLst[1:-1]
        a = 2*i
        b = 2*(i+1)
        probabilityDict[combinations[i]] = temp[a:b]

    #to find probabilityOfSuccess, frequencyOfSuccess
    for section in combinations[:numberOfSections]:
        probabilityOfSuccess = p_zero
        frequencyOfSuccess = p_last* (repaireRate[combinations[-1]])

        for j in range(len(combinations)):
            state = combinations[j]
            if section not in state:
                if state == combinations[-1]:
                    continue
                else:
                    probabilityOfSuccess += probabilityDict[state][1]
            else:
                if state == combinations[-1] :
                    continue
                else:
                    frequencyOfSuccess += (probabilityDict[state][1]) * repaireRate[state]
        lambdaEq.append(frequencyOfFailure/probabilityOfSuccess)
        mdtEq.append((1-probabilityOfSuccess)/frequencyOfSuccess)
    
    for k in range(numberOfSections):
        numerator += lambdaEq[k]*mdtEq[k]

    denominator = sum(lambdaEq)

    MDT = numerator/denominator

    return lambdaEq,mdtEq,MDT