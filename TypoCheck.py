#/usr/bin/python

import sublime
import sublime_plugin
import re
from patterns import patterns
from tagChecks import checkPattern
import threading
import os
from collections import defaultdict

def syntax_name(view):
    syntax = os.path.basename(view.settings().get('syntax'))
    syntax = os.path.splitext(syntax)[0]
    return syntax

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


affectedRegions=defaultdict(list)

def last_selected_lineno(view):
    viewSel = view.sel()
    if not viewSel:
        return None
    return view.rowcol(viewSel[0].end())[0]

class HighlightMistakesCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        self.view = view
        self.regionsToHighlight=[]
        self.myKey = "CheckTypoKey"

    def run_(self, args):

        if syntax_name(self.view) == "LaTeX":
            # if self.view.id not in affectedRegions or last_selected_lineno(self.view) in affectedRegions[self.view.id]:
            if not args or "full_test" not in args:

                self.view.erase_status(self.myKey)
                self.viewMatches = []
                self.matchIterators = []
                self.patternList = []
                self.recalculateMatches()
                # print(self.completeBuffer)
                self.mainThread = threading.Thread(target=self.processBuffer)
                self.mainThread.start()
                # self.processBuffer([completeBuffer])
            else:
                self.displayCurrentError()
                self.higlightAllRegions()

    def recalculateCompleteBuffer(self):
        # print("recalculating buffers")
        regions = self.view.find_all(".*")
        self.completeBuffer = '\n'.join(map(self.view.substr, regions))

    def recalculateMatches(self):
        self.recalculateCompleteBuffer()
        # print("recalculating matches")

        regionToRegexMatchAndPatternMapping = {}
        listOfRegions = []

        for pattern in patterns:  # for each pattern
            regexPattern = pattern["regex"]
            # regexPattern = pattern["regex"]
            #     # print(regexPattern)
            regex = re.compile(regexPattern)
            viewMatchesFound = self.view.find_all(regexPattern)


            for count, match in enumerate(regex.finditer(self.completeBuffer)):
                correspondingView = viewMatchesFound[count]

                regionToRegexMatchAndPatternMapping[correspondingView] = (match, pattern)
                listOfRegions.append(correspondingView)


        listOfRegions = sorted(listOfRegions, key=(lambda region: region.begin()))

        self.patternList = []
        self.matchIterators = []
        self.viewMatches = []

        for region in listOfRegions:
            matchingRegex = regionToRegexMatchAndPatternMapping.get(region)[0]
            pattern = regionToRegexMatchAndPatternMapping.get(region)[1]

            self.patternList.append(pattern)
            self.matchIterators.append(matchingRegex)
            self.viewMatches.append(region)


    def printStatusMessage(self):
        self.view.erase_status(self.myKey)
        self.view.set_status(self.myKey, self.printStatus)



    def higlightAllRegions(self):
        self.view.add_regions("mark", self.regionsToHighlight, "comment", "dot",
                sublime.DRAW_OUTLINED)
        for region in self.regionsToHighlight:
            affectedRegions[self.view.id].append(self.view.rowcol(region.begin())[0])

    def displayCurrentError(self):
        lineno = last_selected_lineno(self.view)
        messagesToPrint= []
        if lineno and self.regionsToHighlight:
            for region in self.regionsToHighlight:
                if self.view.rowcol(region.begin())[0] == lineno:
                    messagesToPrint.append(self.descriptionStringList[region.begin()])


        if messagesToPrint:
            self.printStatus = "; ".join(messagesToPrint)
            self.printStatusMessage()
        else:
            self.printStatus = "Possible errors found"
            self.printStatusMessage()

    def processBuffer(self):
        problemsFound = False


        tagExceptionMatch = False
        self.regionsToHighlight =[]
        self.descriptionStringList ={}
        while len(self.viewMatches) > 0:
            regexMatch = self.matchIterators.pop(0)
            self.currentMatchedRegionInView = self.viewMatches.pop(0)
            pattern = self.patternList.pop(0)
            for option in pattern["tags"]:
                phrase = extractPhrase(regexMatch, self.completeBuffer)
                if checkPattern(option, regexMatch, self.completeBuffer, phrase):
                    # print 'tagExceptionMatch true'
                    tagExceptionMatch = True
                    break
            if tagExceptionMatch:
                tagExceptionMatch = False
                continue
            problemsFound = True
            self.regionsToHighlight.append(self.currentMatchedRegionInView)

            lineno = self.currentMatchedRegionInView.begin()

            self.descriptionStringList[lineno]= pattern["description"]

        if not problemsFound:
            self.printStatus = 'No mistakes found. Good Stuff!'
            sublime.set_timeout(self.higlightAllRegions, 0)
            sublime.set_timeout(self.printStatusMessage, 0)
        else:
            sublime.set_timeout(self.higlightAllRegions, 0)
            sublime.set_timeout(self.displayCurrentError, 0)

class BackgroundLinter(sublime_plugin.EventListener):
    '''This plugin controls a linter meant to work in the background
    to provide interactive feedback as a file is edited. It can be
    turned off via a setting.
    '''

    def __init__(self):
        super(BackgroundLinter, self).__init__()
        self.lastSelectedLineNo = -1


    def on_post_save(self, view):
        view.run_command("highlight_mistakes")

    def on_load(self, view):
        view.run_command("highlight_mistakes")
    # def on_selection_modified(self, view):
    #     if view.is_scratch():
    #         return

    def on_selection_modified(self, view):
        # pass
        view.run_command("highlight_mistakes", "full_test")
        # view.run_command("highlight_mistakes")
