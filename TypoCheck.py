import sublime, sublime_plugin
from grammarCheck import processParagraph

class CheckTyposCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all(".*")
        completeBuffer = ''.join(map(self.paraString, regions))
        processParagraph(completeBuffer.split('\n'))

    def paraString(self, region):
        line= self.view.substr(region)
        if line=="":
            return "\n"
        else:
            return line

