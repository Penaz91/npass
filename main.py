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
import sys
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
l=functions.ListDirs()
ignore_keys=set.union({f for f in range(265,277)},{262,260,261,ord("\t")})
stack=[]
copy=False
#--------------------
# Argument detection
#--------------------
if len(sys.argv)>1:
    if sys.argv[1] in {"-c","--clip"}:
        copy=True
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
txtwin=curses.newwin(3,dim[1]-3,dim[0]-3,1)
txtwin.border()
passwin=curses.newpad(len(l)+2,dim[1]-3)
scroll=dim[0]-5<len(l)+2
#--------------------
# Curses Loop
#--------------------
while True:
    screen.addstr(2,int((dim[1]-5)/2),"nPass",curses.A_BOLD)
    k=sorted(list(l))
    for n in range(len(l)):
        if n==pos:
            passwin.addstr(n,3,k[n],curses.A_REVERSE)
        else:
            passwin.addstr(n,3,k[n])
    #--------------------
    # Screen Refresh
    #--------------------
    txtwin.border()
    txtwin.addstr(1,3,">>>  ")
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
    txtwin.clear()
    passwin.clear()
    if c==27:
        #----------------------------------------
        # Escape: Terminate
        #----------------------------------------
        break
    elif c==127:
        #----------------------------------------
        # Backspace: pop old content from stack
        #----------------------------------------
        pos=0
        s=s[:-1]
        l=set.union(l,stack.pop())
        txtwin.addstr(1,3,">>>  "+s)
    elif c==259:
        #----------------------------------------
        # Up Arrow: Go up in the menu
        #----------------------------------------
        if pos==0:
            pos=len(l)-1
        else:
            pos-=1
    elif c==258:
        #----------------------------------------
        # Down Arrow
        #----------------------------------------
        if pos==len(l)-1:
            pos=0
        else:
            pos+=1
    elif c==10:
        #----------------------------------------
        # Enter/Return: display/copy password
        #----------------------------------------
        if len(l)==0:
            pass
        else:
            k=sorted(list(l))
            if copy:
                Popen(["pass","-c",k[pos]])
            else:
                Popen(["pass",k[pos]])
            break
    elif c in ignore_keys:
        #Ignore some keys
        pass
    else:
        #----------------------------------------
        # Letters/Numbers: perform search
        #----------------------------------------
        pos=0
        s+=chr(c)
        txtwin.addstr(1,3,">>>  "+s)
        oldl=l
        l=functions.Search(l,s)
        stack.append(oldl-l)
        del oldl
#--------------------------------------------------
#Program Termination & Cleanup
#--------------------------------------------------
curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
quit()
