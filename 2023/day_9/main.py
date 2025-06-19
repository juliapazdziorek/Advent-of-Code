from utils import files


# Day 9: Mirage Maintenance
# https://adventofcode.com/2023/day/9


def get_history() -> list[list[int]]:
    lines = files.read_file('data.txt')
    return [[int(value) for value in line.split(' ')] for line in lines]


def count_differences(values: list[int]) -> list[int]:
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


def count_next_value(values: list[int]) -> int:
    if all(value == 0 for value in values):
        return 0
    
    else:
        differences = count_differences(values)
        return values[-1] + count_next_value(differences)


def count_next_values(history: list[list[int]]) -> list[int]:
    return [count_next_value(values) for values in history]


def count_previous_value(values: list[int]) -> int:
    if all(value == 0 for value in values):
        return 0
    
    else:
        differences = count_differences(values)
        return values[0] - count_previous_value(differences)


def count_previous_values(history: list[list[int]]) -> list[int]:
    return [count_previous_value(values) for values in history]


def main() -> None:
    history = get_history()
    sum_of_next_values = sum(value for value in count_next_values(history))
    sum_of_previous_values = sum(value for value in count_previous_values(history))
    print(f"1. The sum of extrapolated next values in history is equal to: {sum_of_next_values}")
    print(f"2. The sum of extrapolated previous values in history is equal to: {sum_of_previous_values}")

if __name__ == "__main__":
    main()