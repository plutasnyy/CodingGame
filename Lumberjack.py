drzewa = []
R = []
tupla = {}


def odleglosc(a, b, x, y):
    return abs(int(a)-int(x))+abs(int(b)-int(y))


def maks_wartosc(lista):
    wartosc = 0
    for i in lista:
        wartosc += i[2]*i[3]*i[5]
    return wartosc


def znajdz(i, trees):
    x = i[0]
    y = i[1]
    wysokosc = trees[x, y]['height']
    pom = trees[x, y]['weight']*trees[x, y]['height']
    ciezar = trees[x, y]['thickness'] * pom
    for j in drzewa:
        if j in R:
            continue
        elif j[0]-x <= wysokosc and i[1] == j[1]:
            if ciezar >= j[2]*j[3]*j[4] and x < j[0]:
                R.append(j)
                znajdz(j, trees)


def wyznacz_wartosci_drzew(trees):
    for i in drzewa:
        R.clear()
        znajdz(i, trees)
        tupla[i[0], i[1]] = {'kierunek': "cut right"}
        for j in R:
            drzewa.remove(j)


def solve(t,  n,  trees):
    wyznacz_wartosci_drzew(trees)
    x,  y = 0,  0
    time = 0
    while True:
        max_wsp = 0
        for i in drzewa:
            pom = trees[i[0], i[1]]['value']*trees[i[0], i[1]]['height']
            wsp = pom
            wsp *= trees[i[0], i[1]]['thickness']/odleglosc(x, y, i[0], i[1])
            if wsp > max_wsp:
                max_wsp = wsp
                drzewo = i
        x1 = drzewo[0]
        y1 = drzewo[1]
        drzewa.remove(drzewo)

        while x != x1 or y != y1:
            if time + 1 <= t:
                time += 1
            else:
                break
            if x1 > x:
                print("move right")
                x += 1
            elif x1 < x:
                print("move left")
                x -= 1
            elif y1 > y:
                print("move up")
                y += 1
            elif y1 < y:
                print("move down")
                y -= 1
        if time == t:
            break
        if time+trees[x, y]['thickness'] <= t:
            print(tupla[x, y]['kierunek'])
            time += trees[x, y]['thickness']


def read_data():
    t, n, k = (int(x) for x in input().split())
    trees = {}
    for i in range(k):
        x, y, h, d, c, p = (int(x) for x in input().split())
        drzewa.append([x, y, h, d, c, p, 0])
        trees[x, y] = {'height': h, 'thickness': d, 'weight': c, 'value': p}
    return t, n, trees


def main():
    solve(*read_data())


if __name__ == "__main__":
    main()
