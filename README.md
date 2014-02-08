CheckTypos
==========

Plugin to highlight some standard mistakes and typos in latex
files. This plugin does not check for spelling mistakes. Only
works on latex files.

The Sublime Text 3 version is a [separate repository](https://github.com/vaisaghvt/CheckTypos3)


Default key mapping
-------------------

mac     : ctrl + command + alt + c - Highlight Mistakes

windows : ctrl + shift + alt + c - Highlight Mistakes

linux   : ctrl + shift + alt + c - Highlight Mistakes



Command in pallete
------------------

Highlight Mistakes: Check Current File

Command in menu
---------------

Tools Menu

Usage
-----

A dot on the gutter bar indicates a line with an error. An
outline is drawn around each error. Moving the caret
to the line of error displays the error description in the
status bar. Errors are determined on save or on running the
command.

Currently Checked Patterns
--------------------------

1. Repeated phrase
2. Title case for sections and chapters
3. Space before punctuation
4. No space after punctuation
5. Missing capitalization of first word after full stop
6. Tilde mark needed before \cite / \ref
7. Capitalize c in chapter and s in section for references
8. Sentence case for subsections and below

The plugin is generally smart enough to avoid certain tags,
environments, etc.




