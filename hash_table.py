from __future__ import annotations

from collections.abc import Callable
from typing import Any, List, Tuple


# An entry in the hash table is a key-value pair
HashEntry = Tuple[Any, Any]
# Each entry in the hash table array will be a list of HashEntry pairs
HashChain = List[HashEntry]


class HashTable:
    """A hash table with separate chaining."""
    def __init__(
            self,
            capacity: int = 10,
            hash_function: Callable[[Any], int] = hash):
        """Creates an empty hash table.

        Args:
            capacity:
                The initial capacity of the backing array.  The default
                capacity is 10.
            hash_function:
                The function to use to compute hash values for the given
                keys.  The default hash function is the Python builtin
                hash function.
        """
        self.table: list[HashChain] = [[] for _ in range(capacity)]

        self.size: int = 0
        self.capacity: int = capacity
        self.hash_function = hash_function


def insert(hash_table: HashTable, key: Any, value: Any) -> None:

    index = hash_table.hash_function(key) % hash_table.capacity
    pair = (key, value)
    # if empty just add to position
    if hash_table.table[index] == []:
        hash_table.table[index].append(pair)
        hash_table.size += 1
        return

    # if key is the same
    for j in range(len(hash_table.table[index])):
        if key in hash_table.table[index][j]:
            hash_table.table[index][j] = pair
            return
    # double capacity and rehash
    if hash_table.size >= hash_table.capacity:
        hash_table.capacity *= 2
        lst = [[] for _ in range(hash_table.capacity)]
        for i in range(len(hash_table.table)):
            for j in range(len(hash_table.table[i])):
                new_key = hash_table.table[i][j][0]
                new_val = hash_table.table[i][j][1]
                new_pair = (new_key, new_val)
                i2 = hash_table.hash_function(new_key) % hash_table.capacity
                lst[i2].append(new_pair)

        hash_table.table = lst
        index = hash_table.hash_function(key) % hash_table.capacity
        hash_table.table[index].append(pair)
    else:
        # add to correct table, if table has more than one tuple
        hash_table.table[index].append(pair)
    hash_table.size += 1


def get_item(hash_table: HashTable, key: Any) -> Any:
    hash_val = hash_table.hash_function(key) % hash_table.capacity
    if hash_table.table[hash_val] == []:
        raise KeyError
    for i in range(len(hash_table.table[hash_val])):
        if hash_table.table[hash_val][i][0] == key:
            return hash_table.table[hash_val][i][1]


def contains(hash_table: HashTable, key: Any) -> bool:
    index = hash_table.hash_function(key) % hash_table.capacity
    if hash_table.table[index] == []:
        return False
    for i in range(len(hash_table.table[index])):
        if hash_table.table[index][i][0] == key:
            return True


def remove(hash_table: HashTable, key: Any) -> tuple[Any, Any]:
    index = hash_table.hash_function(key) % hash_table.capacity
    if hash_table.table[index] == []:
        raise KeyError
    for i in range(len(hash_table.table[index])):
        if hash_table.table[index][i][0] == key:
            out = hash_table.table[index][i]
            hash_table.table[index].pop(i)
            hash_table.size -= 1
            return out


def size(hash_table: HashTable) -> int:
    return hash_table.size


def keys(hash_table: HashTable) -> list[Any]:
    output = []
    for i in range(len(hash_table.table)):
        if hash_table.table[i] == []:
            pass
        else:
            for j in range(len(hash_table.table[i])):
                output.append(hash_table.table[i][j][0])
    return output


def load_factor(hash_table: HashTable) -> float:
    return hash_table.size / hash_table.capacity


def _contents(hash_table: HashTable) -> list[HashChain]:
    return hash_table.table
