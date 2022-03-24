import random
import math
#import numpy


def check_all(n, j):
    l = []
    for i in range(0, n):
        l.append(i)
    for num in l:
        if not num in j:
            return False

    return True


def modular_exponentiation(a, b, n):
    c = 0
    d = 1
    bin_b = bin(b)
    for i in range(len(bin_b) - 1, -1, -1):
        c = c * 2
        d = (d**2) #% n
        if bin_b[i] == 1:
            c+=1
            d =  (d * a) #% n
        print(d)
    print(d)
    return d


def polland_rho(n):
    i = 1
    j = []
    res = []
    x = random.randint(0, n - 1)
    y = x
    k = 2
    #la = check_all(n)
    #print(la)
    while not check_all(n, j):
        i += 1
        if x%n not in j:
            j.append(x%n)
        x = (x**2 - 1) % n
        d = math.gcd(y - x, n)
        if d != 1 and d != n:
            if not d in res:
                res.append(d)
            #else:
             #   break
            print(j, d, res)
        if i == k:
            y = x
            k = 2 * k
    return 0


#polland_rho(17 * 19)
def main():
    a = modular_exponentiation(6, 3, 4)
    print(a)
    print(15)


main()