#!/usr/bin/env python3
#--------------------------------------------------
# nPass
# A simple NCurses frontend for Pass
# By Penaz
#--------------------------------------------------
#--------------------
# Imports
#--------------------
import curses
import functions
import os
from subprocess import Popen
#--------------------
# Environment Setup
#--------------------
os.chdir(os.environ["HOME"])
#--------------------
# Vars
#--------------------
s=""
pos=0
#l=functions.ListDirs()
l=[str(f) for f in range(0,51)]
#--------------------
# Curses Init
#--------------------
screen=curses.initscr()
screen.border()
curses.noecho()
curses.cbreak()
screen.keypad(1)
#--------------------
# Curses Windows
#--------------------
dim=screen.getmaxyx()
txtwin=curses.newwin(3,40,1,1)
txtwin.border()
passwin=curses.newpad(len(l)+2,dim[1]-3)
scroll=dim[0]-5<len(l)+2
#--------------------
# Curses Loop
#--------------------
while True:
    for n in range(len(l)):
        if n==pos:
            passwin.addstr(n,3,l[n],curses.A_REVERSE)
        else:
            passwin.addstr(n,3,l[n])
    #--------------------
    # Screen Refresh
    #--------------------
    txtwin.border()
    screen.border()
    screen.refresh()
    txtwin.refresh()
    if pos>=(dim[0]-5)/4 and scroll:
        passwin.refresh(int(pos-(dim[0]-5)/4),1,5,1,dim[0]-5,dim[1]-3)
    else:
        passwin.refresh(0,1,5,1,dim[0]-5,dim[1]-3)
    #--------------------
    # Capture KeyPresses
    #--------------------
    c=screen.getch()
    screen.clear()
    passwin.clear()
    if c==27:
        #escape
        break
    elif c==127:
        #backspace
        pos=0
        s=s[:-1]
        l=functions.Search(functions.ListDirs(),s)
        txtwin.addstr(1,3,s)
    elif c==259:
        #Up Arrow
        if pos==0:
            pos=len(l)-1
        else:
            pos-=1
    elif c==258:
        #Down Arrow
        if pos==len(l)-1:
            pos=0
        else:
            pos+=1
    elif c==10:
        #Enter/Return
        if len(l)==0:
            pass
        else:
            Popen(["pass",l[pos]])
            break
    else:
        #Letters/Numbers
        pos=0
        s+=chr(c)
        txtwin.addstr(1,3,s)
        l=functions.Search(l,s)
#--------------------------------------------------
#Program End & Cleanup
#--------------------------------------------------
curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
quit()
