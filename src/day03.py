"""
day03.py

Scan a text string for instructions matching mul(left, right), and sum them.
Part two: include conditional do() and don't() statements
"""

from pathlib import Path
from dataclasses import dataclass
from operator import mul

from enum import Enum


class InstructionType(Enum):
    MUL = "mul"
    DO = "do"
    DONT = "dont"


@dataclass
class Instruction:
    type: InstructionType
    tape_position: int
    left: int | None = None
    right: int | None = None

    @property
    def pattern(self) -> str:
        match self.type:
            case InstructionType.MUL:
                return r"mul\(\d+,\d+\)"
            case InstructionType.DO:
                return r"do\(\)"
            case InstructionType.DONT:
                return r"don\'t\(\)"


def parse_input(input_str: str) -> list[Instruction]:
    instructions = []
    cursor = 0
    length = len(input_str)

    while cursor < length:
        # Try to match instructions at current cursor position
        if input_str[cursor:].startswith("mul("):
            # Find the closing parenthesis
            end = input_str.find(")", cursor)
            if end != -1:
                try:
                    left, right = map(int, input_str[cursor + 4 : end].split(","))
                    instructions.append(
                        Instruction(InstructionType.MUL, cursor, left, right)
                    )
                    cursor = end + 1
                    continue
                except ValueError:
                    pass  # Not a valid mul instruction, move on

        elif input_str[cursor:].startswith("do()"):
            instructions.append(Instruction(InstructionType.DO, cursor))
            cursor += 4
            continue

        elif input_str[cursor:].startswith("don't()"):
            instructions.append(Instruction(InstructionType.DONT, cursor))
            cursor += 7
            continue

        cursor += 1  # Move to next character if no instruction found

    return instructions


def part1(input_data: list[Instruction]) -> int:
    return sum(
        mul(inst.left, inst.right)
        for inst in input_data
        if inst.type == InstructionType.MUL
    )


def part2(input_data: list[Instruction]) -> int:
    muls_enabled = True
    total = 0

    for inst in input_data:  # already sorted during parsing
        match inst.type:
            case InstructionType.DO:
                muls_enabled = True
            case InstructionType.DONT:
                muls_enabled = False
            case InstructionType.MUL if muls_enabled:
                total += mul(inst.left, inst.right)

    return total


test_input = (
    """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
)

assert (part1_test := part1(parse_input(test_input))) == 161, part1_test
assert (part2_test := part2(parse_input(test_input))) == 48, part2_test

if __name__ == "__main__":
    with Path("inputs/day03.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
