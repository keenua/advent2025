import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient
import re
from scipy.optimize import LinearConstraint, Bounds, milp
import numpy as np

lights_pattern = re.compile(r"\[([.#]+)\]")
buttons_pattern = re.compile(r"\(([\d,]+)\)")
joltage_pattern = re.compile(r"\{([\d,]+)\}")


@dataclass
class Machine:
    target_lights: list[bool]
    buttons: list[set[int]]
    joltage: list[int]


@dataclass
class Input:
    machines: list[Machine]


class Solver:
    def parse_machine(self, line: str) -> Machine:
        lights_match = lights_pattern.search(line)
        buttons_matches = buttons_pattern.findall(line)
        joltage_match = joltage_pattern.search(line)

        if not lights_match or not buttons_matches or not joltage_match:
            raise ValueError(f"Invalid machine line: {line}")

        target_lights = [c == "#" for c in lights_match.group(1)]
        buttons = [set(int(x) for x in match.split(",")) for match in buttons_matches]
        joltage = [int(x) for x in joltage_match.group(1).split(",")]

        return Machine(
            target_lights=target_lights,
            buttons=buttons,
            joltage=joltage,
        )

    def parse_input(self, input: str) -> Input:
        lines = input.strip().splitlines()

        machines = [self.parse_machine(line) for line in lines if line.strip()]

        return Input(machines=machines)

    def get_min_presses(self, machine: Machine) -> int:
        dp: dict[tuple[int, ...], list[bool]] = {}
        dp[(0,) * len(machine.buttons)] = [False] * len(machine.target_lights)

        presses = 0
        while True:
            presses += 1
            new_dp: dict[tuple[int, ...], list[bool]] = {}
            for state, lights in dp.items():
                for button_index in range(len(machine.buttons)):
                    new_state = list(state)
                    new_state[button_index] += 1
                    new_state_tuple = tuple(new_state)

                    new_lights = lights.copy()
                    for light_index in machine.buttons[button_index]:
                        new_lights[light_index] = not new_lights[light_index]

                    if new_state_tuple not in new_dp:
                        new_dp[new_state_tuple] = new_lights
                    else:
                        existing_lights = new_dp[new_state_tuple]
                        for i in range(len(existing_lights)):
                            existing_lights[i] = existing_lights[i] or new_lights[i]

                    if new_lights == machine.target_lights:
                        return presses
            dp = new_dp

    def get_min_presses_for_joltage(self, machine: Machine) -> int:
        n_buttons = len(machine.buttons)
        n_lights = len(machine.joltage)

        A = np.zeros((n_lights, n_buttons), dtype=int)
        for button_index, button in enumerate(machine.buttons):
            for light_index in button:
                A[light_index, button_index] = 1

        c = np.ones(n_buttons, dtype=int)

        bounds = Bounds(lb=0, ub=sum(machine.joltage))

        integrality = np.ones(n_buttons, dtype=bool)

        target_joltage = np.array(machine.joltage, dtype=int)
        constraints = LinearConstraint(A, lb=target_joltage, ub=target_joltage)  # type: ignore

        result = milp(
            c, constraints=constraints, bounds=bounds, integrality=integrality
        )

        if not result.success:
            raise ValueError("No solution found for joltage machine")

        return int(np.sum(result.x))

    def solve_part1(self, data: Input) -> str:
        total = 0
        for machine in data.machines:
            presses = self.get_min_presses(machine)
            total += presses
        return str(total)

    def solve_part2(self, data: Input) -> str:
        total = 0
        for machine in data.machines:
            presses = self.get_min_presses_for_joltage(machine)
            total += presses
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
