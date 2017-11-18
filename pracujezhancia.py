import sys
import math

class Player(object):
    def __init__(self,id):
        print("jestes tu?",file=sys.stderr)
        self.id = id
        self.data_list = []
        self.storage=dict()
        self.target = str()
        self.completed_data = list()
        self.undiagnozed = list()
        self.data_level = 0
        self.array_of_levels = [1,1,1,2,2,2,3,3]
        
    def _str_(self):
        print("ID: ",self.id,file=sys.stderr)
        print("Target: ",self.target, file=sys.stderr) 
        print("Data list: ",self.data_list,file=sys.stderr)
        print("Storage: ",self.storage,file=sys.stderr)
        print("Completed data :",self.completed_data,file=sys.stderr)
        print("Undiagnozed: ",self.undiagnozed,file=sys.stderr)
        
    def clear(self):
        for i in self.completed_data:
            if i in self.data_list:
                self.data_list.remove(i)
        
robot = Player(0)

def best_sample_id(avaible,avaible_samples):
    best_id = None
    for sample_id in avaible:
        if best_id is None:
            best_id = sample_id
        elif avaible_samples[sample_id]['health'] > avaible_samples[best_id]['health']:
            best_id = sample_id
    return best_id

def enough_molecues(robot,avaible_molecues, dic):
    print("a",avaible_molecues,file=sys.stderr)
    for key, value in avaible_molecues.items():
        if robot.storage[key] + value < dic[key]:
            return False
    return True

def all_avaible_samples(robot,avaible_samples,avaible_molecues):
    options = []
    for sample_id, dic in avaible_samples.items():
        if enough_molecues(robot,avaible_molecues, dic['costs']) and dic['carried_by'] != 1:
            options.append(sample_id)
        
    return options    

def check_costs(costs, mol):
    for key, value in costs.items():
        if value > mol[key]:
            return False
    return True
    
def expensive_samples(robot,avaible_samples,avaible_molecues):
    for sample_id in robot.data_list:
        if check_costs(avaible_samples[sample_id]['costs'],avaible_molecues):
            continue
        else:
            return sample_id
    return -1
            
def select_best_sample(robot,avaible_ids,avaible_samples):
    max_health=-1
    max_key=-1
    for sample_id in avaible_ids:
        dic = avaible_samples[sample_id]
        if int(dic['health']) > int(max_health) and dic['carried_by'] == -1 and sample_id not in robot.data_list:
            print(sample_id,"dic",dic,file=sys.stderr)
            max_health=int(dic['health'])
            max_key=sample_id
            
    print("MAX",max_key,file=sys.stderr)
    return max_key
    
def select_avaible_sample(avaible_samples,robot,avaible_molecues):
    avaible = []
    for key, dic in avaible_samples.items():
        if dic['health'] > 0: #zbadana
            if dic['carried_by'] == -1:
                if check_costs(dic['costs'],avaible_molecues):
                    avaible.append(key)
    return avaible
    
def used_molecues(avaible_samples,robot,molecue):
    molecues_sum = 0
    for i in robot.completed_data: #petla po spelnionych molekuach
        molecues_sum += avaible_samples[i]['costs'][molecue]
    return robot.storage[molecue] - molecues_sum #roznica tego co ma od wykorzystanych
    
def enough_molecoues(avaible_samples,robot,avaible_molecues):
    if sum(robot.storage.values()) < 10:
        for i in range(len(robot.data_list)): #uwzgledniam po kolei dla trzech elementow
            print(i,robot.data_list,file=sys.stderr)
            sample_id = robot.data_list[i]
            needed_dictionary = avaible_samples[sample_id]['costs'] #slownik rzeczy potrzebnych do danej probki
            need = [key for key, value in needed_dictionary.items() if value > 0] #molekuy ktory sa niezerowe (potrzebne)

            for i in need:
                #potrzebuje obliczyc ile molekul do wczesniejszych elementow mam juz w plecaku
                if(used_molecues(avaible_samples,robot,i) < needed_dictionary[i]):
                    if avaible_molecues[i] > 0:
                        return i
                    else:
                        return False
            print("powinieneinm dodac", sample_id,file=sys.stderr)
                    
            if sample_id not in robot.completed_data:
                print("dodaje", sample_id, file=sys.stderr)
                robot.completed_data.append(sample_id)                 
    return True    
    
project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]
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
        
        avaible_samples[sample_id] = sample

    robot._str_()
    print("sample", avaible_samples, file=sys.stderr)
    
    
    if robot.target == "START_POS":
        print("GOTO SAMPLES")
    
    elif robot.target == "SAMPLES":
        if len(robot.data_list)+len(robot.completed_data) < 3:
            print("CONNECT ",robot.array_of_levels[robot.data_level+len(robot.data_list)])
        else:
            eta_move = 2
            print("GOTO DIAGNOSIS")
            if robot.data_level <= 4:    
                robot.data_level +=1
        
    elif robot.target == "DIAGNOSIS": 
        if eta_move > 0:
            print("WAIT")
            eta_move-=1
            
        elif len(robot.undiagnozed) > 0:
            examine_sample = robot.undiagnozed.pop(0)
            print("CONNECT "+str(examine_sample))
        #wyrzuc niepotrzebne        
        else:
            avaible = all_avaible_samples(robot,avaible_samples,avaible_molecues)
            flag = 0
            for sample_id in robot.data_list:
                if sample_id not in avaible:
                    print("CONNECT ", sample_id)
                    flag = 1
                    break
                
            if flag == 0:
                if len(avaible) == 0:
                    print("GOTO SAMPLES")
                
                else:
                    current_id = best_sample_id(avaible,avaible_samples)
                    
                    if len(robot.data_list) > 1:
                        for sample_id in robot.data_list:
                            if sample_id != current_id:
                                print("CONNECT ", sample_id)
                                break
                            
                    elif current_id not in robot.data_list:                        
                        print("CONNECT ", current_id)
                        
                    else:
                        print("GOTO MOLECULES")                                
        
    elif robot.target == "MOLECULES":
        mol = enough_molecoues(avaible_samples,robot,avaible_molecues)
        #robot.clear()
        print("mol: ",mol,file=sys.stderr)
        if mol == True:
            print("ide do laba",file=sys.stderr)
            czekaj=2
            print("GOTO LABORATORY")
        elif mol == False:
            print("GOTO SAMPLES")
        else:
            print("CONNECT " + mol)
    
    elif robot.target == "LABORATORY":
        if czekaj>0:
            czekaj-=1
            print("WAIT")
            
        elif len(robot.completed_data) > 0:
            print("CONNECT ",robot.completed_data.pop(0))
            
        elif len(all_avaible_samples(robot,avaible_samples,avaible_molecues)) > 0:
            print("GOTO DIAGNOSIS")
            
        else:
            print("GOTO SAMPLES")
    else:
        print("SOMETHING IS WRONG BITCH")
        
