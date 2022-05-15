import csv
import pathlib

#We want to get the path to the file, we uese the Path.home for easier transfer and simultaneous work.
initial_path = pathlib.Path.home()
path_to_cls = str(initial_path) + "\PycharmProjects\Trafic_Terminator\data_loader\Data.csv"
file = open(path_to_cls)
csvreader = csv.reader(file)



#Define the variables for the problem
states=["HHH","HHL","HLH","HLL","LHH","LHL","LLH", "LLL"]
goal_states=["LLL"]
actions=["N","E","W"]
probability_dictionary={}
cost={}
for action in actions:
    #This code should be changed adding ifs for variable cost of action, or a usual dictionary could be created.
    cost[action]=20

#We load the probability with the initial states and the possible actions to be performed
for state in states:
    if state not in goal_states:
        probability_dictionary[state]={}
        for action in actions:
            probability_dictionary[state][action]={}


#In this part, we will load add the data into the probability dictionary
#First we put all the times we get from an state with another with an action
for i in csvreader:
    get_elements = i[0].split(";")
    #This is made because we need to not read the first row of the data, if that line dissapears the code still works.
    if get_elements[0][0] == "I":
        pass
    else:
        i_state = get_elements[0][0] + get_elements[1][0] + get_elements[2][0]
        action = get_elements[3]
        f_state = get_elements[4][0] + get_elements[5][0] + get_elements[6][0]
        try:
            probability_dictionary[i_state][action][f_state] += 1
        except KeyError:
            probability_dictionary[i_state][action][f_state] = 1

#Second, we transform that number of times into a probability
for i_state in probability_dictionary:
    for action in probability_dictionary[i_state]:
        total = 0
        for f_state_value in probability_dictionary[i_state][action]:
            total += probability_dictionary[i_state][action][f_state_value]
        for f_state_value in probability_dictionary[i_state][action]:
            probability_dictionary[i_state][action][f_state_value] = probability_dictionary[i_state][action][f_state_value] / total

"""
In probability dictionary we have the probabilities that can be obtained from the Data.csv file.
This dictionary is structured following the next structure:
{'key of starting state':{'Action':{'Resulting state': 'Probability of getting to that state',...},...},...}
We have not included the Resulting states where the probabilities are 0.
"""
print("Probability dictionary on format 'starting_state':{'action1':{'arrived_state':'Paction1(arrived_state|starting_state)',...},...}")
print(probability_dictionary)


def GetAction(Action, Starting_State):
    result=cost[Action]
    for i in probability_dictionary[Starting_State][Action]:
        result += (probability_dictionary[Starting_State][Action][i]*Value[i])

    return result

def GetMin(Starting_State):
    #We want to get all the values for every action
    all_actions=[]
    for action in actions:
        all_actions.append(GetAction(action,Starting_State))
    #Once obtained, we want to return the minimal action
    return round(min(all_actions),6)

Value={}
Next_Value={}
for i in probability_dictionary:
    Value[i]=0
    Next_Value[i]=0

for goal_state in goal_states:
    Value[goal_state]=0
    Next_Value[goal_state]=0


#Of corse, there is no value of 'LLL' as it is always 0

#Next_Value={'HHH':GetMin('HHH'),'HHL':GetMin('HHL'),'HLH':GetMin('HLH'),'HLL':GetMin('HLL'),'LHH':GetMin('LHH'),'LLH':GetMin('LLH'),'LHL':GetMin('LHL'), 'LLL':0}

condition_stop=False
cicles=0
while condition_stop==False:
    cicles+=1
    Value = Next_Value
    Next_Value={}
    for i in states:
        if i not in goal_state:
            Next_Value[i]=GetMin(i)
        elif i in goal_state:
            Next_Value[i]=0
    count = 0
    for k in Next_Value:
        if Next_Value[k] - Value[k] < 0.00001:
            count += 1
        if count == len(Value):
            condition_stop = True

print("Expected Values:")
print(Value)
print("Number of iterations to achieve a fix point:")
print(cicles)


optimal_policy = {}
for state in Value.keys():
    op_action={}
    #We cannot check the goal because the statement determines we stop as soon as we reach the goal state
    if state not in goal_state:
        """
        N_action = GetAction("N",key)
        E_action = GetAction("E",key)
        W_action = GetAction("W",key)
        best = min(N_action, E_action, W_action)

        if best == N_action:
            optimal_policy[key] = "N"
        elif best == E_action:
            optimal_policy[key] = "E"
        else:
            optimal_policy[key] = "W"
        """
        for action in actions:
            op_action[action] = GetAction(action, state)
        optimal_policy[state] = min(op_action, key=op_action.get)
print("optimal policy of the system:")
print(optimal_policy)
