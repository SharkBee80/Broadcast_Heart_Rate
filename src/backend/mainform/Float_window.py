import time

import webview


class FloatWindow:
    def __init__(self):
        self.window = None
        self.url = None
        self.float = None

    def init(self, window):
        self.window = window

    def set_url(self, url):
        self.url = url
        self.open()

    def open(self):
        if self.url:
            if self.float:
                # self.float.destroy()
                self.float.load_url(self.url)
                return
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - 悬浮窗: {self.url}")
            self.float = webview.create_window(
                '悬浮窗',
                width=272,  # 256 + 16
                height=297,  # 256 + 16 + 25
                url=self.url,
                frameless=True,
                on_top=True,
                resizable=False,
            )

    def close(self):
        if self.float:
            self.float.destroy()


if __name__ == '__main__':
    print("不要运行这个文件")
    pass
