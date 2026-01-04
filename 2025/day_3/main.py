from collections.abc import Callable
from utils import files

# Day 3: Lobby
# https://adventofcode.com/2025/day/3


def get_joltage(bank: str) -> int:
    bank_list = [int(char) for char in bank]
    max_joltage = -1
    
    for i in range(len(bank_list)):
        if bank_list[i + 1:]:
            second_max_joltage = max(bank_list[i + 1:])
            current_joltage = bank_list[i] * 10 + second_max_joltage
            if current_joltage > max_joltage:
                max_joltage = current_joltage
    
    return max_joltage


def get_12_joltage(bank: str) -> int:
    bank_list = [int(char) for char in bank]
    result_joltage = []
    to_remove = len(bank_list) - 12
    
    for i in range(len(bank_list)):
        while result_joltage and result_joltage[-1] < bank_list[i] and to_remove > 0:
            result_joltage.pop()
            to_remove -= 1
        
        result_joltage.append(bank_list[i])
    
    while to_remove > 0:
        result_joltage.pop()
        to_remove -= 1
    
    return int(''.join(map(str, result_joltage)))


def count_sum_joltage(banks: list[str], get_joltage_func: Callable[[str], int]) -> int:
    return sum([get_joltage_func(bank) for bank in banks])


def main() -> None:
    banks = files.read_file('data.txt')
    sum_joltage = count_sum_joltage(banks, get_joltage)
    sum_12_joltage = count_sum_joltage(banks, get_12_joltage)

    print(f"1. The sum of joltage output consisting of 2 batteries is equal to: {sum_joltage}")
    print(f"2. The sum of joltage output consisting of 12 batteries is equal to: {sum_12_joltage}")


if __name__ == "__main__":
    main()