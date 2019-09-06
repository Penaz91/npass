"""
Npass: Yet Another NCurses UI for Pass
Abstract State Structure

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):

    """
    Defines a generic structure for a State of Npass
    """

    def __init__(self, requires_list_update=False):
        """
        Initializes The State

        :requires_list_update: Defines if the state requires an update of
                               the password List
        :returns: TODO

        """
        self.requires_list_update = requires_list_update

    @abstractmethod
    def executeAction(self, **kwargs):
        """
        Executes the defined action for this state

        :returns: None

        """
        pass

    @abstractmethod
    def getStateMetadata(self):
        """
        Returns the string and color of the state, as well as some other
        useful data

        :returns: The metadata for the state

        """
        return None
