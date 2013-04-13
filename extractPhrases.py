
def extractPhrase(match, line):
    """Returns the phrase which was matched. Rather than just the matched pattern, it returns
    the complete phrase in which the match occured """

    startCount = 0
    endCount = len(line)
    for i in range(match.start() - 1, -1, -1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            startCount = i
            break
    for i in range(match.end(), len(line), 1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            endCount = i
            break
    return line[startCount:endCount]


def extractPreviousPhrase(match, line):
    """Returns the phrase before the one that was matched"""

    startCount = 0
    endCount = 0
    for i in range(match.start() - 1, -1, -1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            endCount = i
            break
    for i in range(endCount - 1, -1, -1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            startCount = i
            break
    return line[startCount:endCount]


def extractNextPhrase(match, line):
    """Returns the phrase after the one which was matched."""

    startCount = 0
    endCount = 0
    for i in range(match.end() + 1, len(line), 1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            startCount = i
            break
    for i in range(startCount + 1, len(line), 1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            endCount = i
            break
    return line[startCount:endCount]


def extractNextWord(pos, para):
    """ Returns the word starting at passed position"""

    word = ''
    for i in range(pos, len(para)):
        if para[i] == ' ' or not para[i].isalpha():
            return (word, i)
        else:
            word += para[i]



