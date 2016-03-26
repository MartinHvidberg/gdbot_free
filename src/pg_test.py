#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import ppygis

# Connect to an existing spatially enabled database
try:
    con = psycopg2.connect("dbname='testqgis' user='editor' host='localhost' password='iceicebaby'")
except:
    print "I am unable to connect to the database"
cur = con.cursor()
print str(type(cur)), cur

try:
    #cur.execute("""SELECT * from spatial_ref_sys""")
    #cur.execute('SELECT * from public.spatial_ref_sys')
    cur.execute('SELECT * from "in"."solroed"')
except:
    print "I can't SELECT from that table ..."

rows = cur.fetchall()
print "\nRows: \n"
for row in rows:
    print "   ", row[0], row[1], row[2]


# Disconnect from the database
cur.close()
con.close()