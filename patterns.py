from string import *
from extractPhrases import *


def removeSpaceBeforePunctuation(match, para):
    """
    Match   :   Space before punctuation
    Fix     :   Remove space before punctuation"""

    if match.start() == 0:
        newPara = para[1:len(para)]
    for i in range(match.start(), match.end(), 1):
        if para[i] == ' ':
            newPara = para[0:i] + para[i + 1:len(para)]
    return newPara


def addSpaceAfterPunctuation(match, para):
    """ Match   :   Letter right after punctuation
    Fix     :   Add a space after punctuation"""

    for i in range(match.start(), match.end(), 1):
        if para[i] == '.' or para[i] == ',' or para[i] == ';' \
            or para[i] == ':':
            newPara = para[0:i + 1] + ' ' + para[i + 1:len(para)]
    return newPara


def capitalizeFirst(match, para):
    """ Match   :   Space before punctuation
    Fix     :   Remove space before punctuation"""

    if match.start() == 0:
        newPara = para[0].upper() + para[1:len(para)]
    else:
        for i in range(match.start(), match.end(), 1):
            if para[i] == ' ':
                newPara = para[0:i + 1] + para[i + 1].upper() + para[i
                    + 2:len(para)]
    return newPara


def removeExtraSpaces(match, para):
    """ Match   :   Multiple spaces
    Fix     :   Replace with single space"""

    return para[0:match.start()] + ' ' + para[match.end():len(para)]


def addTildeBeforeCite(match, para):
    """ Match   :   /cite without a tilde before. Either a space or a letter.
    Fix     :   Remove any spaces and replace with tilde."""

    for i in range(match.start(), match.end(), 1):
        if para[i] == '\\':
            if para[i - 1] == ' ':
                newPara = para[0:i - 1] + '~' + para[i:len(para)]
            else:
                newPara = para[0:i] + '~' + para[i:len(para)]
    return newPara


def capitalizeChapter(match, para):
    """ Match   :   Chapter reference with 'c' not capital in chapter.
    Fix     :   Capitalize the 'c' in chapter."""

    if match.start() == 0:
        newPara = para[0].upper() + para[1:len(para)]
    for i in range(match.start(), match.end(), 1):
        if para[i] == 'c':
            newPara = para[0:i] + para[i].upper() + para[i
                + 1:len(para)]
    return newPara


def capitalizeSection(match, para):
    """ Match   :   Section reference with 's' not capital in section.
    Fix     :   Capitalize the 's' in section."""

    if match.start() == 0:
        newPara = para[0].upper() + para[1:len(para)]
    for i in range(match.start(), match.end(), 1):
        if para[i] == 's':
            newPara = para[0:i] + para[i].upper() + para[i
                + 1:len(para)]
    return newPara


def convertToTitleCase(match, para):
    """ Match   :   Non title case section or chapter heading.
    Fix     :   Change to title case"""

    for i in range(match.end(), len(para), 1):
        if para[i] == '{':
            pos = i
            break
    newPara = para[0:pos]
    count = 1
    forceCapitalize = True
    while pos < len(para):
        if para[pos] == '{':
            count += 1
            newPara += para[pos]
        elif para[pos] == '}':
            count -= 1
            newPara += para[pos]
            if count == 0:
                break
        if para[pos].isalpha():
            (nextWord, pos) = extractNextWord(pos, para)
            if forceCapitalize:
                newPara += capitalizeFirstLetter(nextWord)
                forceCapitalize = False
            elif nextWord not in (
                'and',
                'the',
                'or',
                'on',
                'at',
                'in',
                ):
                newPara += capitalizeFirstLetter(nextWord)
        else:
            newPara += para[pos]
        pos += 1
    newPara += para[pos:len(para)]


def convertFirstLetterToCapital(match, para):
    """    Match   :   Non sentence case sub or sub sub section.
    Fix     :   Change to sentence case"""

    for i in range(match.end(), len(para), 1):
        if para[i] == '{':
            pos = i
            break
    newPara = para[0:pos]
    count = 1
    forceCapitalize = True
    while pos < len(para):
        if para[pos] == '{':
            count += 1
            newPara += para[pos]
        elif para[pos] == '}':
            count -= 1
            newPara += para[pos]
            if count == 0:
                break
        if para[pos].isalpha():
            (nextWord, pos) = extractNextWord(pos, para)
            if forceCapitalize:
                newPara += capitalizeFirstLetter(nextWord)
                forceCapitalize = False
            elif notFullyCapital(nextWord):
                newPara += uncapitalizeFirstLetter(nextWord)
        else:
            newPara += para[pos]
        pos += 1
    newPara += para[pos:len(para)]


def removeRepeatedPhrase(match, para):
    """ Match   :   Repeated phrase.
    Fix     :   Remove repeated phrase"""

    newpara = para[0:match.start()] + para[match.start():match.start()
        + (match.end() - match.start()) / 2] + para[match.end()
        - 1:len(para)]
    return newpara


# Store this in a dictionary with a short hand description, tags and the replacementFunction for the tag


patterns = [
    # r'\\section|\\chapter':["TITLE CASE FOR SECTIONS AND CHAPTERS", 'c', convertToTitleCase],
    # r'\\(sub)+section':["ONLY FIRST WORD CAPITALIZED IN SUBSECTIONS", 'c', convertFirstLetterToCapital],
    {"regex":r' [\.,;:]',               "description":'SPACE BEFORE PUNCTUATION.',  "tags":'taceh',     "function":removeSpaceBeforePunctuation},
    {"regex":r'[\.,;:][\w]',        "description":'NO SPACE AFTER PUNCTUATION.',"tags":'taceh',     "function":addSpaceAfterPunctuation},
    {"regex":r'([\.]|^)\s+[a-z]',    "description":'MISSING CAPITALIZATION OF FIRST WORD AFTER FULL STOP.',
                                                                                    "tags":'tace',      "function":capitalizeFirst},
    {"regex":r'[^~]\\cite|[^~]\\ref',   "description":'TILDE MARK NEEDED BEFORE CITE',
                                                                                    "tags":'ace',       "function":addTildeBeforeCite},
    {"regex":r'chapter~\\ref',          "description":'CAPITALIZE C IN CHAPTER',    "tags":'c',         "function":capitalizeChapter},
    {"regex":r'section~\\ref',          "description": 'CAPITALIZE S IN SECTION',   "tags":'c',         "function":capitalizeSection},
    {"regex":r' ( )+',                  "description":'TOO MANY SPACES',            "tags":'tcefb',     "function":removeExtraSpaces},
    {"regex":r'(?i)([ ]+|^)(\w[\w ]*)[^\w\d]+\2([ \.,;]|$|)',
                                        "description":'REPEATED PHRASE',            "tags":'i',         "function":removeRepeatedPhrase},
    ]



def capitalizeFirstLetter(word):
    return upper(word[0]) + word[1:len(word)]


def uncapitalizeFirstLetter(word):
    return lower(word[0]) + word[1:len(word)]


def notFullyCapital(word):
    """ Checks whether the word is fully capital. If so , it is likely to be some sort of abbreviation or acronym."""
    return not word.isupper()

