import hashlib
from os import walk
import find as fs
from multiprocessing import Process
import argparse


def to_short_file(dict_adr):
    with open('short.bin', "wb") as file:
        for adr in range(0, 2 ** 11):
            offset = adr
            zippy = 0
            nums = []
            if (adr in dict_adr):
                for s in dict_adr[adr]:
                    for n in range(0, 8):
                        num = 2 ** n

                        if (zippy // num) % 2 == 0 and (s // num) % 2 != 0:
                            zippy += num

                zippy = [zippy]
                file.seek(offset)
                file.write(bytes(zippy))

            else:
                file.seek(offset)
                file.write(bytes(zippy))


def patterns_from_file(hashes, dict_hashes, dict_adr,
                       file_name, dict_patterns):
    with open(file_name, "r") as file:

        for line in file:
            line = str(line).rstrip('\r\n')
            o = hashlib.sha1(bytes(str(line), encoding='utf-8')).hexdigest()
            hashes.append(o)
            p = bin(int(o, 16))[2:37]
            adr = p[0:11]
            tail = p[11:35]
            zippy = 0

            if o not in dict_patterns:
                dict_patterns[o] = []
            dict_patterns[o].append(line)

            if adr not in dict_hashes:
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

    return 0


def proc(first, text_len, pattern_len, text,
         file, dict_adr, dict_hashes, dict_patterns):
    hashes, strs, adrs, zps, indexes = fs.find(first, text_len,
                                               pattern_len, text, file)

    count = 0
    for i in range(0, len(adrs)):
        if adrs[i] in dict_adr:
            for zp in dict_adr[adrs[i]]:
                if zp == zps[i]:
                    adr = bin(int(adrs[i]))[2:13]
                    for hash in dict_hashes[adr]:
                        if hash == hashes[i]:
                            for string in dict_patterns[hash]:
                                if string == strs[i]:
                                    count += 1
                                    print('Found pattern:\n', string)
                                    print('Offset in str symbols:\n', indexes[i])

    print('Number of found pattrens (process', str(first) + '):', count)


def parse_args(text_file, file_name):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', type=str,
                        help='text file')
    parser.add_argument('-p', '--pat', type=str,
                        help='pattern file')
    args = vars(parser.parse_args())

    if(args['text']):
        text_file = args['text']

    if(args['pat']):
        file_name = args['pat']


    return file_name, text_file


def multiprocessing_n_working(text, dict_patterns, dict_adr,
                              hashes, dict_hashes):
    with open('short.bin', "rb") as file:
        p = []

        for j in range(0, 4):
            p.append(0)
            p[j] = Process(target=proc, args=(j, len(text),
                           len(dict_patterns[hashes[0]][0]), text, file,
                           dict_adr, dict_hashes, dict_patterns))

        for j in range(0, 4):
            p[j].start()

        for j in range(0, 4):
            p[j].join()


def main():
    file_name = './tests/patterns1.txt'
    text_file = './tests/text1.txt'
    hashes, dict_hashes, dict_adr, text, dict_patterns = [], {}, {}, [], {}

    file_name, text_file = parse_args(text_file, file_name)
    patterns_from_file(hashes, dict_hashes, dict_adr, file_name, dict_patterns)
    to_short_file(dict_adr)

    with open(text_file, "r", encoding='utf-8') as file:

        text = file.read()

    multiprocessing_n_working(text, dict_patterns,
                              dict_adr, hashes, dict_hashes)


if __name__ == '__main__':
    main()
