#!/usr/bin/env python

from sys import argv, executable
from os import execv
if len(argv) > 1:
    if argv[1] == 'write':
        print(' '.join(argv[2:]))
        execv(executable, ['python3', 'write.py'] + argv[2:])
    elif argv[1] =='read':
        execv(executable, ['python3','read.py'])
    else:
        raise Exception("Unknown command\n\tAvailable commands: write, read")
else:
    from simple_term_menu import TerminalMenu
    choice = TerminalMenu(['Write', 'Read']).show()
    if choice == 0:
        execv(executable, ['python3', 'write.py'])
    elif choice == 1:
        execv(executable, ['python3','read.py'])