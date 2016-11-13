""" gdbot_data
Functions that involve data (.shp file, .csv file, db connections) only.
Mainly establishing connection, but also any pre- or post-check things 
that only requires a data-object, and no rule object.
"""

import logging
import json

from osgeo import ogr
import psycopg2

import ec.uap # Hide the names and passwords in a file not shared as open source...

# create logger
log = logging.getLogger('gdbot.data')
log.info(" init this logger...") # <--- Why is this not showing up in the log? XXX

# use OGR specific exceptions
ogr.UseExceptions()

def write_connection_file(str_file_name):
    uap = ec.uap.UaP()
    dic_test = {'host' : 'localhost',
                'port' : 5432,
                'dbname' : 'pgv',
                'user' : uap.id(),
                'password' : uap.pw()
                }
    with open(str_file_name, 'w') as fil:
        fil.write(json.dumps(dic_test))
    return

class Data(object):
    
    def __init__(self, str_conn_file_name=None):
        self.type = None
        self.dic_raw_conn = None
         
        if str_conn_file_name:
            self.read_connection_file(str_conn_file_name)
        
        if self.dic_raw_conn:
            print str(self.dic_raw_conn)     
        
         
    def read_connection_file(self,str_file_name):
        try:
            with open(str_file_name, 'r') as fil:
                str_samp = fil.readlines()
        except:
            print "ERROR - Can't open file: "+str_file_name
            return (None,None,None)
        self.dic_raw_conn = json.loads(str_samp[0])
        if 'type' in self.dic_raw_conn:
            if self.dic_raw_conn['type'] == "sometype":
                pass
            if self.dic_raw_conn['type'] == "anothertype":
                pass
            else:
                print "Error - Unknown connection type in: "+str_file_name
        return

def data_open(str_data, type="OpenFileGDB", mode='r'):
    log.debug("Opening data connection\n\ttype; "+str(type)+"\n\tmode: "+str(mode))
    if type == "OpenFileGDB":
        """ Connect to database with OGR connection. """
        log.info("open OGR data\n\tdata: "+str(str_data)+"\n\ttype; "+str(type)+"\n\tmode: "+str(mode))
        driver = ogr.GetDriverByName(type)
        tup_allowed_modes = ('r') # ('r', 'rw')
        if not mode in tup_allowed_modes:
            log.error("#201 Unexpected mode > "+mode+" only allowed modes are: "+str(tup_allowed_modes))
            return 0
        try:
            con_data = driver.Open(str_data, 0)
        except Exception, e:
            log.error("#202 can't open data > "+str(e))
            return 0
        if con_data:
            return con_data
        else:
            log.error("#203 No con_data object returned, by ogr.driver.open().")
    elif type == "psycopg2_PostgreSQL":
        """ Connect to PostgreSQL database directly, using psycopg2. """
        log.info("Opening data connection:\n\ttype; "+str(type)+"\n\tmode: "+str(mode))
        return (1,2,3)
    else:
        """ Not a recognised type """
        log.error("Not a recognised type\n\tdata: "+str(str_data)+"\n\ttype; "+str(type)+"\n\tmode: "+str(mode))
        return None

        