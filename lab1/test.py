import sys


def increase(a, b):
    return a <= b


def decrease(a, b):
    return a >= b


def checker(list_num, dict_hash, func):
    i, count = 1, 0
    for obj in list_num[:len(list_num) - 1]:
        if not func(obj, list_num[i]):
            print ("Wrong place of hash " + dict_hash[list_num[i]], "line", i)
            count+=1
        i+=1
    if count == 0:
        print("No mistakes!")
    else:
        print(str(count) + " mistakes")


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
            l = int(n[:16], 16)
            
            if not l in dict_hash:
                list_numd.append(l)
                dict_hash[l] = n
            else:
                dict_hash[l] = dict_hash[l] + '\n' + n
        
        n = file_hashes.readline(). rstrip("\n")

    file_hashes.close()
    
    return list_numd, dict_hash, file_name


def main():
    list_num, dict_hash, file_name = from_file()
    if (file_name.find('decrease') != -1):
        checker(list_num, dict_hash, decrease)
    else:
        checker(list_num, dict_hash, increase)
    return

main()