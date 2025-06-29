from utils import files


# Day 12: Hot Springs
# https://adventofcode.com/2023/day/12


def get_springs_data() -> list[tuple[str, list[int]]]:
    lines = files.read_file('data.txt')
    springs_data = [] 
    for line in lines:
        parts = line.split()
        damaged_groups = [int(damaged_group) for damaged_group in parts[1].split(',')]
        springs_data.append((parts[0], damaged_groups))

    return springs_data


def end_of_springs(damaged_groups, damaged_i, damaged_length):
    if damaged_length > 0:
        if damaged_i >= len(damaged_groups) or damaged_length != damaged_groups[damaged_i]:
            return 0
        damaged_i += 1

    if damaged_i == len(damaged_groups):
        return 1
    else:
        return 0


def continue_damaged(springs_data, springs_i, damaged_i, damaged_length, memo):
    return count_springs_arrangements(springs_data, springs_i + 1, damaged_i, damaged_length + 1, memo)


def continue_operational(springs_data, springs_i, damaged_i, memo):
    return count_springs_arrangements(springs_data, springs_i + 1, damaged_i, 0, memo)


def finish_damaged(springs_data, springs_i, damaged_i, memo):
    return count_springs_arrangements(springs_data, springs_i + 1, damaged_i + 1, 0, memo)


def count_springs_arrangements(springs_data, springs_i=0, damaged_i=0, damaged_length=0, memo=None):
    if memo is None:
        memo = {}

    key = (springs_i, damaged_i, damaged_length)
    if key in memo:
        return memo[key]

    springs, damaged_groups = springs_data
    if springs_i == len(springs):
        return end_of_springs(damaged_groups, damaged_i, damaged_length)
    
    result = 0
    if springs[springs_i] in ['#','?'] and damaged_i < len(damaged_groups) and damaged_length < damaged_groups[damaged_i]:
        result += continue_damaged(springs_data, springs_i, damaged_i, damaged_length, memo)

    if springs[springs_i] in ['.','?'] and damaged_length == 0:
        result += continue_operational(springs_data, springs_i, damaged_i, memo)

    elif springs[springs_i] in ['.','?'] and damaged_i < len(damaged_groups) and damaged_length == damaged_groups[damaged_i]:
        result += finish_damaged(springs_data, springs_i, damaged_i, memo)

    memo[key] = result
    return result


def count_all_arrangements(springs_data: list[tuple[str, list[int]]]) -> int:
    return sum([count_springs_arrangements(data) for data in springs_data])


def unfold(springs_data: list[tuple[str, list[int]]]) -> list[tuple[str, list[int]]]:
    new_data = []
    for springs, damaged_groups in springs_data:
        unfolded_springs = '?'.join([springs] * 5)
        unfolded_groups = damaged_groups * 5
        new_data.append((unfolded_springs, unfolded_groups))
    return new_data


def count_unfolded_all_arrangements(springs_data: list[tuple[str, list[int]]]) -> int:
    return sum([count_springs_arrangements(data) for data in unfold(springs_data)])


def main() -> None:
    springs_data = get_springs_data()
    arrangements = count_all_arrangements(springs_data)
    unfolded_arrangements = count_unfolded_all_arrangements(springs_data)

    print(f"1. The sum of possible arrangements is equal to: {arrangements}")
    print(f"2. The sum of possible arrangements with unfolded records is equal to: {unfolded_arrangements}")


if __name__ == "__main__":
    main()