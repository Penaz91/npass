"""
Npass: Yet Another NCurses UI for Pass
"View" State

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

from .state import State
import curses


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

    def executeAction(self):
        """
        Executes the Display Action
        """
        exit()
