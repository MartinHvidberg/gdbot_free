""" gdbot_data
Functions that involve BOTH Data and Rules.
Mainly the actually gdbot check routines...
"""

import logging

# create logger
log = logging.getLogger('gdbot.check')
log.info(" init this logger...") # <--- Why is this not showing up in the log? XXX

import gdbot_rules

def data_check(con_data, lst_rules):
    """Check the tables of the given data set, according to the rules."""
    #for rule in lst_rules:
    #    print gdbot_rules.show_rule(rule)
    for featsClass_idx in range(con_data.GetLayerCount()):
        featsClass = con_data.GetLayerByIndex(featsClass_idx)
        def_layer = featsClass.GetLayerDefn()
        str_lyr_name = featsClass.GetName()
        print "Layer: ", str_lyr_name        
        for i in range(def_layer.GetFieldCount()):
            str_fld_name = def_layer.GetFieldDefn(i).GetName()
            print "    field:", str_fld_name
            # Select the rules that apply...
            lst_appl_rules = list()
            for rul_i in lst_rules:
                pass#if rul[]

def check_data(dataset, lst_rules):
    """Check a data set, using the given rule set."""
    con_data = data_open(dataset, "OpenFileGDB", 'r')   
    res_check = data_check(con_data, lst_rules) # *** This is the big enchilada 
    return res_check
    
    