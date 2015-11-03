
import gdbot_utils

class Rule:
    """ Rule parser for gdbot version 2.0 """
    def __init__(self, str_id, str_title, str_mode, str_data_table, str_condition, str_action, str_act_param, str_comment):
        # The ID
        self.id = str_id
        # str_title
        self.title = str_title
        # str_mode
        self.mode = str_mode.upper()
        if self.str_mode != "SQL" and self.str_mode != "LOVE":
            gdbot_utils.log("Warning, rule {}: Only SQL and LOVE str_modes are supported, unknown str_mode {}.".format(self.id, str_mode))
            return None
        self.data_table_list = str_data_table.split(",") # split will return a list, even if there are no commas
        # str_condition
        self.str_condition = str_condition.replace("!=","<>")
        if ('"' in self.str_condition): # double quotes won't work
            if(not "'" in self.str_condition):
                self.str_condition = self.str_condition.replace('"',"'")
                gdbot_utils.log("Warning, rule {}: Can't have \"double quotes\" in str_condition, use 'single quotes' instead.".format(self.id))
            else:
                print "Error, rule {}: There are both \"double quotes\" and 'single quotes' in str_condition - this will fail.".format(self.id)
                gdbot_utils.log("Error, rule {}: There are both \"double quotes\" and 'single quotes' in str_condition - this will fail.".format(self.id))
        if (self.str_mode == 'LOVE'):
            if (not '%' in self.str_condition):
                gdbot_utils.log("Error, rule {}: LOVE rule without % character.".format(self.id))
                return None
            self.str_condition = [val.strip() for val in str_condition.split('%')]
            self.str_condition[1] = [val.strip() for val in self.str_condition[1][1:-1].split(',') ]
        # Fix or Log - self.dofix is a bool
        self.dofix = False # (str_action=="FIX") # 'considered harmful' FIX str_mode is not trusted, yet...
        self.act_param = []
        # - for FIXes, self.act_param is a list of pairs of fixes, e.g. PLTS_COMP_SCALE=90000,IS_CONFLATE=TRUE
        if self.dofix:
            if str_act_param: # there's probably a cleaner way of doing this looping and cleaning...
                # TODO: recognize a str_act_param which is another column name
                self.act_param = [fixpair.split("=") for fixpair in str_act_param.split(",")] # split on , and =
                self.act_param = [[val.strip() for val in fixpair] for fixpair in self.act_param] # strip whitespace
                for fix in self.act_param:
#                    fix = [val.strip() for val in fix] # strip whitespace
                    fix[1] = CleanUpFixString(fix[1]) # ugly quote mark removal, recognising None, NULL, UNKNOWN and typecasting int/float
                #print self.act_param
            else:
                self.dofix = False
                gdbot_utils.log("Warning, rule {}: FIX with no repair values; treating as LOG.".format(str(self.id)))
                # if the user didn't supply a fix value, this is more helpful than throwing an error
        # - for LOGs, self.act_param is a list of field names to include in log output
        elif str_act_param: # list of fields to report on
            self.act_param = [val.strip() for val in str_act_param.split(',')] # split by comma and strip whitespace
        self.comm = str_comment
        
    def __repr__(self):
        return "({}; {}; {}; \"{}\"; {}:{}) {}\n".format(\
        str(self.id), str(self.str_title), str(self.data_table_list), 
            self.GetWhereString(), str(self.dofix), str(self.act_param), self.comm)
# end class Rule

def CleanUpFixString(str_act_param): # XXX This is truly Ugly, rethink that...
    """ If string starts and ends with matching quote marks, remove these; also convert None, NULL (and UNKNOWN), and convert to int/double. """
    # This is ugly: we're stripping quote marks off the str_act_param, even when it's a string.
    # They're required in the test value, but not allowed in the fix value,
    # so we'll allow the user to enter them in both places, and remove them here.
    if(str_act_param and str_act_param[0] == str_act_param[-1] and (str_act_param[0]=="'" or str_act_param[0]=='"')):
        str_act_param = str_act_param[1:-1]
    #if str_act_param.upper() == "UNKNOWN":
    #    return -32767 # TODO: is this a good idea? other values to accept?
    if str_act_param.upper() == "NULL" or str_act_param.upper() == "NONE":
        return None # make sure to return, the following lines will choke on a None
    if str_act_param.isdigit():
        return int(str_act_param)
    if gdbot_utils.isFloat(str_act_param): # this will also match on int, so check that first
        return float(str_act_param.replace(",", ".", 1)) # accept either , or . as decimal separator
    return str_act_param

def ReadRules(path):
    """Read rules from a file, and return a list of Rule objects"""
    print " Reading rule file: "+path
    lst_rules = list()
    bol_valid_version = False
    try:
        with open(path, 'r') as f:
            for line_raw in f:
                line = line_raw.split('#')[0].strip()
                if len(line)>0:
                    if(line[0]=="%"): # % Parameter line
                        lst_par = line.strip("%").strip().split('=')
                        if lst_par[0].strip()=='gdbot_syntax_version' and lst_par[1].strip()=='2.0':
                            gdbot_utils.log("Recognise gdbot version 2.0")
                            print "  Recognise gdbot version 2.0"
                            bol_valid_version = True
                    elif(line[0]==":"): # : Rule line
                        lst_items = line[1:].split(":")
                        if len(lst_items)==8:
                            r = Rule(lst_items)
                            if r.id != -1:
                                lst_rules.append(r)
                        else:
                            gdbot_utils.log("Warning: Line does not contain the correct number of elements - Check that you comment do not contain ':'. Ignoring this rule. \n\t"+line.strip()+"\n\t"+str(len(lst_items))+'\t'+str(lst_items))
                    else:
                        gdbot_utils.log("Warning: Rule line must start with #, % or : "+line[0]+" ("+line+")")
            print "Done reading rules."
    except IOError, e:
        gdbot_utils.log(e.errno)
        gdbot_utils.log(e)
        return 101
    if bol_valid_version:
        return lst_rules
    else:
        gdbot_utils.log("Error, rule file {}: Unfortunately the gdbot version is {}.".format(path,bol_valid_version))
        return 201
