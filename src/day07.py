"""
day07.py

Given an equation with value: operands, work out the operators required to produce the value.

We only have adds and multiplies, and operators are always evaluated left to right.
"""

from dataclasses import dataclass
from itertools import product
from math import log10
from operator import add, mul
from pathlib import Path


@dataclass
class Equation:
    value: int
    operands: list[int]


def parse_input(input_str: str) -> list[Equation]:
    equations = []
    for line in input_str.split("\n"):
        if line:
            value, operands = line.strip().split(":")
            value, operands = int(value), [int(x) for x in operands.split()]
            equations.append(Equation(value=value, operands=operands))
    return equations


def get_valid_values(input_data, valid_operators):
    valid_values = []
    for equation in input_data:
        value, operands = equation.value, equation.operands
        for operators in product(valid_operators, repeat=len(operands) - 1):
            test_value = operands[0]
            for op, val in zip(operators, operands[1:]):
                test_value = op(test_value, val)
            if test_value == value:
                valid_values.append(value)
                break
    return valid_values


def concat(x, y):
    y_num_digits = int(log10(y)) + 1
    return x * 10**y_num_digits + y


def part1(input_data: list[Equation]) -> int:
    """
    Given a list of equations with missing operands, work out where to put + and *,
    if possible. Return the sum of all values where an equation can be made.

    Operators are evaluated left to right.
    """
    valid_values = get_valid_values(input_data, valid_operators=(add, mul))
    return sum(valid_values)


def part2(input_data: list[Equation]) -> int:
    """
    As above, but now we have concats
    """
    valid_values = get_valid_values(input_data, valid_operators=(add, mul, concat))
    return sum(valid_values)


test_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

assert (part1_test := part1(parse_input(test_input))) == 3749, part1_test
assert (part2_test := part2(parse_input(test_input))) == 11387, part2_test

if __name__ == "__main__":
    with Path("inputs/day07.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
