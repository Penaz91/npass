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
from subprocess import call
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
mode=0      #0=Open - 1=Copy to clipboard - 2=Edit - 3=Delete
#--------------------
# Argument detection
#--------------------
if len(argv)>1:
    if argv[1] in {"-c","--clip"}:
        mode=1
    if argv[1] in {"-e","--edit"}:
        mode=2
    if argv[1] in {"-d","--delete"}:
        mode=3
    if argv[1] in {"-h","--help"}:
        print("Npass - A simple ncurses frontend for Pass")
        print("Usage:")
        print("npass  -  Show password list")
        print("npass [-c,--clip]  -  Open npass in copy mode")
        print("npass [-e,--edit]  -  Open npass in edit mode")
        print("npass [-d,--delete]  -  Open npass in delete mode")
        print("npass [-h,--help]  -  Show this help page")
        quit()
if len(argv)>2:
    quit("Too many arguments\nTry with fewer arguments.")
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
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
#--------------------
# Termination handler
#--------------------
def term():
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
#--------------------
# Curses Loop
#--------------------
while True:
    screen.addstr(2,int((dim[1]-5)/2),"nPass",curses.A_BOLD)
    if mode==0:
        screen.addstr(3,int((dim[1]-13)/2),"<- Display ->",curses.A_BOLD)
    elif mode==1:
        screen.addstr(3,int((dim[1]-10)/2),"<- Copy ->",curses.A_BOLD)
    elif mode==2:
        screen.addstr(3,int((dim[1]-10)/2),"<- Edit ->",curses.A_BOLD)
    elif mode==3:
        screen.addstr(3,int((dim[1]-18)/2),"<- !!! Delete !!! ->",curses.color_pair(1))
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
        # Enter/Return: <action> password
        #----------------------------------------
        #TODO: Nuove azioni per il tasto enter a seconda del modo
        if len(l)==0:
            pass
        else:
            k=sorted(list(l))
            if mode==0:
                term()
                call(["pass",k[pos]])
            if mode==1:
                term()
                call(["pass","-c",k[pos]])
            elif mode==2:
                term()
                call(["pass","edit",k[pos]])
            elif mode==3:
                term()
                call(["pass","rm",k[pos]])
            break
    elif c==260:
        #----------------------------------------
        # Left arrow: Change mode left
        #----------------------------------------
        mode-=1
        if mode<0:
            mode=3
    elif c==261:
        #----------------------------------------
        # Right arrow: Change mode Right
        #----------------------------------------
        mode+=1
        if mode>3:
            mode=0
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
quit()
