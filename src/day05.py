"""
day05.py

Check lists of numbers and a required ordering, and return the middle values of 
all correctly-ordered lists, summed. 
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass
class Ordering:
    left: int
    right: int

    @classmethod
    def from_str(cls, input_str):
        left, right = input_str.split("|")
        return Ordering(left=int(left), right=int(right))

def parse_input(input_str: str) -> tuple[list[Ordering], list[list[int]]]:
    ordering_str, pages_str = input_str.split("\n\n")
    orderings = [Ordering.from_str(row.strip()) for row in ordering_str.split("\n") if row]
    pages = [[int(x) for x in row.strip().split(",")] for row in pages_str.split("\n") if row]

    return orderings, pages

def is_valid(page_row: list[int], orderings: list[Ordering]):
    """Suboptimal perf to start - check each ordering against the list"""
    page_set = set(page_row)
    for ordering in orderings:
        if ordering.left in page_set and ordering.right in page_set:
            if page_row.index(ordering.left) > page_row.index(ordering.right):
                return False
    return True

def part1(input_data: tuple[list[Ordering], list[list[int]]]) -> int:
    """Check all rows against the required orderings. For all good rows, sum the middle row value."""
    orderings, page_rows = input_data

    valid_row_sum = 0
    for page_row in page_rows:
        if is_valid(page_row, orderings):
            valid_row_sum += page_row[len(page_row)//2]
        
    return valid_row_sum


def reorder(page_row: list[int], orderings: list[Ordering]) -> int:
    """
    Given a bad page_row, work out what orderings apply and reorder <page_row> to be valid accordingly.
    """
    page_set = set(page_row)
    applicable_orderings = [ordering for ordering in orderings if ordering.left in page_set and ordering.right in page_set]
    grouped_orderings = {}
    for ordering in applicable_orderings:
        grouped_orderings[ordering.left] = grouped_orderings.get(ordering.left,[]) + [ordering.right]
    sorted_orderings = sorted(grouped_orderings.items(), key=lambda x: len(x[1]), reverse=True)
    reordered = []
    for val, _ in sorted_orderings:
        reordered.append(val)
        page_set.remove(val) 

    assert len(page_set) == 1, page_set
    reordered.append(page_set.pop())
    return reordered


def part2(input_data: tuple[list[Ordering], list[list[int]]]) -> int:
    """Check all rows against the required orderings. For all bad rows, rearrange them so they're good.
    
    Return the sum of the middle row values for the rearranged rows.
    """
    orderings, page_rows = input_data

    invalid_row_sum = 0
    for page_row in page_rows:
        if not is_valid(page_row, orderings):
            
            rearranged_page_row = reorder(page_row, orderings)

            invalid_row_sum += rearranged_page_row[len(rearranged_page_row)//2]
        
    return invalid_row_sum

test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

assert (part1_test := part1(parse_input(test_input))) == 143, part1_test
assert (part2_test := part2(parse_input(test_input))) == 123, part2_test

if __name__ == "__main__":
    with Path("inputs/day05.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
