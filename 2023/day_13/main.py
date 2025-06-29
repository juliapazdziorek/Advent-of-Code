from utils import files
from utils import maths


# Day 13: Point of Incidence
# https://adventofcode.com/2023/day/13


def get_patterns() -> list[list[list[str]]]:
    lines = files.read_file('data.txt')
    patterns, pattern = [], []
    for line in lines:
        if line != '':
            pattern.append([char for char in line])
        else:
            patterns.append(pattern)
            pattern = []
    patterns.append(pattern)
    return patterns


def is_reflection(pattern: list[list[str]], i: int) -> bool:
    i, j = i - 1, i + 2
    while i >= 0 and j < len(pattern):
        if pattern[i] == pattern[j]:
            i -= 1
            j += 1
        else:
            return False
    return True


def check_reflections(pattern: list[list[str]]) -> int | None:
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i + 1]:
            if is_reflection(pattern, i):
                return i + 1
    return None


def search_for_reflection(pattern: list[list[str]]) -> tuple[int, int]:
    rows, columns = check_reflections(pattern), 0
    if not rows:
        pattern = maths.transpose_2d_array(pattern)
        rows, columns = 0, check_reflections(pattern)
    return rows, columns


def summarize_reflections(reflections: list[tuple[int, int]]) -> int:
    return sum(reflection[0] for reflection in reflections) * 100 + sum(reflection[1] for reflection in reflections)


def one_rock_off(line_i: list[str], line_j: list[str]) -> bool:
    counter = 0
    for i in range(len(line_i)):
        if line_i[i] != line_j[i]:
            counter += 1
    return counter == 1


def is_reflection_with_one_off(pattern: list[list[str]], i: int) -> bool:
    i, j = i - 1, i + 2
    smudge_fixed = False
    while i >= 0 and j < len(pattern):
        if pattern[i] == pattern[j]:
            i -= 1
            j += 1
        elif one_rock_off(pattern[i], pattern[j]) and not smudge_fixed:
            i -= 1
            j += 1
            smudge_fixed = True
        else:
            return False
    return smudge_fixed


def check_reflections_with_fix(pattern: list[list[str]], original_reflection: int) -> int | None:
    for i in range(len(pattern) - 1):
        if one_rock_off(pattern[i], pattern[i + 1]):
            if is_reflection(pattern, i):
                return i + 1
            
        if pattern[i] == pattern[i + 1] and i + 1 != original_reflection:
            if is_reflection_with_one_off(pattern, i):
                return i + 1
    return None


def search_for_reflection_fixed_smudges(pattern: list[list[str]], original_reflection: tuple[int, int]) -> tuple[int, int]:
    original_row, original_column = original_reflection
    rows, columns = check_reflections_with_fix(pattern, original_row), 0
    if not rows:
        pattern = maths.transpose_2d_array(pattern)
        rows, columns = 0, check_reflections_with_fix(pattern, original_column)
    return rows, columns


def main() -> None:
    patterns = get_patterns()
    reflections = [search_for_reflection(pattern) for pattern in patterns]
    summarized_reflections = summarize_reflections(reflections)
    fixed_reflections = [search_for_reflection_fixed_smudges(pattern, original) for pattern, original in zip(patterns, reflections)]
    fixed_summarized_reflections = summarize_reflections(fixed_reflections)

    print(f"1. The number of all notes summarized is equal to: {summarized_reflections}")
    print(f"2. The number of all notes summarized with smudges fixed is equal to: {fixed_summarized_reflections}")


if __name__ == "__main__":
    main()
