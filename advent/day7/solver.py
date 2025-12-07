import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient
from collections import defaultdict

START = "S"
SPLITTER = "^"
EMPTY = "."


@dataclass
class Input:
    grid: list[list[str]]
    start: tuple[int, int]


@dataclass
class StepResult:
    new_beams: dict[int, int]
    count: int


class Solver:
    def parse_input(self, input: str) -> Input:
        grid = [list(line.strip()) for line in input.strip().splitlines()]
        start: tuple[int, int] | None = None
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == START:
                    start = (i, j)

        if start is None:
            raise ValueError("Start position not found in the grid")
        return Input(grid=grid, start=start)

    def step(
        self, grid: list[list[str]], row: int, step_result: StepResult
    ) -> StepResult:
        new_beams = defaultdict(int)

        count = step_result.count

        for beam, paths in step_result.new_beams.items():
            if grid[row][beam] == SPLITTER:
                new_beams[beam - 1] += paths
                new_beams[beam + 1] += paths
                count += 1
            else:
                new_beams[beam] += paths

        return StepResult(new_beams=new_beams, count=count)

    def solve_part1(self, data: Input) -> str:
        current_beams = StepResult(new_beams={data.start[1]: 1}, count=0)

        for r in range(data.start[0] + 1, len(data.grid)):
            current_beams = self.step(data.grid, r, current_beams)

        return str(current_beams.count)

    def solve_part2(self, data: Input) -> str:
        current_beams = StepResult(new_beams={data.start[1]: 1}, count=0)

        for r in range(data.start[0] + 1, len(data.grid)):
            current_beams = self.step(data.grid, r, current_beams)

        return str(sum([paths for paths in current_beams.new_beams.values()]))

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
