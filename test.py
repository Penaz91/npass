#!/usr/bin/env python3
import unittest
import functions
class SearchTest(unittest.TestCase):
    def test(self):
        x=["abc","abd","bdc","cdd"]
        y=functions.Search(x,"a")
        self.assertEqual(y,["abc","abd"])
if __name__=="__main__":
    unittest.main()
