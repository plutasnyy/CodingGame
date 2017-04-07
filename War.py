import sys
import math
kolejka1=[]
kolejka2=[]
kolejka_rundy1=[]
kolejka_rundy2=[]
wartosci=["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
licznik=0
flaga=[]
def odloz(kolejka,karta1,karta2):
    while len(karta1)!=0:
        kolejka.append(karta1.pop(0))
    while len(karta2)!=0:
        kolejka.append(karta2.pop(0))

def wartosc(karta):
    karta=str(karta[:len(karta)-1])
    for i in range(13):
        if wartosci[i]==karta:
            return i+1
    return 0

n = int(input())  # the number of cards for player 1
for i in range(n):
    cardp_1 = input()  # the n cards of player 1
    kolejka1.append(cardp_1)
m = int(input())  # the number of cards for player 2
for i in range(m):
    cardp_2 = input()  # the m cards of player 2
    kolejka2.append(cardp_2)

def sprawdz_wynik(kolejka_rundy1,kolejka_rundy2,kolejka1,kolejka2):
    if wartosc(kolejka_rundy1[-1])>wartosc(kolejka_rundy2[-1]):
        odloz(kolejka1,kolejka_rundy1,kolejka_rundy2)
    elif wartosc(kolejka_rundy1[-1])<wartosc(kolejka_rundy2[-1]):
        odloz(kolejka2,kolejka_rundy1,kolejka_rundy2)
    else:
        count=0
        while len(kolejka1)>0 and len(kolejka2)>0 and count<=3:
            kolejka_rundy1.append(kolejka1.pop(0))
            kolejka_rundy2.append(kolejka2.pop(0))
            count+=1

        if count<=3:
            flaga.append(1)
        else:
            sprawdz_wynik(kolejka_rundy1,kolejka_rundy2,kolejka1,kolejka2)

while len(kolejka1)>0 and len(kolejka2)>0:
    licznik+=1
    kolejka_rundy1.clear()
    kolejka_rundy2.clear()
    print(kolejka1,kolejka2,file=sys.stderr)
    kolejka_rundy1.append(kolejka1.pop(0))
    kolejka_rundy2.append(kolejka2.pop(0))

    sprawdz_wynik(kolejka_rundy1,kolejka_rundy2,kolejka1,kolejka2)
    print(flaga,file=sys.stderr)
    if len(flaga)>0:
        break


if len(flaga)>0:
    print("PAT")
elif len(kolejka1)==0:
    print(2,licznik)
else:
    print(1,licznik)
