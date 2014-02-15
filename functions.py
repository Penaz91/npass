#!/usr/bin/env python3
import os
def Search(l,s):
    return [x for x in l if s.lower() in x.lower()]
def ListDirs():
    x=[os.path.join(dp,f) for dp, dn, fn in os.walk(os.path.expanduser("~/.password-store/")) for f in fn if ".gpg-id" not in f]
    y=[os.path.relpath(d,".password-store") for d in x]
    del x
    return y
def SetupEnv():
    os.chdir(os.environ["HOME"])
