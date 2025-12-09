import sys
from dataclasses import dataclass
from typing import Callable

from dotenv import load_dotenv

from advent.initializer import AdventClient
from scipy.spatial.distance import cdist
import numpy as np

POINT = tuple[int, int, int]
CIRCUITS = dict[int, set[POINT]]


@dataclass
class Input:
    points: list[POINT]


class Solver:
    def parse_input(self, input: str) -> Input:
        lines = input.strip().splitlines()
        points = []
        for line in lines:
            parts = line.strip().split(",")
            x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
            points.append((x, y, z))
        return Input(points=points)

    def merge_closest(
        self, stop_check: Callable[[int, CIRCUITS], bool], data: Input
    ) -> tuple[CIRCUITS, POINT, POINT]:
        dists = cdist(data.points, data.points, metric="euclidean")
        circuits: CIRCUITS = {}
        circuit_mapping: dict[POINT, int] = {}
        for index, point in enumerate(data.points):
            circuit_mapping[point] = index
            circuits[index] = {point}

        np.fill_diagonal(dists, np.inf)
        attempt = 0
        while True:
            a, b = np.unravel_index(np.argmin(dists), dists.shape)
            dists[a, b] = np.inf
            dists[b, a] = np.inf

            a_island = circuit_mapping.get(data.points[a], -1)
            b_island = circuit_mapping.get(data.points[b], -1)

            if a_island == b_island:
                pass
            else:
                circuits[a_island].update(circuits[b_island])
                for point in circuits[b_island]:
                    circuit_mapping[point] = a_island
                del circuits[b_island]
            attempt += 1
            if stop_check(attempt, circuits):
                break
        return circuits, data.points[a], data.points[b]

    def solve_part1(self, data: Input) -> str:
        attempts = 10 if len(data.points) < 1000 else 1000

        circuits, _, _ = self.merge_closest(
            stop_check=lambda attempt, _: attempt >= attempts,
            data=data,
        )

        top_circuits = sorted(circuits.values(), key=lambda x: len(x), reverse=True)[:3]

        result = 1
        for island in top_circuits:
            result *= len(island)
        return str(result)

    def solve_part2(self, data: Input) -> str:
        _, a, b = self.merge_closest(
            stop_check=lambda _, circuits: len(circuits) == 1,
            data=data,
        )

        return str(a[0] * b[0])

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
