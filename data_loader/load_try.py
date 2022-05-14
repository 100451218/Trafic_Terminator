import csv
import pathlib

initial_path = pathlib.Path.home()
path_to_cls = str(initial_path) + "\PycharmProjects\Trafic_Terminator\data_loader\Data.csv"
file = open(path_to_cls)
csvreader = csv.reader(file)

probability_dictionary = {"HHH": {"N": {}, "W": {}, "E": {}},
         "HHL": {"N": {}, "W": {}, "E": {}},
         "HLH": {"N": {}, "W": {}, "E": {}},
         "HLL": {"N": {}, "W": {}, "E": {}},
         "LHH": {"N": {}, "W": {}, "E": {}},
         "LHL": {"N": {}, "W": {}, "E": {}},
         "LLH": {"N": {}, "W": {}, "E": {}}
         }

for i in csvreader:
    get_elements = i[0].split(";")
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

print(probability_dictionary)


def GetAction(Action, Starting_State):
    result=20
    for i in probability_dictionary[Starting_State][Action]:
        result += (probability_dictionary[Starting_State][Action][i]*Value[i])

    return result

def GetMin(Starting_State):
    Action_N=GetAction('N', Starting_State)
    Action_W=GetAction("W",Starting_State)
    Action_E=GetAction("E", Starting_State)
    return round(min(Action_E,Action_W,Action_N),6)

Value={'HHH':0,'HHL':0,'HLH':0,'HLL':0,'LHH':0,'LLH':0,'LHL':0, 'LLL':0}
Next_Value={'HHH':0,'HHL':0,'HLH':0,'HLL':0,'LHH':0,'LLH':0,'LHL':0, 'LLL':0}
#Of corse, there is no value of 'LLL' as it is always 0

#Next_Value={'HHH':GetMin('HHH'),'HHL':GetMin('HHL'),'HLH':GetMin('HLH'),'HLL':GetMin('HLL'),'LHH':GetMin('LHH'),'LLH':GetMin('LLH'),'LHL':GetMin('LHL'), 'LLL':0}

condition_stop=False
cicles=0
while condition_stop==False:
    cicles+=1
    Value = Next_Value

    Next_Value = {'HHH': GetMin('HHH'), 'HHL': GetMin('HHL'), 'HLH': GetMin('HLH'), 'HLL': GetMin('HLL'),
                  'LHH': GetMin('LHH'), 'LLH': GetMin('LLH'), 'LHL': GetMin('LHL'), 'LLL': 0}
    count = 0
    for k in Next_Value:
        if Next_Value[k] - Value[k] < 0.00001:
            count += 1
        if count == len(Value):
            condition_stop = True


print(Value)
print(cicles)


optimal_policy = {}
for key in Value.keys():
    if key != "LLL":
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
print(optimal_policy)
