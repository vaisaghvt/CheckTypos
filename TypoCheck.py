import sublime, sublime_plugin
from grammarCheck import processParagraph

class CheckTyposCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all(".*")
        completeBuffer = ' '.join(map(self.paraString, regions))
        print(sublime.active_window())
        processParagraph([completeBuffer],self)

    def paraString(self, region):
        line= self.view.substr(region)
        if line=="":
            return "\n"
        else:
            return line

    def printDescription(self, descriptionString):
        self.view.erase_status("description")
        self.view.set_status("description", descriptionString)


    def getUserInput(self, replacement, on_done, on_change, on_cancel):
        sublime.active_window().show_input_panel("Mistake found:", replacement, on_done, on_change, on_cancel)

