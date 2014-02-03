import re
from string import upper, lower


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
    print match.groups()
    if match.group(1) is None:
        return match.group(3)+" "
    else:
        return match.group(2)+" "


def capitalizeFirst(match, para):
    """ Match   :   Space before punctuation
    Fix     :   Remove space before punctuation"""

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


patterns = (
    # r'\\(sub)+section':["ONLY FIRST WORD CAPITALIZED IN SUBSECTIONS", 'c', convertFirstLetterToCapital],
    {"regex": r'((?<=(\\subsection\{))|(?<=(\\subsubsection\{))|(?<=(\\paragraph\{))|(?<=(\\subparagraph\{)))(([^A-Z](.*?))|([A-Z](.*?)[A-Z](.*?)))(?=\})',
     "description": 'Sentence Case For Subsections And Below',
     "tags": 'c',
     "function": convertToSentenceCase},
    {"regex": r'((?<=(\\section\{))|(?<=(\\chapter\{)))((|(.*) )[a-z].*)(?=\})',
     "description": 'Title Case For Sections And Chapters',
     "tags": 'c',
     "function": convertToTitleCase},
    {"regex": r'( +)([\.,;:])',
     "description": 'Space Before Punctuation',
     "tags": 'acehmrfp',
     "function": removeSpaceBeforePunctuation},
    {"regex": r'((\.)(?![\s\d\]\}\)]))|([,;:\?\]\)\}])(?=[a-zA-Z0-9])',
     "description": 'No Space After Punctuation',
     "tags": 'acehmrfp',
     "function": addSpaceAfterPunctuation},
    {"regex": r'((?<=(\.\s))|(?<=(\n\n))|(?<=\A))[a-z]',
     "description": 'Missing Capitalization Of First Word After Full Stop',
     "tags": 'acehmpb',
     "function": capitalizeFirst},
    {"regex": r'(\s*)(?<!~)((\\cite)|(\\ref))',
     "description": 'Tilde Mark Needed Before Cite / Ref',
     "tags": 'ac',
     "function": addTildeBeforeCite},
    {"regex": r'(chapter)(~\\ref)',
     "description": 'Capitalize C In Chapter',
     "tags": 'c',
     "function": titleCaseFirstWord},
    {"regex": r'(section)(~\\ref)',
     "description": 'Capitalize S In Section',
     "tags": 'c',
     "function": titleCaseFirstWord},
    {"regex": r'(?i)((?<=\s)|(?<=^))([A-Za-z][A-Za-z ]*)([^\w\d]+)\2((?=([ \n\.,;]))|(?=$))',
     "description": 'Repeated Phrase',
     "tags": 'ce',
     "function": removeRepeatedPhrase},
)


def capitalizeFirstLetter(word):
    return upper(word[0]) + word[1:len(word)]


def uncapitalizeFirstLetter(word):
    return lower(word[0]) + word[1:len(word)]


def notFullyCapital(word):
    """ Checks whether the word is fully capital. If so ,
    it is likely to be some sort of abbreviation or acronym."""
    return not word.isupper()
