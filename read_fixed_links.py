def flf_read(filename):
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


class FixedLinkMachine():

    def parse(self,filename):
        for d in flf_read(filename):
            self.write_link(d)

    def write_link(self,d):
        pass
