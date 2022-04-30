import csv
import pathlib
initial_path = pathlib.Path.home()
print(initial_path)
path_to_cls = str(initial_path) + "\PycharmProjects\Trafic_Terminator\data_loader\Data.csv"
file = open(path_to_cls)
csvreader = csv.reader(file)

Super={"HHH":{"N":0,"W":0,"E":0},
"HHL":{"N":0,"W":0,"E":0},
"HLH":{"N":0,"W":0,"E":0},
"HLL":{"N":0,"W":0,"E":0},
"LHH":{"N":0,"W":0,"E":0},
"LHL":{"N":0,"W":0,"E":0},
"LLH":{"N":0,"W":0,"E":0}
}






for i in csvreader:
    get_elements = i[0].split(";")
    if get_elements[0][0]=="I":
        pass
    else:
        i_state=get_elements[0][0]+get_elements[1][0]+get_elements[2][0]
        action=get_elements[3]
        f_state=get_elements[4][0]+get_elements[5][0]+get_elements[6][0]
        print(i_state, action, f_state)
        Super[i_state][action]=Super[i_state][action]+1

print(Super)