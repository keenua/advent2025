import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient
import re


@dataclass
class Node:
    name: str
    outputs: list[str]


@dataclass
class Input:
    nodes: dict[str, Node]


class Solver:
    def parse_input(self, input: str) -> Input:
        nodes: dict[str, Node] = {}
        for line in input.strip().splitlines():
            match = re.match(r"(\w+): (.+)", line)
            if not match:
                raise ValueError(f"Invalid line: {line}")
            name = match.group(1)
            outputs = match.group(2).split(" ")
            nodes[name] = Node(name=name, outputs=outputs)

        nodes["out"] = Node(name="out", outputs=[])
        return Input(nodes=nodes)

    def count_paths(
        self, data: Input, starting_node: str, path_must_contain: list[str]
    ) -> int:
        memo: dict[tuple[str, tuple[bool, ...]], int] = {}
        num_requirements = len(path_must_contain)

        def dp(node_name: str, requirements_seen: tuple[bool, ...]) -> int:
            if node_name == "out":
                return 1 if all(requirements_seen) else 0

            cache_key = (node_name, requirements_seen)
            if cache_key in memo:
                return memo[cache_key]

            if node_name not in data.nodes:
                return 0
            node = data.nodes[node_name]

            new_requirements = list(requirements_seen)
            for i, required_node in enumerate(path_must_contain):
                if node_name == required_node:
                    new_requirements[i] = True
            new_requirements = tuple(new_requirements)

            total_paths = sum(dp(child, new_requirements) for child in node.outputs)

            memo[cache_key] = total_paths
            return total_paths

        initial_state = tuple([False] * num_requirements)
        return dp(starting_node, initial_state)

    def solve_part1(self, data: Input) -> str:
        return str(self.count_paths(data, "you", []))

    def solve_part2(self, data: Input) -> str:
        return str(self.count_paths(data, "svr", ["dac", "fft"]))

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
