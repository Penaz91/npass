#!/usr/bin/env python3
#-----------------------------
# UnitTest suite for npass
# Part of the Npass Project
# By Penaz.
#-----------------------------
import unittest
import functions
#-----------------------------
# Search must work correctly
#-----------------------------
class SearchTest(unittest.TestCase):
    def test(self):
        x=["abc","abd","bdc","cdd"]
        y=functions.Search(x,"a")
        self.assertEqual(y,{"abc","abd"})
#-----------------------------
# I have a password store, so the 
# function must provide a non-empty
# set without the .gpg-id file
#-----------------------------
class ListTest(unittest.TestCase):
    def testempty(self):
        self.assertNotEqual(functions.ListDirs(),[])
    def testid(self):
        self.assertNotIn(".gpg-id",functions.ListDirs())
if __name__=="__main__":
    unittest.main()
