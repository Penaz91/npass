#!/usr/bin/env python3
import curses
import functions
import os
from subprocess import Popen
s=""
pos=0
l=functions.ListDirs()
screen=curses.initscr()
screen.border()
curses.noecho()
curses.cbreak()
screen.keypad(1)
txtwin=curses.newwin(3,40,1,1)
txtwin.border()
dim=screen.getmaxyx()
passwin=curses.newpad(dim[0]-5,dim[1]-3)
os.chdir(os.environ["HOME"])
while True:
    global s
    global pos
    global l
    for n in range(len(l)):
        if n==pos:
            passwin.addstr(n,3,l[n],curses.A_REVERSE)
        else:
            passwin.addstr(n,3,l[n])
    if pos>=(dim[0]-5)/4:
        passwin.refresh(int(pos-(dim[0]-5)/4),1,5,1,dim[0]-5,dim[1]-3)
    else:
        passwin.refresh(0,1,5,1,dim[0]-5,dim[1]-3)
    txtwin.clear()
    c=screen.getch()
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
        #Su
        if pos==0:
            pos=len(l)-1
        else:
            pos-=1
    elif c==258:
        #giu
        if pos==len(l)-1:
            pos=0
        else:
            pos+=1
    elif c==10:
        #enter
        if len(l)==0:
            pass
        else:
            Popen(["pass",l[pos]])
            break
    else:
        pos=0
        s+=chr(c)
        txtwin.addstr(1,3,s)
        l=functions.Search(l,s)
    screen.clear()
    passwin.clear()
    txtwin.border()
    screen.border()
    screen.refresh()
    txtwin.refresh()
    passwin.border()
    passwin.refresh(pos,1,5,1,dim[0]-5,dim[1]-3)
#Chiusura del programma
curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
quit()
