"""
day10.py

Given a 2d array of ints representing height at each x,y (i.e a topographic map), generate
paths of up-down-left-right that start at height 0, end at height 9, and always increase by 1 each time.

Part 1: For each trailhead (point with z=0), find the number of valid paths - sum the total number
"""

from collections import deque
import numpy as np
from pathlib import Path


def parse_input(input_str: str) -> np.array:
    return np.array(
        [[int(x) for x in line] for line in input_str.split("\n") if line], dtype=int
    )


def get_neighbours(m, n, i, j):
    neighbours = []
    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        candidate_i, candidate_j = i + direction[0], j + direction[1]
        if 0 <= candidate_i < m and 0 <= candidate_j < n:
            neighbours.append((candidate_i, candidate_j))
    return neighbours


def find_trails(matrix: np.array, start_i: int, start_j: int, visited_track) -> int:
    """Bfs to find trails"""
    m, n = matrix.shape
    trails = 0
    queue = deque()
    visited = set()
    queue.append((start_i, start_j, 0))
    if visited_track:
        visited.add((start_i, start_j))
    while queue:
        i, j, val = queue.popleft()
        if val == 9:
            trails += 1
            continue
        for next_i, next_j in get_neighbours(m, n, i, j):
            if matrix[next_i, next_j] == val + 1 and (
                not visited_track or (next_i, next_j) not in visited
            ):
                queue.append((next_i, next_j, val + 1))
                if visited_track:
                    visited.add((next_i, next_j))

    return trails


def part1(input_data: np.array) -> int:
    """From each zero, find the number of reachable nines. Return the total number"""
    zero_locs = np.argwhere(input_data == 0)
    num_valid_trails = 0
    for i, j in zero_locs:
        num_valid_trails += find_trails(input_data, i, j, visited_track=True)
    return num_valid_trails


def part2(input_data: np.array) -> int:
    """From each zero, find the number of valid paths. Return the total number"""
    zero_locs = np.argwhere(input_data == 0)
    num_valid_trails = 0
    for i, j in zero_locs:
        num_valid_trails += find_trails(input_data, i, j, visited_track=False)
    return num_valid_trails


test_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

assert (part1_test := part1(parse_input(test_input))) == 36, part1_test
assert (part2_test := part2(parse_input(test_input))) == 81, part2_test

if __name__ == "__main__":
    with Path("inputs/day10.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
