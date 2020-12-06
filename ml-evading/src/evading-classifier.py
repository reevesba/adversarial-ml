from os import listdir
from os.path import isfile, join

benigns = [join("dat/benign", f) for f in listdir("dat/benign") if isfile(join("dat/benign", f))]

def get_bytes(file):
    with open(file, "rb") as fd:
        data = fd.read()
        return bytearray(data)

def record_file(bytez, name):
    f = open(name + ".exe", "wb")
    f.write(bytez)
    f.close()

jigsaw = get_bytes("src/in/jigsaw")

for benign in benigns:
    file_so_far = jigsaw.copy()
    file_name = benign.split("/")[2].split(".")[0]
    append_file = get_bytes(benign)
    while len(file_so_far) < 50000000:
        file_so_far += append_file
    record_file(file_so_far, "src/in/jigsaw_and_" + file_name)


