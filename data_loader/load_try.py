import csv
import pathlib

initial_path = pathlib.Path.home()
path_to_cls = str(initial_path) + "\PycharmProjects\Trafic_Terminator\data_loader\Data.csv"
file = open(path_to_cls)
csvreader = csv.reader(file)

Super = {"HHH": {"N": {}, "W": {}, "E": {}},
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
            if type(Super[i_state][action][f_state]) == int:
                Super[i_state][action][f_state] += 1
        except KeyError:
            Super[i_state][action][f_state] = 0

print(Super)
for i_state in Super:
    for action in Super[i_state]:
        total = 0
        for f_state_value in Super[i_state][action]:
            total += Super[i_state][action][f_state_value]
        for f_state_value in Super[i_state][action]:
            Super[i_state][action][f_state_value] = Super[i_state][action][f_state_value] / total

print(Super)