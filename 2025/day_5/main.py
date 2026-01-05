from utils import files

# Day 5: Cafeteria
# https://adventofcode.com/2025/day/5


def parse_ids(lines: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    id_ranges, ids = [], []
    for line in lines:
        if '-' in line:
            start, end = line.split('-')
            id_ranges.append((int(start), int(end)))
            continue

        if len(line) != 0:
            ids.append(int(line))

    return id_ranges, ids


def count_fresh_ids(id_ranges: list[tuple[int, int]], ids: list[int]) -> int:
    fresh_ids = 0
    for ingredient_id in ids:
        for id_range in id_ranges:
            if id_range[0] <= ingredient_id <= id_range[1]:
                fresh_ids += 1
                break
    return fresh_ids


def merge_id_ranges(id_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    sorted_ranges = sorted(id_ranges, key=lambda x: x[0])
    merged_id_ranges = [sorted_ranges[0]]
    for id_range in sorted_ranges[1:]:
        last_merged = merged_id_ranges[-1]

        if id_range[0] <= last_merged[1] + 1:
            merged_id_ranges[-1] = (last_merged[0], max(last_merged[1], id_range[1]))
        else:
            merged_id_ranges.append(id_range)
    
    return merged_id_ranges


def count_all_fresh_ids(id_ranges: list[tuple[int, int]]) -> int:
    merged_id_ranges = merge_id_ranges(id_ranges)
    return sum([id_range[1] - id_range[0] + 1 for id_range in merged_id_ranges])


def main() -> None:
    lines = files.read_file('data.txt')
    id_ranges, ids = parse_ids(lines)
    fresh_ids = count_fresh_ids(id_ranges, ids)
    all_fresh_ids = count_all_fresh_ids(id_ranges)

    print(f"1. The number of fresh ID's is equal to: {fresh_ids}")
    print(f"2. The total number of fresh ID is equal to: {all_fresh_ids}")


if __name__ == "__main__":
    main()