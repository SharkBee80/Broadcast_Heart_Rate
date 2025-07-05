import time
from threading import Timer
from typing import Optional
import webview
from src.backend.mainform import config, get_path, timer

path = get_path.get_path('config.ini', use_mei_pass=False)
cfg = config.config(path)
DELAY = 0.25
move_timer = timer.timer_(DELAY)


class FloatWindow:
    def __init__(self):
        self.window: Optional[webview.Window] = None
        self.url = None
        self.timer = None
        self.float: Optional[webview.Window] = None
        self.switch = {
            "open": cfg.read_config('float', 'open') == 'True',
            "move": cfg.read_config('float', 'move') == 'True',
            "transparent": cfg.read_config('float', 'transparent') == 'True'
        }

    def init(self, window):
        self.window = window
        self.window.expose(self.set_url)

    def set_url(self, url):
        self.url = url
        self.open()

    def open(self):
        if self.url and self.switch['open']:
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
                transparent=not self.switch["move"] and self.switch["transparent"],
                shadow=False
            )
            self.float.events.moved += self.on_move
            self.float.events.closed += self.on_closed

            self.after_load()
        elif not self.switch['open'] and self.float:
            self.float.destroy()

    def after_load(self):
        if self.switch['move']:
            self.float.evaluate_js("document.querySelector('.pywebview-drag-region').style.display = 'block'")

    def on_move(self):
        move_timer.task(self.record_position)

    def record_position(self):
        cfg.write_config('float', 'x', self.float.x.__str__())
        cfg.write_config('float', 'y', self.float.y.__str__())
        print(f"悬浮窗位置: {self.float.x}, {self.float.y}")

    def on_closed(self):
        if self.float:
            self.float.destroy()
            self.float = None

    def switch_toggle(self, switch_name, switch_state):
        if switch_state:
            self.switch[switch_name] = True
        else:
            self.switch[switch_name] = False
        if switch_name != 'open':
            cfg.write_config('float', switch_name, self.switch[switch_name])
        self.open()
