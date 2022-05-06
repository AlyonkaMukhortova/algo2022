import os
import sys

import hash as hs
from multiprocessing import Pool


def fun(v):
    pa, pb, pc, pd, i, hash = v
    t = 0
    while t < (1 << 32):
        first = bin(t)[2:].rjust(32, "0")
        second = bin(i)[2:].rjust(32, "0")
        str1 = str = first + second
        str = hs.adding_f(str)
        X = hs.init_m(str)
        aa, bb, cc, dd = hs.md4_half_hash(hs.A, hs.B, hs.C, hs.D, X, hs.M, hs.N)
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
    
    i = 0
    end_flag = False
    args = [None] * num
    while i < (1 << 32) and not end_flag:
        
        with Pool(processes=num ) as pool:
            
            for j in range(num):
                
                t = 0
                first = bin(t)[2:].rjust(32, "0")
                second = bin(j)[2:].rjust(32, "0")
                str1 = str = first + second
                str = hs.adding_f(str)
                X = hs.init_m(str)
                
                pa, pb, pc, pd = hs.reverse_steps(hash, X, hs.N, hs.A, hs.B, hs.C, hs.D)
                
                args[j] = pa, pb, pc, pd, j, hash
            
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
