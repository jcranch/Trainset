"""
Takes a dataset, writes it to sqlite.
"""

import os
import sqlite3

from sqlite_writer.interchanges import *
from sqlite_writer.links import *
from sqlite_writer.schedules import *
from sqlite_writer.stations import *



def make_sqlite(indir, outfile):

    indir_files = os.listdir(indir)

    def do(ext, act):
        if ext[0] != ".":
            ext = "." + ext
        for basename in indir_files:
            if basename[-len(ext):] == ext:
                print "Converting %s"%(basename,)
                fullname = os.path.join(indir,basename)
                act(fullname)

    try:
        conn = sqlite3.connect(outfile)
        c = conn.cursor()

        do("FLF", SqliteLinkMachine(cursor=c, style="fixed").parse)
        do("ALF", SqliteLinkMachine(cursor=c, style="additional").parse)
        do("TSI", SqliteInterchangeMachine(cursor=c).parse)
        do("MSN", SqliteStationMachine(cursor=c).parse)
        do("MCA", SqliteScheduleMachine(cursor=c).parse)
        do("CFA", SqliteScheduleMachine(cursor=c).parse)
        do("ZTR", SqliteScheduleMachine(cursor=c,manual=True).parse)

        conn.commit()

    finally:
        conn.close()


if __name__=="__main__":
    outfile = "../data.sqlite"
    os.remove(outfile)
    make_sqlite("../traindata/trains-043/", outfile)
