from utils import files


# Day 2: Red-Nosed Reports
# https://adventofcode.com/2024/day/2


def get_reports() -> list[list[int]]:
    lines = files.read_file('data.txt')
    return [[int(element) for element in line.split(' ')] for line in lines]


def count_differences(report: list[int]) -> list[int]:
    return [report[i] - report[i + 1] for i in range(len(report) - 1)]


def is_safe(report: list[int]) -> bool:
    differences = count_differences(report)
    first = differences[0]
    if first == 0:
        return False
    allowed = {1, 2, 3} if first > 0 else {-1, -2, -3}
    return all(diff in allowed for diff in differences)


def count_safe_reports(reports: list[list[int]]) -> int:
    return sum(1 for report in reports if is_safe(report))


def get_sub_reports(report: list[int]):
    for i in range(len(report)):
        yield report[:i] + report[i+1:]


def count_safe_reports_problem_dumper(reports: list[list[int]]) -> int:
    counter = 0
    for report in reports:
        if is_safe(report):
            counter += 1
            continue
    
        if any(is_safe(sub_report) for sub_report in get_sub_reports(report)):
            counter += 1
            
    return counter


def main() -> None:
    reports = get_reports()
    safe_reports = count_safe_reports(reports)
    safe_report_problem_dumper = count_safe_reports_problem_dumper(reports)

    print(f"1. The number of safe reports is equal to: {safe_reports}")
    print(f"2. The number of safe reports using the Problem Dampener rule is equal to: {safe_report_problem_dumper}")


if __name__ == "__main__":
    main()