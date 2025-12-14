from .solver import Solver


def run(first_part: bool, expected: str):
    solver = Solver()
    test_path = __file__.replace("test_solver.py", "test.txt")
    result = solver.solve(test_path, first_part=first_part)
    assert result == expected


def test_part1():
    run(True, "7")


def test_part2():
    run(False, "33")
