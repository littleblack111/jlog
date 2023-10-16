from sys import argv, executable
from os import execv
if argv[1] == 'write':
    execv(executable, ['python3', 'write.py'])
elif argv[1] =='read':
    execv(executable, ['python3','read.py'])
else:
    raise Exception("Unknown command")