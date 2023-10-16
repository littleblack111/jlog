#!/dev/null

# imports
from rich.console import Console as console
from rich.syntax import Syntax as syntax
from rich import print as rprint
from argparse import ArgumentParser as arg


# text ascii codes
class ascii:
    ### ASCII
    #\33[0m   # remove all attribute
    bright = "\33[1m"   # control brightness
    itectic = "\33[4m"  # underline
    bold = "\033[1m"  # bold
    blink = "\33[5m"   # blink
    reverse = "\33[7m"   # reverse
    disappear = "\33[8m"   # disappear
    #\33[30m -- \33[37m   # foreground
    #\33[40m -- \33[47m   # background
    clear = "\33[2J"   # clear screen
    def cursor(self, func, n=0, x=0, y=0):
            if func == 'upper':
                return f"\33[{n}A"   # upper cursor n line
            elif func == 'lower':
                return f"\33[{n}B"   # lower cursor n line
            elif func == 'righter':
                return f"\33[{n}C"   # righter cursor n line
            elif func == 'lefter':
                return f"\33[{n}D"   # lefter cursor n line
            elif func == 'pos':
                return f"\33[{y};{x}H" # set cursor x/y
            elif func == 'clearline':
                return "\33[K"    # clear from cursor to end
            elif func == 'savpos':
                return "\33[s"    # save cursor pos
            elif func == 'recpos':
                return "\33[u"    # recover saved cursor pos
            elif func == 'hide':
                return "\33[?25l" # hide cursor
            elif func == 'show':
                return "\33[?25h" # show cursor

    class color:
        reset = "\33[0m"

        black = "\033[30m" # black
        red = "\033[31m" # red
        green = "\033[32m" # green
        yellow = "\033[33m" # yellow
        blue = "\033[34m" # blue
        purple = "\033[35m" # purple
        cyan = "\033[36m" # cyan
        gray = "\033[37m" # gray

        lblack = "\033[1;30m" # light-black
        lred = "\033[1;31m" # light-red
        lgreen = "\033[1;32m" # light-green
        lyellow = "\033[1;33m" # light-yellow
        lblue = "\033[1;34m" # light-blue
        lpurple = "\033[1;35m" # light-purple
        lcyan = "\033[1;36m" # light-cyan
        white = "\033[1;37m" # white

# convert iterable into string
def istr(value):
    return str(''.join(map(str, value)))

# convert color types

# convert RGB to hex
def rgb2hex(r: int, g: int, b: int) -> int:
    hex_value = f"{r:02x}{g:02x}{b:02x}"
    return hex_value

# convert RGB to ASCII
def rgb2ascii(r: int, g: int, b: int) -> int:
    ascii_value = (r + g + b) // 3
    return ascii_value

# convert hex to RGB
def hex2rgb(hex_value: int) -> list:
    r = int(hex_value[1:3], 16)
    g = int(hex_value[3:5], 16)
    b = int(hex_value[5:7], 16)
    return [r, g, b]

# convert hex to ASCII
def hex2ascii(hex_value: int) -> int:
    rgb_values = hex2rgb(hex_value)
    ascii_value = rgb2ascii(*rgb_values)
    return ascii_value

# convert ASCII to hex
def ascii2hex(ascii_value: int) -> int:
    hex_value = hex(ascii_value)[2:]
    if len(hex_value) % 2 != 0:
        hex_value = "0" + hex_value
    return hex_value

# convert ASCII to RGB
def ascii2rgb(ascii_value: int) -> list:
    hex_value = ascii2hex(ascii_value)
    rgb_values = hex2rgb(hex_value)
    return rgb_values

# print but formatly without newline and will flush stream
def printf(*value: str):
    print(str(istr(value)), end='', flush=True)

# mixly(shuffle) join a list to another
def shufflejoin(str1: str, str2: str, *others):
    from random import shuffle
    tmpstr = str1 + str2
    if others:
        for o in others:
            tmpstr += o

    tmpstrlst = list(tmpstr)
    shuffle(tmpstrlst)
    return ''.join(tmpstrlst)

# limit string to how much charactor it can use, and delete other then that
def limitstring(string: str, limit: int):
    if len(string) > limit:
        return string[0:limit]
    else:
        return string

# animated print
def aprintf(*value: str, end=None):
    from time import sleep
    waitime = 0.01
    value = istr(list(value))
    ani=True
    if len(value) >= 8*32:
        ani = ainputf("Print string is bigger, fast animation(Y/n): ")
        if ani.lower() == 'y':
            ani=False
    for i in value:
        printf(i)
        if ani:
            sleep(waitime)
    if end == None:
        printf('\n')
    else:
        printf(end)

# print with info([*]) or selected([+]) and green color
def printinfo(str: str, outputter=aprintf, ccolor=ascii.color.green, selection=False, end=None):
    if selection:
        outputter(f"{ccolor}[+] {str}{ascii.color.reset}", end=end)
    else:
        outputter(f"{ccolor}[*] {str}{ascii.color.reset}", end=end)

# print with warning([!]) and yellow color
def printwarning(str: str, outputter=aprintf, ccolor=ascii.color.yellow, end=None):
    outputter(f"{ccolor}[!] {str}{ascii.color.reset}", end=end)

# print with error(#) and red color
def printerror(str: str, outputter=aprintf, ccolor=ascii.color.red, end=None):
    outputter(f"{ccolor}[#] {str}{ascii.color.reset}", end=end)

def ainputf(str: str, end='', ccolor=ascii.color.purple):
    aprintf(str, end=end)
    return input()

def askinput(str: str, inputter=ainputf, ccolor=ascii.color.blue):
    return inputter(f"{ccolor}[?] {str}{ascii.color.reset}")

# animated countdown from @timeoutsec
def countdown(timeoutsec: int):
    from time import sleep
    timeoutsec = timeoutsec
    for _ in range(timeoutsec-1):
        printf(timeoutsec)
        for _ in range(3):
            printf('.')
            sleep(0.8/3)
        timeoutsec -= 1
        sleep(0.2)
    print(1)

# animated loading with @msg
def aloading(msg="Loading...", stop=False):
    from itertools import cycle
    from time import sleep
    for c in cycle(['|', '/', '-', '\\']):
        if stop:
            break
        printf(f"\r[{c}] {msg}")
        sleep(0.1)

# automated execute @func in background with @arg
def bgexec(func, arg=False, stop=False):
    from threading import Thread
    if stop:
        try:
            t.join()
        except AttributeError:
            raise AttributeError("Thread is not started")
        except UnboundLocalError:
            raise UnboundLocalError("Thread is not started")
    else:
        if arg:
            t = Thread(target=func, args=arg).start()
        else:
            t = Thread(target=func).start()

# catch & handle signals
def sigcatch(sig, error=None, sysexit=False, handler=None):
    from signal import signal
    if handler != None:
        pass
    elif error == None:
        def handler(sig, stack):
            printerror(f"catched kill signal: {sig}")
            if sysexit:
                import sys.exit
                sys.exit(sig)
    elif error:
        def handler(sig, stack):
            printerror(error)
            if sysexit:
                sys.exit(sig)
    if sig == str:
        from signal import sig
        signal(signal.sig, handler)
    elif sig == int:
        signal(sig, handler)
    else:
        raise TypeError("Please input @sig as a int(signal number, like 15) or str(signal name, like SIGTERM")


# self test
if __name__ == '__main__':
    from stdlib import *
