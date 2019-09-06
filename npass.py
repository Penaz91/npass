"""
Npass: Yet Another NCurses UI for Pass
Main Program

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

import curses
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

    def handleInput(self):
        """
        Handles The key Presses for The window

        :returns: None

        """
        c = self.screen.getch()
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
        elif c == 261:
            # ----------------------------------------
            # Right arrow: Change mode Right
            # ----------------------------------------
            self.modeIndex += 1
            if self.modeIndex > 3:
                self.modeIndex = 0
        elif c == 127 or c == curses.KEY_DC:
            # ----------------------------------------
            # Backspace/Delete Char: pop old content from stack
            # ----------------------------------------
            self.searchString = self.searchString[:-1]
        else:
            # ----------------------------------------
            # Letters/Numbers: perform search
            # ----------------------------------------
            self.searchString += chr(c)

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

    def drawWindow(self):
        """
        Draws the Ncurses Window

        :returns: None

        """
        # Clear Screen
        self.screen.clear()
        self.textInputWindow.clear()
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
        # Write The search Prompt for the search window
        self.textInputWindow.addstr(
            1,
            3,
            "Search >>> {}".format(self.searchString)
        )
        # Draw the screen
        self.screen.refresh()
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
