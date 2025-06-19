from dataclasses import dataclass
from utils import files


# Day 5: If You Give A Seed A Fertilizer
# https://adventofcode.com/2023/day/5


@dataclass
class Range:
    start: int
    end: int


@dataclass
class Mapping:
    dest_start: int
    src_start: int
    length: int


def read_seeds_file() -> tuple[list[int], list[Range], list[list[Mapping]]]:
    lines = files.read_file('data.txt')
    seed_values = list(map(int, lines[0].split()[1:]))

    seeds_numbers = [int(value) for value in seed_values]

    seeds_ranges = []
    for i in range(0, len(seed_values), 2):
        start = seed_values[i]
        length = seed_values[i + 1]
        seeds_ranges.append(Range(start, start + length - 1))

    maps = []
    current_map = None

    for line in lines[1:]:
        if line.endswith('map:'):
            if current_map is not None:
                maps.append(current_map)
            current_map = []

        parts = line.split()
        if len(parts) == 3:
            triple = list(map(int, parts))
            current_map.append(Mapping(triple[0], triple[1], triple[2]))
    maps.append(current_map)

    return seeds_numbers, seeds_ranges, maps


def count_min_values_location(seeds_values: list[int], maps: list[list[Mapping]]) -> int:
    i = 0
    while i < len(seeds_values):
        value = seeds_values[i]

        for current_map in maps:
            for mapping in current_map:
                src_start = mapping.src_start
                src_end = mapping.src_start + mapping.length - 1

                if src_start <= value <= src_end:
                    value = mapping.dest_start + (value - src_start)
                    break
                
        seeds_values[i] = value
        i += 1
    return min(seeds_values)


def map_ranges_through_map(ranges: list[Range], current_map: list[Mapping]) -> list[Range]:
    result = []
    for current_range in ranges:

        to_map = [current_range]
        for mapping in current_map:
            src_start = mapping.src_start
            src_end = mapping.src_start + mapping.length - 1
            dest_start = mapping.dest_start

            new_to_map = []
            for to_map_range in to_map:

                if to_map_range.end < src_start or to_map_range.start > src_end:
                    new_to_map.append(to_map_range)
                    continue

                if to_map_range.start < src_start:
                    new_to_map.append(Range(to_map_range.start, src_start - 1))
                    to_map_range = Range(src_start, to_map_range.end)

                if to_map_range.end > src_end:
                    new_to_map.append(Range(src_end + 1, to_map_range.end))
                    to_map_range = Range(to_map_range.start, src_end)

                mapped_start = dest_start + (to_map_range.start - src_start)
                mapped_end = dest_start + (to_map_range.end - src_start)
                result.append(Range(mapped_start, mapped_end))
            to_map = new_to_map

        result.extend(to_map)
    return result


def count_min_ranges_location(seeds_ranges: list[Range], maps: list[list[Mapping]]) -> int:
    current_ranges: list[Range] = seeds_ranges[:]
    for current_map in maps:
        current_ranges = map_ranges_through_map(current_ranges, current_map)

    return min(r.start for r in current_ranges)


def get_min_seeds_locations() -> tuple[int, int]:
    seeds_values, seeds_ranges, maps = read_seeds_file()

    lowest_individual_numbers_location = count_min_values_location(seeds_values, maps)
    lowest_ranges_location = count_min_ranges_location(seeds_ranges, maps)

    return lowest_individual_numbers_location, lowest_ranges_location 


def main() -> None:
    lowest_values_location, lowest_ranges_location = get_min_seeds_locations()
    print(f"1. The lowest location when seed's values corresponds to individual seeds is equal to {lowest_values_location}")
    print(f"1. The lowest location when seed's values corresponds to ranges of seeds is equal to {lowest_ranges_location}")


if __name__ == "__main__":
    main()