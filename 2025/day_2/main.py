from utils import files

# Day 2: Gift Shop
# https://adventofcode.com/2025/day/2


def parse_ranges(line: list[str]) -> list[tuple[int, int]]:
    str_ranges = line[0].split(',')
    ranges = []
    for str_range in str_ranges:
        parts = str_range.split('-')
        ranges.append((int(parts[0]), int(parts[1])))
    return ranges


def sum_in_range(id_range: tuple[int, int]) -> int:
    sum_of_ids = 0
    for id_in_range in range(id_range[0], id_range[1] + 1):
        str_id = str(id_in_range)

        if len(str_id) % 2 != 0:
            continue

        if str_id[:len(str_id) // 2] == str_id[len(str_id) // 2:]:
            sum_of_ids += id_in_range

    return sum_of_ids


def count_sum_of_invalid_ids(ranges: list[tuple[int, int]]) -> int:
    return sum(sum_in_range(id_range) for id_range in ranges)


def generate_patterns(ranges: list[tuple[int, int]]) -> list[int]:
    max_id = max(id_range[1] for id_range in ranges)
    max_length = len(str(max_id))
    patterns = set()

    for length in range(2, max_length + 1):
        for part_count in range(2, length + 1):
            if length % part_count != 0:
                continue

            part_length = length // part_count
            start = 10 ** (part_length - 1) if part_length > 1 else 1
            end = 10 ** part_length

            for base in range(start, end):
                base_str = f"{base:0{part_length}d}"
                if base_str[0] == '0':
                    continue

                pattern_str = base_str * part_count
                pattern_val = int(pattern_str)

                if pattern_val <= max_id:
                    patterns.add(pattern_val)

    return sorted(patterns)


def sum_in_range_new_rule(id_range: tuple[int, int], patterns: list[int]) -> int:
    return sum(pattern for pattern in patterns if id_range[0] <= pattern <= id_range[1])


def count_sum_of_invalid_ids_new_rule(ranges: list[tuple[int, int]]) -> int:
    patterns = generate_patterns(ranges)
    return sum(sum_in_range_new_rule(id_range, patterns) for id_range in ranges)


def main() -> None:
    line = files.read_file('data.txt')
    ranges = parse_ranges(line)
    sum_of_invalid_ids = count_sum_of_invalid_ids(ranges)
    sum_of_invalid_ids_new_rule = count_sum_of_invalid_ids_new_rule(ranges)

    print(f"1. The sum of invalid ids is equal to: {sum_of_invalid_ids}")
    print(f"2. The sum of invalid ids using the new rule is equal to: {sum_of_invalid_ids_new_rule}")


if __name__ == "__main__":
    main()