"""
Npass: Yet Another NCurses UI for Pass
List and Search Functions

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

import re
from os import walk
from os.path import join, relpath, splitext, expanduser


def FuzzyFilter(collection, searchInput):
    """
    Fuzzy Filters a defined collection

    :collection: The collection to filter
    :searchInput: The input string to fuzzy match
    :returns: An ordered list of suggestions, sorted by length of the match

    """
    suggestions = []
    pattern = '.*?'.join(searchInput)   # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern, re.IGNORECASE)  # Compiles a regex.
    for item in collection:
        # Current item matches the regex?
        match = regex.search(item, re.IGNORECASE)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions, reverse=True)]


def getPasswordList(password_dir="~/.password-store/"):
    """
    Given a password directory, returns the list of passwords present,
    relative to that directory

    :password_dir: A string representing the password directory, defaults
                   to '~/.password-store/'
    :returns: A list of files, relative to the password directory,
              without extensions
    """
    exclude = {".gpg-id", ".git"}
    fileSet = {join(dp, f)
               for dp, dn, fn in walk(expanduser(password_dir))
               for f in fn}
    toExclude = set()
    for exclusion in exclude:
        toExclude = {item for item in fileSet if exclusion in item}
        fileSet = fileSet.difference(toExclude)
    relativeFileSet = {relpath(item, expanduser(password_dir))
                       for item in fileSet}
    noExtFileSet = [splitext(item)[0] for item in relativeFileSet]
    return noExtFileSet
