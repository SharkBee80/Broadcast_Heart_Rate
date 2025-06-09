import os
from src.backend.mainform.get_path import get_path

directory = get_path("src/frontend/web")


class Web_page:
    def __init__(self):
        self.window = None

    def init(self, window):
        self.window = window

    def get_html_files(self):
        global directory
        dir = os.listdir(directory)
        html_files = {
            filename
            for filename in dir
            if filename.lower().endswith(".html")
        }
        return html_files


if __name__ == "__main__":
    web_page = Web_page()
    directory = get_path("../../../src/frontend/web")
    print(web_page.get_html_files())
