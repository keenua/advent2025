import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient
from shapely.geometry import Polygon

POINT = tuple[int, int]


@dataclass
class Input:
    red_tiles: list[POINT]


class Solver:
    def parse_input(self, input: str) -> Input:
        lines = input.strip().splitlines()
        points: list[POINT] = []
        for line in lines:
            x, y = line.split(",")
            points.append((int(x), int(y)))

        return Input(red_tiles=points)

    def area(self, a: POINT, b: POINT) -> int:
        return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

    def is_valid(self, a: POINT, b: POINT, polygon: Polygon) -> bool:
        min_x = min(a[0], b[0])
        max_x = max(a[0], b[0])
        min_y = min(a[1], b[1])
        max_y = max(a[1], b[1])

        inner_polygon = Polygon(
            [
                (min_x, min_y),
                (min_x, max_y),
                (max_x, max_y),
                (max_x, min_y),
            ]
        )

        return polygon.contains(inner_polygon)

    def solve_part1(self, data: Input) -> str:
        max_area = 0
        for i in range(len(data.red_tiles)):
            for j in range(i + 1, len(data.red_tiles)):
                a = data.red_tiles[i]
                b = data.red_tiles[j]
                area = self.area(a, b)
                if area > max_area:
                    max_area = area

        return str(max_area)

    def solve_part2(self, data: Input) -> str:
        max_area = 0
        polygon = Polygon(data.red_tiles)

        for i in range(len(data.red_tiles)):
            for j in range(i + 1, len(data.red_tiles)):
                a = data.red_tiles[i]
                b = data.red_tiles[j]
                if self.is_valid(a, b, polygon):
                    area = self.area(a, b)
                    if area > max_area:
                        max_area = area
        return str(max_area)

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
