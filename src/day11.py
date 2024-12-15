"""
day11.py

stones that change every timestep.stone rules:
1. if a stone is engraved with the number 0, it is replaced with a stone with number 1
2. if the stone has an even number of digits, it splits into two [left half of digits, right half of digits]
3. otherwise, replace with val*2024.

Part 1 and 2 are only distinguished by runtime. Cache is doing all the work here.
"""

import math
from functools import cache
from pathlib import Path


def parse_input(input_str: str) -> list[int]:
    return [int(x.strip()) for x in input_str.split()]


@cache
def analyze_growth(stone: int, steps: int) -> int:
    """Analyze how many stones a single stone will produce after n steps"""
    if steps == 0:
        return 1

    if stone == 0:
        return analyze_growth(1, steps - 1)

    num_digits = math.floor(math.log10(stone)) + 1
    if num_digits % 2 == 0:
        # When splitting, we get two new stones
        left = stone // 10 ** (num_digits // 2)
        right = stone % 10 ** (num_digits // 2)
        return analyze_growth(left, steps - 1) + analyze_growth(right, steps - 1)
    else:
        # When multiplying by 2024, we get a larger number
        return analyze_growth(stone * 2024, steps - 1)


def part1(input_data: list[int], steps: int) -> int:
    """Calculate final stone count analytically"""
    total = 0
    for stone in input_data:
        total += analyze_growth(stone, steps)
    return total


test_input = "125 17"

assert (part1_test := part1(parse_input(test_input), steps=6)) == 22, part1_test
assert (part1_test := part1(parse_input(test_input), steps=25)) == 55312, part1_test

if __name__ == "__main__":
    with Path("inputs/day11.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data.copy(), 25)}")
    print(f"part 2: {part1(data, 75)}")
