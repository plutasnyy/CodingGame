import sys
import math
lista=[]
maks=[]
def rek(licznik,ostatni):
    for i in lista:
        if i[0]==ostatni:
            rek(licznik+1,i[1])
    maks.append(licznik+1)

n = int(input())  # the number of relationships of influence
for i in range(n):
    x, y = [int(j) for j in input().split()]
    lista.append([x,y])

for i in lista:
    rek(1,i[1])

print(max(maks))
