import sys
import time
from multiprocessing import Process


def increase(a, b):
    return a <= b


def decrease(a, b):
    return a >= b


def partition(array, func, first, last):
    ptr = first
    
    for i in range(first+1, last+1):
        
        if func(array[i], array[first]):
            ptr += 1
            array[i], array[ptr] = array[ptr], array[i]
    array[ptr], array[first] = array[first], array[ptr]
    
    return ptr


def quick_sort(array, func, first=0, last=None):
    
    if last is None:
        last = len(array) - 1
    
    if first < last:
        ptr = partition(array, func, first, last)
        quick_sort(array, func, first, ptr-1)
        quick_sort(array, func, ptr+1, last)


def merge_sort(array, func, first=0, last=None):
    
    if last is None:
        last = len(array)
    
    if first < last:
        middle = (first + last)//2
        merge_sort(array, func, first, middle)
        merge_sort(array, func, middle + 1, last)
        merge(array, func, first, last, middle)


def merge(array, func, first, last, middle):
    larr = array[first:middle + 1]
    rarr = array[middle+1:last+1]
    larr_ind, rarr_ind = 0, 0
    sorted_index = first
    
    while larr_ind < len(larr) or rarr_ind < len(rarr):

        if larr_ind < len(larr) and rarr_ind < len(rarr):
        
            if func(larr[larr_ind], rarr[rarr_ind]):
                array[sorted_index] = larr[larr_ind]
                larr_ind+=1
            else:
                array[sorted_index] = rarr[rarr_ind]
                rarr_ind+=1
            sorted_index+=1
    
        elif larr_ind < len(larr):
            array[sorted_index] = larr[larr_ind]
            larr_ind+=1
            sorted_index+=1

        elif rarr_ind < len(rarr):
            array[sorted_index] = rarr[rarr_ind]
            rarr_ind+=1
            sorted_index+=1


def to_file(list_num, dict_hash, type_sort='unknownsort', updown=''):
    new_file=open("result_" + type_sort + "_" + updown + ".txt",mode="w",encoding="utf-8")
    
    for obj in list_num:
        o = dict_hash[obj]
        new_file.write(o.rstrip("\n") +'\n')

    new_file.close()


def printing(end, start, list_numi, list_numd, dict_hash, child):    
    if child:
        print("Time for quick sort: " + str(round(((end - start)*1000), 5)) + " ms")
        to_file(list_numi, dict_hash, 'quick', 'increase')
        to_file(list_numd, dict_hash, 'quick', 'decrease')
    else:
        print("Time for merge sort: " + str(round(((end - start)*1000), 5)) + " ms")
        to_file(list_numi, dict_hash, 'merge', 'increase')
        to_file(list_numd, dict_hash, 'merge', 'decrease')


def sorting(child, list_numd, list_numi, dict_hash):
    start = time.time()
    
    if child:
        quick_sort(list_numd, decrease)
        quick_sort(list_numi, increase)
    else:
        merge_sort(list_numd, decrease)
        merge_sort(list_numi, increase)
        pass
    
    end = time.time()
    printing(end, start, list_numi, list_numd, dict_hash, child)


def from_file():
    
    if (len(sys.argv) > 1):
        file_name = sys.argv[1]
    else:
        file_name = "input.txt"
    
    file_hashes = open(file_name, "r")
    n = file_hashes.readline()
    list_numd = []
    dict_hash = {}
    
    while n != '':
        
        if len(n) > 5:
            l = int(n[:4], 16)
            
            if not l in dict_hash:
                list_numd.append(l)
                dict_hash[l] = n
            else:
                dict_hash[l] = dict_hash[l] + '\n' + n
        
        n = file_hashes.readline(). rstrip("\n")

    file_hashes.close()
    list_numi = list_numd[0:len(list_numd)]
    
    return list_numi, list_numd, dict_hash


def main():
    list_numi, list_numd, dict_hash = from_file()
    
    p1 = Process(target=sorting, args=(0, list_numd, list_numi, dict_hash))
    p2 = Process(target=sorting, args=(1, list_numd, list_numi, dict_hash))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':
    main()