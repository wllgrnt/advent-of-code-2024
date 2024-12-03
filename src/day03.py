"""
day03.py

Scan a text string for instructions matching mul(left, right), and sum them.
Part two: include conditional do() and don't() statements
"""

from pathlib import Path
from dataclasses import dataclass
from operator import mul
import re


@dataclass
class Mul:
    tape_position: int
    operation = mul
    pattern = r"mul\(\d+,\d+\)"
    left: int
    right: int


@dataclass
class Do:
    tape_position: int
    pattern = r"do\(\)"


@dataclass
class Dont:
    tape_position: int
    pattern = r"don\'t\(\)"


def parse_input(input_str: str) -> list[Mul | Do | Dont]:
    # suboptimal implementation here, parses the string thrice. Should do a pointer-based thing.
    mul_matches = re.finditer(Mul.pattern, input_str)  # have to read the tape manually
    instructions = []
    for match in mul_matches:
        match_str = match.group()
        left, right = match_str[match_str.index("(") + 1 : match_str.index(")")].split(
            ","
        )
        instructions.append(
            Mul(left=int(left), right=int(right), tape_position=match.start())
        )

    do_matches = re.finditer(Do.pattern, input_str)
    for match in do_matches:
        instructions.append(Do(tape_position=match.start()))

    dont_matches = re.finditer(Dont.pattern, input_str)
    for match in dont_matches:
        instructions.append(Dont(tape_position=match.start()))

    return instructions


def part1(input_data: list[Mul | Do | Dont]) -> int:
    return sum(
        instruction.operation(instruction.left, instruction.right)
        for instruction in input_data
        if isinstance(instruction, Mul)
    )


def part2(input_data: list[Mul | Do | Dont]) -> int:
    muls_enabled = True
    count = 0
    for instruction in sorted(input_data, key=lambda x: x.tape_position):
        if isinstance(instruction, Do):
            muls_enabled = True
        elif isinstance(instruction, Dont):
            muls_enabled = False
        elif isinstance(instruction, Mul):
            if muls_enabled:
                count += instruction.operation(instruction.left, instruction.right)
        else:
            raise ValueError(f"unexpected instruction: {instruction}")

    return count


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
