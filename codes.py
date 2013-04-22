class Misc():

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class CATE():

    types = {'0': "Not an Interchange Point",
             '1': "Small Interchange Point",
             '2': "Medium Interchange Point",
             '3': "Large Interchange Point",
             '9': "Subsidiary TIPLOC" }


class Timetable():

    # bank holiday restrictions
    bhx = {"X" : "Does not run on specified Bank Holiday Mondays",
           "E" : "Does not run on specified Edinburgh Holiday dates", # no longer used
           "G" : "Does not run on specified Glasgow Holiday dates."}

    # status
    status = {"B" : "Bus (Permanent)",
              "F" : "Freight (Permanent - WTT)",
              "P" : "Passenger & Parcels (Permanent - WTT)",
              "S" : "Ship (Permanent)",
              "T" : "Trip (Permanent)",
              "1" : "STP Passenger & Parcels",
              "2" : "STP Freight",
              "3" : "STP Trip",
              "4" : "STP Ship",
              "5" : "STP Bus"}

    category_pre = {"Ordinary Passenger Trains":
                        {"OL": "London Underground/Metro Service",
                         "OU": "Unadvertised Ordinary Passenger",
                         "OO": "Ordinary Passenger",
                         "OS": "Staff Train",
                         "OW": "Mixed"},
                    "Express Passenger Trains":
                        {"XC": "Channel Tunnel",
                         "XD": "Sleeper (Europe Night Services)",
                         "XI": "International",
                         "XR": "Motorail",
                         "XU": "Unadvertised Express",
                         "XX": "Express Passenger",
                         "XZ": "Sleeper (Domestic)"},
                    "Buses":
                        {"BR": "Replacement due to engineering work",
                         "BS": "WTT Service"},
                    "Empty Coaching Stock Trains":
                        {"EE": "Empty Coaching Stock",
                         "EL": "ECS, London Underground/Metro Service",
                         "ES": "ECS & Staff"},
                    "Parcels and Postal Trains":
                        {"JJ": "Postal",
                         "PM": "Post Office Controlled Parcels",
                         "PP": "Parcels",
                         "PV": "Empty NPCCS"},
                    "Departmental Trains":
                        {"DD": "Departmental",
                         "DH": "Civil Engineer",
                         "DI": "Mechanical & Electrical Engineer",
                         "DQ": "Stores",
                         "DT": "Test",
                         "DY": "Signal & Telecommunications Engineer"},
                    "Light Locomotives":
                        {"ZB": "Locomotive & Brake Van",
                         "ZZ": "Light Locomotive"},
                    "Railfreight Distribution":
                        {"J2": "RfD Automotive (Components)",
                         "H2": "RfD Automotive (Vehicles)",
                         "J3": "RfD Edible Products (UK Contracts)",
                         "J4": "RfD Industrial Minerals (UK Contracts)",
                         "J5": "RfD Chemicals (UK Contracts)",
                         "J6": "RfD Building Materials (UK Contracts)",
                         "J8": "RfD General Merchandise (UK Contracts)",
                         "H8": "RfD European",
                         "J9": "RfD Freightliner (Contracts)",
                         "H9": "RfD Freightliner (Other)"},
                    "Trainload Freight":
                        {"A0": "Coal (Distributive)",
                         "E0": "Coal (Electricity) MGR",
                         "B0": "Coal (Other) and Nuclear",
                         "B1": "Metals",
                         "B4": "Aggregates",
                         "B5": "Domestic and Industrial Waste",
                         "B6": "Building Materials (TLF)",
                         "B7": "Petroleum Products"},
                    "Railfreight Distribution (Channel Tunnel)":
                        {"H0": "RfD European Channel Tunnel (Mixed Business)",
                         "H1": "RfD European Channel Tunnel Intermodal",
                         "H3": "RfD European Channel Tunnel Automotive",
                         "H4": "RfD European Channel Tunnel Contract Services",
                         "H5": "RfD European Channel Tunnel Haulmark",
                         "H6": "RfD European Channel Tunnel Joint Venture"}}
    category = dict((k,(a,b)) for (a,d) in category_pre.iteritems() for (k,b) in d.iteritems())

    power_type = {
        "D"   : "Diesel",
        "DEM" : "Diesel Electric Multiple Unit",
        "DMU" : "Diesel Mechanical Multiple Unit",
        "E"   : "Electric",
        "ED"  : "Electro-Diesel",
        "EML" : "EMU plus D, E, ED locomotive",
        "EMU" : "Electric Multiple Unit",
        "EPU" : "Electric Parcels Unit",
        "HST" : "High Speed Train",
        "LDS" : "Diesel Shunting Locomotive"}

    #timing_load

    operating_chars = {
        "B" : "Vacuum Braked",
        "C" : "Timed at 100 m.p.h.",
        "D" : "DOO (Coaching stock trains)",
        "E" : "Conveys Mark 4 Coaches",
        "G" : "Trainman (Guard) required",
        "M" : "Timed at 110 m.p.h.",
        "P" : "Push/Pull train",
        "Q" : "Runs as required",
        "R" : "Air conditioned with PA system",
        "S" : "Steam Heated",
        "Y" : "Runs to Terminals/Yards as required",
        "Z" : "May convey traffic to SB1C gauge. Not to be diverted from booked route without authority" }

    train_class = {
        "B" : "First & Standard seats",
        "S" : "Standard class only" }

    sleepers = {
        "B" : "First & Standard Class",
        "F" : "First Class only",
        "S" : "Standard Class only" }

    reservations = {
        "A" : "Seat Reservations Compulsory (R symbol in white box)",
        "E" : "Reservations for Bicycles Essential (Inverted black triangle)",
        "R" : "Seat Reservations Recommended (R symbol in black box)",
        "S" : "Seat Reservations possible from any station (white diamond symbol)" }

    catering = {
        "C": "Buffet Service",
        "F": "Restaurant Car available for First Class passengers",
        "H": "Service of hot food available",
        "M": "Meal included for First Class passengers",
        "P": "Wheelchair only reservations",
        "R": "Restaurant",
        "T": "Trolley Service"}

    service_branding = {
        "E": "Eurostar",
        "U": "Alphaline"}

    stp_indicator = {
        "C" : "STP Cancellation of Permanent schedule",
        "N" : "New STP schedule (not an overlay)",
        "O" : "STP overlay of Permanent schedule",
        "P" : "Permanent" }

    atoc_code = {
        "AW": "ARRIVA Trains Wales",
        "CC": "c2c",
        "CH": "Chiltern Railway Co.",
        "CT": "Central Trains",
        "EM": "East Midlands Trains",
        "ES": "Eurostar (UK)",
        "FC": "First Capital Connect",
        "GC": "Grand Central",
        "GR": "GNER",
        "GW": "First Great Western",
        "GX": "Gatwick Express",
        "HC": "Heathrow Connect",
        "HT": "Hull Trains",
        "HX": "Heathrow Express",
        "IL": "Island Line",
        "LE": "'one'",
        "LM": "London Midlands",
        "LO": "London Overground",
        "LT": "London Underground",
        "ME": "Merseyrail",
        "ML": "Midland Mainline",
        "NT": "Northern",
        "NY": "North Yorkshire Moors Railway",
        "SE": "Southeastern",
        "SN": "Southern",
        "SR": "First ScotRail",
        "SS": "Silverlink Train Services",
        "SW": "South West Trains",
        "TP": "First TransPennine Express",
        "TW": "Nexus (Tyne & Wear Metro)",
        "VT": "Virgin Trains",
        "WR": "West Coast Railway Co.",
        "XC": "CrossCountry"}

    train_activity = {
        "A":"Stops or shunts for other trains to pass",
        "AE":"Attach/detach assisting locomotive",
        "BL":"Stops for banking locomotive",
        "C":"Stops to change trainmen",
        "D":"Stops to set down passengers",
        "-D":"Stops to detach vehicles",
        "E":"Stops for examination",
        "G":"National Rail Timetable data to add",
        "H":"Notional activity to prevent WTT timing columns merge",
        "HH":"As H, where a third column is involved",
        "K":"Passenger count point",
        "KC":"Ticket collection and examination point",
        "KE":"Ticket examination point",
        "KF":"Ticket Examination Point, 1st Class only",
        "KS":"Selective Ticket Examination Point",
        "L":"Stops to change locomotives",
        "N":"Stop not advertised",
        "OP":"Stops for other operating reasons",
        "OR":"Train Locomotive on rear",
        "PR":"Propelling between points shown",
        "R":"Stops when required",
        "RM":"Reversing movement, or driver changes ends",
        "RR":"Stops for locomotive to run round train",
        "S":"Stops for railway personnel only",
        "T":"Stops to take up and set down passengers",
        "-T":"Stops to attach and detach vehicles",
        "TB":"Train begins (Origin)",
        "TF":"Train finishes (Destination)",
        "TS":"Detail Consist for TOPS Direct requested by EWS",
        "TW":"Stops (or at pass) for tablet, staff or token.",
        "U":"Stops to take up passengers",
        "-U":"Stops to attach vehicles",
        "W":"Stops for watering of coaches",
        "X":"Passes another train at crossing point on single line"}

    connection_indicator = {
        "C":"Connections not allowed into this train.",
        "S":"Connections not allowed out of this train.",
        "X":"Connections not allowed at all."}

    association_category = {
        "JJ":"join",
        "VV":"divide",
        "NP":"next"}

    assocation_date_ind = {
        "S":"standard (same day)",
        "N":"over-next-midnight",
        "P":"over-previous-midnight"}

    association_type = {
        "P":"passenger use",
        "O":"operating use only"}
