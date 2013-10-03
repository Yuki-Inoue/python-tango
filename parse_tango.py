#!/usr/bin/python

import sys
import sqlite3
from time import strptime, strftime

if len(sys.argv) != 3:
    print "usage: %s <tango file> <target db>" % sys.argv[0]
    exit()

tango = sys.argv[1]
conn = sqlite3.connect(sys.argv[2])
conn.text_factory = str
c = conn.cursor()

c.execute('''create table cards
(nexptime datetime, crct int, question text, answer text)''')


f = open(tango,'r')
i = 0
data = []
all_data = []
for line in f:
    i += 1
    i %= 5
    line = line.rstrip('\n')
    if not i:
        print data
        c.execute('insert into cards values(?,?,?,?)',
                  (data[0],data[1],data[2],data[3]))
        data = []
    else:
        if i == 1:
            data.append(strftime("%Y-%m-%d %H:%M:%S",strptime(line,"%Y-%b-%d %H:%M:%S")))
        else:
            data.append(line)


conn.commit()
conn.close()


