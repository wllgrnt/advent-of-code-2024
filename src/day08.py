"""
day08.py

Given a map of antennae, find the antinodes.
Part one: Antinodes occur where the distance from antenna A is double antenna B, in a straight line, i.e. like lagrange points.
Part two: Antinodes occur on every point in a straight line along the two antennas, i.e wherever i,j are both integers along the line.

"""

from pathlib import Path
from collections import defaultdict


def parse_input(input_str: str):
    antenna_locs: dict[str, tuple[int, int]] = defaultdict(list)
    for i, line in enumerate(input_str.split("\n")):
        if line:
            for j, letter in enumerate(line):
                if letter != ".":
                    antenna_locs[letter].append((i, j))

    m = len([line for line in input_str.split("\n") if line])
    n = len(input_str.split("\n")[0])
    return antenna_locs, (m, n)


def find_antinodes(loc, other_loc, m, n):
    # there are two locations of antinodes for each pair of antenna
    i1, j1 = loc
    i2, j2 = other_loc
    delta_i, delta_j = i2 - i1, j2 - j1
    antinodes = []
    for antinode_i, antinode_j in [
        (i2 + delta_i, j2 + delta_j),
        (i1 - delta_i, j1 - delta_j),
    ]:
        if 0 <= antinode_i < m and 0 <= antinode_j < n:
            antinodes.append((antinode_i, antinode_j))

    return antinodes


def is_integer(x: float, epsilon: float = 1e-10) -> bool:
    return abs(round(x) - x) < epsilon


def find_antinodes_along_line(loc, other_loc, m, n):
    # there is a line of possible antinode locations of antinodes for each pair of antenna
    # work out the equation y = mx+c where x goes from 0 to m, storing values where y is integer.
    i1, j1 = loc
    i2, j2 = other_loc
    delta_i, delta_j = i2 - i1, j2 - j1
    grad = delta_j / delta_i
    c = j2 - grad * i2
    antinodes = []
    for x in range(0, m):
        y = grad * x + c
        if is_integer(y) and 0 <= round(y) < n:
            antinodes.append((x, round(y)))
    return antinodes


def part1(input_data) -> int:
    """Two antinodes for each pair of antennae."""
    antenna_locs, (m, n) = input_data
    # for all pairs of antenna locations, find the antinodes.
    antinode_locs = set()
    for letter, locations in antenna_locs.items():
        # print(letter, locations)
        for i, loc in enumerate(locations):
            for other_loc in locations[:i]:
                # print(loc, other_loc, end=' ')
                antinodes = find_antinodes(loc, other_loc, m, n)
                # print(antinodes)
                antinode_locs.update(antinodes)

    return len(antinode_locs)


def part2(input_data) -> int:
    """A line of antinodes for each pair of antennae."""
    antenna_locs, (m, n) = input_data
    antinode_locs = set()
    for _, locations in antenna_locs.items():
        for i, loc in enumerate(locations):
            for other_loc in locations[:i]:
                antinodes = find_antinodes_along_line(loc, other_loc, m, n)
                antinode_locs.update(antinodes)
    return len(antinode_locs)


test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

assert (part1_test := part1(parse_input(test_input))) == 14, part1_test
assert (part2_test := part2(parse_input(test_input))) == 34, part2_test

if __name__ == "__main__":
    with Path("inputs/day08.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
