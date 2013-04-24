def read_flf(filename):
    return list(read_flf_generator(filename))

def read_flf_generator(filename):
    with open(filename,'r') as f:
        for l in f:
            l = l.split()
            if l[0] != "END":
                d = {}
                d["mode"] = l[2]
                d["origin"] = l[4]
                d["destination"] = l[6]
                d["duration"] = int(l[8])
                yield d
