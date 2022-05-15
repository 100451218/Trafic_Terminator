import csv
import pathlib

# We want to get the path to the file, we uese the Path.home for easier transfer and simultaneous work.
initial_path = pathlib.Path.home()
path_to_cls = str(initial_path) + "\PycharmProjects\Trafic_Terminator\data_loader\Data.csv"
file = open(path_to_cls)
csvreader = csv.reader(file)

# Define the variables for the problem
states = ["HHH", "HHL", "HLH", "HLL", "LHH", "LHL", "LLH", "LLL"]
"""
#This is for increasing the adaptability of the MDP, remove the strings if using itertools is allowed.
types_of_traffic = ["H","L"]
number_of_streets = 3
import itertools
states_aux = list(itertools.product(types_of_traffic, repeat=3))
states = []
for state in states_aux:
    states.append("".join(state))
"""
goal_states = ["LLL"]
actions = ["N", "E", "W"]
probability_dictionary = {}
cost = {}
for action in actions:
    # This code should be changed adding ifs for variable cost of action, or a usual dictionary could be created.
    cost[action] = 20

# We load the probability with the initial states and the possible actions to be performed
for state in states:
    if state not in goal_states:
        probability_dictionary[state] = {}
        for action in actions:
            probability_dictionary[state][action] = {}

# In this part, we will add the data into the probability dictionary
# First we put all the times we get from an state with another with an action
for i in csvreader:
    get_elements = i[0].split(";")
    # This next if statement is made because we need to not read the first row of the data
    if get_elements[0][0] == "I":
        pass
    else:
        # We get the initial state, the action performed and the final action of each row
        i_state = get_elements[0][0] + get_elements[1][0] + get_elements[2][0]
        action = get_elements[3]
        f_state = get_elements[4][0] + get_elements[5][0] + get_elements[6][0]
        # And we store them in the corresponding position in the dictionary
        try:
            # If the key has been created, we add one to the value of that key
            probability_dictionary[i_state][action][f_state] += 1
        except KeyError:
            # If it is the first time that the key is used, we need to create it
            probability_dictionary[i_state][action][f_state] = 1

# After executing the code above, the probability dictionary will contain only the number of times
# we reached a state from an initial state and performing some action

# In second place, we need to transform that number of times into a probability
for i_state in probability_dictionary:
    for action in probability_dictionary[i_state]:
        # To get the probabilities, for every state and action possible, we add the number of
        # final states that can occur.
        total = 0
        for f_state_value in probability_dictionary[i_state][action]:
            total += probability_dictionary[i_state][action][f_state_value]

        # And after that we divide the number obtained to all the final states, getting the probability
        for f_state_value in probability_dictionary[i_state][action]:
            probability_dictionary[i_state][action][f_state_value] = probability_dictionary[i_state][action][
                                                                         f_state_value] / total

"""
In probability dictionary we have the probabilities that can be obtained from the Data.csv file.
This dictionary is structured following the next structure:
{'key of starting state':{'Action':{'Resulting state': 'Probability of getting to that state',...},...},...}
We have not included the Resulting states where the probabilities are 0.
"""
print(
    "Probability dictionary on format 'starting_state':{'action1':{'arrived_state':'Paction1(arrived_state|starting_state)',...},...}")
print(probability_dictionary)


def GetAction(Action, Starting_State):
    """Get action performs the summation inside the Bellman equation for one state and one action,
        taking into account the cost of the action"""
    result = cost[Action]
    for i in probability_dictionary[Starting_State][Action]:
        result += (probability_dictionary[Starting_State][Action][i] * Value[i])

    return result


def GetMin(Starting_State):
    """GetMin will get one starting state and return the expected values for
    that state, to do so, it """
    # We want to get all the values for every action
    all_actions = []
    for action in actions:
        # GetAction is executed for every action possible in the state given.
        all_actions.append(GetAction(action, Starting_State))
    # Once obtained, we want to return the minimal action
    return round(min(all_actions), 6)


# In this part, we create the dictionaries that will be used to store the expected values for each state
Value = {}
Next_Value = {}

for i in probability_dictionary:
    Value[i] = 0
    Next_Value[i] = 0

for goal_state in goal_states:
    Value[goal_state] = 0
    Next_Value[goal_state] = 0

# Of course, there is no value of 'LLL' as it is always 0

# Once the dictionaries for the next state and the previous state have been created,
# the code starts to create the Bellman equations until the difference between the
# expected values for one iteration are equal up to 3 decimal places in all the states

condition_stop = False
cicles = 0
while condition_stop == False:
    cicles += 1
    Value = Next_Value
    # Nest_Value is emptied to store the new expected values, using Value as the previous iteration
    Next_Value = {}
    for i in states:
        if i not in goal_state:
            Next_Value[i] = GetMin(i)
        elif i in goal_state:
            Next_Value[i] = 0

    # This final part checks when to end the code, if the expected values of all the states
    # differ by less than 0.0001 to the previous iteration, the code should stop.
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

# The final step is to check the optimal policy, it is easy to do so with the function GetAction
optimal_policy = {}
for state in Value.keys():
    op_action = {}
    # We cannot check the goal because the statement determines we stop as soon as we reach the goal state
    if state not in goal_state:
        for action in actions:
            # We just use GetAction for every possible action in each state,
            # so we have the cost of each action in a dictionary
            op_action[action] = GetAction(action, state)
        # And we select the action with minimum cost and store it in another dictionary
        optimal_policy[state] = min(op_action, key=op_action.get)
print("optimal policy of the system:")
print(optimal_policy)
