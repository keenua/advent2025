import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient
from math import copysign


@dataclass
class Input:
    raw_data: str


class Solver:
    def parse_input(self, input: str) -> Input:
        return Input(raw_data=input)

    def solve_part1(self, data: Input) -> str:
        return "Not implemented yet"

    def solve_part2(self, data: Input) -> str:
        return "Not implemented yet"

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
