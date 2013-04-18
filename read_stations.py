


def read_msn(filename):
    with open(filename,'r') as f:
        station_details = {}
        station_aliases = {}
        routeing_groups = {}
        for l in f:
            if l[0] == "A" and "FILE-SPEC=" not in l:
                # Station details
                name = l[5:35].strip()
                d = {}
                d["CATE Type"] = l[35]
                d["TIPLOC Code"] = l[36:43].strip()
                d["3-Alpha Code"] = l[49:52]
                if l[43:46] != d["3-Alpha Code"]:
                    d["Subsidiary 3-Alpha Code"] = l[43:46]
                d["Easting"] = int(l[52:57])
                d["Estimated"] = l[57] == "E"
                d["Northing"] = int(l[58:63])
                d["Change Time"] = int(l[63:65].strip())
                assert(name not in station_details) # should be replaced by proper handling
                station_details[name] = d
            elif l[0] == "L":
                # Station aliases
                name = l[5:35].strip()
                aliases = l[36:66].strip()
                assert(name not in station_aliases) # should be replaced by proper handling
                station_aliases[name] = aliases
            elif l[0] == "V":
                # Routeing groups
                name = l[5:35].strip()
                stations = l[36:].split()
                assert(name not in routeing_groups) # should be replaced by proper handling
                routeing_groups[name] = stations
        info = {"Station Details": station_details,
                "Station Aliases": station_aliases,
                "Routeing Groups": routeing_groups}
        return info
        


if __name__=="__main__":
    print read_msn("../traindata/trains-043/TTISF043.MSN")
