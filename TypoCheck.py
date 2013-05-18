#/usr/bin/python

import sublime, sublime_plugin
import re
from patterns import patterns
from tagChecks import checkPattern
import threading



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


def suggestReplacement(match, para, replacementFunction):
        """ Calls the replacement function with the right arguments"""

        return replacementFunction(match, para)

def findBegin(region):
    return region.begin()

class CheckMistakesCommand(sublime_plugin.TextCommand):


    def run(self, edit):
        self.currentLocation =-1
        self.replacementMade = False
        self.inputLock = threading.Lock()
        self.user_input_ready = False
        self.myKey = "CheckTypoKey"
        self.view.erase_status(self.myKey)
        self.viewMatches = []
        self.matchIterators = []
        self.patternList=[]
        self.recalculateMatches()
        # print(self.completeBuffer)
        self.mainThread = threading.Thread(target=self.processBuffer)
        self.mainThread.start()
        # self.processBuffer([completeBuffer])

    def recalculateCompleteBuffer(self):
        # print("recalculating buffers")
        regions = self.view.find_all(".*")
        self.completeBuffer = '\n'.join(map(self.view.substr, regions))


    def recalculateMatches(self):
        self.recalculateCompleteBuffer()
        # print("recalculating matches")

        regionToRegexMatchAndPatternMapping = {}
        listOfRegions = []

        for pattern in patterns: # for each pattern
            regexPattern = pattern["regex"]
            # regexPattern = pattern["regex"]
            #     # print(regexPattern)
            regex = re.compile(regexPattern)
            viewMatchesFound = self.view.find_all(regexPattern)
            iteratorOverAllRegexMatchesFound = regex.finditer(self.completeBuffer);
            count =0
            for match in iteratorOverAllRegexMatchesFound:
                correspondingView = viewMatchesFound[count]

                regionToRegexMatchAndPatternMapping[correspondingView] = (match,pattern)
                listOfRegions.append(correspondingView)
                count = count+1


        listOfRegions = sorted(listOfRegions, key= findBegin)

        beforeCurrentList=[]
        afterCurrentList=[]
        for region in listOfRegions:
            if region.begin() <self.currentLocation:
                beforeCurrentList.append(region)
            else :
                afterCurrentList.append(region)

        listOfRegions = []
        listOfRegions.extend(afterCurrentList)
        listOfRegions.extend(beforeCurrentList)

        self.patternList=[]
        self.matchIterators=[]
        self.viewMatches=[]

        for region in listOfRegions:
            matchingRegex = regionToRegexMatchAndPatternMapping.get(region)[0]
            pattern = regionToRegexMatchAndPatternMapping.get(region)[1]

            self.patternList.append(pattern)
            self.matchIterators.append(matchingRegex)
            self.viewMatches.append(region)








    def getUserInput(self):
        # print("current suggested replacement"+self.currentReplacement)
        sublime.active_window().show_input_panel(self.descriptionString,
            self.currentReplacement, self.on_done, None, self.on_cancel)

    def dealWithIt(self, match, para, replacementFunction):
        """ Deals with a pattern match. Checks for replacement, displays it for user and asks what to do with
        it"""

        self.currentReplacement = suggestReplacement(match, para, replacementFunction)
        sublime.set_timeout(self.getUserInput, 0)
        # return para, False
        # else:
        #     print 'invalid choice'

    def on_done(self, userInput):
        # print("Done:"+userInput)
        editObject =self.view.begin_edit()
        self.view.replace(editObject, self.currentMatchedRegionInView, userInput)
        self.view.end_edit(editObject)
        self.recalculateMatches()
        self.user_input_ready = True
        self.replacementMade= True
        self.inputLock.release()

    def on_cancel(self):
        self.user_input_ready = True
        self.inputLock.release()

    def printStatusMessage(self):
        self.view.erase_status(self.myKey)
        self.view.set_status(self.myKey,self.printStatus)


    def input_is_ready(self):
        return user_input_ready

    def changeSelection(self):
        self.view.sel().clear()
        self.view.sel().add(self.currentMatchedRegionInView)
        self.view.show(self.currentMatchedRegionInView)

    def processBuffer(self):
        problemsFound = False
        user_input_ready = False
        self.inputLock.acquire(True)


        # for iteration in range(2):
            # for pattern in patterns: # for each pattern
                # regexPattern = pattern["regex"]
                # # regexPattern = pattern["regex"]
                # #     # print(regexPattern)
                # regex = re.compile(regexPattern)



                # for viewMatch in viewMatches:
                #     print(sublime.set_timeout(self.view.substr(sublime.set_timeout(self.view.word(viewMatch))),0)
        tagExceptionMatch = False

        while len(self.viewMatches)>0:
            regexMatch = self.matchIterators.pop(0)
            self.currentMatchedRegionInView = self.viewMatches.pop(0)
            pattern = self.patternList.pop(0)
            self.currentLocation =  self.currentMatchedRegionInView.begin()


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
            sublime.set_timeout(self.changeSelection,0)
            # print 'Problem: ', pattern["description"]
            #      # '; Para', index+1
            # print 'Phrase: ', extractPhrase(regexMatch, self.completeBuffer)
            # print self.currentMatchedRegionInView

            # print "context: ",para
            self.descriptionString = pattern["description"]

            self.dealWithIt(regexMatch,
                    self.completeBuffer, pattern["function"])
            self.inputLock.acquire(True)
            # sublime.set_timeout(self.recalculateMatches,0)
        # print("done")
        if not problemsFound:
            self.printStatus='No mistakes found. Good Stuff!'
        else:
            self.printStatus='Typo check complete'
        sublime.set_timeout(self.printStatusMessage,0)
        #     saveChanges(paragraphs, fileName)
        #     problemsFound = False
