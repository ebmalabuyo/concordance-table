from __future__ import annotations

from typing import TextIO

# Add more imports here as you use functions from your hash table.
from hash_table import (HashTable, insert, contains, get_item, keys)
import string


def djbx33a(s: str) -> int:
    """Returns a modified DJBX33A hash of the given string.

    See the project specification for the formula.
    """
    n = min(len(s), 8)
    sum = 0
    for i in range(n):
        val = ord(s[i]) * 33**(n - 1 - i)
        sum += val
    out = 5381 * (33**n) + sum
    return out


def build_stop_words_table(stop_words_file: TextIO) -> HashTable:
    """Returns a hash table whose keys are the stop words.

    This will read the stop words from the file and add them to the stop
    words table.  The values stored in the table will not matter.

    Args:
        stop_words_file: the open stop words file.

    Returns:
        A hash table whose keys are the stop words.
    """
    ht = HashTable()
    for line in stop_words_file:
        line = line.rstrip()
        insert(ht, line, None)
    return ht


def build_concordance_table(file: TextIO, stop_table: HashTable) -> HashTable:
    """Returns the concordance table for the given file.

    This will read the given file and build a concordance table
    containing all valid words in the file.

    Args:
        file: the open file to read
        stop_table: a hash table whose keys are the stop words

    Returns:
        A concordance table built from the given file.
    """
    # created concord table
    concord_table = HashTable(10, djbx33a)

    # tracker for counting line number
    count_lines = 0
    for line in file:
        count_lines += 1
        # make line lower case
        line = line.lower()
        # removing all the apostrophe characters
        line = line.replace("'", '')
        # convert all special characters to spaces
        clean = ''.join(' ' if val in string.punctuation
                        else val for val in line)
        # split each word into tokens
        tokens = clean.split()
        # check if alphabetic
        for word in tokens:
            if word.isalpha():
                # check if its a stopping word
                if contains(stop_table, word):
                    pass
                else:
                    if contains(concord_table, word):
                        if count_lines == get_item(concord_table, word)[-1]:
                            pass
                        else:
                            item = get_item(concord_table, word)
                            item.append(count_lines)
                            insert(concord_table, word, item)
                    else:
                        val = [count_lines]
                        insert(concord_table, word, val)
    return concord_table


def write_concordance_table(
        file: TextIO, concordance_table: HashTable) -> None:
    """Writes the concordance table to the given file.

    This will sort the strings in the concordance table alphabetically
    and write them to the given file along with the line numbers on
    which they occurred.

    Args:
        file: the open file in which to store the table
        concordance_table: the concordance table
    """
    # get list of keys from concord table
    key_words = keys(concordance_table)
    # sort the keys in alphabetic
    key_words = sorted(key_words)

    # for each key in list of keys:
    for word in key_words:
        file.write(f"{word}:")
        # write the key, write :, write space
        item = get_item(concordance_table, word)
        # for line numbers in get_items:
        for line_num in item:
            file.write(' ' + str(line_num))
        file.write('\n')
