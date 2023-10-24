#!/usr/bin/env python

from stdlib import *
from datetime import datetime
from configparser import ConfigParser as config
from configparser import NoOptionError, NoSectionError
from os import path


expanduser = path.expanduser

# function to get config
if not path.isfile(f"{expanduser('~')}/.config/jlog/jlog.conf"):
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
if not path.isfile(log_file):
    printerror(f"Log file {log_file} not found")
    raise FileNotFoundError(f"Log file {log_file} not found")
else:
    printinfo(f"Using log file {log_file}")

def colorize(log: str) -> str:
    lines = log.splitlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('DEBUG', f"{ascii.color.lcyan}DEBUG{ascii.color.reset}")
        lines[i] = lines[i].replace('INFO', f"{ascii.color.green}INFO{ascii.color.reset}")
        lines[i] = lines[i].replace('WARNING', f"{ascii.color.yellow}WARNING{ascii.color.reset}")
        lines[i] = lines[i].replace('ERROR', f"{ascii.color.lred}ERROR{ascii.color.reset}")
        lines[i] = lines[i].replace('CRITICAL', f"{ascii.color.red}CRITICAL{ascii.color.reset}")
        lines[i] = lines[i].replace('FATAL', f"{ascii.color.red}FATAL{ascii.color.reset}")

    return '\n'.join(lines)



# main function(process)
def get_log() -> str:
    return open(log_file, 'r').read()


# main function(ui)
def main() -> None:
    global log

    log = get_log()

    log = colorize(log)

if __name__ == "__main__":
    main()

aprintf(log, interval=0.001)