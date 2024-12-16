"""
day13.py

A claw machine where it costs 3 tokens to push A, and 1 to push B. These buttons move a specific +x, +y amount.
Each machine has a prize. What is the minimum number of tokens to win the prize?
"""

from dataclasses import dataclass
from math import gcd
import numpy as np
from pathlib import Path
import re


@dataclass
class ClawMachine:
    a_translation: tuple[int, int]
    b_translation: tuple[int, int]
    prize_coords: tuple[int, int]

    def __hash__(self) -> int:
        return hash(self.a_translation + self.b_translation + self.prize_coords)


A_COST = 3
B_COST = 1


def parse_input(input_str: str) -> list[ClawMachine]:
    claw_machines = []
    for machine_str in input_str.split("\n\n"):
        try:
            a_str, b_str, prize_str = machine_str.split("\n")
        except ValueError:
            continue
        assert a_str.startswith("Button A:")
        assert b_str.startswith("Button B:")
        assert prize_str.startswith("Prize:")
        a_coords = tuple(int(x) for x in re.findall(r"(?<=\+)\d+", a_str))
        b_coords = tuple(int(x) for x in re.findall(r"(?<=\+)\d+", b_str))
        prize_coords = tuple(int(x) for x in re.findall(r"(?<=\=)\d+", prize_str))
        assert len(a_coords) == len(b_coords) == len(prize_coords) == 2
        claw_machine = ClawMachine(
            a_translation=a_coords, b_translation=b_coords, prize_coords=prize_coords
        )
        claw_machines.append(claw_machine)
    return claw_machines


def part1(input_data: list[ClawMachine]) -> int:
    """For each machine, get the minimum number of tokens required to win. Return the sum over all machines.

    (For some machines it will be impossible).

    I.e. minimise (3a+b) with the constraint that a*a_trans + b*b_trans = target

    Tried a DFS but hit recursion issues.
    """

    def min_tokens(machine):
        """below is very convoluted/"""
        if any(
            x % gcd(machine.a_translation[i], machine.b_translation[i]) != 0
            for i, x in enumerate(machine.prize_coords)
        ):
            return float("inf")

        # Track minimum cost for each position
        costs = {(0, 0): 0}
        # Use list of (cost, x, y) tuples, sorted by cost
        queue = [(0, 0, 0)]

        while queue:
            cost, x, y = queue.pop(0)

            # Skip if we've found a better path to this position
            if cost > costs[(x, y)]:
                continue

            if (x, y) == machine.prize_coords:
                return cost

            for (dx, dy), button_cost in [
                (machine.a_translation, A_COST),
                (machine.b_translation, B_COST),
            ]:
                new_x = x + dx
                new_y = y + dy
                new_pos = (new_x, new_y)
                new_cost = cost + button_cost

                # Skip if we've gone too far
                if (
                    new_x
                    > machine.prize_coords[0]
                    + max(machine.a_translation[0], machine.b_translation[0])
                    or new_y
                    > machine.prize_coords[1]
                    + max(machine.a_translation[1], machine.b_translation[1])
                    or new_x < 0
                    or new_y < 0
                ):
                    continue

                if new_pos not in costs or new_cost < costs[new_pos]:
                    costs[new_pos] = new_cost
                    insert_pos = 0
                    while insert_pos < len(queue) and queue[insert_pos][0] <= new_cost:
                        insert_pos += 1
                    queue.insert(insert_pos, (new_cost, new_x, new_y))

        return float("inf")

    total_cost = 0
    for machine in input_data:
        cost = min_tokens(machine)
        if cost != float("inf"):
            total_cost += cost

    return total_cost


def part2(input_data: list[ClawMachine], use_correction=True) -> int:
    """
    Now we actually have to do the minimisation:
        Minimise (3a+b) with the constraint that a*a_trans + b*b_trans = target

    Add 10000000000000 to the X, Y of the prize coords, then proceed as before.
    """
    correction_term = 10000000000000 if use_correction else 0

    def min_tokens(machine):
        """solve with numpy instead"""
        trans_matrix = np.column_stack((machine.a_translation, machine.b_translation))
        prize_coords = np.array(machine.prize_coords, dtype=np.int64) + correction_term
        solution = np.rint(np.linalg.solve(trans_matrix, prize_coords))
        if np.all(trans_matrix @ solution == prize_coords):
            return A_COST * solution[0] + B_COST * solution[1]
        else:
            return None

    total_cost = 0
    for machine in input_data:
        cost = min_tokens(machine)
        if cost is not None:
            total_cost += cost

    return int(total_cost)


test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

assert (part1_test := part1(parse_input(test_input))) == 480, part1_test
# assert (part2_test := part2(parse_input(test_input))) == 480, part2_test

if __name__ == "__main__":
    with Path("inputs/day13.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part2(data, use_correction=False)}")
    print(f"part 2: {part2(data)}")
