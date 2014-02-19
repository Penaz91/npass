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
    x={join(dp,f) for dp, dn, fn in walk(expanduser("~/.password-store/")) for f in fn if ".gpg-id" not in f}
    y={relpath(d,".password-store") for d in x}
    x={splitext(l)[0] for l in y}
    del y
    return x
