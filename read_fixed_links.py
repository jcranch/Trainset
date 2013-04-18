def read_flf(filename):
    return list(read_flf_generator(filename))

def read_flf_generator(filename):
    with open(filename,'r') as f:
        for l in f:
            l = l.split()
            if l[0] != "END":
                d = {}
                d["Mode"] = l[2]
                d["Origin"] = l[4]
                d["Destination"] = l[6]
                d["Duration"] = int(l[8])
                yield d
            
if __name__ == "__main__":
    print read_flf("../traindata/trains-043/TTISF043.FLF")
