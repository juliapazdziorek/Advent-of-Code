from utils import files
import re

# Day 19: Aplenty
# https://adventofcode.com/2023/day/19


class Instruction:

    def __init__(self, instruction: str):
        if ":" in instruction:
            self.end_instruction = False
            condition, self.result = instruction.split(':')
            self.category = re.findall(r'([xmas])', condition)[0]

            if '>=' in condition:
                self.operation = '>='
            elif '<=' in condition:
                self.operation = '<='
            elif '>' in condition:
                self.operation = '>'
            elif '<' in condition:
                self.operation = '<'

            self.value = int(re.findall(r'[0-9]+', condition)[0])
        else:
            self.end_instruction = True
            self.result = instruction
            self.category = None
            self.operation = None
            self.value = None

    def get_result(self, part):
        if self.end_instruction or self.check_condition(part):
            return self.result
        else:
            return None

    def check_condition(self, part: dict[str, int]) -> bool:
        if self.end_instruction:
            return True

        value = part[self.category]
        if self.operation == ">":
            return value > self.value
        elif self.operation == "<":
            return value < self.value
        elif self.operation == ">=":
            return value >= self.value
        elif self.operation == "<=":
            return value <= self.value
        else:
            return False


def get_data() -> tuple[dict[str, list[Instruction]], list[dict[str, int]]]:
    lines = files.read_file('data.txt')
    workflows, parts = {}, []
    i = 0
    
    while i < len(lines) and len(lines[i]) != 0:
        name, instructions_str = lines[i].split('{')
        instructions_str = instructions_str.split('}')[0]
        instructions = []
        for instruction in instructions_str.split(','):
            instructions.append(Instruction(instruction))
        
        workflows[name] = instructions
        i += 1
    i += 1
    
    while i < len(lines):
        part_str = lines[i].strip('{}')
        part = {}
        for assignment in part_str.split(','):
            category, value = assignment.split('=')
            part[category] = int(value)
        parts.append(part)
        i += 1
    
    return workflows, parts


def is_accepted(workflow_name: str, part: dict[str, int], workflows: dict[str, list[Instruction]]) -> bool:
    if workflow_name == 'A':
        return True
    if workflow_name == 'R':
        return False
    
    for instruction in workflows[workflow_name]:
        if (result := instruction.get_result(part)) is not None:
            return is_accepted(result, part, workflows)

    return False
    

def count_rating_sum(workflows: dict[str, list[Instruction]], parts: list[dict[str, int]]) -> int:
    return sum(
        sum(part.values())
        for part in parts
        if is_accepted('in', part, workflows)
    )


def negate_instruction(instruction: Instruction) -> Instruction:
    operation_negation = {'<': '>=', '>': '<='}
    negated_operation = operation_negation.get(instruction.operation, '')
    return Instruction(f'{instruction.category}{negated_operation}{instruction.value}:{instruction.result}')


def get_accepting_instructions(workflows: dict[str, list[Instruction]]) -> list[list[Instruction]]:
    accepting_instructions = []

    def search_instruction_path(workflow_name: str, current_path: list[Instruction]) -> None:
        if workflow_name == 'A':
            accepting_instructions.append(current_path.copy())
            return

        elif workflow_name == 'R':
            return

        negated_conditions = []
        for instruction in workflows[workflow_name]:
            if instruction.end_instruction:
                path = current_path + negated_conditions + [instruction]
                search_instruction_path(instruction.result, path)
                break

            else:
                path = current_path + negated_conditions + [instruction]
                search_instruction_path(instruction.result, path)
                negated_instruction = negate_instruction(instruction)
                negated_conditions.append(negated_instruction)

    search_instruction_path('in', [])
    return accepting_instructions


def find_intersection(instruction: Instruction, intervals: dict[str, tuple[int, int]]) -> dict[str, tuple[int, int]]:
    if instruction.end_instruction:
        return intervals
    
    new_intervals = intervals.copy()
    current_min, current_max = intervals[instruction.category]
    
    if instruction.operation == '<':
        new_intervals[instruction.category] = (current_min, min(current_max, instruction.value - 1))
    elif instruction.operation == '>':
        new_intervals[instruction.category] = (max(current_min, instruction.value + 1), current_max)
    elif instruction.operation == '<=':
        new_intervals[instruction.category] = (current_min, min(current_max, instruction.value))
    elif instruction.operation == '>=':
        new_intervals[instruction.category] = (max(current_min, instruction.value), current_max)
    
    return new_intervals


def count_combinations_for_path(instruction_path: list[Instruction]) -> int:
    intervals = {
        'x': (1, 4000),
        'm': (1, 4000),
        'a': (1, 4000),
        's': (1, 4000)
    }
    for instruction in instruction_path:
        intervals = find_intersection(instruction, intervals)
    
    combinations = 1
    for interval in intervals.values():
        min_value, max_value = interval
        if min_value > max_value:
            return 0
        combinations *= (max_value - min_value + 1)
    
    return combinations


def count_combinations(workflows: dict[str, list[Instruction]]) -> int:
    accepting_instructions = get_accepting_instructions(workflows)
    return sum(count_combinations_for_path(instruction_path) for instruction_path in accepting_instructions)


def main() -> None:
    workflows, parts = get_data()
    rating_sum = count_rating_sum(workflows, parts)
    combinations = count_combinations(workflows)

    print(f"1. The sum of all rating numbers is equal to: {rating_sum}")
    print(f"2. The number of distinct combinations is equal to: {combinations}")


if __name__ == "__main__":
    main()