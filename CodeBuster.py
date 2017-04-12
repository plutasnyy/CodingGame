import sys
import string
from math import sqrt
busters_per_player = int(input())  # liczba strzelcow
ghost_count = int(input())  # liczba duszkow
my_team_id = int(input())  # 0, your base is on the top left of the map, if it is one, on the bottom right
Duchy=[]
Team=[]
Wrogowie=[]
mapa=[[3500,4000],[10000,5000],[2000,7000],[13000,1000],[8000,8000],[1000,8000],[4000,1000]]
baza=[]
strzaly=[]
wid_cele=[]

if my_team_id==0:#ustawiam wartosci bazy, pozniej potrzebne przy znajdowaniu miejsca do wypuszczenia ducha
    baza=[1000,1000]
else:
    baza=[15000,8000] # nie sa dokladne narozniki bo nie ide do naroznika tylko do bazy

for i in range(0,16000,500):
    for j in range (9000,0,-1000):
        if i<2500 and j<2500 or i>10000 and j>5000:
            continue
        else:
            mapa.append([i,j])

def zbadaj_polozenie(punkt):
    blad=100
    for i in range(len(mapa)):
        if abs(mapa[i][0]-punkt[0])+abs(mapa[i][1]-punkt[1])<=blad :
            mapa.remove(mapa[i])
            break

def szukaj(k):
    if len(mapa)>0+k:
        i=mapa[0+k]
        print("MOVE",str(i[0]),str(i[1]),"MOVE",i[0],i[1])

def jest_w_zasiegu(a,b,x,y,min_z,max_z):
    odleglosc=sqrt((a-x)**2+(b-y)**2)
    if odleglosc<=max_z and odleglosc>=min_z:
        return True
    return False

def zaatakuj(napastnik,wid_cele):#za przeciwnikiem nie gonie, ale jesli jest w zasiegu to uderzam
    for i in wid_cele:
        min_z=760 if i[5]==-1 else 0
        if jest_w_zasiegu(napastnik[1],napastnik[2],i[1],i[2],min_z,1760)==True:
            if i[5]==-1:
                print("BUST ",str(i[0]),"BUST",i[0])

            elif strzaly[napastnik[0]][1]==0:
                print("STUN",str(i[0]),"STUN",i[0])

        else:
            x=i[1]-1200
            y=i[2]
            print("MOVE",str(x),str(y),"MOVE",x,y)

def widoczne_cele(x,y,wid_cele):
    for i in Wrogowie:
        if jest_w_zasiegu(x,y,i[1],i[2],0,2200):
            wid_cele.append(i)
    for i in Duchy:
        if jest_w_zasiegu(x,y,i[1],i[2],0,2200):
            wid_cele.append(i)
    return True if len(wid_cele)>=1 else False

while True:
    Duchy.clear()
    Team.clear()
    Wrogowie.clear()

    entities = int(input())  # the number of busters and ghosts visible to you

    for i in range(entities):
        entity_id, x, y, entity_type, state, value = [int(j) for j in input().split()]
        if entity_type==my_team_id:
            Team.append([entity_id, x, y, state, value])
            strzaly.append([entity_id,0])

        elif entity_type==-1:
            Duchy.append([entity_id, x, y, state, value,entity_type])
        else:
            Wrogowie.append([entity_id, x, y, state, value,entity_type])
        # entity_id: buster id or ghost id # y: position of this buster / ghost # entity_type: the team id if it is a buster, -1 if it is a ghost. # state: For busters: 0=idle, 1=carrying a ghost. # value: For busters: Ghost id being carried. For ghosts: number of busters attempting to trap this ghost.

    for i in range(busters_per_player):
        if strzaly[Team[i][0]][1]>=0:
                strzaly[Team[i][0]][1]-=1
        wid_cele.clear()
        zbadaj_polozenie([Team[i][1],Team[i][2]])

        if Team[i][3]==1:#Duch zlapany
            if [Team[i][1],Team[i][2]]==baza:
                print("RELEASE RELASE")
            else:
                if my_team_id==0:
                    print("MOVE 1000 1000 MOVE 1000 1000")
                else:
                    print("MOVE 15000 8000 MOVE 15000 8000")

        elif widoczne_cele(Team[i][1],Team[i][2],wid_cele):
            zaatakuj(Team[i],wid_cele)

        else:
            szukaj(i)
        print(mapa,file=sys.stderr)
        # To debug: print("Debug messages...", file=sys.stderr)
        # MOVE x y | BUST id | RELEASE
