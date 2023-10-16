from stdlib import *
from sys import argv
from datetime import datetime
from configparser import ConfigParser as config
from os import path

expanduser = path.expanduser

# function to get config
if not path.isfile(f"{expanduser('~')}/.config/jlog/jlog.conf"):
    raise FileNotFoundError(f"Config {expanduser('~')}/.config/jlog/jlog.conf not found")
else:
    printinfo(f"Using config file {expanduser('~')}/.config/jlog/jlog.conf")
config = config()
config.read(f"{expanduser('~')}/.config/jlog/jlog.conf")
log_file = config.get('global', 'file').replace('~', expanduser('~'))
if not path.isfile(log_file):
    printerror(f"Log file {log_file} not found")
    printwarning(f"Creating new log file {log_file}")
    open(log_file, 'x').close()

else:
    printinfo(f"Using log file {log_file}")

if '-sk' not in argv:
    try:
        if askinput("continue? (y/n)").lower() != 'y':
            printwarning("Reseting...")
            from os import execv
            from sys import executable
            execv(executable, ['python3'] + argv)
    except AttributeError:
        printwarning("Reseting...")
        from os import execv
        from sys import executable
        execv(executable, ['python3'] + argv)


def convert_PRIORITY(priority) -> str:
    try:
        priority = int(priority)
        if priority == 1:
            priority = "DEBUG"
        elif priority == 2:
            priority = "INFO"
        elif priority == 3:
            priority = "WARNING"
        elif priority == 4:
            priority = "ERROR"
        elif priority == 5:
            priority = "CRITICAL"
        elif priority == 6:
            priority = "FATAL"
    except ValueError:
        priority = priority.upper()
        if priority not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid priority")
    
    return priority


# main function(process)
def log_message(priority: int, message: str):
    priority = convert_PRIORITY(priority)
    current_date = datetime.now()
    return f"[{current_date.date()} {current_date.strftime('%A')} {current_date.hour:02d}:{current_date.minute:02d}] [{priority}]: {message}"

# main function(ui)
def main():
    global log
    priority = askinput("Priority of log messages: ")

    # check if priority is valid
    
    message = askinput("Message to log: ")

    log = log_message(priority, message)

if __name__ == "__main__" and not len(argv) in [3, 4]:
    main()
elif len(argv) in [3, 4]:
    global log
    log = log_message(argv[1], argv[2])


printinfo(f"Logging into file {log_file}")
open(log_file, 'a').write(log)