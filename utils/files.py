
def read_file(path: str) -> list[str]:
    """
    Reads a text file and returns a list of strings, where each string is a line from the file without a newline character.
    """
    try:
        with open(path, 'r') as file:
            return [line.rstrip('\n') for line in file]
        
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
        return []
    except IOError as e:
        print(f"Error reading file {path}: {e}")
        return []


def read_file_into_2d_array(path: str) -> list[list[str]]:
    """
    Reads a text file and returns its contents as a 2D array (list of lists of characters),
    where each sublist represents a line of characters.
    """
    rows = []
    try:
        with open(path, 'r') as file:
            for line in file:
                line = line.rstrip('\n')
                rows.append(list(line))
                
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
    except IOError as e:
        print(f"Error reading file {path}: {e}")
    return rows
