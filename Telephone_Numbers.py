import sys

null=-1
root_list=[]

class root(object):
    def __init__(self,value):
        self.value=value
        self.child_list=[]

    def add_child(self,child):
        self.child_list.append(child)

    def print_tree(self):
        print(self.value,file=sys.stderr)
        if len(self.child_list)>0:
            for i in self.child_list:
                i.print_tree()
    def return_size(self):
        suma=0
        for i in self.child_list:
            suma+=i.return_size()
        return suma+len(self.child_list)

def create_tree(number):
    value=0
    if len(number)>1:
        value=create_tree(number[1:])
    korzen=root(number[0])
    if value != 0:
        korzen.add_child(value)
    return korzen

def find_child(korzen,number):
    value=number[0]
    for i in korzen.child_list:
        if i.value==value:
            if len(number)==1:
                return 0,0
            korzen,number= find_child(i,number[1:])
            break
    return korzen, number

def add_number(number):
    korzen=0
    for i in root_list:
        if i.value==number[0]:
            korzen=i
            break
    if korzen==0:
        root_list.append(create_tree(number))
    else:
        child,new_number=find_child(korzen,number[1:])
        if(child != 0 and number !=0):
            child.add_child(create_tree(new_number))

def find_size():
    size=0
    for i in root_list:
        size+=i.return_size()
    return size+len(root_list)

n = int(input())
for i in range(n):
    telephone = input()
    add_number(telephone)
    print(telephone," ",file=sys.stderr)

print(find_size())
