from collections import defaultdict

from utils import files


# Day 1: Historian Hysteria
# https://adventofcode.com/2024/day/1


def get_lists() -> tuple[list[int], list[int]]:
    lines = files.read_file('data.txt')
    first_list, second_list = [], []
    for line in lines:
        parts = line.split()
        first_list.append(int(parts[0]))
        second_list.append(int(parts[1]))
    return first_list, second_list


def count_total_distance(first_list: list[int], second_list: list[int]) -> int:
    distances = [abs(first_element - second_element) for first_element, second_element in zip(sorted(first_list), sorted(second_list))]
    return sum(distances)


def count_similarity_score(first_list: list[int], second_list: list[int]) -> int:
    count_dict = defaultdict(int)
    for element in second_list:
        count_dict[element] += 1
        
    scores = [element * count_dict[element] for element in first_list]
    return sum(scores)


def main() -> None:
    first_list, second_list = get_lists()
    total_distance = count_total_distance(first_list, second_list)
    similarity_score = count_similarity_score(first_list, second_list)

    print(f"1. The total distance between lists is equal to: {total_distance}")
    print(f"2. The similarity score of lists is equal to: {similarity_score}")


if __name__ == "__main__":
    main()