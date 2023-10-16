from stdlib import *
from sys import argv
from datetime import datetime

def convert_PRIORITY(priority) -> str:
    try:
        priority = int(priority[1])
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
        if priority not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid argument")
    
    return priority


# main function(process)
def log_message(priority: int, message: str):
    priority = convert_PRIORITY(priority)
    current_date = datetime.now()
    return f"[{current_date.date()} {current_date.strftime('%A')} {current_date.hour:02d}:{current_date.minute:02d}] [{priority}]: {message}"

# main function(ui)
def main():
    priority = ainputf("Priority of log messages: ")

    # check if priority is valid
    
    message = ainputf("Message to log: ")

    aprintf(log_message(priority, message))

if __name__ == "__main__" and not len(argv) == 3:
    main()
elif len(argv) == 3:
    print(log_message(argv[1], argv[2]))