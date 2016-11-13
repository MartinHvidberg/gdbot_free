""" gdbot_data
Functions that involve data (.shp file, .csv file, db connections) only.
Mainly establishing connection, but also any pre- or post-check things 
that only requires a data-object, and no rule object.
"""

import logging
import json

from osgeo import ogr
import psycopg2

# create logger
log = logging.getLogger('gdbot.data')
log.info(" init this logger...") # <--- Why is this not showing up in the log? XXX

# use OGR specific exceptions
ogr.UseExceptions()

class Data(object):
    
    def __init__(self, str_conn_file_name=None):
        self.conn_type = None
        self.dic_raw_conn = None
         
        if str_conn_file_name:
            self.read_connection_file(str_conn_file_name)
        
        #if self.dic_raw_conn:
        #    print str(self.dic_raw_conn)     
        
    def read_connection_file(self,str_file_name):
        try:
            with open(str_file_name, 'r') as fil:
                str_samp = fil.readlines()
        except:
            print "ERROR - Can't open file: "+str_file_name
            return (None,None,None)
        self.dic_raw_conn = json.loads(str_samp[0])
        if 'conn_type' in self.dic_raw_conn:
            if self.dic_raw_conn['conn_type'] == "PostgreSQL": # The OGR driver...
                try:
                    self.conn_type = self.dic_raw_conn['conn_type']
                    #self.conn_mode = self.dic_raw_conn['conn_mode']
                    self.host = self.dic_raw_conn['host']
                    #self.port = self.dic_raw_conn['port']
                    self.dbname = self.dic_raw_conn['dbname']
                    self.user = self.dic_raw_conn['user']
                    self.password = self.dic_raw_conn['password']
                except:
                    print "Error - One or more parameters missing in connection: "+str(self.dic_raw_conn)
            elif self.dic_raw_conn['conn_type'] == "psycopg2_PostgreSQL":
                try:
                    self.conn_type = self.dic_raw_conn['conn_type']
                    self.conn_mode = self.dic_raw_conn['conn_mode']
                    self.host = self.dic_raw_conn['host']
                    self.port = self.dic_raw_conn['port']
                    self.dbname = self.dic_raw_conn['dbname']
                    self.user = self.dic_raw_conn['user']
                    self.password = self.dic_raw_conn['password']
                except:
                    print "Error - One or more parameters missing in connection: "+str(self.dic_raw_conn)
            else:
                print "Error - Unknown connection type in: "+str_file_name
        return

    def data_open(self):
        log.debug("Opening data connection\n\ttype; "+str(self.conn_type))
        # e.g. CSV, ESRI Shapefile, GeoJSON, OpenFileGDB, PostgreSQL, S57, WFS
        if self.conn_type == "PostgreSQL":
            log.info("open OGR type: "+str(self.conn_type))
            driver = ogr.GetDriverByName(str(self.conn_type))            
            connString = "PG: host=%s dbname=%s user=%s password=%s" %(self.host,self.dbname,self.user,self.password)
            try:
                self.con = driver.Open(connString, 0)
            except Exception, e:
                log.error("#202 can't open data > "+str(e))
        elif self.conn_type == "OpenFileGDB":
            log.info("open OGR data\n\tdata: "+str(str_data)+"\n\ttype; "+str(type)+"\n\tmode: "+str(mode))
            driver = ogr.GetDriverByName(type)
            tup_allowed_modes = ('r') # ('r', 'rw')
            if not mode in tup_allowed_modes:
                log.error("#201 Unexpected mode > "+mode+" only allowed modes are: "+str(tup_allowed_modes))
                return 0
            try:
                self.con = driver.Open(str_data, 0)
            except Exception, e:
                log.error("#202 can't open data > "+str(e))
            else:
                log.error("#203 No con_data object returned, by ogr.driver.open().")
        elif self.conn_type == "psycopg2_PostgreSQL":
            """ Connect to PostgreSQL database directly, using psycopg2. """
            log.info("Opening data connection:\n\ttype; "+str(type)+"\n\tmode: "+str(mode))
            return (1,2,3)
        else:
            """ Not a recognized type """
            log.error("Not a recognized type in self.conn_type; "+str(self.conn_type))
            return None
        
    def list_geo_layers(self):        
        if self.conn_type in ["PostgreSQL"]:
            self.lst_layer = list()
            for i in self.con:
                lay_name = i.GetName()
                if not lay_name in self.lst_layer:
                    self.lst_layer.append(lay_name)            
            self.lst_layer.sort()
            self.lst_feat_count = list()
            for str_layname in self.lst_layer:
                lyr = self.con.GetLayer(str_layname)
                self.lst_feat_count.append(lyr.GetFeatureCount())