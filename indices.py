def getIndices(probabilityLst,failurerRate,repaireRate,numberOfSections):
    totalFailureRate = sum(list(failurerRate.values()))
    p_zero = probabilityLst[0]
    p_last = probabilityLst[-1]
    lambdaEq = []
    uEq = []

    frequencyOfFailure = p_zero * totalFailureRate 
    combinations = list(failurerRate.keys())
    probabilityDict = {}

    iterations = (pow(2,numberOfSections)-1)

    print(iterations)

    for i in range(iterations-1):
        temp = probabilityLst[1:-1]
        a = 2*i
        b = 2*(i+1)
        probabilityDict[combinations[i]] = temp[a:b]

    print(probabilityDict)

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
        uEq.append(frequencyOfSuccess/(1-probabilityOfSuccess))
   
    return lambdaEq,uEq

        
    