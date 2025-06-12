import time
from typing import Optional
import webview
from src.backend.mainform import config


class FloatWindow:
    def __init__(self):
        self.window: Optional[webview.Window] = None
        self.url = None
        self.float: Optional[webview.Window] = None
        self.floatable = config.get_config('float', 'open') == 'True'

    def init(self, window):
        self.window = window
        self.window.expose(self.set_url, self.switch_toggle)

    def set_url(self, url):
        self.url = url
        self.open()

    def open(self):
        if self.url and self.floatable:
            if self.float:
                # self.float.destroy()
                self.float.load_url(self.url)
                return
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - 悬浮窗: {self.url}")
            self.float = webview.create_window(
                '悬浮窗',
                x=0,
                y=1080 - 256 - 50,
                width=272,  # 256 + 16
                height=297,  # 256 + 16 + 25
                url=self.url,
                frameless=True,
                on_top=True,
                transparent=True,
            )
            self.float.events.closed += self.on_closed
        elif not self.floatable and self.float:
            self.float.destroy()

    def on_closed(self):
        if self.float:
            self.float.destroy()
            self.float = None

    def switch_toggle(self, switch_name, switch_state):
        if switch_name == 'open':
            if switch_state:
                self.floatable = True
            else:
                self.floatable = False
            self.open()
