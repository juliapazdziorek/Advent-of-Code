from typing import List


def read_file(path: str) -> List[str]:
    """
    Reads a text file and returns a list of strings, where each string is a line from the file without a newline character.
    """

    with open(path, 'r') as file:
        return [line.rstrip('\n') for line in file]


def read_file_into_2d_array(path: str) -> List[List[str]]:
    """
    Reads a text file and returns its contents as a 2D array (list of lists of characters),
    where each sublist represents a line of characters.
    """
    rows = []

    with open(path, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            rows.append(list(line))
    return rows
