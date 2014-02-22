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
from os import chdir, environ
from sys import argv
from subprocess import Popen
#--------------------
# Environment Setup
#--------------------
chdir(environ["HOME"])
#--------------------
# Vars
#--------------------
s=""
pos=0
l=functions.ListDirs()
ignore_keys=set.union({f for f in range(265,328)},{262,260,261,ord("\t"),curses.KEY_IC})
stack=[]
copy=False
#--------------------
# Argument detection
#--------------------
if len(argv)>1:
    if argv[1] in {"-c","--clip"}:
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
scroll=dim[0]-10<len(l)+2
#--------------------
# Termination handler
#--------------------
def term():
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    quit()
#--------------------
# Curses Loop
#--------------------
while True:
    screen.addstr(2,int((dim[1]-5)/2),"nPass",curses.A_BOLD)
    if copy:
        screen.addstr(3,int((dim[1]-15)/2),"-- Copy Mode --",curses.A_BOLD)
    else:
        screen.addstr(3,int((dim[1]-18)/2),"-- Display Mode --",curses.A_BOLD)
    screen.hline(4,1,curses.ACS_HLINE,dim[1]-2)
    k=sorted(list(l))
    for n in range(len(l)):
        if n==pos:
            passwin.addstr(n,3,functions.ShortenPath(k[n],dim[1]),curses.A_REVERSE)
        else:
            passwin.addstr(n,3,functions.ShortenPath(k[n],dim[1]))
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
    elif c==127 or c==curses.KEY_DC:
        #----------------------------------------
        # Backspace/Delete Char: pop old content from stack
        #----------------------------------------
        pos=0
        s=s[:-1]
        if len(stack)>0:
           l=set.union(l,stack.pop())
        txtwin.addstr(1,3,">>>  "+s)
    elif c==259 or c==curses.KEY_PPAGE:
        #----------------------------------------
        # Up Arrow/PGUP: Go up in the menu
        #----------------------------------------
        if pos==0:
            pos=len(l)-1
        else:
            pos-=1
    elif c==258 or c==curses.KEY_NPAGE:
        #----------------------------------------
        # Down Arrow: Go Down in the menu
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
        #----------------------------------------
        # Ignore some Keys
        #----------------------------------------
    elif c in ignore_keys:
        txtwin.addstr(1,3,">>>  "+s)
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
term()
