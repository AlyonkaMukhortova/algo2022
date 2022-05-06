import os
import sys

import hash as hs
from multiprocessing import Pool

"""
def proc(i, A, B, C, D, hash, num):
    #return
    num = (1 << 32) // num
    #print(num)
    #print("process", i)
    t = i - 1
    for k in range(0, num):
        t += k
        #if i == 2:
            #print(t)
        for j in range(0, 1 << num):
            #print(hash)
            first = bin(j)[2:].rjust(32, "0")
            second = bin(t)[2:].rjust(32, "0")
            if j == 10 and t == 5:
                print("here")
                str1 = str = first + second
                str = hs.adding_f(str)
                k1 = hs.func(str, A, B, C, D, hash, str1)
                if i == 9 and j == 10:
                    print("stop")
                    os.kill(os.getpid(), signal.SIGINT)
                    sys.exit()
                    os._exit(0)
                    quit()
                    return True
                if k1 is True:
                    print("found: ", str1)
                    return True
    print("process", i, "found nothing")"""

def fun(v):
    pa, pb, pc, pd, i, hash = v
    t = 0
    while t < (1 << 32):
        first = bin(t)[2:].rjust(32, "0")
        second = bin(i)[2:].rjust(32, "0")
        str1 = str = first + second
        str = hs.adding_f(str)
        #print(str)
        X = hs.init_m(str)
        aa, bb, cc, dd = hs.md4_half_hash(hs.A, hs.B, hs.C, hs.D, X, hs.M, hs.N)
        #if t == 10 and i == 5:
            #print(aa, bb, cc, dd)
        if aa == pa and bb == pb and cc == pc and dd == pd:
            if hex(int(hs.md4_hash(str, hs.A, hs.B, hs.C, hs.D), 2)) == hex(hash):

                print('found password', first + second)

                return True
        t += 1


def main():
    if (len(sys.argv) > 1):
        hash = sys.argv[1]
        hash = (int(hash, 16))
    else:
        print("usage\npython manage.py hash")
        return None
    print("given hash:", hex(hash))
    num = os.cpu_count() - 1
    """t = 0
    A = hs.A
    B = hs.B
    C = hs.C
    D = hs.D
    i = 5
    j = 10
    first = bin(j)[2:].rjust(32, "0")
    second = bin(i)[2:].rjust(32, "0")
    str1 = str = first + second
    #print(str1)
    str = hs.adding_f(str)
    hash1 = hs.md4_hash(str, A, B, C, D)"""
    #print("h", hex(int(hash1, 2)))
    #print("hash1", hash1[:32], hash1[32:64], hash1[64:96], hash1[96:])

    #p = []
    
    #hash = 0xf96c1cd690fbcec05199108064dfc759
    """
    for i in range(1, num):
        print(i)
        p.append(Process(target=proc, args=(i, A, B, C, D, hash, num)))
        p[i-1].start()

    for i in range(1, num):

        p[i-1].join()"""
    i = 0
    end_flag = False
    args = [None] * num
    while i < (1 << 32) and not end_flag:
        """t = 0
        first = bin(t)[2:].rjust(32, "0")
        second = bin(i)[2:].rjust(32, "0")
        str1 = str = first + second
        str = hs.adding_f(str)
        #print(str)
        X = hs.init_m(str)
        print(X)"""
        #args = [None] * num
        
        with Pool(processes=num ) as pool:
            for j in range(num):
                t = 0
                first = bin(t)[2:].rjust(32, "0")
                second = bin(j)[2:].rjust(32, "0")
                str1 = str = first + second
                str = hs.adding_f(str)
                #print(str)
                X = hs.init_m(str)
                #print(X)
                pa, pb, pc, pd = hs.reverse_steps(hash, X, hs.N, hs.A, hs.B, hs.C, hs.D)
                
                #print(pa, pb, pc, pd)
                #args[j] = (i, prev_hash, image_hash)
                
                args[j] = pa, pb, pc, pd, j, hash
                #print(type(args[j]), args[j])
            
            for r in pool.imap_unordered(fun, args):
                if r:
                    pool.terminate()
                    end_flag = True
                    break
        i += 1
    if not end_flag:
        print('Nothing found')


if __name__ == '__main__':
    main()
