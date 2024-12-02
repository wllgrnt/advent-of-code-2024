"""
day01.py

Part one: pair up the smallest number in the left list with the smallest number in the right list, then second-smallest, etc etc.
Add up all the pairwise differences and return the sum.

Part two: calculate the similarity score by adding up each number in the left list * the number of occurrences of that number in the right list.
"""

from collections import Counter


def parse_input(input_str: str) -> list[list[int]]:
    """Return two lists of ints: the left-hand numbers, and the right-hand numbers."""
    left = []
    right = []
    for line in input_str.split("\n"):
        if line:
            left_val, right_val = line.strip().split()
            left.append(int(left_val))
            right.append(int(right_val))
    return [left, right]


def part1(input_data: list[list[int]]) -> int:
    left, right = input_data
    return sum(abs(x - y) for x, y in zip(sorted(left), sorted(right)))


def part2(input_data: list[list[int]]) -> int:
    left, right = input_data
    right_counts = Counter(right)
    return sum(val * right_counts[val] for val in left)


test_input = """
3   4
4   3
2   5
1   3
3   9
3   3"""

assert part1(parse_input(test_input)) == 11
assert part2(parse_input(test_input)) == 31

if __name__ == "__main__":
    with open("inputs/day01.txt") as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
