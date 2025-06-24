from utils import files
from utils import maths
import itertools
import copy


# Day 11: Cosmic Expansion
# https://adventofcode.com/2023/day/11


class Cosmos:
    cosmos_array: list[list[str]]

    def __init__(self, cosmos_array: list[list[str]]):
        self.cosmos_array = cosmos_array

    def find_empty_rows(self) -> list[int]:
        return [i for i, row in enumerate(self.cosmos_array) if '#' not in row]

    def find_empty_columns(self) -> list[int]:
        transposed = maths.transpose_2d_array(self.cosmos_array)
        return [i for i, col in enumerate(transposed) if '#' not in col]

    @staticmethod
    def extend_cosmos_dimension(cosmos_array: list[list[str]], empty_in_dimension: list[int]) -> list[list[str]]:
        extended_cosmos_array = []
        for i, row in enumerate(cosmos_array):
            extended_cosmos_array.append(row)
            if i in empty_in_dimension:
                extended_cosmos_array.append(row)
        return extended_cosmos_array

    def extend_cosmos(self) -> 'Cosmos':
        copy_of_cosmos_array = copy.deepcopy(self.cosmos_array)
        extended_cosmos_array = self.extend_cosmos_dimension(copy_of_cosmos_array, self.find_empty_rows())
        transposed_extended_cosmos_array = maths.transpose_2d_array(extended_cosmos_array)
        extended_cosmos_array = self.extend_cosmos_dimension(transposed_extended_cosmos_array, self.find_empty_columns())
        return Cosmos(maths.transpose_2d_array(extended_cosmos_array))

    def find_galaxies(self) -> list[tuple[int, int]]:
        return [(i, j) for i, row in enumerate(self.cosmos_array) for j, char in enumerate(row) if char == '#']


def get_cosmos() -> Cosmos:
     return Cosmos(files.read_file_into_2d_array('data.txt'))


def get_all_galaxy_pairs(galaxies: list[tuple[int, int]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    return list(itertools.combinations(galaxies, 2))


def count_distances_between_galaxies(galaxies_pairs: list[tuple[tuple[int, int], tuple[int, int]]]) -> list[int]:
    return [maths.count_manhattan_distance(pair) for pair in galaxies_pairs]


def count_shortest_paths(galaxies: list[tuple[int, int]]) -> list[int]:
    galaxies_pairs = get_all_galaxy_pairs(galaxies)
    return count_distances_between_galaxies(galaxies_pairs)


def find_galaxies_in_older_cosmos(cosmos: Cosmos) -> list[tuple[int, int]]:
    galaxies = cosmos.find_galaxies()
    empty_rows = set(cosmos.find_empty_rows())
    empty_columns = set(cosmos.find_empty_columns())
    older_galaxies = []

    for i, j in galaxies:
        rows = sum(1 for row in empty_rows if row < i)
        columns = sum(1 for col in empty_columns if col < j)
        i_new = i + 999999 * rows
        j_new = j + 999999 * columns

        older_galaxies.append((i_new, j_new))

    return older_galaxies


def count_sum_of_paths() -> tuple[int, int]:
    cosmos = get_cosmos()

    extended_cosmos = cosmos.extend_cosmos()
    galaxies = extended_cosmos.find_galaxies()
    shortest_paths = count_shortest_paths(galaxies)
    sum_of_shortest_paths = sum(shortest_paths)

    older_galaxies = find_galaxies_in_older_cosmos(cosmos)
    shortest_paths_older = count_shortest_paths(older_galaxies)
    sum_of_shortest_paths_older = sum(shortest_paths_older)

    return sum_of_shortest_paths, sum_of_shortest_paths_older


def main() -> None:
    sum_of_shortest_paths, sum_of_shortest_paths_older = count_sum_of_paths()
    print(f"1. The sum of shortest paths between galaxies is equal to: {sum_of_shortest_paths}")
    print(f"2. The sum of shortest paths between older galaxies in is equal to: {sum_of_shortest_paths_older}")


if __name__ == "__main__":
    main()