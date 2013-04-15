import sublime, sublime_plugin
#/usr/bin/python
import itertools as it
import re
import os
import Getch as gc
from patterns import *
from extractPhrases import *
from tagChecks import *
import sys
import threading



def suggestReplacement(match, para, replacementFunction):
        """ Calls the replacement function with the right arguments"""

        return replacementFunction(match, para)


class CheckTyposCommand(sublime_plugin.TextCommand):


    def run(self, edit):
        self.replacementMade = False
        self.inputLock = threading.Lock()
        self.user_input_ready = False
        self.myKey = "CheckTypoKey"
        self.view.erase_status(self.myKey)
        self.recalculateMatches()
        print(self.completeBuffer)
        dj = threading.Thread(target=self.processParagraph, args=())
        dj.start()
        # self.processParagraph([completeBuffer])

    def recalculateCompleteBuffer(self):
        # print("recalculating buffers")
        regions = self.view.find_all(".*")
        self.completeBuffer = '\n'.join(map(self.view.substr, regions))


    def recalculateMatches(self):
        self.recalculateCompleteBuffer()
        # print("recalculating matches")
        self.viewMatches = {}
        self.matchIterators = {}
        for pattern in patterns: # for each pattern
            regexPattern = pattern["regex"]
            self.viewMatches[regexPattern] = self.view.find_all(regexPattern)
            regex = re.compile(regexPattern)
            self.matchIterators[regexPattern] = regex.finditer(self.completeBuffer)





    def getUserInput(self):
        print("current suggested replacement"+self.currentReplacement)
        sublime.active_window().show_input_panel(self.descriptionString, self.currentReplacement, self.on_done, None, self.on_cancel)

    def dealWithIt(self, match, para, replacementFunction):
        """ Deals with a pattern match. Checks for replacement, displays it for user and asks what to do with
        it"""

        self.currentReplacement = suggestReplacement(match, para, replacementFunction)
        sublime.set_timeout(self.getUserInput, 0)
        # return para, False
        # else:
        #     print 'invalid choice'

    def on_done(self, userInput):
        print("Done:"+userInput)
        editObject =self.view.begin_edit()
        self.view.replace(editObject, self.currentMatchedRegionInView, userInput)
        self.recalculateMatches()
        self.view.end_edit(editObject)
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

    def processParagraph(self):
        problemsFound = False
        user_input_ready = False
        self.inputLock.acquire(True)

        for iteration in range(2):
            for pattern in patterns: # for each pattern

                regexPattern = pattern["regex"]
                # print(regexPattern)
                regex = re.compile(regexPattern)


                # for viewMatch in viewMatches:
                #     print(sublime.set_timeout(self.view.substr(sublime.set_timeout(self.view.word(viewMatch))),0)
                flag = False

                while True:
                    self.replacementMade = False
                    sublime.set_timeout(self.recalculateMatches,0)
                    count=0
                    for match in self.matchIterators[regexPattern]: # for each match in the paragraph
                        # print(match)

                        self.currentMatchedRegionInView = self.viewMatches[regexPattern][count]


                        count= count+1
                        for option in pattern["tags"]:
                            if checkPattern(option, match, self.completeBuffer):
                                # print 'flag true'
                                flag = True
                                break
                        if flag:
                            flag = False
                            continue
                        problemsFound = True
                        sublime.set_timeout(self.changeSelection,0)
                        # print 'Problem: ', pattern["description"]
                        #      # '; Para', index+1
                        print 'Phrase: ', extractPhrase(match, self.completeBuffer)
                        print self.currentMatchedRegionInView

                        # print "context: ",para
                        self.descriptionString = pattern["description"]

                        self.dealWithIt(match,
                                self.completeBuffer, pattern["function"])
                        self.inputLock.acquire(True)
                        # para = paragraphs[index]
                        # print '**********************'
                        if self.replacementMade:
                            break
                    if not self.replacementMade:
                        break

        # print("done")
        if not problemsFound:
            self.printStatus='No mistakes found. Good Stuff!'
        else:
            self.printStatus='Typo check complete'
        sublime.set_timeout(self.printStatusMessage,0)
        #     saveChanges(paragraphs, fileName)
        #     problemsFound = False
