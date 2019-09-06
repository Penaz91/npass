"""
Npass: Yet Another NCurses UI for Pass
"Clip/Copy" State

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

from .state import State
import curses
from subprocess import Popen, PIPE


class ClipState(State):

    """
    Defines Actions for a state that is used to copy passwords in clipboard
    """

    def __init__(self):
        """
        Initializes The State
        """
        State.__init__(self)
        self.name = "Copy"
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
        """
        curses.endwin()
        pwid = kwargs.get("pwid", None)
        if pwid:
            proc = Popen(["pass", "-c", pwid],
                         stdout=PIPE, stderr=PIPE)
            # If we don't quit, the program will be left hanging until the
            # memory gets cleaned
            if proc.returncode == 0:
                quit()
        return False
