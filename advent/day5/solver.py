import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient


@dataclass
class Input:
    ranges: list[tuple[int, int]]
    ids: list[int]


class Solver:
    def parse_input(self, input: str) -> Input:
        ranges: list[tuple[int, int]] = []
        ids: list[int] = []

        is_ids_line = False

        for line in input.strip().splitlines():
            data = line.strip()

            if data == "":
                is_ids_line = True
                continue

            if is_ids_line:
                ids.append(int(data))
            else:
                parts = data.split("-")
                ranges.append((int(parts[0]), int(parts[1])))

        return Input(ranges=ranges, ids=ids)

    def solve_part1(self, data: Input) -> str:
        count = 0
        for id in data.ids:
            for start, end in data.ranges:
                if start <= id <= end:
                    count += 1
                    break
        return str(count)

    def solve_part2(self, data: Input) -> str:
        merged_ranges: list[tuple[int, int]] = []
        for start, end in sorted(data.ranges):
            if not merged_ranges or merged_ranges[-1][1] < start - 1:
                merged_ranges.append((start, end))
            else:
                merged_ranges[-1] = (
                    merged_ranges[-1][0],
                    max(merged_ranges[-1][1], end),
                )
        count = sum([end - start + 1 for start, end in merged_ranges])
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
