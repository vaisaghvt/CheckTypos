#/usr/bin/python
import itertools as it
import re
import os
import Getch as gc
from patterns import *
from extractPhrases import *
from tagChecks import *
import sys


def dealWithIt(match, para, replacementFunction):
    """ Deals with a pattern match. Checks for replacement, displays it for user and asks what to do with
    it"""

    replacement = suggestReplacement(match, para, replacementFunction)
    while True:
        print 'Suggested replacement:', replacement
        print '(a)ccept suggestion | (i)gnore:',
        option = gc.getch()
        print option
        if option == 'a':
            return replacement, True
        elif option == 'i':

        # elif option == 'e':
        #     print "code to edit and write own correction here"
        #     return getReplacement(match, para)

            print 'ignored... '
            return para, False
        else:
            print 'invalid choice'


def suggestReplacement(match, para, replacementFunction):
    """ Calls the replacement function with the right arguments"""

    return replacementFunction(match, para)


def saveChanges(group, fileName):
    """ Saves the changes that are made."""

    # for para in group:
    #     print para

    tempFileName = fileName + '.temp'
    with open(tempFileName, 'w') as writeFile:
        for para in group:
            writeFile.write(para + '\n')
    os.remove(fileName)
    os.rename(tempFileName, fileName)


def processParagraph(paragraphs):
    problemsFound = False
    for iteration in range(2):
        for pattern in patterns:

            flag = False
            for index, para in enumerate(paragraphs):
                regex = re.compile(pattern["regex"])

                while True:
                    replacementMade = False
                    for match in regex.finditer(para):
                        for option in pattern["tags"]:
                            if checkPattern(option, match, para):
                                # print 'flag true'
                                flag = True
                                break
                        if flag:
                            flag = False
                            continue
                        problemsFound = True
                        print 'Problem: ', pattern["description"], \
                            '; Para', index+1
                        print 'Phrase: ', extractPhrase(match, para)

                        # print "context: ",para

                        # paragraphs[index], replacementMade = dealWithIt(match,
                        #         para, pattern["function"])
                        para = paragraphs[index]
                        print '**********************'
                        if replacementMade:
                            break
                    if not replacementMade:
                        break
    # if not problemsFound:
    #     print 'No mistakes found. Good Stuff!'
    # else:
    #     print 'Corrections made in ', fileName
    #     saveChanges(paragraphs, fileName)
    #     problemsFound = False

# write as seperate module
# Also, try to seperate itemize , etc. maybe have another function to slice it further.

# paragraph_lists = []

# def main():
#     for fileName in sys.argv[1:]:
#         print '//////////////Checking ', fileName, '/////////////////////'
#         print '********************'
#         paragraphs = []
#         with open(fileName) as f:
#             paragraphs = getParagraphs(f)
#         processParagraph(paragraphs, fileName)



# if __name__=="__main__":
#     if len(sys.argv) <= 1:
#         print 'Usage : grammarCheck file1 file2 ...'
#     main()
