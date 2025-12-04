import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient
from functools import cache


@dataclass
class Input:
    numbers: list[str]


class Solver:
    def parse_input(self, input: str) -> Input:
        lines = [line.strip() for line in input.strip().splitlines()]
        return Input(numbers=lines)

    def calculate_joltage(self, number: str) -> int:
        max_joltage = 0

        for i in range(9, 1, -1):
            if str(i) not in number:
                continue

            index = number.index(str(i))
            if index == len(number) - 1:
                joltage = i
            else:
                highest_after = max(int(digit) for digit in number[index + 1 :])
                joltage = i * 10 + highest_after
            if joltage > max_joltage:
                max_joltage = joltage
        return max_joltage

    @cache
    def calculate_joltage_recursive(self, number: str, depth: int = 2) -> int:
        if depth == 0:
            return 0

        if depth > len(number):
            return -1

        try:
            digit = number[0]
            next_number = number[1:]
            next_joltage_with = self.calculate_joltage_recursive(next_number, depth - 1)
            joltage_without = self.calculate_joltage_recursive(next_number, depth)
            joltage_with = int(digit) * (10 ** (depth - 1)) + next_joltage_with

            joltage = max(joltage_with, joltage_without)

            return joltage
        except:
            print(number, depth)
            raise

    def solve_part1(self, data: Input) -> str:
        total = 0
        for number in data.numbers:
            joltage = self.calculate_joltage_recursive(number, 2)
            total += joltage
        return str(total)

    def solve_part2(self, data: Input) -> str:
        total = 0
        for number in data.numbers:
            joltage = self.calculate_joltage_recursive(number, 12)
            total += joltage
        return str(total)

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
