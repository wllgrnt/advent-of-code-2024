"""
dayxx.py

"""

from pathlib import Path


def parse_input(input_str: str) -> list[list[int]]:
    pass


def part1(input_data: list[list[int]]) -> int:
    return 0


def part2(input_data: list[list[int]]) -> int:
    return 0


test_input = """
"""

assert (part1_test := part1(parse_input(test_input))) == 0, part1_test
assert (part2_test := part2(parse_input(test_input))) == 0, part2_test

if __name__ == "__main__":
    with Path("inputs/dayxx.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
