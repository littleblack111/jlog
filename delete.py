#!/usr/bin/env python

from stdlib import *
from sys import argv
from datetime import datetime
from configparser import ConfigParser as config
from configparser import NoOptionError, NoSectionError
from os.path import expanduser, isfile


expanduser = expanduser

# function to get config
if not isfile(f"{expanduser('~')}/.config/jlog/jlog.conf"):
    raise FileNotFoundError(f"Config {expanduser('~')}/.config/jlog/jlog.conf not found")
else:
    printinfo(f"Using config file {expanduser('~')}/.config/jlog/jlog.conf")
config = config()
config.read(f"{expanduser('~')}/.config/jlog/jlog.conf")
try:
    log_file = config.get('global', 'file').replace('~', expanduser('~'))
except NoSectionError:
    raise NoSectionError(f"Section global not found in {expanduser('~')}/.config/jlog/jlog.conf")
except NoOptionError:
    log_file = f"{expanduser('~')}/.config/jlog/jlog_{datetime.now()}"
if not isfile(log_file):
    printerror(f"Log file {log_file} not found")
    printwarning(f"Creating new log file {log_file}")
    open(log_file, 'x').close()
try:
    skip_ask = config.get('global','skip_ask')
    try:
        skip_ask = bool(skip_ask)
    except ValueError:
        raise ValueError("Invalid skip asking option")
except NoSectionError:
    raise NoSectionError(f"Section global not found in {expanduser('~')}/.config/jlog/jlog.conf")
except NoOptionError:
    printerror(f"Option skip_ask not found in {expanduser('~')}/.config/jlog/jlog.conf")
    skip_ask = False
try:
    ddate = config.get('global', 'detailed_date')
    try:
        ddate = bool(ddate)
    except ValueError:
        raise ValueError("Invalid detailed_date")
except NoSectionError:
    raise NoSectionError(f"Section global not found in {expanduser('~')}/.config/jlog/jlog.conf")
except NoOptionError:
    ddate = False

else:
    printinfo(f"Using log file {log_file}")

if '-sk' in argv:
    skip_ask = True
elif '-dd' in argv:
    ddate = True

if not skip_ask:
    try:
        if askinput("continue? (y/n)").lower() != 'y':
            printwarning("Reseting...")
            
    except AttributeError:
        printwarning("Reseting...")
        from os import execv
        from sys import executable
        execv(executable, [executable] + argv)

def remove_line(line: int):
    
    


# main function(process)
def log_message(priority: int, message: str):
    priority = convert_PRIORITY(priority)
    current_date = datetime.now()
    if not ddate:
        return f"[{current_date.date()} {current_date.strftime('%A')} {current_date.hour:02d}:{current_date.minute:02d}] [{priority}]: {message}"
    elif ddate:
        return f"[{current_date}] [{priority}]: {message}"


# main function(ui)
def main():
    global log
    priority = askinput("Priority of log messages: ")

    # check if priority is valid
    message = askinput("Message to log: ")

    log = log_message(priority, message)

if __name__ == "__main__" and not len(argv) in [2, 3, 4]:
    main()
elif len(argv) in [2, 3, 4]:
    global log
    log = log_message(argv[1], argv[2])
else:
    exit(1)

printinfo(f"Logging into file {log_file}")
open(log_file, 'a').write(log + '\n')

# to delete last line:
open(log_file, 'w').writelines(open(log_file, 'r').readlines()[-1])