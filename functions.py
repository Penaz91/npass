"""
Npass: Yet Another NCurses UI for Pass
List and Search Functions

Copyright © 2014-2019, Daniele Penazzo.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.
"""

import json
import re
from datetime import date
from os import walk, getenv
from os.path import join, relpath, splitext, expanduser, isdir, exists

_frecencylist_: str = join(getenv("HOME", "/"), ".npass_frecency")


def FuzzyFilter(frecency_dict, collection, searchInput):
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
    return sorted(
        [x for _, _, x in suggestions],
        key=lambda x: sorter(frecency_dict, x)
    )


def getPasswordList(frecency_dict: dict, password_dir="~/.password-store/"):
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
    return sorted(noExtFileSet, key=lambda x: sorter(frecency_dict, x))


def sorter(frecency, item):
    fr_item = frecency.get(item, [0, None])
    if fr_item[1] is None:
        return (fr_item[0], None, item)
    return (fr_item[0], date.today() - date.fromisoformat(fr_item[1]), item)


def loadfrecencylist() -> dict:
    """
    Loads the npass frecency list

    Returns
    -------
    dict
        Representation of the frecency list
    """
    if exists(_frecencylist_) and not isdir(_frecencylist_):
        with open(_frecencylist_) as fh:
            return json.load(fh)
    return {}


def savefrecencylist(frec: dict):
    """
    Saves the given frecency list to file

    Parameters
    ----------
    frec : dict
        The dictionary containing the frecency list to save
    """
    with open(_frecencylist_, "w") as fh:
        json.dump(frec, fh)
