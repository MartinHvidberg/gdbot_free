import smtplib, re

lst_log = [] # Collector list for things to log ...

def log(string):
    """Append message to the log."""
    global lst_log
    lst_log.append(string)
    return 0

def writeLogToFile(filename):
    """Write compiled log messages to file."""
    with open(filename, 'w') as f:
        for log in lst_log:
            f.write(log+'\n')

def sendLogToEmail(lst_recipients, subject, flag):
    '''Send contents of lst_log to given recipients.'''
    # Set up contents
    SERVER = "mailgate.mim.dk"
    FROM = "TeamNIS batch script <halpe@gst.dk>"
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

floatPattern = re.compile("^[0-9.,]+$")
def isFloat(string):
    """ Check if string looks like a float (or int) number. """
    return re.search(floatPattern, string)

def encodeIfUnicode(strval):
    """Encode if string is unicode."""
    if isinstance(strval, unicode):
        return strval.encode('utf8')
    return str(strval)

#def decodeIfUnicode(strval):
#    """Decode if string is unicode."""
#    if isinstance(strval, unicode):
#        return strval.encode('iso-8859-1')
#    return str(strval)

