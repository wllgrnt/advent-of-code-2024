"""
day06.py

Given a map of a guard's position (^) and obstructions (#), and knowledge that the guard starts off going up,
then turns right 90 on obstruction, then forwards, etc, either finding a cycle or leaving the map area, work
out the distinct positions visited by the guard.
"""

from itertools import cycle
import numpy as np
from pathlib import Path


direction_list = [(0, -1), (1,0), (0, 1), (-1,0)]
directions = cycle(direction_list)


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
    
def get_guard_positions(obstacles, guard_position) -> set:
    visited_coords_and_dir = set()
    visited_coords = set()
    guard_direction = next(directions)
    visited_coords.add(guard_position)
    visited_coords_and_dir.add((guard_position, guard_direction))

    # keep looping until we see the same coords and direction, or fall off the map.
    m, n = obstacles.shape
    while True:
        candidate_x, candidate_y = guard_position[0] + guard_direction[0],  guard_position[1] + guard_direction[1]
        if not (0 <= candidate_x < m and 0 <= candidate_y < n):
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
    return visited_coords_and_dir


def part1(input_data: list[list[int]]) -> int:
    """
    Simulate the movement of the guard, counting all distinct positions.
    """
    obstacles, guard_position = input_data
    visited_coords_and_dir = get_guard_positions(obstacles, guard_position)
    return len(set(pos for pos, dir in visited_coords_and_dir))



def check_for_loop(obstacles: np.ndarray, guard_position: tuple[int, int]) -> bool:
    """
    Run guard simulation and check if it enters a loop.
    Returns True if a loop is detected, False if guard exits map.
    """
    visited_coords_and_dir = set()
    guard_direction = next(directions)  # Start going up
    visited_coords_and_dir.add((guard_position, guard_direction))
    
    m, n = obstacles.shape
    while True:
        # Check next position
        candidate_x = guard_position[0] + guard_direction[0]
        candidate_y = guard_position[1] + guard_direction[1]
        
        # Exit if we're off the map
        if not (0 <= candidate_x < m and 0 <= candidate_y < n):
            return False
            
        # If path is clear, move forward
        if not obstacles[candidate_x, candidate_y]:
            guard_position = (candidate_x, candidate_y)
        else:
            # Turn right
            guard_direction = next(directions)
        
        # If we've seen this position and direction before, we're in a loop
        state = (guard_position, guard_direction)
        if state in visited_coords_and_dir:
            return True
            
        visited_coords_and_dir.add(state)

def part2(input_data: tuple[np.ndarray, tuple[int, int]]) -> int:
    """
    For each position the guard visits (except starting position),
    try placing an obstruction there and check if it creates a loop.
    """
    original_obstacles, start_position = input_data
    
    # First get all positions the guard visits without modifications
    visited_coords_and_dir = get_guard_positions(original_obstacles, start_position)
    visited_positions = set(pos for pos, _ in visited_coords_and_dir)
    
    # Remove starting position as it's not allowed
    visited_positions.remove(start_position)
    
    # Try each position as a new obstacle
    loop_count = 0
    for pos in visited_positions:
        # Create new obstacle map with this position blocked
        obstacles = original_obstacles.copy()
        obstacles[pos] = True
        
        # Reset the directions iterator
        global directions
        directions = cycle(direction_list)
        
        # Check if this creates a loop
        if check_for_loop(obstacles, start_position):
            loop_count += 1
            
    return loop_count

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
assert (part2_test := part2(parse_input(test_input))) == 6, part2_test

if __name__ == "__main__":
    with Path("inputs/day06.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
