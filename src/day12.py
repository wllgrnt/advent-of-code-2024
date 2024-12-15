"""
day12.py

Given a 2d array of chars, separate the different distint chars into regions, and find the area and perimeter of each region.

"""

from collections import deque
import numpy as np
from pathlib import Path


def parse_input(input_str: str) -> np.array:
    return np.array([list(row) for row in input_str.split("\n") if row])


def get_neighbours(map, index):
    m, n = map.shape
    neighbours = []
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        candidate_i, candidate_j = index[0] + direction[0], index[1] + direction[1]
        if 0 <= candidate_i < m and 0 <= candidate_j < n:
            neighbours.append((candidate_i, candidate_j))
    return neighbours


def find_region(map, visited, index):
    """bfs starting from <index> looking for area with the same value."""
    queue = deque()
    val = map[index]
    queue.append(index)
    region = [index]
    visited[index] = True
    while queue:
        index = queue.popleft()
        neighbours = get_neighbours(map, index)
        for neighbour in neighbours:
            if not visited[neighbour] and map[neighbour] == val:
                queue.append(neighbour)
                visited[neighbour] = True
                region.append(neighbour)
    return region


def get_regions(map: np.array) -> list[np.array]:
    # return a list of regions where each region is defined by an array of indices.
    visited = np.zeros(map.shape, dtype=bool)
    regions = []
    for index, value in np.ndenumerate(map):
        if not visited[index]:
            regions.append(find_region(map, visited, index))

    return regions


def get_price(map, region) -> int:
    area = len(region)
    perimeter = 0
    for index in region:
        for neighbour in get_neighbours(map, index):
            if map[index] != map[neighbour]:
                perimeter += 1
        if index[0] == 0 or index[0] == map.shape[0] - 1:
            perimeter += 1
        if index[1] == 0 or index[1] == map.shape[1] - 1:
            perimeter += 1
    return area * perimeter


def part1(input_data: np.array) -> int:
    regions = get_regions(input_data)
    total_price = sum(get_price(input_data, region) for region in regions)
    return total_price


def part2(input_data: np.array) -> int:
    return 0


test_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

assert (part1_test := part1(parse_input(test_input))) == 1930, part1_test
assert (part2_test := part2(parse_input(test_input))) == 0, part2_test

if __name__ == "__main__":
    with Path("inputs/day12.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
