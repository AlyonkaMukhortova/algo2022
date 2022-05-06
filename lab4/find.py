import hashlib


def compare(adr, zippy, file):
    file.seek(adr)
    p = file.read(1)
    p = int.from_bytes(p, "little")

    for n in range(0, 8):
        num = 2 ** n

        if (zippy // num) % 2 == 1 and (p // num) % 2 == 0:
            return False

    return True


def find(first, text_len, pattern_len, text, file, processes):
    hashes, strs, adrs, zps, indexes = [], [], [], [], []

    for ind in range(first, text_len - pattern_len + 1, processes):
        string = text[ind:ind + pattern_len]
        str_hash = hashlib.sha1(bytes(string, encoding='utf-8')).hexdigest()
        p = bin(int(str_hash, 16))[2:37]
        adr = int(p[0:11], 2)
        tail = p[11:35]
        zippy = 0

        for i in range(0, len(tail) - 1, 3):
            num = int(tail[i:i+3], 2)
            num = 2 ** num

            if (zippy // num) % 2 == 0:
                zippy += num

        flag = compare(adr, zippy, file)

        if flag:
            hashes.append(str_hash)
            strs.append(string)
            adrs.append(adr)
            zps.append(zippy)
            indexes.append(ind)

    return hashes, strs, adrs, zps, indexes
