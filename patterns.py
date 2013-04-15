from string import *
from extractPhrases import *
import re

def titleCase(s):

    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                lambda mo: mo.group(0)[0].upper() +
                            mo.group(0)[1:].lower(),
                            s)

def removeSpaceBeforePunctuation(match, para):
    """
    Match   :   Space before punctuation
    Fix     :   Remove space before punctuation"""
    return match.group(2)


def addSpaceAfterPunctuation(match, para):
    """ Match   :   Letter right after punctuation
    Fix     :   Add a space after punctuation"""

    return match.group(1)+" "+match.group(2)


def capitalizeFirst(match, para):
    """ Match   :   Space before punctuation
    Fix     :   Remove space before punctuation"""

    # if match.start() == 0:
    #     newPara = para[0].upper() + para[match.end()]
    # else:
    #     for i in range(match.start(), match.end(), 1):
    #         if para[i] == ' ':
    #             newPara = para[0:i + 1] + para[i + 1].upper() + para[i
    #                 + 2:len(para)]
    return match.group(0).upper()



def removeExtraSpaces(match, para):
    """ Match   :   Multiple spaces
    Fix     :   Replace with single space"""

    return " "


def addTildeBeforeCite(match, para):
    """ Match   :   /cite without a tilde before. Either a space or a letter.
    Fix     :   Remove any spaces and replace with tilde."""

    return "~"+match.group(2)



def titleCaseFirstWord(match, para):
    """ Match   :   Section reference with 's' not capital in section.
    Fix     :   Capitalize the 's' in section."""

    return match.group(1)[0].upper() + match.group(1)[1:].lower()+match.group(2)


def convertToTitleCase(match, para):
    """ Match   :   Non-title case cheapter/ section heading
    Fix     :   Title cased"""
    return titleCase(match.group(0))

def convertToSentenceCase(match, para):
    print(match.group(0))
    return match.group(0)[0].upper()+match.group(0)[1:].lower()



def removeRepeatedPhrase(match, para):
    """ Match   :   Repeated phrase.
    Fix     :   Remove repeated phrase"""
    # newpara = para[0:match.start()] + para[match.start():match.start()
    #     + (match.end() - match.start()) / 2] + para[match.end()
    #     - 1:len(para)]
    newpara = match.group(2)+match.group(3)
    return newpara


# Store this in a dictionary with a short hand description, tags and the replacementFunction for the tag


patterns = [
    # r'\\(sub)+section':["ONLY FIRST WORD CAPITALIZED IN SUBSECTIONS", 'c', convertFirstLetterToCapital],
    {"regex":r'((?<=(\\subsection\{))|(?<=(\\subsubsection\{))|(?<=(\\paragraph\{))|(?<=(\\subparagraph\{)))(([^A-Z](.*?))|([A-Z](.*?)[A-Z](.*?)))(?=\})',    "description":'SENTENCE CASE FOR SUBSECTIONS AND BELOW',  "tags":'c',     "function":convertToSentenceCase},
    {"regex":r'((?<=(\\section\{))|(?<=(\\chapter\{)))((|(.*) )[a-z].*)(?=\})',    "description":'TITLE CASE FOR SECTIONS AND CHAPTERS',  "tags":'c',     "function":convertToTitleCase},
    {"regex":r'( +)([\.,;:])',          "description":'SPACE BEFORE PUNCTUATION',  "tags":'aceh',     "function":removeSpaceBeforePunctuation},
    {"regex":r'(?<!\d)([\.,;:])([\w])',        "description":'NO SPACE AFTER PUNCTUATION',"tags":'aceh',     "function":addSpaceAfterPunctuation},
    {"regex":r'((?<=(\.\s))|(?<=(^\s))|(?<=\A))[a-z]',    "description":'MISSING CAPITALIZATION OF FIRST WORD AFTER FULL STOP',
                                                                                    "tags":'ace',      "function":capitalizeFirst},
    {"regex":r'(\s*)(?<!~)((\\cite)|(\\ref))',   "description":'TILDE MARK NEEDED BEFORE CITE / REF',
                                                                                    "tags":'ace',       "function":addTildeBeforeCite},
    {"regex":r'(chapter)(~\\ref)',          "description":'CAPITALIZE C IN CHAPTER',    "tags":'c',         "function":titleCaseFirstWord},
    {"regex":r'(section)(~\\ref)',          "description": 'CAPITALIZE S IN SECTION',   "tags":'c',         "function":titleCaseFirstWord},
    {"regex":r' ( )+',                  "description":'TOO MANY SPACES',            "tags":'cefb',     "function":removeExtraSpaces},
    {"regex":r'(?i)((?<=\s)|(?<=^))([A-Za-z][A-Za-z ]*)([^\w\d]+)\2((?=([ \n\.,;]))|(?=$))',
                                        "description":'REPEATED PHRASE',            "tags":'ce',         "function":removeRepeatedPhrase},
    ]
# change too many spaces to be more specific
# |([A-Z](.*?)[A-Z](.*?))
# |([A-Z](.*?)[A-Z](.*?))
# (?<=("description":'))(.*?)(?=')


def capitalizeFirstLetter(word):
    return upper(word[0]) + word[1:len(word)]


def uncapitalizeFirstLetter(word):
    return lower(word[0]) + word[1:len(word)]


def notFullyCapital(word):
    """ Checks whether the word is fully capital. If so , it is likely to be some sort of abbreviation or acronym."""
    return not word.isupper()

