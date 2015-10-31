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
import sys
from datetime import datetime # for datetime.now()

import gdbot_utils

import rule_parser
import data_checker

def main(data, rulefile, logfile, mails):
    
    print "    logfile: "+logfile
    print "    rulefile: "+rules
    print "    dataconn: "+data
    print "    e-mail(s): "+str(mails)
    
    timStart = datetime.now()
    
    # Read the .gdbot file and build the list of bot-rules
    lstRules = rule_parser.ReadRules(rulefile)
    #print lstRules
    
    if isinstance(lstRules, int): # if ReadRules returned a number, it's an error code...
        gdbot_utils.log("ReadRules returned an error...")
        return lstRules

    print "Number of rules: "+str(len(lstRules))
    gdbot_utils.log("  Checking {}, {} rules".format(rulefile, len(lstRules)))
    
    data_checker.CheckData(data, lstRules)

    timEnd = datetime.now()
    durRun = timEnd - timStart
    gdbot_utils.log("   Total " + __file__ + " duration (h:mm:ss.dd): " + str(durRun)[:-3])
    
    # Finish off logfiles, etc. and clean up nicely...
    if len(logfile) > 0:
        gdbot_utils.writeLogToFile(logfile)
    if len(mails) > 0:
        gdbot_utils.sendLogToEmail(mails, 'gdbot run, {}'.format(rulefile.split('\\')[-1]), "Found")
    
    timEnd = datetime.now()
    durRun = timEnd - timStart
    print "\n   Total " + __file__ + " duration (h:mm:ss.dd): " + str(durRun)[:-3]

    return 0
    
if __name__ == "__main__":

    rules = r"~/rules/test.gdbot"
    logfile = r"~/logs/log.txt"
    data = r"~/data/some_data.file"
    mails = []
    
    if (len(sys.argv)>1):
        rules = sys.argv[1]
    else:
        print "Usage: gdbot.py <rules.gdbot> <logfile.txt> <data_source> <e-mails>"
        sys.exit()
    
    if len(sys.argv) > 2:
        logfile = sys.argv[2]
    
    if len(sys.argv) > 3:
        db = sys.argv[3]
    
    if len(sys.argv) > 4:
        mails = sys.argv[4].split(',')
    
    main(data, rules, logfile, mails)
