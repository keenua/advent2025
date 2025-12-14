from datetime import datetime
from os import getenv, listdir, makedirs
from os.path import exists, join, isfile

from dotenv import load_dotenv
from requests import Response, get, post
from shutil import copyfile
from selectolax.lexbor import LexborHTMLParser


class AdventClient:
    def __init__(self):
        self.cookie = getenv("COOKIE")
        self.base_url = "https://adventofcode.com/2025"
        self.headers = {"Cookie": f"session={self.cookie}"}

    def _get_request(self, day: int, path: str) -> Response:
        url = f"{self.base_url}/day/{day}"
        if path:
            url += f"/{path}"
        response: Response = get(url, headers=self.headers)
        response.raise_for_status()
        return response

    def _post_request(self, day: int, path: str, data: dict) -> Response:
        url = f"{self.base_url}/day/{day}/{path}"
        response: Response = post(url, headers=self.headers, data=data)
        response.raise_for_status()
        return response

    def get_input(self, day: int) -> str:
        return self._get_request(day, "input").text

    def get_task(self, day: int) -> str:
        html = self._get_request(day, "").text
        parser = LexborHTMLParser(html)
        article = parser.css_first("article.day-desc")
        if article is None or not article.inner_html:
            raise ValueError(f"Could not find task description for day {day}")

        return article.inner_html

    def submit_response(self, day: int, level: int, answer: str) -> str:
        data = {"level": level, "answer": answer}
        html = self._post_request(day, "answer", data).text
        parser = LexborHTMLParser(html)
        message = parser.css_first("article")
        return message.text() if message else "No response message found"


class AdventInitializer:
    def __init__(self):
        self.client = AdventClient()

    def initialize_day(self, day: int):
        day_dir = f"advent/day{day}"

        if exists(day_dir):
            return

        makedirs(day_dir, exist_ok=True)

        template_dir = "advent/template"
        for filename in listdir(template_dir):
            src_file = join(template_dir, filename)

            if not isfile(src_file):
                continue
            dest_file = join(day_dir, filename)
            copyfile(src_file, dest_file)

        data_file = join(day_dir, "data.txt")

        if not exists(data_file):
            input_text = self.client.get_input(day)
            with open(data_file, "w") as f:
                f.write(input_text)

        task_file = join(day_dir, "task.html")
        task_text = self.client.get_task(day)
        with open(task_file, "w") as f:
            f.write(task_text)

    def initialize_all_days(self):
        now = datetime.now()
        current_day = 12 if now > datetime(now.year, 12, 12) else now.day

        for day in range(1, current_day + 1):
            self.initialize_day(day)


if __name__ == "__main__":
    load_dotenv()
    initializer = AdventInitializer()
    initializer.initialize_all_days()
