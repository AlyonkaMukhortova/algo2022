import hashlib
from os import walk
import find as fs


def to_short_file(dict_adr):
    with open('short.bin', "wb") as file:
        for adr in range (0, 2 ** 11):
            offset = adr
            zippy = 0
            if (adr in dict_adr):
                for s in dict_adr[adr]:
                    for n in range (0, 8):
                        num = 2 ** n
                        if (s // num) % 2 != 0:
                            zippy += num
                zippy = [zippy]
                file.seek(offset)
                file.write(bytes(zippy))

            else:
                file.seek(offset)
                file.write(bytes(zippy))


def patterns_from_file(hashes, dict_hashes, dict_adr, file_name, dict_patterns):
    with open(file_name, "r") as file:
        for line in file:
            line = str(line).rstrip('\r\n')
            o = hashlib.sha1(bytes(str(line), encoding='utf-8')).hexdigest()
            hashes.append(o)
            p = bin(int(o, 16))[2:37]
            adr = p[0:11]
            tail = p[11:35]
            zippy = 0
            if not o in dict_patterns:
                dict_patterns[o] = []
            dict_patterns[o].append(line)
            if not adr in dict_hashes:
                dict_hashes[adr] = []
            dict_hashes[adr].append(o)
            b = bytes(int(adr, 2))
            for i in range(0, len(tail) - 1, 3):
                num = int(tail[i:i+3], 2)
                num = 2 ** num
                if (zippy // num) % 2 == 0:
                    zippy += num
            if not int(adr, 2) in dict_adr:
                dict_adr[int(adr, 2)] = []
            dict_adr[int(adr, 2)].append(zippy)
    return 


def main():
    file_name = './tests/patterns1.txt'
    hashes = []
    dict_hashes = {}
    dict_adr = {}
    text = []
    dict_patterns = {}
    patterns_from_file(hashes, dict_hashes, dict_adr, file_name, dict_patterns)
    to_short_file(dict_adr)
    with open('./tests/text1.txt', "r", encoding='utf-8') as file:
        
        text = file.read()
    with open('short.bin', "rb") as file:
        print("I'm working. Wait, please.\n")
        hashes, strs, adrs, zps, indexes = fs.find(0, len(text), len(dict_patterns[hashes[0]][0]), text, file)
        
        count = 0

        for i in range(0, len(adrs)):
            for zp in dict_adr[adrs[i]]:
                if zp == zps[i]:
                    adr = bin(int(adrs[i]))[2:13]
                    for hash in dict_hashes[adr]:
                        if hash == hashes[i]:
                            for string in dict_patterns[hash]:
                                if string == strs[i]:
                                    count+= 1
                                    print('Found pattern:\n', string)
                                    print('Offset in str symbols:\n', indexes[i])
        
        print('Number of found pattens:', count)

    print("\nThat's all. Thank you for waiting!\n")


if __name__ == '__main__':
    main()   