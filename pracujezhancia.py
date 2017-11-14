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
        self.undiagnozed = []
        
    def _str_(self):
        print("ID: ",self.id,file=sys.stderr)
        print("Data list: ",self.data_list,file=sys.stderr)
        print("Storage: ",self.storage,file=sys.stderr)
        print("Completed data :",self.completed_data,file=sys.stderr)
        print("Undiagnozed: ",self.undiagnozed,file=sys.stderr)
        
    def clear(self):
        for i in self.completed_data:
            if i in self.data_list:
                self.data_list.remove(i)
        
robot = Player(0)

used_samples = []
def select_best_sample(avaible_samples):
    max_health=0
    max_key=0
    for key, dic in avaible_samples.items():
        if int(dic['health']) > int(max_health) and key not in used_samples:
            max_health=int(dic['health'])
            max_key=key
    if max_key not in used_samples:
        used_samples.append(max_key)
    print("MAX",max_key,file=sys.stderr)
    return max_key

def used_molecues(avaible_samples,robot,molecue):
    molecues_sum = 0
    for i in robot.completed_data: #petla po spelnionych molekuach
        molecues_sum += avaible_samples[i]['costs'][molecue]
    return robot.storage[molecue] - molecues_sum #roznica tego co ma od wykorzystanych
    
def enough_molecoues(avaible_samples,robot):
    if sum(robot.storage.values()) < 10:
        for i in range(len(robot.data_list)): #uwzgledniam po kolei dla trzech elementow
            print(i,robot.data_list,file=sys.stderr)
            sample_id = robot.data_list[i]
            needed_dictionary = avaible_samples[str(sample_id)]['costs'] #slownik rzeczy potrzebnych do danej probki
            need = [key for key, value in needed_dictionary.items() if value > 0] #molekuy ktory sa niezerowe (potrzebne)

            for i in need:
                #potrzebuje obliczyc ile molekul do wczesniejszych elementow mam juz w plecaku
                if(used_molecues(avaible_samples,robot,i) < needed_dictionary[i]):
                    return i
            if sample_id not in robot.completed_data:
                robot.completed_data.append(sample_id)                 
    return True    
    
project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]

while True:
    print("used samples: ",used_samples, file=sys.stderr)
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
            
        if i==1 and target == "DIAGNOSIS" and robot.target == "DIAGNOSIS":
            print("WAIT")
            
    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
    print("Target: ",robot.target, file=sys.stderr)
    robot._str_()
    if robot.target == "START_POS":
        print("GOTO SAMPLES")
    
    elif robot.target == "SAMPLES":
        if len(robot.undiagnozed) == 3:
            print("GOTO DIAGNOSIS")
        else:
            print("CONNECT " + str(3 - len(robot.undiagnozed)))
        
    elif robot.target == "DIAGNOSIS": 
        if len(robot.data_list) < 3:
            best_sample_id = select_best_sample(avaible_samples)
            print("best",best_sample_id,file=sys.stderr)
            print("CONNECT "+str(best_sample_id))
            print(best_sample_id, file = sys.stderr)
            robot.data_list.append(best_sample_id)
        else:
            print("GOTO MOLECULES")
        
    elif robot.target == "MOLECULES":
        mol = enough_molecoues(avaible_samples,robot)
        robot.clear()
        print("mol: ",mol,file=sys.stderr)
        if mol == True:
            print("ide do laba",file=sys.stderr)
            print("GOTO LABORATORY")
        else:
            print("CONNECT " + mol)

    elif robot.target == "LABORATORY":
        if len(robot.completed_data) > 0:
            robot._str_()
            print("CONNECT ",robot.completed_data.pop(0))
            robot._str_()
        else:
            print("GOTO DIAGNOSIS")
    else:
        print("SOMETHING IS WRONG")
        

    avaible_samples = dict()
    sample_count = int(input())
    for i in range(sample_count):
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
        carried_by = int(carried_by)
        if sample_id not in used_samples and carried_by != -1:
             used_samples.append(sample_id)
        rank = int(rank)
        
        if carried_by == 0 and health == -1:
            robot.undiagnozed = set(robot.undiagnozed.append(sample_id))
            
        cost=dict()
        cost['A']=int(cost_a)
        cost['B']=int(cost_b)
        cost['C']=int(cost_c)
        cost['D']=int(cost_d)
        cost['E']=int(cost_e)
        
        sample=dict()
        sample['health']=int(health)
        sample['costs']=cost
        
        avaible_samples[str(sample_id)] = sample
        
    print("sample", avaible_samples, file=sys.stderr)
