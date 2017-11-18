import sys
import time
from itertools import chain, combinations
from copy import deepcopy

project_count = int(input())
projects = list()
for i in range(project_count):
    x=input().split()
    x = [int(j) for j in x]
    projects.append(x)
project = sorted(projects, key = lambda x: sum(x))[0]
main_project = list()
print(project,file=sys.stderr)
for i in range(len(project)):
    if project[i] > 0:
        for j in range(i):
            main_project.append(chr(65+i))
print(main_project,file=sys.stderr)
### DIAGNOSIS MODULE ###
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def return_powersets(array):
    powerset_result = []
    all_samples = list()
    start_time = time.time()
    
    for key,dic in array.items():
        if dic['carried_by'] != 1 and dic['health'] > 0:
            all_samples.insert(0,key)
             
    for result in powerset(all_samples):
        if len(result) <= 3:
            powerset_result.append(list(result))
        if len(result) == 4:
            break
        if time.time() - start_time > 0.00055:
            break
    return powerset_result

def enough_molecues(robot,avaible_molecues, dic):
    for key, value in avaible_molecues.items():
        if robot.storage[key] + value < dic[key]:
            return False
    return True

def costs_of_set(one_set, avaible_molecules,avaible_samples):
    cost = dict()
    for key, value in avaible_molecules.items():
        cost[key] = 0
        for sample_id in one_set:
            cost[key] += avaible_samples[sample_id]['costs'][key]
    return cost
    
def afford_on_set(robot,avaible_molecules,set_costs):
    empty_slots = 10 - sum(robot.storage.values())
    #print("set_costs",set_costs,file=sys.stderr)
    for key,value in set_costs.items():
        needed_slots = value-robot.storage[key]
        
        if needed_slots > 0:
            empty_slots -= needed_slots
            
        if avaible_molecules[key] < needed_slots or empty_slots < 0:
            return False        
    return True

def health_of_set(one_set, avaible_samples):
    health = 0
    for i in one_set:
        health += avaible_samples[i]['health']
    return health
        
def all_avaible_powersets(robot,avaible_molecules,avaible_samples):
    subsets = return_powersets(avaible_samples)
    avaible_subsets = list()
    #print("subset",subsets,file=sys.stderr)
    for one_set in subsets:
        set_cost = costs_of_set(one_set,avaible_molecules,avaible_samples)
        if afford_on_set(robot,avaible_molecules,set_cost):
            avaible_subsets.append([one_set, health_of_set(one_set,avaible_samples)])
    return avaible_subsets

def consider_project(x,avaible_samples):
    equal_molecule = 0
    print(x,file=sys.stderr)
    for sample_id in x[0]:
        print(sample_id,"if",file=sys.stderr)
        if avaible_samples[sample_id]['gain'] in main_project:
            equal_molecule += 1
            
    return equal_molecule * 10
    
def best_set(robot, avaible_molecules,avaible_samples):
    x = all_avaible_powersets(robot,avaible_molecules,avaible_samples)
    x = sorted(x)
    return sorted(x, key = lambda x: x[1]+len(x[0])*5 + consider_project(x,avaible_samples), reverse = True)[0][0]
    
### STRUCTURE ###

class Player(object):
    def __init__(self,id):
        self.id = id
        self.data_list = []
        self.storage=dict()
        self.target = str()
        self.completed_data = list()
        self.undiagnozed = list()
        self.data_level = 0
        self.array_of_levels = [1,1,1,1,1,1,2,2,2,3]
        
    def _str_(self):
        print("ID: ",self.id,file=sys.stderr)
        print("Target: ",self.target, file=sys.stderr) 
        print("Data list: ",self.data_list,file=sys.stderr)
        print("Storage: ",self.storage,file=sys.stderr)
        print("Completed data :",self.completed_data,file=sys.stderr)
        print("Undiagnozed: ",self.undiagnozed,file=sys.stderr)

robot = Player(0)

### MOLECULES MODULE ###

def enough_molecoues(avaible_samples,robot,avaible_molecues):
    if sum(robot.storage.values()) < 10:
        for i in range(len(robot.data_list)): #uwzgledniam po kolei dla trzech elementow
            sample_id = robot.data_list[i]
            needed_dictionary = avaible_samples[sample_id]['costs'] #slownik rzeczy potrzebnych do danej probki
            need = [key for key, value in needed_dictionary.items() if value > 0] #molekuy ktory sa niezerowe (potrzebne)

            for j in need:
                #potrzebuje obliczyc ile molekul do wczesniejszych elementow mam juz w plecaku
                used = 0
                for k in range(0,i):
                    used_id = robot.data_list[k]
                    used += avaible_samples[used_id]['costs'][j]
                
                if(robot.storage[j] - used < needed_dictionary[j]):
                    if avaible_molecues[j] > 0:
                        return j
                        
   # print("wyrzucam prawde", needed_dictionary, need, file=sys.stderr)
    return True    
    
### LABORATORY MODULE ###
def good_sample(new_set,avaible_samples,level):
    health_sum = 0
    for sample_id in new_set:
        health_sum += avaible_samples[sample_id]['health']
        
    if level <= 2 and health_sum >= 10 or health_sum >=20:
        return True
    
    return False
    
def complete(sample_id,storage,avaible_samples):
    for key, value in avaible_samples[sample_id]['costs'].items():
        if storage[key] < value:
            return False
    return True
    
def data_finished(robot):
    finished_data = list()
    storage = deepcopy(robot.storage)
    for sample_id in robot.data_list:
        if complete(sample_id,storage, avaible_samples):
            for key, value in avaible_samples[sample_id]['costs'].items():
                storage[key] -= value
            finished_data.append(sample_id)
    return finished_data
        

avaible_samples = dict()
avaible_molecues = dict()
czekaj=0
eta_move=0
diagnosis_capture=0
while True:
    for i in range(2):        
        target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = input().split()
        eta = int(eta)
        score = int(score)
        expertise_a = int(expertise_a)
        expertise_b = int(expertise_b)
        expertise_c = int(expertise_c)
        expertise_d = int(expertise_d)
        expertise_e = int(expertise_e)
        if i==0:
            robot.storage['A'] = int(storage_a)
            robot.storage['B'] = int(storage_b)
            robot.storage['C'] = int(storage_c)
            robot.storage['D'] = int(storage_d)
            robot.storage['E'] = int(storage_e)
            robot.target = target
            
       # if i==1 and target == "DIAGNOSIS" and robot.target == "DIAGNOSIS":
        #    print("WAIT")
            
    [A,B,C,D,E] = [int(i) for i in input().split()]
    avaible_molecues['A']=A
    avaible_molecues['B']=B
    avaible_molecues['C']=C
    avaible_molecues['D']=D
    avaible_molecues['E']=E
  
    avaible_samples.clear()
    robot.data_list.clear()
    sample_count = int(input())
    print("po wczytaniu danych",file=sys.stderr)
    for i in range(sample_count):
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
        carried_by = int(carried_by)
        health = int(health)
        sample_id = int(sample_id)
        
        rank = int(rank)
        
        if health == -1 and carried_by == 0 and sample_id not in robot.undiagnozed:
                print("sample id: ",sample_id,file=sys.stderr)
                robot.undiagnozed.append(sample_id)
        
        if carried_by == 0:
            robot.data_list.append(sample_id)
            
        cost=dict()
        cost['A']=int(cost_a)
        cost['B']=int(cost_b)
        cost['C']=int(cost_c)
        cost['D']=int(cost_d)
        cost['E']=int(cost_e)
        
        sample=dict()
        sample['health']=int(health)
        sample['costs']=cost
        sample['carried_by']=carried_by
        sample['gain']=expertise_gain
        
        avaible_samples[sample_id] = sample
    
    print(avaible_samples, file=sys.stderr)
    robot._str_()
    #print("sample", avaible_samples, file=sys.stderr)
    
    if robot.target == "START_POS":
        print("GOTO SAMPLES")
    
    elif robot.target == "SAMPLES":
        if len(robot.data_list)+len(robot.completed_data) < 3:
            print("CONNECT ",robot.array_of_levels[robot.data_level+len(robot.data_list)])
        else:
            eta_move = 2
            print("GOTO DIAGNOSIS")
        
    elif robot.target == "DIAGNOSIS": 
        print("diagnozujemy",file=sys.stderr)
        if eta_move > 0:
            print("eta",file=sys.stderr)
            print("WAIT")
            eta_move-=1
            
        elif len(robot.undiagnozed) > 0:
            examine_sample = robot.undiagnozed.pop(0)
            print("CONNECT "+str(examine_sample))
        #wyrzuc niepotrzebne        
        else:
            print("cr",file=sys.stderr)
            current_set = best_set(robot,avaible_molecues,avaible_samples)
            print("www",current_set,file=sys.stderr)
            flag = 0
            for sample_id in robot.data_list:
                if sample_id not in current_set:
                    print("CONNECT ", sample_id)
                    flag = 1
                    break
                
            if flag == 0:
                if len(current_set) == 0:
                    if robot.data_level >= 1:
                        robot.data_level-=1
                        
                    print("GOTO SAMPLES")    
                else:
                    if len(current_set) != len(robot.data_list):
                        
                        for sample_id in current_set:
                            if sample_id not in robot.data_list:
                                print("CONNECT ", sample_id)
                                break                        
                    else:
                        print("GOTO MOLECULES")                                
        
    elif robot.target == "MOLECULES":
        mol = enough_molecoues(avaible_samples,robot,avaible_molecues)

        if mol == True:
            robot.completed_data = data_finished(robot)
            if len(robot.completed_data) > 0:
                eta_move=2
                print("GOTO LABORATORY")
            else:
                print("GOTO DIAGNOSIS")

        else:
            print("CONNECT " + mol)
    
    elif robot.target == "LABORATORY":
        print("lab",file=sys.stderr)
        if eta_move>0:
            eta_move-=1
            print("WAIT")
            
        elif len(robot.completed_data) > 0:
            sample_id = robot.completed_data.pop(0)
            print("CONNECT ",sample_id)            
            if robot.data_level <= len(robot.array_of_levels)-4:    
                robot.data_level +=1
            if avaible_samples[sample_id]['gain'] in main_project:
                main_project.remove(avaible_samples[sample_id]['gain'])
            
        else:
            print("rzed",file=sys.stderr)
            new_set = best_set(robot, avaible_molecues,avaible_samples)
            print("poP",file=sys.stderr)
            if len(new_set) == 0 or not good_sample(new_set,avaible_samples,robot.data_level):                
                print("GOTO SAMPLES")   
             
            else:                
                if new_set == robot.data_list:
                    print("GOTO MOLECULES")
                else:
                    print("GOTO DIAGNOSIS")   
    else:
        print("SOMETHING IS WRONG BITCH")
        
