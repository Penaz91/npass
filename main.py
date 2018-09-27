#!/usr/bin/env python3
# --------------------------------------------------
# nPass
# A simple NCurses frontend for Pass
# By Penaz
# --------------------------------------------------
# --------------------
# Imports
# --------------------
import curses
import functions
from os import chdir, environ, remove
from os.path import join, expanduser
# from sys import argv
from subprocess import Popen, PIPE
import argparse

# --------------------
# Environment Setup
# --------------------
chdir(environ["HOME"])
stdout, stderr = b"", b""
status = 0
mode = 0      # 0=Open - 1=Copy to clipboard - 2=Edit - 3=Delete


def main(screen):
    # --------------------
    # Vars
    # --------------------
    running = True
    s = ""
    pos = 0
    dirlist = functions.ListDirs()
    l = dirlist
    ignore_keys = set.union({f for f in range(265, 328)}, {262, 260,
                            261, ord("\t"), curses.KEY_IC})
    global mode
    global stdout
    global stderr
    global aboutToDelete
    aboutToDelete = False
    # --------------------
    # Curses Windows
    # --------------------
    dim = screen.getmaxyx()
    txtwin = curses.newwin(3, dim[1]-3, dim[0]-3, 1)
    txtwin.border()
    passwin = curses.newpad(len(l)+2, dim[1]-3)
    scroll = dim[0]-10 < len(l)+2
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    # --------------------
    # Curses Loop
    # --------------------
    while running:
        screen.addstr(2, int((dim[1]-5)/2), "nPass", curses.A_BOLD)
        if mode == 0:
            screen.addstr(3, int((dim[1]-13)/2), "<- Display ->",
                          curses.A_BOLD)
        elif mode == 1:
            screen.addstr(3, int((dim[1]-10)/2), "<- Copy ->", curses.A_BOLD)
        elif mode == 2:
            screen.addstr(3, int((dim[1]-10)/2), "<- Edit ->", curses.A_BOLD)
        elif mode == 3:
            if aboutToDelete:
                screen.addstr(3, int((dim[1]-56)/2),
                              "<- Press ENTER again to delete, any other key to Abort ->",
                              curses.color_pair(2))
            else:
                screen.addstr(3, int((dim[1]-20)/2), "<- !!! Delete !!! ->",
                              curses.color_pair(1))
        screen.hline(4, 1, curses.ACS_HLINE, dim[1]-2)
        k = sorted(list(l))
        for n in range(len(l)):
            if n == pos:
                if aboutToDelete:
                    passwin.addstr(n, 3, functions.ShortenPath(k[n], dim[1]),
                                   curses.color_pair(2))
                else:
                    passwin.addstr(n, 3, functions.ShortenPath(k[n], dim[1]),
                                   curses.A_REVERSE)
            else:
                passwin.addstr(n, 3, functions.ShortenPath(k[n], dim[1]))
        # --------------------
        # Screen Refresh
        # --------------------
        txtwin.border()
        txtwin.addstr(1, 3, "Search >>> ")
        screen.border()
        screen.refresh()
        txtwin.refresh()
        if pos >= (dim[0]-5)/4 and scroll:
            passwin.refresh(int(pos-(dim[0]-5)/4), 1, 5, 1, dim[0]-5, dim[1]-3)
        else:
            passwin.refresh(0, 1, 5, 1, dim[0]-5, dim[1]-3)
        # --------------------
        # Capture KeyPresses
        # --------------------
        c = screen.getch()
        screen.clear()
        txtwin.clear()
        passwin.clear()
        if c == 27:
            # ----------------------------------------
            # Escape: Terminate
            # ----------------------------------------
            running = False
        elif c == 127 or c == curses.KEY_DC:
            # ----------------------------------------
            # Backspace/Delete Char: pop old content from stack
            # ----------------------------------------
            pos = 0
            s = s[:-1]
            txtwin.addstr(1, 3, "Search >>>  "+s)
            if aboutToDelete:
                aboutToDelete = False
            l = functions.Search(dirlist, s)
        elif c == 259 or c == curses.KEY_PPAGE:
            # ----------------------------------------
            # Up Arrow/PGUP: Go up in the menu
            # ----------------------------------------
            if pos == 0:
                pos = len(l)-1
            else:
                pos -= 1
            if aboutToDelete:
                aboutToDelete = False
        elif c == 258 or c == curses.KEY_NPAGE:
            # ----------------------------------------
            # Down Arrow: Go Down in the menu
            # ----------------------------------------
            if pos == len(l)-1:
                pos = 0
            else:
                pos += 1
            if aboutToDelete:
                aboutToDelete = False
        elif c == 10:
            # ----------------------------------------
            # Enter/Return: <action> password
            # ----------------------------------------
            if len(l) == 0:
                pass
            else:
                k = sorted(list(l))
                proc = None
                if mode == 0:
                    proc = Popen(["pass", k[pos]], stdout=PIPE, stderr=PIPE)
                    stdout, stderr = proc.communicate()
                    running = False
                if mode == 1:
                    proc = Popen(["pass", "-c", k[pos]],
                                 stdout=PIPE, stderr=PIPE)
                    if proc.returncode == 0:
                        quit()
                    running = False
                elif mode == 2:
                    proc = Popen(["pass", "edit", k[pos]]).wait()
                    running = False
                elif mode == 3:
                    if not aboutToDelete:
                        aboutToDelete = True
                    else:
                        remove(join(expanduser("~/.password-store"),
                                    k[pos])+".gpg")
                        running = False
        elif c == 260:
            # ----------------------------------------
            # Left arrow: Change mode left
            # ----------------------------------------
            mode -= 1
            if mode < 0:
                mode = 3
            if aboutToDelete:
                aboutToDelete = False
        elif c == 261:
            # ----------------------------------------
            # Right arrow: Change mode Right
            # ----------------------------------------
            mode += 1
            if mode > 3:
                mode = 0
            if aboutToDelete:
                aboutToDelete = False
            # ----------------------------------------
            # Ignore some Keys
            # ----------------------------------------
        elif c in ignore_keys:
            txtwin.addstr(1, 3, "Search >>>  "+s)
        else:
            # ----------------------------------------
            # Letters/Numbers: perform search
            # ----------------------------------------
            pos = 0
            s += chr(c)
            txtwin.addstr(1, 3, "Search >>>  "+s)
            l = functions.Search(dirlist, s)
            if aboutToDelete:
                aboutToDelete = False


if __name__ == "__main__":
    # --------------------
    # Argument detection
    # --------------------
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--clip", "--copy",
                       help="Open npass in copy mode", action="store_const",
                       dest="mode", const=1, default=0)
    group.add_argument("-e", "--edit", help="Open npass in edit mode",
                       action="store_const", dest="mode", const=2,
                       default=0)
    group.add_argument("-d", "--delete", help="Open npass in delete mode",
                       action="store_const", dest="mode", const=3,
                       default=0)
    args = parser.parse_args()
    mode = args.mode
    curses.wrapper(main)
    stdout = stdout.decode("UTF-8").strip("\n")
    stderr = stderr.decode("UTF-8").strip("\n")
    if stdout != "":
        print("----------<>----------")
        print(stdout)
        print("----------<>----------")
    if stderr != "":
        print("Errors detected:")
        print(stderr)
