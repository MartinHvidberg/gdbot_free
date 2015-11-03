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
str_version = "2.0.0 build 20151103"

import sys
from datetime import datetime # for datetime.now()

import gdbot_utils
import gdbot_rules
#import data_checker

def main(data, rulefile, logfile, mails):
    
    # Read .gdbot file
    rul_a = gdbot_rules.str_to_rule("")
    print str(rul_a)
    
    # Read the .gdbot file and build the list of bot-rules
    lst_para, lst_good, lst_badr = gdbot_rules.read_gdbot_file(rulefile)
    print lst_para
    
    #===========================================================================
    # lstRules = rule_parser.ReadRules(rulefile)    
    # if isinstance(lstRules, int): # if ReadRules returned a number, it's an error code...
    #     gdbot_utils.log("ReadRules returned an error...")
    #     return lstRules
    # print "Number of rules: "+str(len(lstRules))
    # gdbot_utils.log("  Checking {}, {} rules".format(rulefile, len(lstRules)))
    #===========================================================================
    
    ###data_checker.CheckData(data, lstRules)
    
    # send e-mail, if required
    #gdbot_utils.send_log_to_email(mails, "gdbot report: "+str(datetime.now()), "Error")

    return 0
    
if __name__ == "__main__":
    
    timStart = datetime.now()

    # Initialise 
    rules = r"../rules/small.gdbot"
    logfile = r"../logs/log.txt"
    data = r"../data/some_data.file"
    mails = []
    if (len(sys.argv)>1 and sys.argv[1]!="#"): # # means default
        rules = sys.argv[1]    
    if len(sys.argv)>2 and sys.argv[2]!="#":
        logfile = sys.argv[2]
    if len(sys.argv)>3 and sys.argv[3]!="#":
        data = sys.argv[3]
    if len(sys.argv)>4 and sys.argv[4]!="#":
        mails = sys.argv[4].split(',')
    
    # Start message
    str_start_message = str(datetime.now())+"\n*** "+str_title+"\n\tversion: "+str_version+"\n\tlogfile: "+logfile+"\n\trulefile: "+rules+"\n\tdataconn: "+data+"\n\te-mail(s): "+str(mails)
    print str_start_message
    log = gdbot_utils.log_init()
    gdbot_utils.log(str_start_message, log)
    gdbot_utils.log_write_to_file(log, logfile, 'w')  
    
    # Run
    main(data, rules, logfile, mails)

    # Clean and close
    timEnd = datetime.now()
    durRun = timEnd - timStart
    str_end_message = "Python script completed " + str_title + " duration (h:mm:ss.dd): " + str(durRun)[:-3]
    gdbot_utils.log(str_end_message, log)
    gdbot_utils.log_write_to_file(log, logfile)
    print str_end_message    
    
# End of Python script ------    
