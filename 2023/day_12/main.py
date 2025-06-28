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


def check_base_case(groups: list[int], group_index: int, group_length: int) -> int:
    if group_length > 0: # end of springs in a group
        if group_index >= len(groups) or group_length != groups[group_index]: # group length doesn't match
            return 0
        group_index += 1

    if group_index == len(groups): # groups match
        return 1
    else:
        return 0


def count_springs_arrangements(springs: str, groups: list[int], springs_index: int=0, group_index: int=0, group_length: int=0, memo: dict=None) -> int:
    if memo is None:
        memo = {}
        
    key = (springs_index, group_index, group_length)
    if key in memo:
        return memo[key]

    if springs_index == len(springs):
        return check_base_case(groups, group_index, group_length)
        
    result = 0
    current_spring = springs[springs_index]
    if current_spring in ['#', '?']:
        if group_index < len(groups) and group_length < groups[group_index]: # continue a group
            result += count_springs_arrangements(springs, groups, springs_index + 1, group_index, group_length + 1, memo)

    if current_spring in ['.', '?']:
        if group_length == 0: # no group
            result += count_springs_arrangements(springs, groups, springs_index + 1, group_index, 0, memo)
        elif group_index < len(groups) and group_length == groups[group_index]: # finish a group
            result += count_springs_arrangements(springs, groups, springs_index + 1, group_index + 1, 0, memo)

    memo[key] = result
    return result


def count_all_arrangements(springs_data: list[tuple[str, list[int]]]) -> int:
    return sum([count_springs_arrangements(spring, damaged_groups) for spring, damaged_groups in springs_data])


def unfold(springs_data: list[tuple[str, list[int]]]) -> list[tuple[str, list[int]]]:
    new_data = []
    for springs, damaged_groups in springs_data:
        unfolded_springs = '?'.join([springs] * 5)
        unfolded_groups = damaged_groups * 5
        new_data.append((unfolded_springs, unfolded_groups))
    return new_data


def count_unfolded_all_arrangements(springs_data: list[tuple[str, list[int]]]) -> int:
    springs_data = unfold(springs_data)
    return sum([count_springs_arrangements(spring, damaged_groups) for spring, damaged_groups in springs_data])


def main() -> None:
    springs_data = get_springs_data()
    arrangements = count_all_arrangements(springs_data)
    unfolded_arrangements = count_unfolded_all_arrangements(springs_data)

    print(f"1. The sum of possible arrangements is equal to: {arrangements}")
    print(f"2. The sum of possible arrangements with unfolded records is equal to: {unfolded_arrangements}")


if __name__ == "__main__":
    main()