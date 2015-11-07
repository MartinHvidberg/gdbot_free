
import logging

from osgeo import ogr
# create logger

import gdbot_rules

log = logging.getLogger('gdbot.data')

# use OGR specific exceptions
ogr.UseExceptions()

def data_open(str_data, type="OpenFileGDB", mode='r'):
    """ Connect to database with OGR connection, and prepare a version for editing. """
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
    
    