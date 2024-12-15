"""
day09.py

Given a disk map that alternates number of file blocks, number of blocks of free space, etc,
and where each file's ID is its order in the map, move file blocks from the right to free space
on the left one at a time, then calculate a checksum.

For part 2, move whole blocks.
"""

import numpy as np
from pathlib import Path


def parse_input(input_str: str) -> np.array:
    """Return a list of occupied and free blocks"""
    array_length = sum(int(char) for char in input_str)

    disk = np.empty(array_length, dtype=int)
    disk[:] = -1
    is_occupied = True
    occupied_id = 0
    cursor = 0
    for char in input_str:
        if not char.isdigit():
            raise ValueError(f"expected digit, got {char}")
        if is_occupied:
            disk[cursor : cursor + int(char)] = occupied_id
            is_occupied = False
            occupied_id += 1
        else:
            is_occupied = True

        cursor += int(char)

    return disk

    # input alternates between occupied and free
    # occupied = []
    # free = []
    # is_occupied = True
    # occupied_id = 0
    # cursor = 0
    # for char in input_str:
    #     if not char.isdigit():
    #         raise ValueError(f"expected digit, got {char}")
    #     if is_occupied:
    #         occupied.append(File(id=occupied_id, ranges=[Range(start=cursor, end=cursor+int(char))]))
    #         is_occupied = False
    #         occupied_id += 1
    #     else:
    #         free.append(Range(start=cursor, end=cursor+int(char)))
    #         is_occupied = True

    #     cursor += int(char)
    # return free, occupied


def checksum(disk: np.array) -> int:
    checksum_val = 0
    for position, block_id in enumerate(disk):
        if block_id == -1:
            continue
        checksum_val += position * block_id
    return checksum_val


def part1(input_data: np.array) -> int:
    """Move file blocks from the right into free space on the left.
    Then return the sum of id*position for all occupied blocks.

    I actually think its easiest to make the whole disk here.
    """
    # move the blocks, very stupidly
    block_tracker = len(input_data) - 1
    free_space = list(np.where(input_data == -1)[0])[::-1]
    while free_space and free_space[-1] < block_tracker:
        free_cursor = free_space.pop(-1)
        input_data[block_tracker], input_data[free_cursor] = (
            input_data[free_cursor],
            input_data[block_tracker],
        )

        block_tracker -= 1
        while input_data[block_tracker] == -1 and block_tracker > 0:
            block_tracker -= 1

    return checksum(input_data)


def part2(input_data: np.array) -> int:
    """As in part 1 but now move whole blocks."""
    free_space = np.where(input_data == -1)[0]
    for block_id in range(np.max(input_data), -1, -1):
        block_indices = np.where(input_data == block_id)[0]
        if len(block_indices) == 0:
            continue
        block_size = len(block_indices)

        for i in range(len(free_space) - block_size + 1):
            if np.all(
                np.diff(free_space[i : i + block_size]) == 1
            ):  # Check for contiguous free space
                target_indices = free_space[i : i + block_size]
                if (
                    target_indices[0] < block_indices[0]
                ):  # Only move if it's to the left
                    input_data[block_indices] = -1
                    input_data[target_indices] = block_id
                    free_space = np.where(input_data == -1)[0]
                break

    return checksum(input_data)


test_input = "2333133121414131402"

assert (part1_test := part1(parse_input(test_input))) == 1928, part1_test
assert (part2_test := part2(parse_input(test_input))) == 2858, part2_test

if __name__ == "__main__":
    with Path("inputs/day09.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data.copy())}")
    print(f"part 2: {part2(data)}")
