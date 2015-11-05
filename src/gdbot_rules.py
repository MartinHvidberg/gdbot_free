"""
Functions handeling gdbot rules
mainly reading rules from text files and generating rule objects (dictionary)
some elementary sanity checking of the rules, before they are applied
"""
import logging

# create logger
log = logging.getLogger('gdbot.rules')

def str_to_rule(str_in):
    """reads a text string, and try to make a rule dictionary out of it.
    returns a dictionary"""
    lst_in = str_in.split('#')[0].strip()
    if len(str_in)>0:
        log.info("str_to_rule: "+str_in.strip())
        dic_rule = dict(valid=False,type=None,errors=list(),
                        id="",title="",mode="",data_table="",condition="",action="",act_param="",comment="",
                        key="",val="")
        if(str_in[0]=="%"): # % Parameter str_in
            lst_par = str_in.strip("%").strip().split('=')
            log.info(str(lst_par))
            if lst_par[0].strip()=='gdbot_syntax_version' and lst_par[1].strip()=='2.0':
                dic_rule['type']='para'
                dic_rule['key']=lst_par[0].strip()
                dic_rule['val']=lst_par[1].strip()
                dic_rule['valid']=True
                log.info("Recognise gdbot version 2.0")
        elif(str_in[0]==":"): # : Rule str_in
            lst_items = str_in[1:].split(":")
            log.info(str(lst_items))
            if len(lst_items)==8:
                dic_rule['type']='rule'
                dic_rule['id']=lst_items[0]
                dic_rule['title']=lst_items[1]
                dic_rule['mode']=lst_items[2].upper()
                dic_rule['data_table']=lst_items[3]
                dic_rule['connection']=lst_items[4]
                dic_rule['action']=lst_items[5]
                dic_rule['act_param']=lst_items[6]
                dic_rule['comment']=lst_items[7]
                dic_rule = sanity_check(dic_rule)
            else:
                dic_rule['errors'].append("Rule string does not contain the correct number of elements - Check that you comment do not contain ':'. Ignoring this rule. \n\t"+str_in.strip()+"\n\t"+str(len(lst_items))+'\t'+str(lst_items))
                dic_rule['valid']=False
                log.warning('MSG1')
        else:
            dic_rule['errors'].append("Rule string must start with #, % or : "+str_in[0]+" ("+str_in+")")
            dic_rule['valid']=False
            log.warning(dic_rule['errors'][-1:])
        return dic_rule
    return 0

def sanity_check(dic_rule):
    dic_rule['valid']=True # Assumed good, until proved bad
    lst_valid_type = ['para','rule']
    if dic_rule['type'] not in lst_valid_type:
        dic_rule['errors'].append("Rule have invalid type: "+str(dic_rule['type'])+'. Valid modes are '+str(lst_valid_type))
        dic_rule['valid']=False
    for field in ['id','title','mode','data_table','action','act_param','comment']: # 'connection', should likely allow local chars
        if not isinstance(dic_rule[field], str):
            dic_rule['errors'].append("Please don't use unicode in rules field: "+str(field))
            dic_rule['valid']=False
    for field in ['id','title','mode','data_table','connection','action','act_param','comment']:
        if isinstance(dic_rule[field], str):
            if len(dic_rule[field]) < 1:
                dic_rule['errors'].append("Parameter in rule seems to be very short. field: "+str(field)+" value: "+dic_rule[field])
                dic_rule['valid']=False
    lst_valid_modes = ['SQL','LOVE']
    if dic_rule['mode'] not in lst_valid_modes:
        dic_rule['errors'].append("Rule have invalid mode: "+str(dic_rule['mode'])+'. Valid modes are '+str(lst_valid_modes))
        dic_rule['valid']=False
    lst_valid_action = ['LOG','FIX']
    if dic_rule['action'] not in lst_valid_action:
        dic_rule['errors'].append("Rule have invalid action: "+str(dic_rule['action'])+'. Valid modes are '+str(lst_valid_action))
        dic_rule['valid']=False
    return dic_rule

def read_gdbot_file(str_infile):
    lst_para = list()
    lst_good_rules = list()
    lst_bad_rules = list()
    with open(str_infile, 'r') as f:
        for line_raw in f:
            dic_r = str_to_rule(line_raw)
            if dic_r['valid']:
                if dic_r['type']=='rule':
                    lst_good_rules.append(dic_r)
                elif dic_r['type']=='para':
                    lst_para.append(dic_r)
                else:
                    lst_bad_rules.append(dic_r)
            else:
                lst_bad_rules.append(dic_r)
    return [lst_para,lst_good_rules,lst_bad_rules]
