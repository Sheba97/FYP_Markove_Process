import itertools
# function to generate all the sub lists

def getCombinations(num):

    def get_sub_lists(l):
        combinations = []
        for r in range(len(l)+1):
            for combination in itertools.combinations(l, r):
                combinations.append(combination)
        return combinations

    # function to generate states
    def get_states(s):
        state = ""
        states_list = []
        for i in s:
            for j in i:
                state = state+str(j)
            states_list.append(state)
            state = ""
        return states_list

    # function to generate sorted list
    def sort_list(states):
        sorted_list = []
        for i in states:
            sorted_list.append(int(i))
        sorted_list.sort()
        return sorted_list

    #driver code
    l1 = []
    for k in range(1, num+1):
        l1.append(k)

    sub = get_sub_lists(l1)
    sub.pop(0)

    Lst =sort_list(get_states(sub))

    for i in range(len(Lst)):
        Lst[i] = str(Lst[i])
    
    return Lst