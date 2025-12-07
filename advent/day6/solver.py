import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from advent.initializer import AdventClient


@dataclass
class Expression:
    values: list[int]
    operation: str

    def eval(self) -> int:
        if self.operation == "+":
            return sum(self.values)
        elif self.operation == "*":
            result = 1
            for value in self.values:
                result *= value
            return result
        else:
            raise ValueError(f"Unknown operation: {self.operation}")


@dataclass
class Input:
    expressions: list[Expression]
    column_expressions: list[Expression]


class Solver:
    def parse_input(self, input: str) -> Input:
        lines = [line for line in input.splitlines() if line.strip()]
        rows = [row.split() for row in lines if row.split()]
        expressions: list[Expression] = []

        expression_count = len(rows[0])

        for i in range(expression_count):
            values = [int(row[i]) for row in rows[:-1]]
            operation = rows[-1][i]
            expressions.append(Expression(values=values, operation=operation))

        operation_line = lines[-1]

        current_values: list[int] = []
        current_operation = ""
        column_expressions: list[Expression] = []

        for i in range(len(operation_line)):
            if operation_line[i] in ("+", "*"):
                if current_values:
                    column_expressions.append(
                        Expression(values=current_values, operation=current_operation)
                    )
                current_values = []
                current_operation = operation_line[i]

            column = [line[i] for line in lines[:-1]]

            number = "".join(column)
            if number.strip() == "":
                continue

            current_values.append(int(number))

        if current_values:
            column_expressions.append(
                Expression(values=current_values, operation=current_operation)
            )
        return Input(expressions=expressions, column_expressions=column_expressions)

    def evaluate_expressions(self, expressions: list[Expression]) -> int:
        result = 0
        for expression in expressions:
            result += expression.eval()
        return result

    def solve_part1(self, data: Input) -> str:
        return str(self.evaluate_expressions(data.expressions))

    def solve_part2(self, data: Input) -> str:
        return str(self.evaluate_expressions(data.column_expressions))

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
