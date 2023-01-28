"""
Npass: Yet Another NCurses UI for Pass
Main Program

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

import curses
from datetime import date
from functions import (
    getPasswordList, FuzzyFilter, loadfrecencylist, savefrecencylist
)
from states import ViewState, ClipState, EditState, DeleteState


class Npass(object):

    """
    The main component of Npass: takes care of rendering the screen, handling
    input and executing commands
    """

    def __init__(self, screen, mode):
        """
        Initializes the program

        :screen: The NCurses Screen
        :mode: The mode selected from command line arguments

        """
        self.screen = screen
        self.modeIndex = mode
        self.running = True
        self.stateList = [ViewState(), ClipState(), EditState(), DeleteState()]
        self.mode = self.stateList[self.modeIndex]
        self.cursorIndex = 0   # The index of the selected password in the pad
        self.searchString = ""  # The String searched by the user
        self.screeny, self.screenx = screen.getmaxyx()
        # Initialize Color pairs
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        # Initialize Windows and Pads
        self.textInputWindow = curses.newwin(
            3,  # Window Height
            self.screenx - 3,  # Window Width
            self.screeny - 3,  # Y Position
            1  # X Position
        )
        self.textInputWindow.border()
        # Load frecency list
        self.frecency = loadfrecencylist()
        self.passwordList = getPasswordList(self.frecency)
        self.filteredPasswordList = self.passwordList
        self.passWin = curses.newpad(
            len(self.filteredPasswordList)+2,  # Height of the pad
            self.screenx - 3  # Width of the pad
        )
        # In case the length of the password list is longer than the space
        # available or the pad, then scrolling will be needed
        self.needsScrolling = self.screeny - 10 \
            < len(self.filteredPasswordList) - 2
        # Initialize keys to ignore
        self.ignored_keys = set.union({f for f in range(265, 328)}, {262,
                                      ord("\t"), curses.KEY_IC,
                                      curses.KEY_RESIZE})

    def handleInput(self):
        """
        Handles The key Presses for The window

        :returns: None

        """
        c = self.screen.getch()
        if c in self.ignored_keys:
            return
        if c == 27:
            # ----------------------------------------
            # Escape: Terminate
            # ----------------------------------------
            self.running = False
        elif c == 260:
            # ----------------------------------------
            # Left arrow: Change mode left
            # ----------------------------------------
            self.modeIndex -= 1
            if self.modeIndex < 0:
                self.modeIndex = 3
            if isinstance(self.mode, DeleteState):
                self.mode.revertDeleteState()
        elif c == 261:
            # ----------------------------------------
            # Right arrow: Change mode Right
            # ----------------------------------------
            self.modeIndex += 1
            if self.modeIndex > 3:
                self.modeIndex = 0
            if isinstance(self.mode, DeleteState):
                self.mode.revertDeleteState()
        elif c in (127, curses.KEY_DC, curses.KEY_BACKSPACE):
            # ----------------------------------------
            # Backspace/Delete Char: pop old content from stack
            # ----------------------------------------
            self.searchString = self.searchString[:-1]
            if isinstance(self.mode, DeleteState):
                self.mode.revertDeleteState()
        elif c == 10:
            # ----------------------------------------
            # Enter/Return: <action> password
            # ----------------------------------------
            # Executes action and uses its return value to detect if npass
            # Should continue running
            self.running = self.mode.executeAction(
                pwid=self.filteredPasswordList[self.cursorIndex])
            if self.mode.requires_list_update:
                self.passwordList = getPasswordList()
                self.filteredPasswordList = FuzzyFilter(
                    self.passwordList,
                    self.searchString
                )
            oldfrec = self.frecency.get(self.filteredPasswordList[self.cursorIndex], [0, None])
            self.frecency[self.filteredPasswordList[self.cursorIndex]] = [oldfrec[0] - 1, date.today().isoformat()]

        elif c == 259 or c == curses.KEY_PPAGE:
            # ----------------------------------------
            # Up Arrow/PGUP: Go up in the menu
            # ----------------------------------------
            if self.cursorIndex == 0:
                self.cursorIndex = len(self.filteredPasswordList) - 1
            else:
                self.cursorIndex -= 1
            if isinstance(self.mode, DeleteState):
                self.mode.revertDeleteState()
        elif c == 258 or c == curses.KEY_NPAGE:
            # ----------------------------------------
            # Down Arrow: Go Down in the menu
            # ----------------------------------------
            if self.cursorIndex == len(self.filteredPasswordList) - 1:
                self.cursorIndex = 0
            else:
                self.cursorIndex += 1
            if isinstance(self.mode, DeleteState):
                self.mode.revertDeleteState()
        else:
            # ----------------------------------------
            # Letters/Numbers: perform search
            # ----------------------------------------
            self.searchString += chr(c)
            self.cursorIndex = 0
            if isinstance(self.mode, DeleteState):
                self.mode.revertDeleteState()

    def updateStatus(self):
        """
        Updates the program internal status

        :returns: None
        """
        # Refresh the state
        self.mode = self.stateList[self.modeIndex]
        # Check if window is resized
        resized = curses.is_term_resized(self.screeny, self.screenx)
        if resized:
            # Resize the main window
            self.screeny, self.screenx = self.screen.getmaxyx()
            self.screen.clear()
            curses.resizeterm(self.screeny, self.screenx)
            self.screen.refresh()
            # Resize and reposition the Windows and pads
            self.textInputWindow.resize(
                3,  # Window Height
                self.screenx - 3,  # Window Width
            )
            self.textInputWindow.mvwin(
                self.screeny - 3,  # New Y
                1  # New X
            )
            # Recalculate the need for scrolling
            self.needsScrolling = self.screeny - 10 \
                < len(self.filteredPasswordList) - 2
        # Recalculate the list
        self.filteredPasswordList = FuzzyFilter(self.frecency,
                                                self.passwordList,
                                                self.searchString)

    def drawWindow(self):
        """
        Draws the Ncurses Window

        :returns: None

        """
        # Clear Screen
        self.screen.clear()
        self.textInputWindow.clear()
        self.passWin.clear()
        # Add the nPass Title in the middle of the 2nd row
        self.screen.addstr(2, int((self.screenx-5)//2), "nPass", curses.A_BOLD)
        # Gets the current State and writes its defining information
        modeMetadata = self.mode.getStateMetadata()
        titleLen = len(modeMetadata["name"])
        self.screen.addstr(
            3,
            int((self.screenx - (titleLen + 6))//2),
            "<- {} ->".format(modeMetadata["name"]),
            modeMetadata["font"]
        )
        # Add the separator in line 4
        self.screen.hline(4, 1, curses.ACS_HLINE, self.screenx-2)
        # Add a border to the screen and windows
        self.screen.border()
        self.textInputWindow.border()
        # Fill the pad with the password list
        for n in range(len(self.filteredPasswordList)):
            if n == self.cursorIndex:
                self.passWin.addstr(
                    n, 3, self.filteredPasswordList[n], curses.A_REVERSE)
            else:
                self.passWin.addstr(n, 3, self.filteredPasswordList[n])
        # Write The search Prompt for the search window
        self.textInputWindow.addstr(
            1,
            3,
            "Search >>> {}".format(self.searchString)
        )
        # Draw the screen
        self.screen.refresh()
        # If i passed 1/4th of the pad, with scrolling necessary,
        # start scrolling, so you can see the remaining passwords
        fourthOfPadHeight = (self.screeny - 5) // 4
        if self.cursorIndex >= fourthOfPadHeight and self.needsScrolling:
            self.passWin.refresh(
                self.cursorIndex - fourthOfPadHeight,  # First pad row to show
                1,  # First pad column to show
                5,  # First row of the window that has the pad
                1,  # First column of the window that has the pad
                self.screeny - 5,  # Last row of the window that has the pad
                self.screenx - 3,  # Last column of the window that has the pad
            )
        else:
            self.passWin.refresh(
                0,  # First pad row to show
                1,  # First pad column to show
                5,  # First row of the window that has the pad
                1,  # First column of the window that has the pad
                self.screeny - 5,  # Last row of the window that has the pad
                self.screenx - 3,  # Last column of the window that has the pad
            )
        self.textInputWindow.refresh()

    def run(self):
        """
        Runs the main ncurses loop

        :returns: None

        """
        self.drawWindow()  # Does the first paint
        while self.running:
            self.handleInput()
            self.updateStatus()
            self.drawWindow()
        savefrecencylist(self.frecency)
