import smtplib

def log_init():
    """ Initialise log """
    return list()

def log(string, log):
    """ Append message to the log. """
    log.append(str(string))
    return log

def log_write_to_file(log, filename, mode='a'):
    """ Write compiled log messages to file. """
    if len(log) > 0:
        #print "writelog: "+str(len(log))+" to: "+filename
        with open(filename, mode) as f:
            for l in log:
                try:
                    f.write(l+'\n')
                except:
                    print "Can't write: "+l
        log = list() # clear the log after sucessfull write
    return 0

def send_log_to_email(lst_recipients, subject, flag):
    """ Send contents of lst_log to given recipients. """
    # Set up contents
    SERVER = "mailgate.mim.dk"
    FROM = "gdbot <gdbot@work.com>"
    TO = lst_recipients
    MSG = ''
    status = 0
    for logline in lst_log:
        MSG += "{}\n".format(logline)
        if flag in str(logline):
            status += 1
    SUBJ = "{} - {} issues".format(subject, status)

    # Prepare actual message
    # Avoid putting leading spaces at beginning of each line, so use \n instead of linebreaks w indent
    MESSAGE = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJ, MSG)

    # Send the mail
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, MESSAGE)
    server.quit()

    return 0


# def encodeIfUnicode(strval):
#     """Encode if string is unicode."""
#     if isinstance(strval, unicode):
#         return strval.encode('utf8')
#     return str(strval)

#def decodeIfUnicode(strval):
#    """Decode if string is unicode."""
#    if isinstance(strval, unicode):
#        return strval.encode('iso-8859-1')
#    return str(strval)

