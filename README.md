# Advent

My solutions to the Advent of Code 2025 challenges.

## Setup
All solutions are created using a template from the [/advent/template](./advent/template) folder.
In order to generate packages for each day, first copy the [.env.example](./.env.example) file to .env and set the `COOKIE` variable to your Advent of Code session cookie (you can snatch this from your browser after logging in to Advent of Code).
It should look something like this:

```
COOKIE="_ga=GA1.XXX; _gid=GA1.2.XXX; session=XXX; _ga_MHSNPJKWC7=XXX"
```

Then run the following command to create folder structure for all the days up to today.

```bash
uv run advent/initializer.py
```

Note that you might need to rerun this setup when a new day is unlocked.

This will create folders like `./advent/day1`, `./advent/day2`, etc. with the necessary files to get started.
It will also download the task input to `data.txt`, and task description to `task.html`. It also create `test.txt` file for you to add the test input from the task. These are used by the [template code to run tests](./advent/template/test_solver.py). The [solver itself](./advent/template/solver.py) has the setup for parsing inputs, solving both parts of the task, and the code to submit the answers.

## Running
To run tests for the day (day 1 used as an example), use the following command:

```bash
uv run python -m pytest advent/day1/test_solver.py
```

To run the part1 solver with the test input:

```bash
uv run advent/day1/solver.py 1 test.txt
```

To run the part2 solver with the actual input:

```bash
uv run advent/day1/solver.py 2 data.txt
```

## Submitting
To submit the answer for part 1 using the actual input:
```bash
uv run advent/day1/solver.py 1 data.txt submit
```
