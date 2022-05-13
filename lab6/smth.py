import numpy as np
from multiprocessing import Pool
import re
import time
import argparse


matrix = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
matrix2 = np.array([[5, 6, 7], [7, 8, 9], [2, 3, 4]])


#works    
def split_matrix(matrix):
    lenm = len(matrix)
    len_minim = lenm // 2
    left_top = matrix[:len_minim, :len_minim]
    right_top = matrix[:len_minim, len_minim:]
    left_down = matrix[len_minim:, :len_minim]
    right_down = matrix[len_minim:, len_minim:]
    return left_top, right_top, left_down, right_down

#works
def adding_zeroes(matrix):
    lenm1 = lenm = len(matrix)
    if lenm == 1:
        return matrix
    count = 1
    while lenm > 2:
        lenm = lenm >> 1
        count += 1
    if 2 ** count < lenm1:
         count += 1
    newlen = 2 ** count
    lenm = lenm1
    N = newlen
    if lenm == N:
        return matrix
    b = np.zeros((N, N))
    zeroes_line = np.zeros((1, lenm))
    diff = N - lenm
    for i in range(diff):
        matrix = np.append(matrix, zeroes_line, axis = 0)
    b[:,:lenm - newlen] = matrix
    return b


#works
def make_matr_from_blocks(lt, rt, ld, rd):
    matrix = lt
    matrix = np.append(matrix, rt, axis = 1)
    m1 = np.append(ld, rd, axis = 1)
    matrix = np.append(matrix, m1, axis = 0)
    return matrix


#works
def multiplying(matrix_A, matrix_B, matrix=None):
    start = time.time()
    if len(matrix_A) < 2:
        return matrix_A * matrix_B
    
    matrix_A = adding_zeroes(matrix_A)
    matrix_B = adding_zeroes(matrix_B)
    lt_A, rt_A, ld_A, rd_A = split_matrix(matrix_A)
    lt_B, rt_B, ld_B, rd_B = split_matrix(matrix_B)
    
    matrix_D = multiplying(lt_A + rd_A, lt_B + rd_B)
    matrix_D1 = multiplying(rt_A - rd_A, ld_B + rd_B)
    matrix_D2 = multiplying(ld_A - lt_A, lt_B + rt_B)
    matrix_H1 = multiplying(lt_A + rt_A, rd_B)
    matrix_H2 = multiplying(ld_A + rd_A, lt_B)
    matrix_V1 = multiplying(rd_A, ld_B - lt_B)
    matrix_V2 = multiplying(lt_A, rt_B - rd_B)
    
    matrix_AB = make_matr_from_blocks(matrix_D + matrix_D1 + matrix_V1 - matrix_H1,
                                        matrix_V2 + matrix_H1,
                                        matrix_V1 + matrix_H2,
                                        matrix_D + matrix_D2 + matrix_V2 - matrix_H2)
    end = time.time()
    print("Time for multiplying:", round((end - start) * 1000, 5), "ms")
    return matrix_AB


def block_1(lt_A, rd_A, lt_B, rd_B, matrix_D,
            rt_A, ld_B, matrix_D1, ld_A, rt_B, matrix_D2):
    #md, md1, md2 = matrix_D, matrix_D1, matrix_D2
    md = multiplying(lt_A + rd_A, lt_B + rd_B, matrix_D)
    md1 = multiplying(rt_A - rd_A, ld_B + rd_B, matrix_D1)   
    md2 = multiplying(ld_A - lt_A, lt_B + rt_B, matrix_D2)
    matrix_D[0] = md
    matrix_D1[0] = md1
    matrix_D2[0] = md2
    return [matrix_D1], [matrix_D2], [matrix_D]


def block_2(lt_A, rt_A, rd_B, matrix_H1,
            ld_A, rd_A, lt_B, matrix_H2):
    mh1 = multiplying(lt_A + rt_A, rd_B, matrix_H1)
    mh2 = multiplying(ld_A + rd_A, lt_B, matrix_H2)
    matrix_H1[0] = mh1
    matrix_H2[0] = mh2
    return matrix_H1, matrix_H2


def block_3(rd_A, ld_B, lt_B, matrix_V1,
            lt_A, rt_B, rd_B, matrix_V2):
    mv1 = multiplying(rd_A, ld_B - lt_B, matrix_V1)
    mv2 = multiplying(lt_A, rt_B - rd_B, matrix_V2)
    matrix_V1[0] = mv1
    matrix_V2[0] = mv2
    return matrix_V1, matrix_V2


def blocks(v):
    #v = v[0]
    if (v[0] == 0):
        lt_A, rd_A, lt_B, rd_B, matrix_D,\
        rt_A, ld_B, matrix_D1, ld_A, rt_B, matrix_D2 = v[1:]
        block_1(lt_A, rd_A, lt_B, rd_B, matrix_D,\
        rt_A, ld_B, matrix_D1, ld_A, rt_B, matrix_D2)
        return 0, matrix_D, matrix_D1, matrix_D2
    if (v[0] == 1):
        lt_A, rt_A, rd_B, matrix_H1,\
        ld_A, rd_A, lt_B, matrix_H2 = v[1:]
        block_2(lt_A, rt_A, rd_B, matrix_H1,
        ld_A, rd_A, lt_B, matrix_H2)
        return 1, matrix_H1, matrix_H2
    if (v[0] == 2):
        rd_A, ld_B, lt_B, matrix_V1,\
        lt_A, rt_B, rd_B, matrix_V2 = v[1:]
        block_3(rd_A, ld_B, lt_B, matrix_V1,
        lt_A, rt_B, rd_B, matrix_V2)
        return 2, matrix_V1, matrix_V2
    return True


def multiplying_multi(matrix_A, matrix_B, matrix=None):
    start = time.time()
    if len(matrix_A) < 2:
        return matrix_A * matrix_B
    
    matrix_A = adding_zeroes(matrix_A)
    matrix_B = adding_zeroes(matrix_B)
    lt_A, rt_A, ld_A, rd_A = split_matrix(matrix_A)
    lt_B, rt_B, ld_B, rd_B = split_matrix(matrix_B)
    
    matrix_D, matrix_D1, matrix_D2 = [None], [None], [None]
    matrix_H1, matrix_H2 = [None], [None]
    matrix_V1, matrix_V2 = [None], [None]

    myargs = ((0, lt_A, rd_A, lt_B, rd_B, matrix_D,
            rt_A, ld_B, matrix_D1, ld_A, rt_B, matrix_D2),
            (1, lt_A, rt_A, rd_B, matrix_H1,
            ld_A, rd_A, lt_B, matrix_H2),
            (2, rd_A, ld_B, lt_B, matrix_V1,
            lt_A, rt_B, rd_B, matrix_V2))

    pool = Pool(processes=3)
    data = pool.map(blocks, [t for t in myargs])
    pool.close()

    matrix_D, matrix_D1, matrix_D2 = data[0][1:]
    matrix_H1, matrix_H2 = data[1][1:]
    matrix_V1, matrix_V2 = data[2][1:]
    matrix_D, matrix_D1, matrix_D2 = matrix_D[0], matrix_D1[0], matrix_D2[0]
    matrix_H1, matrix_H2 = matrix_H1[0], matrix_H2[0]
    matrix_V1, matrix_V2 = matrix_V1[0], matrix_V2[0]
    
    matrix_AB = make_matr_from_blocks(matrix_D + matrix_D1 + matrix_V1 - matrix_H1,
                                        matrix_V2 + matrix_H1,
                                        matrix_V1 + matrix_H2,
                                        matrix_D + matrix_D2 + matrix_V2 - matrix_H2)
    end = time.time()
    print("Time for multiprocessing multiplying:", round((end - start) * 1000, 5), "ms")
    return matrix_AB


def wrong_file(filename='matrix_file_example.txt'):
    with open(filename, "w") as file:
        file.write("matrix A\nhere's space for your matrix A\n\
attention! Dimensions of 2 matrix should be same!\n\
please, input your square matrix here\nmatrix B\n\
don't change lines with names of matrix\n\
don't change format of file\ninput nums\n")


def get_matrix(filename='./matrix.txt'):
    matrix_A = [[]]
    matrix_B = [[]]
    count = 0
    PTR = 0
    with open(filename, "r") as file:
        for line in file:
            if line == 'matrix B\n' or line == 'matrix A\n':
                count += 1
                ptr = 1
                continue
            l = re.findall(r'\d+', line)
            l = np.array([[int(i) for i in l]])
            try:
                if ptr == 1 and count == 1:
                    matrix_A = l
                elif ptr == 1 and count == 2:
                    matrix_B = l
                elif ptr == 0 and count == 2:
                    matrix_B = np.append(matrix_B, l, axis=0)
                else:
                    matrix_A = np.append(matrix_A, l, axis=0)
            except:
                wrong_file(filename)
            ptr = 0
    if count < 2 or len(matrix_B) != len(matrix_A):
        wrong_file(filename)
    return matrix_A, matrix_B


def main():
    parser = argparse.ArgumentParser(description='Multiplying matrix.')
    parser.add_argument('-u', '--multi', action = 'store_true',
                        help='multiprocessing')
    parser.add_argument('-m', '--mono', action = 'store_true',
                        help='1 process')
    args = vars(parser.parse_args())
    matrix_A, matrix_B = get_matrix()
    l = len(matrix_A)
    if args['multi']:
        newm = multiplying_multi(matrix_A, matrix_B)
    elif args['mono']:
        newm = multiplying(matrix_A, matrix_B)
    else:
        print("Multyplying by 1 process")
        newm = multiplying(matrix_A, matrix_B)
    newm = newm[:l, :l]
    print("res\n", newm)
    #print("nedded res\n", matrix_A.dot(matrix_B))
                
"""
matrix_A, matrix_B = get_matrix()

l = len(matrix_A)
newm = multiplying_multi(matrix_A, matrix_B)
newm = newm[:l, :l]
print("res\n", newm)
print("nedded res\n", matrix_A.dot(matrix_B))
newm = multiplying(matrix_A, matrix_B)
newm = newm[:l, :l]
print("res\n", newm)
print("nedded res\n", matrix_A.dot(matrix_B))"""


if __name__ == '__main__':
    main()