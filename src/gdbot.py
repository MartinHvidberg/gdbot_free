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
import os, sys
from datetime import datetime # for datetime.now()

import gdbot_utils

import rule_parser
import ogr_checker


def test():
    """Test to verify syntax and rule validity."""
    print "Starting check tests..."
    lst_rules = rule_parser.ReadRules(checkrules)
    print lst_rules
    dataset = "./some_test_data_source"
    data_checker.CheckData(dataset, lst_rules)
    print "Finished check tests."


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
        utils.log("ReadRules returned an error...")
        return lstRules

    print "Number of rules: "+str(len(lstRules))
    utils.log("  Checking {}, {} rules".format(rulefile, len(lstRules)))
    
    data_checker.CheckData(data, lstRules)

    timEnd = datetime.now()
    durRun = timEnd - timStart
    utils.log("   Total " + __file__ + " duration (h:mm:ss.dd): " + str(durRun)[:-3])
    
    # Finish off logfiles, etc. and clean up nicely...
    if len(logfile) > 0:
        utils.writeLogToFile(logfile)
    if len(mails) > 0:
        utils.sendLogToEmail(mails, 'gdbot run, {}'.format(rulefile.split('\\')[-1]), "Found")
    
    timEnd = datetime.now()
    durRun = timEnd - timStart
    print "\n   Total " + __file__ + " duration (h:mm:ss.dd): " + str(durRun)[:-3]

    return 0
    
if __name__ == "__main__":

    #test()

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
