#!/usr/bin/env python
"""
Npass: Yet Another NCurses UI for Pass
Bootstrapping component

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""
import argparse
import curses
from npass import Npass


def main(screen, mode):
    """
    The main loop for the software

    :screen: The Curses Screen
    :mode: The mode that has been selected via command line arguments
    :returns: None

    """
    npass = Npass(screen, mode)
    npass.run()


if __name__ == "__main__":
    """
    When Starting, parse the command line arguments and start the
    curses loop
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--clip", "--copy",
                       help="Open npass in copy mode", action="store_const",
                       dest="mode", const=1, default=0)
    group.add_argument("-e", "--edit", help="Open npass in edit mode",
                       action="store_const", dest="mode", const=2,
                       default=0)
    group.add_argument("-d", "--delete", help="Open npass in delete mode",
                       action="store_const", dest="mode", const=3,
                       default=0)
    args = parser.parse_args()
    curses.wrapper(main, args.mode)
