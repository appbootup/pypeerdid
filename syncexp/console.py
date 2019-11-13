import os
import sys
import textwrap
import threading

try:
    cols = max(os.get_terminal_size()[0] - 1, 40)
except:
    cols = 79


def wrap(str, width=0):
    if width == 0: width = cols
    paragraphs = [x.rstrip() for x in str.split('\n\n')]
    wrapped = ['\n'.join(textwrap.wrap(p.replace('\n', ' '), cols)) for p in paragraphs]
    return '\n\n'.join(wrapped)


class Console:
    def __init__(self):
        self.lock = threading.Lock()
        self.prompting = False

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.lock.release()

    def prompt(self):
        with self:
            sys.stdout.write('> ')
            self.prompting = True

    def say(self, msg):
        with self:
            if self.prompting:
                sys.stdout.write('\n')
                self.prompting = False
            sys.stdout.write(wrap(msg))
            sys.stdout.write('\n')
