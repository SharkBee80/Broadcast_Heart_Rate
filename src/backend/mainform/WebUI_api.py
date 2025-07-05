from src.backend.mainform import Device_handle, Web_page, Float_window, Setting, timer, config, get_path
import webview
from typing import Optional

ble = Device_handle.Device_handle()
web = Web_page.Web_page()
float_window = Float_window.FloatWindow()
setting = Setting.Setting()
cfg = config.config(get_path.get_path('config.ini', use_mei_pass=False))

DELAY = 0.25
move_timer = timer.timer_(DELAY)
resize_timer = timer.timer_(DELAY)


class WebUI_api:
    # 提供给前端调用的方法
    def __init__(self, window, server):
        self.window: Optional[webview.Window] = window
        self.server = server

        ble.init(self.window, self.server)
        web.init(self.window)
        float_window.init(self.window)
        setting.init(self.window)

        self.window.expose(self.onload_init, self.switch_toggle)

    def onload_init(self):
        web.set_()
        setting.load_setting()

    def on_closed(self):
        ble.disconnect_device()
        float_window.on_closed()
        self.server.stop()

    def switch_toggle(self, switch_name, switch_state):
        if switch_name in {'open', 'move', 'transparent'}:
            float_window.switch_toggle(switch_name, switch_state)
        if switch_name == 'bg-f':
            if switch_state:
                self.window.evaluate_js(r"""
                    document.querySelectorAll('.bg-f').forEach(function(item) {
                        item.style.display = '';
                    });
                """)
            else:
                self.window.evaluate_js(r"""
                    document.querySelectorAll('.bg-f').forEach(function(item) {
                        item.style.display = 'none';
                    });
                """)

    # window.events

    def on_moved(self, x, y):
        def record_position():
            if x < -2000:
                return
            if y < -2000:
                return
            cfg.write_config('main', 'x', x)
            cfg.write_config('main', 'y', y)

        move_timer.task(record_position)

    def on_resized(self, width, height):
        def record_size():
            if width < 0 or webview.screens[0].width <= width:
                return
            if height < 0 or webview.screens[0].height <= height:
                return
            cfg.write_config('main', 'width', width)
            cfg.write_config('main', 'height', height)

        resize_timer.task(record_size)

    def on_maximized(self):
        cfg.write_config('main', 'maximized', True)
        move_timer.cancel()

    def on_restored(self):
        cfg.write_config('main', 'maximized', False)
