import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient


@dataclass
class Input:
    grid: list[list[str]]


class Solver:
    def __init__(self):
        self.directions = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                self.directions.append((i, j))

    def parse_input(self, input: str) -> Input:
        lines = input.strip().splitlines()
        grid = [list(line.strip()) for line in lines]

        return Input(grid=grid)

    def count_around(self, grid: list[list[str]], r: int, c: int) -> int:
        count = 0
        for dr, dc in self.directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if grid[nr][nc] == "@":
                    count += 1
        return count

    def remove_possible(self, data: Input) -> int:
        count = 0
        for r, row in enumerate(data.grid):
            for c, _ in enumerate(row):
                around = self.count_around(data.grid, r, c)
                if around < 4 and data.grid[r][c] == "@":
                    count += 1
                    data.grid[r][c] = "."
        return count

    def solve_part1(self, data: Input) -> str:
        count = 0
        for r, row in enumerate(data.grid):
            for c, _ in enumerate(row):
                around = self.count_around(data.grid, r, c)
                if around < 4 and data.grid[r][c] == "@":
                    count += 1
        return str(count)

    def solve_part2(self, data: Input) -> str:
        count = 0
        while True:
            removed = self.remove_possible(data)
            if removed == 0:
                break
            count += removed
        return str(count)

    def solve(self, input_file: str, first_part: bool) -> str:
        with open(input_file, "r") as f:
            input_data = f.read()
        data = self.parse_input(input_data)
        return self.solve_part1(data) if first_part else self.solve_part2(data)


if __name__ == "__main__":
    load_dotenv()
    solver = Solver()

    folder = __file__.split("/")[-2]

    input_file = __file__.replace("solver.py", sys.argv[1])
    part_one = int(sys.argv[2]) == 1
    should_submit = len(sys.argv) > 3

    solution = solver.solve(input_file=input_file, first_part=part_one)
    print("Solution:", solution)

    if should_submit:
        client = AdventClient()
        day = int(folder.replace("day", ""))

        response = client.submit_response(
            day=day, level=1 if part_one else 2, answer=solution
        )
        print("Submission Response:", response)
