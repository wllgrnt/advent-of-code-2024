"""
day11.py

stones that change every timestep.stone rules:
1. if a stone is engraved with the number 0, it is replaced with a stone with number 1
2. if the stone has an even number of digits, it splits into two [left half of digits, right half of digits]
3. otherwise, replace with val*2024.

Part 1 and 2 are only distinguished by runtime.
"""
import math
from pathlib import Path
from tqdm import tqdm

def parse_input(input_str: str) -> list[int]:
    return [int(x.strip()) for x in input_str.split()]

def run_game(stones: list[int]) -> None:
    new_stones = []
    for i,stone in enumerate(stones):
        if stone == 0:
            stones[i] = 1
        elif (num_digits := math.floor(math.log10(stone)) +1) % 2 == 0:
            stones[i] = stone // 10**(num_digits // 2)
            new_stones.append(stone % 10 **(num_digits // 2))
        else:
            stones[i] = stone*2024
    stones.extend(new_stones)

def part1(input_data: list[int], steps: int) -> int:
    """Run the stones <steps> times"""
    for _ in tqdm(range(steps)):
        run_game(input_data)
    
    return len(input_data)
    


def part2(input_data: list[int]) -> int:
    return 0


test_input = "125 17"

assert (part1_test := part1(parse_input(test_input), steps=6)) ==22, part1_test
assert (part1_test := part1(parse_input(test_input), steps=25)) == 55312, part1_test

if __name__ == "__main__":
    with Path("inputs/day11.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data.copy(), 25)}")
    print(f"part 2: {part1(data, 75)}")
