""" GDBOT - a Geodata (ro)bot
    The purpose of this project is to keep a geo-data clean and tidy
    The script acts based on a number of rules, the rules are stores in a .gdbot file
    
    THIS IS THE Open Source version of gdbot !!! 
    For the deprecated Esri/arcpy based version, look at https://github.com/MartinHvidberg/gdbot
    
    Author: Martin Hvidberg <martin@hvidberg.net>
    
    SYNTAX:  gdbot.py rulefile logfile database_connection
        e.g. gdbot.py rules/nulls.gdbot logs/nulls.log MyDatabase_connection_file
"""

str_title = __file__
str_version = "2.0.1 build 20161023"

""" Version history:
    2.0.0 - Initial Open source version, works (fundamental functionality) with GDAL connections to Esri .sde. '20151107/Martin
    2.0.1 - Introducing PostgreSQL connections, alongside GDAL connections. '20161023/Martin
            Action is limited to LOG (not FIX)
            interpretation mode is limited to SQL (not LOVE)

    To do:
        More smooth behaviour across GDAL and PostgreSQL connections
        Implement LOVE interpreter
        Implement FIX action
"""

import sys
from datetime import datetime # for datetime.now()
import logging

import gdbot_data  # Data (connection) only
import gdbot_rules # Rules handling only, not applying 
import gdbot_check # Using Data and Rules together

def main(conn, rulefile, logfile, mails):
    
    # Read the connection info and build a connection
    log.info("*** Making Connection...")
    dic_conn = gdbot_data.read_connection_file(conn)
    if dic_conn:
        str_type = dic_conn['conn_type']
        str_mode = dic_conn['conn_mode']
        con_data = gdbot_data.data_open(dic_conn, str_type, str_mode)
        log.info("Connection: "+str(con_data))
        if con_data:
            # Read the .gdbot file and build the list of bot-rules
            log.info("*** Making Rules...")
            lst_para, lst_good, lst_badr = gdbot_rules.read_gdbot_file(rulefile)
            log.info("para:"+str(len(lst_para)))
            log.info("good:"+str(len(lst_good)))
            log.info("badr:"+str(len(lst_badr)))
        
            if len(lst_good)>0:
                # gdbot_data.check_data(data, lst_good)
                log.info("*** Checking data...")
                
                # send e-mail, if required
                log.info("*** Writing results...")
        
                return 0
        else:
            num_err = 102
            log.error("Warning {} - Didn't find any valid rules in rule file. See logfile for details: ".format(num_err))
            return num_err
    else:
        num_err = 101
        log.error("ERROR {} - Failed to connect to data base...".format(num_err))
        return num_err
    
if __name__ == "__main__":
    
    # Initialise 
    #rules = r"../rules/small.gdbot"
    rules = r"../rules/test.gdbot"
    conn = r"../data/pg_samp.gdbot_cnct"
    logfile = r"../logs/log.txt"
    mails = []
    if (len(sys.argv)>1 and sys.argv[1]!="#"): # # means default
        rules = sys.argv[1]    
    if len(sys.argv)>2 and sys.argv[2]!="#":
        conn = sys.argv[2]
    if len(sys.argv)>3 and sys.argv[3]!="#":
        logfile = sys.argv[3]
    if len(sys.argv)>4 and sys.argv[4]!="#":
        mails = sys.argv[4].split(',')
    
    # Start message, and logging
    str_start_message = "*** Start\n\tprogram : "+str_title+"\n\tversion : "+str_version+"\n\tlogfile : "+logfile+"\n\trulefile: "+rules+"\n\tdataconn: "+conn+"\n\te-mails : "+str(mails)
    log = logging.getLogger('gdbot')
    log.setLevel(logging.DEBUG)
    log_fil = logging.FileHandler(logfile, mode='w')
    log_fil.setLevel(logging.INFO)
    log_fil.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')) #
    log.addHandler(log_fil)
    log.info(str_start_message)
    
    # Run
    timStart = datetime.now()
    status = main(conn, rules, logfile, mails)
    if status != 0:
        print "Error code {}. See logfile for details: {}".format(status, logfile)
    timEnd = datetime.now()

    # Clean and close
    durRun = timEnd - timStart
    str_end_message = "Python script completed - duration (h:mm:ss.dd): " + str(durRun)[:-3]
    log.info(str_end_message)
    print str_end_message    
    
# End of Python script ...
