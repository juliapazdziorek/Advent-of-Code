from utils import files

# Day 5: Print Queue
# https://adventofcode.com/2024/day/5


def read_data(path: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    lines = files.read_file(path)
    ordering_rules = []
    updates = []
    last_ordering_rule_index = 0
    for i, line in enumerate(lines):
        if len(line) == 0:
            last_ordering_rule_index = i
            break
        pages = line.split('|')
        ordering_rules.append((int(pages[0]), int(pages[1])))

    for line in lines[last_ordering_rule_index + 1:]:
        updates.append([int(num) for num in line.split(',')])

    return ordering_rules, updates


def is_sorted(update: list[int], ordering_rules: list[tuple[int, int]]) -> bool:
    mapped_update = {}
    for i, num in enumerate(update):
        mapped_update[num] = i

    sorted_update = True
    for rule in ordering_rules:
        if rule[0] not in mapped_update or rule[1] not in mapped_update:
            continue
        if mapped_update[rule[0]] > mapped_update[rule[1]]:
            sorted_update = False
            break
    return sorted_update


def filter_updates(ordering_rules: list[tuple[int, int]], updates: list[list[int]], keep_sorted: bool = True) -> list[list[int]]:
    return [update for update in updates if is_sorted(update, ordering_rules) == keep_sorted]


def sum_middle_of_sorted(ordering_rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    sorted_updates = filter_updates(ordering_rules, updates)
    return sum(update[len(update) // 2] for update in sorted_updates)


def sort_updates(ordering_rules: list[tuple[int, int]], updates: list[list[int]]) -> list[list[int]]:
    sorted_updates = []
    for update in updates:
        page_positions = {page: i for i, page in enumerate(update)}
        pages_after = {page: set() for page in update}
        before_counts = {page: 0 for page in update}

        update_pages = set(update)
        for before, after in ordering_rules:
            if before in update_pages and after in update_pages:
                if after not in pages_after[before]:
                    pages_after[before].add(after)
                    before_counts[after] += 1

        zero_before = [page for page in update if before_counts[page] == 0]
        zero_before.sort(key=lambda page: page_positions[page])

        sorted_update = []
        while zero_before:
            current = zero_before.pop(0)
            sorted_update.append(current)
            for page_after in sorted(pages_after[current], key=lambda page: page_positions[page]):
                before_counts[page_after] -= 1
                if before_counts[page_after] == 0:
                    zero_before.append(page_after)

        sorted_updates.append(sorted_update)

    return sorted_updates


def sum_middle_of_corrected(ordering_rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    unsorted_updates = filter_updates(ordering_rules, updates, keep_sorted=False)
    sorted_updates = sort_updates(ordering_rules, unsorted_updates)
    return sum(update[len(update) // 2] for update in sorted_updates)


def main() -> None:
    ordering_rules, updates = files.read_data('data.txt')
    sum_of_middle = sum_middle_of_sorted(ordering_rules, updates)
    sum_of_middle_sorted = sum_middle_of_corrected(ordering_rules, updates)

    print(f"1. The sum of middle numbers is equal to: {sum_of_middle}")
    print(f"2. The sum of middle numbers of corrected updates is equal to: {sum_of_middle_sorted}")


if __name__ == "__main__":
    main()