"""
Npass: Yet Another NCurses UI for Pass
"Delete" State

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

from .state import State
from os.path import expanduser, join
from os import remove
import curses


class DeleteState(State):

    """
    Defines Actions for a state that is used to Delete passwords
    """

    def __init__(self):
        """
        Initializes The State
        """
        State.__init__(self, True)
        self.name = "Delete"
        self.font = curses.color_pair(1)
        self.aboutToDelete = False

    def getStateMetadata(self):
        """
        Gets the State Metadata, like state name and identifying color

        :returns: The State Metadata

        """
        return {
            "name": self.name,
            "font": self.font
        }

    def revertDeleteState(self):
        """
        Reverts the aboutToDelete State to false
        """
        self.aboutToDelete = False
        self.font = curses.color_pair(1)

    def executeAction(self, **kwargs):
        """
        Executes the Display Action
        """
        pwid = kwargs.get("pwid", None)
        passpath = kwargs.get("passpath", "~/.password-store/")
        if not self.aboutToDelete:
            self.aboutToDelete = True
            self.font = curses.color_pair(2)
        else:
            if pwid:
                remove(join(expanduser(passpath),
                            pwid)+".gpg")
        return True
