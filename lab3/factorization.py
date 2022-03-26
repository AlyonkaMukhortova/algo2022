import random
import math
import argparse
import sys


def check_all(n, j):
    l = []
    for i in range(0, n):
        l.append(i)
    for num in l:
        if not num in j:
            return False

    return True


def witness(a, n):
    if n == 2:
        return False
    if not n % 2:
        return True
    bin_n = bin(n - 1)[2:]
    t = 0
    x = []
    for i in range(len(bin_n) - 1, -1, -1):
        if bin_n[i] == '1':
            t = len(bin_n) - 1 - i
            break
    u = (n - 1) // (2**t)
    x.append(modular_exponentiation(a, u, n))
    for i in range(1, t + 1):
        x.append((x[i-1] ** 2) % n)
        if x[i] == 1 and x[i-1] != 1 and x[i-1] != n - 1:
            return True
    if x[t] != 1:
        return True
    return False


def modular_exponentiation(a, b, n):
    c = 0
    d = 1
    bin_b = bin(b)
    for i in range(len(bin_b) - 1, 0, -1):
        c = c * 2
        d = (d**2) % n
        if bin_b[i] == '1':
            c+=1
            d =  (d * a) % n
    return d


def polland_rho(n):
    i = 1
    j = []
    res = []
    x = random.randint(0, n + 1)
    y = x
    k = 2
    while True:
        i += 1
        if x%n not in j:
            j.append(x%n)
        else:
            break
        x = (x**2 - 1) % n
        d = math.gcd(y - x, n)
        if d != 1 and d != n:
            if not d in res:
                res.append(d)
        if i == k:
            y = x
            k = 2 * k
    print(res)
    return res


def miller_rabin(n, s):
    for i in range(0, s):
        a = random.randint(0, n)
        if witness(a, n):
            return True
        else:
            return False


def factor(n):
    nums = polland_rho(n)
    res = []
    for num in nums:
        i = miller_rabin(num, n//2)
        if i == False: res.append(num) 
    print(res)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--dec', type=int,
                        help='a decimal integer')
    parser.add_argument('-e', '--hex', type=str,
                        help='a hexadecimal integer')
    args = vars(parser.parse_args())
    num = 17 * 19 * 23 * 101 * 137
    if(args['hex']):
        num = int(args['hex'], 16)
        factor(num)
    elif(args['dec']):
        num = args['dec']
        factor(num)
    else:
        factor(num)

    

if __name__ == '__main__':
    main()