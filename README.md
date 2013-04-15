CheckTypos
==========

Plugin to fix some standard mistakes and typos in plain text or
latex files. This plugin does not check for spelling mistakes.

Usage
-----

KeyMapping:
mac: ctrl + command + alt +x

Each error is highlighted on the screen and an input panel appears
at the bottom with a suggested replacement. This suggestion can
either be accepted or edited. Press enter to accept the inputted
string. Press esc to ignore this. The status bar indicates the check
is complete

Currently Checked Patterns
--------------------------

1. Repeated phrase
2. Title case for sections and chapters
3. Space before punctuation
4. No space after punctuation
5. Missing capitalization of first word after full stop
6. Tilde mark needed before cite / ref
7. Capitalize c in chapter
8. Too many spaces
9. Sentence case for subsections and below

TODO
----

Being a very early stage there are several problems to fix. Besides
the need to check all regexes for special situations that I haven't
thought of:

1. Exit cleanly from typoCheck in the middle of a check
2. Speed up

