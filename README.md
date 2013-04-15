CheckTypos
==========

Plugin to fix some standard mistakes and typos in plain text or
latex files. This plugin does not check for spelling mistakes.


Default key mapping
-------------------

mac     : ctrl + command + alt + c
windows : ctrl + shift + alt + c
linux   : ctrl + shift + alt + c

Command in pallete
------------------

CheckTypos: Check Current File

Command in menu
---------------

Tools Menu

Usage
-----

Each error is highlighted on the screen and an input panel appears
at the bottom with a suggested replacement. This suggestion can
either be accepted or edited. Press "enter (return)" to accept the change.
Press "esc" to ignore this. The status bar indicates the check
completion when no more mistakes are left.

Currently Checked Patterns
--------------------------

1. Repeated phrase
2. Title case for sections and chapters
3. Space before punctuation
4. No space after punctuation
5. Missing capitalization of first word after full stop
6. Tilde mark needed before \cite / \ref
7. Capitalize c in chapter and s in section for references
8. Too many spaces
9. Sentence case for subsections and below

Plugin is smart enough to avoid certain tags, environments, etc.

TODO
----

Being a very early stage there are several problems to fix. Besides
the need to check all regexes for special situations that I haven't
thought of:

1. Exit cleanly from typoCheck in the middle of a check. (Hold escape
key down for now)



