import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient


@dataclass
class Input:
    ranges: list[tuple[int, int]]


class Solver:
    def parse_range(self, line: str) -> tuple[int, int]:
        parts = line.split("-")
        return int(parts[0]), int(parts[1])

    def parse_input(self, input: str) -> Input:
        lines = input.strip().split(",")
        print(lines)
        ranges = [self.parse_range(line) for line in lines]
        return Input(ranges=ranges)

    def split_into_parts(self, number: int, parts: int) -> list[int]:
        number_str = str(number)
        part_length = len(number_str) // parts
        try:
            return [
                int(number_str[i * part_length : (i + 1) * part_length])
                for i in range(parts)
            ]
        except:
            print(part_length, parts, number_str)
            raise

    def count_invalids(self, start: int, end: int, only_two: bool) -> int:
        count = 0
        for number in range(start, end + 1):
            if number < 10:
                continue
            possible_parts = [2] if only_two else range(2, len(str(number)) + 1)
            for part_count in possible_parts:
                if len(str(number)) % part_count != 0:
                    continue
                parts = self.split_into_parts(number, part_count)

                if all(part == parts[0] for part in parts):
                    count += number
                    break

        return count

    def solve_part1(self, data: Input) -> str:
        sum = 0
        for start, end in data.ranges:
            sum += self.count_invalids(start, end, True)
        return str(sum)

    def solve_part2(self, data: Input) -> str:
        sum = 0
        for start, end in data.ranges:
            sum += self.count_invalids(start, end, False)
        return str(sum)

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
