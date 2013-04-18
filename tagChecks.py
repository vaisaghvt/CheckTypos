from extractPhrases import *
from urlparse import urlparse
import re

def checkPattern(option, match, line):

    if option =='a':
        # print 'checking acronym'
        return isAcronym(extractPhrase(match, line))
    elif option =='c':
        # print 'checking comment'
        return isComment(match, line)
    elif option =='e':
        # print 'checking equation'
        return isEquation(match, line)
    elif option =='p':
        return isPicture(match, line)
    elif option =='b':
        return isTable(match, line)
    elif option =='h':
        return isInHyperLink(extractPhrase(match, line))
    elif option =='m':
        return isInMail(extractPhrase(match, line))
    elif option =='r':
        return isInRefCiteOrLabel(extractPhrase(match, line))
    elif option =='f':
        return isLikelyFile(extractPhrase(match, line))

def isLikelyFile(phrase):
    if re.search(r"(\\input\{.*?\})|(\\bibliography\{.*?\})", phrase) is not None:
        return True
    return False

def isInRefCiteOrLabel(phrase):
    if re.search(r"(\\ref\{.*?\})|(\\label\{.*?\})|(\\cite\{.*?\})", phrase) is not None:
        return True
    return False

def isInHyperLink(phrase):
    phrase=phrase.strip()
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
    if(phrase.rfind('i.e.')!=-1
        or phrase.rfind('e.g.')!=-1
        or phrase.rfind('etc.')!=-1):
#        print "returning true"
        return True
    else :
        return False


def isInCite(phrase):
    '''Returns a true if the match is in Cite'''
    if(phrase.rfind(r'\cite')==0):
        return True
    else :
        return False

def inLineEquation(match, line):
    """ Returns true if in inline equation"""
    hasDollarTagBefore=False
    for i in range(match.start()-1,-1,-1):
        if line[i] == '$':
            hasDollarTagBefore=True
            break
    if hasDollarTagBefore:
        for i in range(match.end(),len(line),1):
            if line[i] == '$':
                return True
    return False

def inEquationBody(match, line):
    # print 'checking equation', match.start()-1
    end= line[0:match.start()].rfind(r'\end{equation}')
    pos= 0
    while(end!=-1):
        pos= end+3
        # print pos, 'line', line[pos:match.start()]
        end= line[pos:match.start()].rfind(r'\end{equation}')
        # print '*******'
    beg=line[pos:match.start()].rfind(r'\begin{equation}')
    if(beg!=-1):
        return True
    return False

def isPicture(match, line):
    end= line[0:match.start()].rfind(r'\end{figure}')
    pos= 0
    while(end!=-1):
        pos= end+3
        # print pos, 'line', line[pos:match.start()]
        end= line[pos:match.start()].rfind(r'\end{figure}')
        # print '*******'
    beg=line[pos:match.start()].rfind(r'\begin{figure}')
    if(beg!=-1):
        return True
    return False

def isTable(match, line):
    end= line[0:match.start()].rfind(r'\end{table}')
    pos= 0
    while(end!=-1):
        pos= end+3
        # print pos, 'line', line[pos:match.start()]
        end= line[pos:match.start()].rfind(r'\end{table}')
        # print '*******'
    beg=line[pos:match.start()].rfind(r'\begin{table}')
    if(beg!=-1):
        return True
    return False

def isEquation(match, line):
    if(inLineEquation(match,line) or inEquationBody(match, line)):
       return True
    else:
       return False

def isComment(match, line):
    for i in range(match.start()-1,-1,-1):
        # print line[i]
        if line[i] == '\n':
            break
        if line[i] == '%':
            return True
    return False