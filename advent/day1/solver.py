import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient
from math import copysign


@dataclass
class Input:
    rotations: list[int]


class Solver:
    def parse_rotation(self, line: str) -> int:
        direction = line[0]
        value = int(line[1:])
        return value if direction == "R" else -value

    def parse_input(self, input: str) -> Input:
        rotations = [self.parse_rotation(line) for line in input.strip().splitlines()]
        return Input(rotations=rotations)

    def solve_part1(self, data: Input) -> str:
        counter = 0

        start = 50
        position = start

        for rotation in data.rotations:
            position = (position + rotation) % 100
            if position == 0:
                counter += 1

        return str(counter)

    def solve_part2(self, data: Input) -> str:
        counter = 0

        start = 50
        position = start

        for rotation in data.rotations:
            prev_position = position

            full_rotations = abs(rotation) // 100
            counter += full_rotations

            rotation = rotation - full_rotations * 100 * int(copysign(1, rotation))
            new_position = position + rotation

            if new_position > 100:
                counter += 1

            if new_position < 0 and position != 0:
                counter += 1

            if new_position % 100 == 0 and position != 0:
                counter += 1

            position = new_position % 100

            print(
                f"From {prev_position} to {position} with rotation {rotation}, total {counter}"
            )

        return str(counter)

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
