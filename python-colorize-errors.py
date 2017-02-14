#!/usr/bin/env python

import sys
import re


GRAY         = '\033[1;30m'
DARK_RED     = '\033[0;31m'
RED          = '\033[1;31m'
DARK_GREEN   = '\033[0;32m'
GREEN        = '\033[1;32m'
DARK_YELLOW  = '\033[0;33m'
YELLOW       = '\033[1;33m'
DARK_BLUE    = '\033[0;34m'
BLUE         = '\033[1;34m'
DARK_MAGENTA = '\033[0;35m'
MAGENTA      = '\033[1;35m'
DARK_CYAN    = '\033[0;36m'
CYAN         = '\033[1;36m'
DARK_WHITE   = '\033[0;37m'
WHITE        = '\033[1;37m'
RESET        = '\033[0m'


class Colorizer(object):
    def __init__(self):
        pass

    def run(self, file_in=None, file_out=None):
        if file_in is None:
            file_in = sys.stdin
        if file_out is None:
            file_out = sys.stdout

        re_stack_frame_header = re.compile(
            r'^  File (?P<filename>".*"), line (?P<linenum>[0-9]+), in (?P<func>.*)')

        error_mode = False

        while True:
            line = file_in.readline()
            if len(line) == 0:
                break


            if error_mode:
                m = re_stack_frame_header.match(line)
                if m is not None:
                    line = '  File {}, line {}, in {}\n'.format(
                        GREEN + m.group('filename') + RESET,
                        YELLOW + m.group('linenum') + RESET,
                        CYAN + m.group('func') + RESET,
                    )
                elif line.startswith('    '):
                    line = DARK_WHITE + line + RESET

                else:
                    line = BLUE + line + RESET
                    error_mode = False

            else:
                if line == 'Traceback (most recent call last):\n':
                    line = RED + line + RESET
                    error_mode = True


            file_out.write(line)
            file_out.flush()


def main(args):
    colorizer = Colorizer()
    colorizer.run(sys.stdin, sys.stdout)


if __name__ == '__main__':
    main(sys.argv[1:])
