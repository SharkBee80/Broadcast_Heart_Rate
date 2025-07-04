import json
import os

from src.backend.mainform.get_path import get_path

temper = get_path("src/frontend/web")
directory = get_path("", config_dir="web", use_mei_pass=False, create_base_dir=False)
print(directory)
if os.path.exists(directory):
    folder_path = os.listdir(directory)
else:
    folder_path = os.listdir(temper)

priority_order = ['.png', '.jpg', '.jpeg', '.webp', '.gif']
DEFAULT_IMAGE = 'none.png'


class Web_page:
    def __init__(self):
        self.window = None

    def init(self, window):
        self.window = window

    def set_(self):
        self.window.evaluate_js(f"set_html_files({json.dumps(self.get_html_files())})")
        if not os.path.exists(directory):
            self.window.evaluate_js(r"""
            document.querySelector('#choice-4 .bg-f').innerHTML = "在程序目录添加web文件夹来自定义"; 
            """)


    def get_html_files(self):
        html_files = []
        for file in folder_path:
            if file.endswith(".html"):
                filename = os.path.splitext(file)[0]
                image = self.get_images_with_priority(filename)
                html_files.append({'name': filename, 'html': file, 'image': image})
        return html_files

    def get_images_with_priority(self, filename):
        images = DEFAULT_IMAGE
        for priority in priority_order:
            image_file = filename + priority
            if image_file in folder_path:
                images = image_file
                break
        return images


if __name__ == "__main__":
    web_page = Web_page()
    temper = get_path("../../../src/frontend/web")
    folder_path = os.listdir(temper)
    print(web_page.get_html_files())
