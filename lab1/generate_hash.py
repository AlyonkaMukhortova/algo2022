import hashlib
import sys

def main_gen(n):
    new_file=open("input.txt",mode="w",encoding="utf-8")


    for num in range(0, n):
        o = hashlib.sha1(bytes(str(num), encoding='utf-8')).hexdigest()
        new_file.write(o+'\n')

    new_file.close()


def sorted_gen(n=1000, type='increase'):
    new_file=open("input_sorted.txt",mode="w",encoding="utf-8")

    if type == 'increase':
        k = n
    else:
        k = 0
    for num in range(0, n):
        if k == 0:
            num = hex(n - num)
        else:
            num = hex(n + num)
        o = str(num).ljust(40, '0')
        new_file.write(o+'\n')

    new_file.close()
    return


def main():
    n, type = 1000, 'increase'
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    if len(sys.argv) > 2:
        type = sys.argv[2]

    main_gen(n)
    sorted_gen(n , type)


main()