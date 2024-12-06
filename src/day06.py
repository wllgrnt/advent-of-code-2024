"""
day06.py

Given a map of a guard's position (^) and obstructions (#), and knowledge that the guard starts off going up,
then turns right 90 on obstruction, then forwards, etc, either finding a cycle or leaving the map area, work
out the distinct positions visited by the guard.
"""

from itertools import cycle
import numpy as np
from pathlib import Path


def parse_input(input_str: str) -> tuple[np.array, tuple[int, int]]:
    """Return a 2d numpy array where element is True if theres an obstruction, along
    with the guards position."""
    # i'm sure you can do this casting more efficiently
    guard_map = np.array([list(line) for line in input_str.split('\n') if line])
    guard_position_ys, guard_position_xs = np.where(guard_map == '^')
    assert len(guard_position_xs) == len(guard_position_ys) == 1
    guard_position = (int(guard_position_xs[0]), int(guard_position_ys[0]))
    obstacles = guard_map == '#'
    return obstacles.T, guard_position
    


def part1(input_data: list[list[int]]) -> int:
    obstacles, guard_position = input_data
    visited_coords_and_dir = set()
    visited_coords = set()
    directions = cycle([(0, -1), (1,0), (0, 1), (-1,0)])
    guard_direction = next(directions)
    visited_coords.add(guard_position)
    visited_coords_and_dir.add((guard_position, guard_direction))

    # keep looping until we see the same coords and direction, or fall off the map.
    m, n = obstacles.shape
    while True:
        candidate_x, candidate_y = guard_position[0] + guard_direction[0],  guard_position[1] + guard_direction[1]
        if not (0 <= candidate_x < m) and (0 <= candidate_y < n):
            break
        try: 
            if not obstacles[candidate_x,candidate_y]:
                # step in direction            
                guard_position = (candidate_x, candidate_y)
            else:
                guard_direction = next(directions)
            
            if (guard_position, guard_direction) in visited_coords_and_dir:
                break
        except IndexError:
            break

        
        visited_coords.add(guard_position)
        visited_coords_and_dir.add((guard_position, guard_direction))
    return len(visited_coords)


def part2(input_data: list[list[int]]) -> int:
    return 0


test_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

assert (part1_test := part1(parse_input(test_input))) == 41, part1_test
assert (part2_test := part2(parse_input(test_input))) == 0, part2_test

if __name__ == "__main__":
    with Path("inputs/day06.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
