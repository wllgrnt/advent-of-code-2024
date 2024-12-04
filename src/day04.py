"""
day04.py

Part 1: Find occurrences of XMAS in a string (horizontal, vertical, diagonal, backwards)
Part 2: Find occurences of MAS, in an X shape
"""

from pathlib import Path


def parse_input(input_str: str) -> list[str]:
    return [line.strip() for line in input_str.split("\n") if line]


def get_string(input_data, start_coords, direction, match="XMAS") -> str:
    """Get the 4 letters starting from <start_coords> and ending with string of length 4"""
    size = len(match)
    chars = []
    i, j = start_coords
    m, n = len(input_data), len(input_data[0])
    try:
        for _ in range(size):
            if i < 0 or i >= m or j < 0 or j >= n:
                return False
            chars.append(input_data[i][j])
            i, j = i + direction[0], j + direction[1]
        return "".join(chars) == match

    except IndexError:
        return False


def part1(input_data: list[str]) -> int:
    """
    For each position in the input data, look if XMAS appears in any of the 8 possible directions.
    """
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    # assert len(directions) == len(set(directions)) == 8
    m, n = len(input_data), len(input_data[0])

    count = 0
    for i in range(m):
        for j in range(n):
            for direction in directions:
                count += get_string(input_data, (i, j), direction)

    return count


def part2(input_data: list[str]) -> int:
    """
    Look for two MAS, in the shape of an X. (MAS can be forward or backward)
    """
    m, n = len(input_data), len(input_data[0])
    count = 0
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            patch = [row[j - 1 : j + 2] for row in input_data[i - 1 : i + 2]]
            patch_diag_1 = "".join(patch[i][i] for i in range(3))
            patch_diag_2 = "".join(patch[i][2 - i] for i in range(3))
            count += patch_diag_1 in {"SAM", "MAS"} and patch_diag_2 in {"SAM", "MAS"}

    return count


test_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

assert (part1_test := part1(parse_input(test_input))) == 18, part1_test
assert (part2_test := part2(parse_input(test_input))) == 9, part2_test

if __name__ == "__main__":
    with Path("inputs/day04.txt").open() as flines:
        data = parse_input(flines.read())

    print(f"part 1: {part1(data)}")
    print(f"part 2: {part2(data)}")
