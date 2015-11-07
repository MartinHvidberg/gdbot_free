"""
    GDBOT - a Geodatabase (ro)bot
    The purpose of this project is to keep a geo data base clean and tidy
    The script acts based on a number of rules, the rules are stores in a .gdbot file
    
    THIS IS THE GDAL version of gdbot !!! 
    For the arcpy based version, look elsewhere ...
    
    Author: Martin Hvidberg <martin@hvidberg.net>
    
    SYNTAX:  gdbot.py rulefile logfile database_connection
        e.g. gdbot.py rules/nulls.gdbot logs/nulls.log MyDatabase.sde
    
    To do:
"""

str_title = __file__
str_version = "2.0.0 build 20151107"

import sys
from datetime import datetime # for datetime.now()
import logging

import gdbot_rules
import gdbot_data

def main(data, rulefile, logfile, mails):
    
    # Read the .gdbot file and build the list of bot-rules
    lst_para, lst_good, lst_badr = gdbot_rules.read_gdbot_file(rulefile)
    log.info("para:"+str(len(lst_para)))
    log.info("good:"+str(len(lst_good)))
    log.info("badr:"+str(len(lst_badr)))
    
    gdbot_data.check_data(data, lst_good)
    
    # send e-mail, if required

    return 0
    
if __name__ == "__main__":
    
    # Initialise 
    rules = r"../rules/small.gdbot"
    data = r"../data/some_data.file"
    logfile = r"../logs/log.txt"
    mails = []
    if (len(sys.argv)>1 and sys.argv[1]!="#"): # # means default
        rules = sys.argv[1]    
    if len(sys.argv)>2 and sys.argv[2]!="#":
        data = sys.argv[2]
    if len(sys.argv)>3 and sys.argv[3]!="#":
        logfile = sys.argv[3]
    if len(sys.argv)>4 and sys.argv[4]!="#":
        mails = sys.argv[4].split(',')
    
    # Start message, and logging
    str_start_message = "Start\n\tprogram : "+str_title+"\n\tversion : "+str_version+"\n\tlogfile : "+logfile+"\n\trulefile: "+rules+"\n\tdataconn: "+data+"\n\te-mails : "+str(mails)
    log = logging.getLogger('gdbot')
    log.setLevel(logging.DEBUG)
    log_fil = logging.FileHandler(logfile, mode='w')
    log_fil.setLevel(logging.INFO)
    log_fil.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')) #
    log.addHandler(log_fil)
    log.info(str_start_message)
    
    # Run
    timStart = datetime.now()
    main(data, rules, logfile, mails)
    timEnd = datetime.now()

    # Clean and close
    durRun = timEnd - timStart
    str_end_message = "Python script completed - duration (h:mm:ss.dd): " + str(durRun)[:-3]
    log.info(str_end_message)
    print str_end_message    
    
# End of Python script ...
