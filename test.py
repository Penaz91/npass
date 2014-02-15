#!/usr/bin/env python3
import unittest
import functions
#The search must work correctly
class SearchTest(unittest.TestCase):
    def test(self):
        x=["abc","abd","bdc","cdd"]
        y=functions.Search(x,"a")
        self.assertEqual(y,["abc","abd"])
#I have a password store, so the list directory function must provide a non-empty list without gpg-id
class ListTest(unittest.TestCase):
    def testempty(self):
        self.assertNotEqual(functions.ListDirs(),[])
    def testid(self):
        self.assertNotIn(".gpg-id",functions.ListDirs())
if __name__=="__main__":
    unittest.main()
