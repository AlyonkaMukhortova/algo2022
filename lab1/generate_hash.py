import hashlib


new_file=open("input.txt",mode="w",encoding="utf-8")


for num in range(0, 1000):
    o = hashlib.sha256(bytes(str(num), encoding='utf-8')).hexdigest()
    new_file.write(o+'\n')

new_file.close()