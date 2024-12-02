"""
day02.py

Each row corresponds to a report, and each report has a number of levels.
A report is safe if:
  - the levels are all decreasing or all increasing
  - any two adjacent levels differ by at least one and at most three
"""

from pathlib import Path


def parse_input(input_str: str) -> list[list[int]]:
    return [
        [int(x) for x in line.strip().split()] for line in input_str.split("\n") if line
    ]


def is_safe(row: list[int]) -> bool:
    diff_set = {row[i] - row[i - 1] for i in range(1, len(row))}
    return diff_set <= {1, 2, 3} or diff_set <= {-1, -2, -3}


def part1(input_data: list[list[int]]) -> int:
    """
    Count the number of 'safe' levels
    """
    count = 0
    for row in input_data:
        count += is_safe(row)
    return count


def part2(input_data: list[list[int]]) -> int:
    """
    Count the number of 'safe' levels, where now if removing a single level makes it safe, then its safe.
    """
    count = 0
    for row in input_data:
        count += is_safe(row) or any(
            is_safe(row[:i] + row[i + 1 :]) for i in range(len(row))
        )
    return count


test_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

assert part1(parse_input(test_input)) == 2
assert part2(parse_input(test_input)) == 4

if __name__ == "__main__":
    with Path("inputs/day02.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
