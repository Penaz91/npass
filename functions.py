#!/usr/bin/env python3
#-----------------------------
# Functions.py
# Part of the npass project
# By Penaz
#-----------------------------

#-----------------------------
# Imports
#-----------------------------
from os.path import join, relpath, splitext, expanduser
from os import walk
#-----------------------------
# Filter the set "l"
#-----------------------------
def Search(l,s):
    return {x for x in l if s.lower() in x.lower()}
#-----------------------------
# List all passwords
#-----------------------------
def ListDirs():
    exclude = set([".gpg-id", ".git"])
    x={join(dp,f) for dp, dn, fn in walk(expanduser("~/.password-store/")) for f in fn}
    toexclude=set([])
    for exclusion in exclude:
        toexclude = set([item for item in x if exclusion in item])
        x=x.difference(toexclude)
    y={relpath(d,".password-store") for d in x}
    x={splitext(l)[0] for l in y}
    del y
    return x
#-----------------------------
# Display condensed paths if necessary
#-----------------------------
def ShortenPath(string,rowl):
    if len(string)>rowl-5:
        #Shorten the string
        l=string.split("/")
        return join(join(l[0],*[".." for i in range(len(l)-2)]),l[len(l)-1])
    else:
        #Return the same string
        return string
