#!/usr/bin/env python

from sys import argv
from os.path import islink, dirname, abspath
from stdlib import runutil

if islink(__file__):
    from os import readlink
    file = readlink(__file__)
else:
    file = __file__
cwd = dirname(abspath(file))

def write():
    runutil("write.py")
def read():
    runutil("read.py")
if len(argv) > 1:
    if argv[1] == 'write':
        write()
    elif argv[1] =='read':
        read()
    else:
        raise Exception("Unknown command\n\tAvailable commands: write, read")
else:
    from simple_term_menu import TerminalMenu
    choice = TerminalMenu(['Write', 'Read']).show()
    if choice == 0:
        write()
    elif choice == 1:
        read()
