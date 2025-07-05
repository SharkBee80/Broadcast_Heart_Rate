from src.backend.mainform import Device_handle, Web_page, Float_window, Setting

ble = Device_handle.Device_handle()
web = Web_page.Web_page()
float_window = Float_window.FloatWindow()
setting = Setting.Setting()


class WebUI_api:
    # 提供给前端调用的方法
    def __init__(self, window, server):
        self.window = window
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
