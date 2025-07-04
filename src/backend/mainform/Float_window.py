import time
from threading import Timer
from typing import Optional
import webview
from src.backend.mainform import config, get_path

path = get_path.get_path('config.ini', use_mei_pass=False)
cfg = config.config(path)


class FloatWindow:
    def __init__(self):
        self.window: Optional[webview.Window] = None
        self.url = None
        self.timer = None
        self.float: Optional[webview.Window] = None
        self.floatable = cfg.read_config('float', 'open') == 'True'
        self.movable = cfg.read_config('float', 'move') == 'True'
        self.transparent = cfg.read_config('float', 'transparent') == 'True'

    def init(self, window):
        self.window = window
        self.window.expose(self.set_url, self.switch_toggle)

    def set_url(self, url):
        self.url = url
        self.open()

    def open(self):
        if self.url and self.floatable:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - 悬浮窗: {self.url}")
            if self.float:
                self.float.destroy()
            self.float = webview.create_window(
                '悬浮窗',
                x=int(cfg.read_config('float', 'x')),
                y=int(cfg.read_config('float', 'y')),
                width=272,  # 256 + 16
                height=297,  # 256 + 16 + 25
                url=self.url,
                frameless=True,
                on_top=True,
                transparent=not self.movable and self.transparent,
                shadow=False
            )
            self.float.events.moved += self.on_move
            self.float.events.closed += self.on_closed

            self.after_load()
        elif not self.floatable and self.float:
            self.float.destroy()

    def after_load(self):
        if self.movable:
            self.float.evaluate_js("document.querySelector('.pywebview-drag-region').style.display = 'block'")

    def on_move(self):
        # 取消之前的定时器
        if self.timer is not None:
            self.timer.cancel()

        # 创建新定时器
        delay = 0.25
        self.timer = Timer(delay, self.record_position)
        self.timer.start()

    def record_position(self):
        cfg.write_config('float', 'x', self.float.x.__str__())
        cfg.write_config('float', 'y', self.float.y.__str__())
        print(f"悬浮窗位置: {self.float.x}, {self.float.y}")

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
        if switch_name == 'move':
            if switch_state:
                self.movable = True
            else:
                self.movable = False
            cfg.write_config('float', 'move', self.movable)
        if switch_name == 'transparent':
            if switch_state:
                self.transparent = True
            else:
                self.transparent = False
            cfg.write_config('float', 'transparent', self.transparent)
        self.open()
