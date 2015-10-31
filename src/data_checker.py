import ogr

import gdbot_utils

def DataOpen(str_data, mode):
    """Connect to database with OGR connection, and prepare a version for editing."""
    gdbot_utils.log("   < DataOpen() >")
    gdbot_utils.log("   "+str_data)
    if not mode in ('r', 'rw'):
        gdbot_utils.log("   Unexpected mode: "+mode)
        return 201
    data_connection = ogr.open(str_data, mode) XXX
    if not data_connection:
        gdbot_utils.log("   Can't open data source: "+str_data)
        return 202        
    return data_connection

def DataClose(data_connection):
    """Close the data connection"""    
    gdbot_utils.log("   < DataClose() >")
    data_connection.close() XXX
    return 0

def CheckTables(dataset, rules):
    """Check the tables of the given dataset, according to the rules."""
    
    # If you get: "RuntimeError: An expected Field was not found or could not be retrieved properly."
    # don't use double quotes in condition input, use single quotes!!!

    gdbot_utils.log("   < CheckTables() >")
    totalFixes = 0
    totalLogs = 0

    Walk the data table, and apply each rule in rules

    str_end_message = "Done checking tables, total {} log hits and {} fixes.".format(totalLogs, totalFixes)
    gdbot_utils.log("     "+str_end_message)
    print str_end_message


def CheckData(dataset, rules, verbosity):
    """Check a dataset, using the given rule set."""
    gdbot_utils.log("   < CheckData() >")    
    hasEdits = False
    for rule in rules:
        if rule.dofix:
            hasEdits = True    
    con_data = DataOpen(dataset)    
    CheckTables(con_data, rules, verbosity) # *** This is the big enchilada 
    DataClose(con_data)
    