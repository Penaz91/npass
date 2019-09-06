"""
Npass: Yet Another NCurses UI for Pass
"View" State

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

from .state import State
import curses
from subprocess import Popen, PIPE


class ViewState(State):

    """
    Defines Actions for a state that is used to view passwords
    """

    def __init__(self):
        """
        Initializes The State
        """
        State.__init__(self)
        self.name = "View"
        self.font = curses.A_BOLD

    def getStateMetadata(self):
        """
        Gets the State Metadata, like state name and identifying color

        :returns: The State Metadata

        """
        return {
            "name": self.name,
            "font": self.font
        }

    def executeAction(self, **kwargs):
        """
        Executes the Display Action

        :returns: A boolean defining if the program should keep running
        """
        # Exit Curses Mode, we're closing the program anyway
        curses.endwin()
        pwid = kwargs.get("pwid", None)
        if pwid:
            proc = Popen(["pass", pwid], stdout=PIPE, stderr=PIPE)
            stdout, stderr = proc.communicate()
            stdout = stdout.decode("UTF-8").strip("\n")
            stderr = stderr.decode("UTF-8").strip("\n")
            if stdout != "":
                print("Password for: " + pwid)
                print("----------<>----------")
                print(stdout)
                print("----------<>----------")
            if stderr != "":
                print(stderr)
        # Tell the rest of the software we're closing down
        return False
