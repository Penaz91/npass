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
    :returns: A list of suggestions

    """
    suggestions = []
    pattern = '.*?'.join(searchInput)   # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern, re.IGNORECASE)  # Compiles a regex.
    for item in collection:
        # Current item matches the regex?
        match = regex.search(item, re.IGNORECASE)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return sorted([x for _, _, x in suggestions])


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
    # Get all files in the password_dir
    fileSet = {
        join(dirpath, fname)
        for dirpath, dirname, filenames in walk(expanduser(password_dir))
        for fname in filenames
    }
    # Exclude what we don't care about
    toExclude = set()
    for exclusion in exclude:
        toExclude = {item for item in fileSet if exclusion in item}
        fileSet = fileSet.difference(toExclude)
    # Get the relative path, pinned on the password_dir
    relativeFileSet = {
        relpath(item, expanduser(password_dir))
        for item in fileSet
    }
    # Remove extensions
    noExtFileSet = [splitext(item)[0] for item in relativeFileSet]
    return sorted(noExtFileSet)
