import re


def checkPattern(option, match, completeBuffer, phrase):
    # print phrase
    if option == 'a':
        # print 'checking acronym'
        return isAcronym(phrase)
    elif option == 'b':
        # print 'checking acronym'
        return afterAcronym(match, completeBuffer)
    elif option == 'c':
        # print 'checking comment'
        return isComment(match, completeBuffer)
    elif option == 'e':
        # print 'checking equation'
        return isEquation(match, completeBuffer)
    elif option == 'p':
        return isPicture(match, completeBuffer)
    elif option == 'b':
        return isTable(match, completeBuffer)
    elif option == 'h':
        return isInHyperLink(phrase)
    elif option == 'm':
        return isInMail(phrase)
    elif option == 'r':
        return isInRefCiteOrLabel(phrase)
    elif option == 'f':
        return isLikelyFile(phrase)


def isLikelyFile(phrase):
    if re.search(r"(\\input\{.*?\})|(\\bibliography\{.*?\})", phrase) is not None:
        return True
    return False


def isInRefCiteOrLabel(phrase):
    # print phrase
    if re.search(r"(\\ref\{.*?\})|(\\label\{.*?\})|(\\cite\{.*?\})||(\\eqref\{.*?\})", phrase) is not None:
        return True
    return False


def isInHyperLink(phrase):
    phrase = phrase.strip()
    if re.search(r"www\..*\.", phrase) is not None:
        return True

    # phrase = phrase[:-1]
    # print phrase
    # o = urlparse(phrase)
    # if len(o.netloc) >0 :
    #     return True
    return False


def isInMail(phrase):
    if re.search(r".*@.*\.", phrase) is not None:
        return True
    return False


def isAcronym(phrase):
    '''Returns a true if the match is an acronym'''
#    print "testing if", phrase, "is an acronym"
    if phrase.rfind('i.e.') != -1 or phrase.rfind('e.g.') != -1 or phrase.rfind('etc.') != -1:
        return True
    else:
        return False


def afterAcronym(match, completeBuffer):
    '''Returns a true if the match is an acronym'''
#    print "testing if", phrase, "is an acronym"
    if match.start() > 2:
        char = completeBuffer[match.start()-2]
        if char == '.':
            stringAsList = []
            i = match.start() - 2
            while completeBuffer[i] != ' ' and i != 0:
                stringAsList.insert(0, completeBuffer[i])
                i = i-1
            string = ''.join(stringAsList)
            if string.rfind('i.e.') != -1 or string.rfind('e.g.') != -1:
        #        print "returning true"
                return True
    return False


def isInCite(phrase):
    '''Returns a true if the match is in Cite'''
    if(phrase.rfind(r'\cite') == 0):
        return True
    else:
        return False


def isPicture(match, completeBuffer):
    end = completeBuffer[0:match.start()].rfind(r'\end{figure}')
    pos = 0
    while end != -1:
        pos = end+3
        # print pos, 'completeBuffer', completeBuffer[pos:match.start()]
        end = completeBuffer[pos:match.start()].rfind(r'\end{figure}')
        # print '*******'
    beg = completeBuffer[pos:match.start()].rfind(r'\begin{figure}')
    if(beg != -1):
        return True
    return False


def isTable(match, completeBuffer):
    end = completeBuffer[0:match.start()].rfind(r'\end{table}')
    pos = 0
    while(end != -1):
        pos = end+3
        # print pos, 'completeBuffer', completeBuffer[pos:match.start()]
        end = completeBuffer[pos:match.start()].rfind(r'\end{table}')
        # print '*******'
    beg = completeBuffer[pos:match.start()].rfind(r'\begin{table}')
    if beg != -1:
        return True
    return False


def isEquation(match, completeBuffer):
    if (inLineEquation(match, completeBuffer) or inEquationBody(match, completeBuffer)):
        return True
    else:
        return False


#Obsolete : to be replaced
def inLineEquation(match, completeBuffer):
    """ Returns true if in incompleteBuffer equation"""
    hasDollarTagBefore=False
    for i in range(match.start()-1,-1,-1):
        if completeBuffer[i] == '\n':   # TODO : replace this something else.
            break;
        if completeBuffer[i] == '$':
            hasDollarTagBefore=True
            break
    if hasDollarTagBefore:
        for i in range(match.end(),len(completeBuffer),1):
            if completeBuffer[i] == '\n':   # TODO : replace this something else.
                break;
            if completeBuffer[i] == '$':
                return True
    return False

# Issue : ignores end equations that are commented out.
def inEquationBody(match, completeBuffer):
    # print 'checking equation', match.start()-1
    end= completeBuffer[0:match.start()].rfind(r'\end{equation}') # Find the end of last equation
    pos= 0
    while(end!=-1):     # If it found some other equation in the file, keep finding till there are
                        # no  more end equations after the pos position
        pos= end+3
        # print pos, 'completeBuffer', completeBuffer[pos:match.start()]
        end= completeBuffer[pos:match.start()].rfind(r'\end{equation}')
        # print '*******'
    beg=completeBuffer[pos:match.start()].rfind(r'\begin{equation}')
    if(beg!=-1):
        return True
    return False


def isComment(match, completeBuffer):
    for i in range(match.start()-1,-1,-1):
        # print completeBuffer[i]
        if completeBuffer[i] == '\n':
            break
        if completeBuffer[i] == '%':
            return True
    return False